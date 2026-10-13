"""Run a game's own routine (decompressor, parser...) on an emulated ARM7 with the GBA memory map.

This turns any routine found in Ghidra into an exact decoder without reimplementing it first, and gives a reference
to test a native reimplementation against.
"""
from unicorn import (Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_MEM_READ, UC_HOOK_MEM_UNMAPPED,
                     UC_HOOK_MEM_WRITE)
from unicorn.arm_const import (UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1,
                               UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP)

EWRAM, IWRAM, IO, ROM = 0x02000000, 0x03000000, 0x04000000, 0x08000000
RETURN_ADDR = 0x0000_1000  # address inside the (unused) BIOS region; reaching it means the routine returned
ARG_REGS = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)


class Gba:
    def __init__(self, rom):
        self.rom = rom
        uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        uc.mem_map(0, 0x4000)                       # BIOS (holds the return trap)
        uc.mem_map(EWRAM, 0x40000)
        uc.mem_map(IWRAM, 0x8000)
        uc.mem_map(IO, 0x1000)
        size = (rom.size + 0xFFF) & ~0xFFF
        uc.mem_map(ROM, size)
        uc.mem_write(ROM, rom.data)
        uc.mem_write(RETURN_ADDR, b"\xfe\xff\xff\xea")  # ARM 'b .' so a stray return can't run off
        self.unmapped = []
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self._unmapped)
        # DMA: a write that sets a channel's enable bit runs the transfer at once (good enough for decoders, which
        # use immediate DMA to copy or fill runs). Hooked on the control registers of all four channels.
        uc.hook_add(UC_HOOK_MEM_WRITE, self._dma_write, begin=IO + 0xB0, end=IO + 0xDF)
        self.uc = uc

    def _dma_write(self, uc, access, addr, size, value, data):
        # Registers per channel n: SAD 0xB0+12n, DAD 0xB4+12n, CNT_L 0xB8+12n (count), CNT_H 0xBA+12n (control).
        off = addr - IO - 0xB0
        ch, reg = divmod(off, 12)
        if ch > 3:
            return
        # Control lives in CNT_H; it's written either as a halfword at +0xA or as the top of a word at +0x8.
        if reg == 0xA and size >= 2:
            ctrl, count = value & 0xFFFF, int.from_bytes(uc.mem_read(IO + 0xB8 + 12 * ch, 2), "little")
        elif reg == 0x8 and size == 4:
            ctrl, count = (value >> 16) & 0xFFFF, value & 0xFFFF
        else:
            return
        if not ctrl & 0x8000:
            return
        base = IO + 0xB0 + 12 * ch
        src = int.from_bytes(uc.mem_read(base, 4), "little")
        dst = int.from_bytes(uc.mem_read(base + 4, 4), "little")
        unit = 4 if ctrl & 0x400 else 2
        count = count or (0x10000 if ch == 3 else 0x4000)
        dstep = {0: unit, 1: -unit, 2: 0, 3: unit}[(ctrl >> 5) & 3]
        sstep = {0: unit, 1: -unit, 2: 0, 3: unit}[(ctrl >> 7) & 3]
        try:
            if sstep == unit and dstep == unit:
                uc.mem_write(dst, bytes(uc.mem_read(src, count * unit)))
            else:
                for i in range(count):
                    uc.mem_write(dst + i * dstep, bytes(uc.mem_read(src + i * sstep, unit)))
        except UcError:
            self.unmapped.append(("dma", src, dst, count))
        self.dma_log = getattr(self, "dma_log", [])
        self.dma_log.append((ch, src, dst, count, unit))

    def _unmapped(self, uc, access, addr, size, value, data):
        self.unmapped.append(addr)
        return False

    def call(self, addr, args=(), thumb=None, sp=IWRAM + 0x7F00, max_instructions=200_000_000):
        """Call the routine at addr with up to 4 register arguments; returns r0."""
        uc = self.uc
        thumb = bool(addr & 1) if thumb is None else thumb
        for reg, val in zip(ARG_REGS, args):
            uc.reg_write(reg, val)
        uc.reg_write(UC_ARM_REG_SP, sp)
        uc.reg_write(UC_ARM_REG_LR, RETURN_ADDR)
        cpsr = uc.reg_read(UC_ARM_REG_CPSR)
        uc.reg_write(UC_ARM_REG_CPSR, (cpsr | 0x20) if thumb else (cpsr & ~0x20))
        start = (addr & ~1) | (1 if thumb else 0)
        try:
            uc.emu_start(start, RETURN_ADDR, count=max_instructions)
        except UcError as e:
            pc = uc.reg_read(UC_ARM_REG_PC)
            raise RuntimeError(f"emulation stopped at 0x{pc:08X}: {e}; unmapped accesses {self.unmapped[:4]}")
        if uc.reg_read(UC_ARM_REG_PC) & ~1 != RETURN_ADDR:
            raise RuntimeError("routine did not return within the instruction limit")
        return uc.reg_read(UC_ARM_REG_R0)

    def call_tracking_reads(self, addr, args, watch_start, watch_len, **kw):
        """Like call(), but also return the highest address read in [watch_start, watch_start + watch_len)."""
        top = [watch_start - 1]

        def on_read(uc, access, a, size, value, data):
            if a + size - 1 > top[0]:
                top[0] = a + size - 1

        h = self.uc.hook_add(UC_HOOK_MEM_READ, on_read, begin=watch_start, end=watch_start + watch_len - 1)
        try:
            r0 = self.call(addr, args, **kw)
        finally:
            self.uc.hook_del(h)
        return r0, top[0] + 1 - watch_start

    def call_tracking(self, addr, args, read_window, write_window, **kw):
        """Like call(), but also report how far the routine read into read_window and wrote into write_window,
        each given as (start, length). Returns (r0, bytes read from the start, bytes written from the start)."""
        top = {"r": read_window[0] - 1, "w": write_window[0] - 1}

        def hook(key):
            def on(uc, access, a, size, value, data):
                if a + size - 1 > top[key]:
                    top[key] = a + size - 1
            return on

        hr = self.uc.hook_add(UC_HOOK_MEM_READ, hook("r"), begin=read_window[0],
                              end=read_window[0] + read_window[1] - 1)
        hw = self.uc.hook_add(UC_HOOK_MEM_WRITE, hook("w"), begin=write_window[0],
                              end=write_window[0] + write_window[1] - 1)
        try:
            r0 = self.call(addr, args, **kw)
        finally:
            self.uc.hook_del(hr)
            self.uc.hook_del(hw)
        return r0, top["r"] + 1 - read_window[0], top["w"] + 1 - write_window[0]

    def read(self, addr, size):
        return bytes(self.uc.mem_read(addr, size))

    def write(self, addr, data):
        self.uc.mem_write(addr, data)
