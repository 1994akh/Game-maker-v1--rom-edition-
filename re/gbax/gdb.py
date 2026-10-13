"""Minimal GDB remote-protocol client, enough to drive mGBA's GDB server (mgba -g ROM, port 2345).

Supports: breakpoints (Z0/z0), read/write/access watchpoints (Z2-Z4), continue, single step, interrupt,
register and memory reads.
"""
import socket
import time

ARM_REG_COUNT = 16


class GdbError(Exception):
    pass


class Gdb:
    def __init__(self, host="127.0.0.1", port=2345, connect_timeout=30):
        deadline = time.time() + connect_timeout
        while True:
            try:
                self.sock = socket.create_connection((host, port), timeout=5)
                break
            except OSError:
                if time.time() > deadline:
                    raise GdbError(f"no GDB server on {host}:{port}")
                time.sleep(0.5)
        self.buf = b""

    # ---------------------------------------------------------------- framing

    def _send(self, data):
        payload = data.encode("latin-1")
        self.sock.sendall(b"$" + payload + b"#" + f"{sum(payload) % 256:02x}".encode())

    def _recv(self, timeout=None):
        """Return the next packet's payload, acknowledging it. Skips '+'/'-' acks."""
        self.sock.settimeout(timeout)
        while True:
            start = self.buf.find(b"$")
            if start >= 0:
                end = self.buf.find(b"#", start)
                if end >= 0 and len(self.buf) >= end + 3:
                    payload = self.buf[start + 1:end]
                    self.buf = self.buf[end + 3:]
                    self.sock.sendall(b"+")
                    return payload.decode("latin-1")
            chunk = self.sock.recv(65536)
            if not chunk:
                raise GdbError("connection closed")
            self.buf += chunk

    def drain(self):
        """Discard anything already waiting (mGBA sometimes sends an extra stop packet after a step or stop)."""
        self.sock.settimeout(0.02)
        try:
            while True:
                chunk = self.sock.recv(65536)
                if not chunk:
                    break
                if b"$" in chunk:
                    self.sock.sendall(b"+")
        except (TimeoutError, OSError):
            pass
        self.buf = b""

    def cmd(self, data, timeout=10):
        self.drain()
        self._send(data)
        return self._recv(timeout)

    # ---------------------------------------------------------------- control

    def halt_reason(self):
        return self.cmd("?")

    def cont(self, timeout=None):
        """Resume; block until the target stops. Returns the stop reply (e.g. 'T05...')."""
        self._send("c")
        return self._recv(timeout)

    def step(self):
        return self.cmd("s")

    def interrupt(self, timeout=10):
        self.sock.sendall(b"\x03")
        return self._recv(timeout)

    def detach(self):
        try:
            self.cmd("D", timeout=3)
        except Exception:
            pass
        self.sock.close()

    # ---------------------------------------------------------------- break/watch points

    def _point(self, op, kind, addr, length):
        r = self.cmd(f"{op}{kind},{addr:x},{length:x}")
        if r != "OK":
            raise GdbError(f"{op}{kind} at 0x{addr:08X} refused: {r!r}")

    def breakpoint(self, addr, thumb=True):
        self._point("Z", 0, addr & ~1, 2 if thumb else 4)

    def clear_breakpoint(self, addr, thumb=True):
        self._point("z", 0, addr & ~1, 2 if thumb else 4)

    def watch(self, addr, length=4, mode="read"):
        self._point("Z", {"write": 2, "read": 3, "access": 4}[mode], addr, length)

    def clear_watch(self, addr, length=4, mode="read"):
        self._point("z", {"write": 2, "read": 3, "access": 4}[mode], addr, length)

    # ---------------------------------------------------------------- state

    def registers(self):
        """r0..r15 and cpsr (None if the server doesn't send it)."""
        for _ in range(3):
            h = self.cmd("g")
            if len(h) >= ARM_REG_COUNT * 8 and all(c in "0123456789abcdefABCDEF" for c in h[:ARM_REG_COUNT * 8]):
                break
        else:
            raise GdbError(f"bad register reply: {h[:40]!r}")
        regs = [int.from_bytes(bytes.fromhex(h[i * 8:(i + 1) * 8]), "little") for i in range(ARM_REG_COUNT)]
        cpsr = None
        if len(h) >= 336:  # r0-r15, f0-f7 (12 bytes each), fps, cpsr: the standard GDB ARM layout
            cpsr = int.from_bytes(bytes.fromhex(h[328:336]), "little")
        else:  # mGBA sends r0-r15 only; ask for cpsr (register 25) directly
            try:
                p = self.cmd("p19")
                if len(p) == 8:
                    cpsr = int.from_bytes(bytes.fromhex(p), "little")
            except GdbError:
                pass
        return regs, cpsr

    def read(self, addr, length):
        out = bytearray()
        while length > 0:
            n = min(length, 0x100)  # mGBA's packet buffer is small; bigger reads fail
            r = self.cmd(f"m{addr:x},{n:x}")
            if r.startswith("E"):
                raise GdbError(f"read 0x{addr:08X} failed: {r}")
            out += bytes.fromhex(r)
            addr += n
            length -= n
        return bytes(out)
