"""Reverse-engineering helpers: find references to an address, and decompile functions through Ghidra."""
import numpy as np

from .rom import ROM_BASE


def find_refs(rom, value):
    """Aligned words equal to value (or value|1 for Thumb code). Returns ROM addresses of the words."""
    w = np.frombuffer(rom.data[: rom.size & ~3], dtype="<u4")
    hits = np.nonzero((w == value) | (w == (value | 1)))[0]
    return [int(i) * 4 + ROM_BASE for i in hits]


def find_literal_loads(rom, word_addr):
    """Thumb 'ldr rX, [pc, #imm]' instructions (up to 1020 bytes before) that load the word at word_addr."""
    out = []
    w = word_addr - ROM_BASE
    for pc in range(max(0, w - 1020), w, 2):
        h = int.from_bytes(rom.data[pc:pc + 2], "little")
        if (h & 0xF800) == 0x4800 and ((pc + 4) & ~3) + (h & 0xFF) * 4 == w:
            out.append(pc + ROM_BASE)
    return out


def find_callers(rom, target):
    """BL calls to target, directly or through long-jump stubs ('ldr rX,=target; bx rX') that point at it.
    Returns {call address: stub address or None}."""
    from .scan import veneers
    out = {c: None for c in find_bl_callers(rom, target)}
    for stub, tgt in veneers(rom.data).items():
        if tgt + ROM_BASE == target & ~1:
            for c in find_bl_callers(rom, stub + ROM_BASE):
                out[c] = stub + ROM_BASE
    return out


def find_bl_callers(rom, target):
    """Thumb BL instructions that call target. Returns ROM addresses of the calls."""
    h = np.frombuffer(rom.data[: rom.size & ~1], dtype="<u2").astype(np.int64)
    first = (h[:-1] & 0xF800) == 0xF000
    second = (h[1:] & 0xF800) == 0xF800
    idx = np.nonzero(first & second)[0]
    off = ((h[idx] & 0x7FF) << 12) | ((h[idx + 1] & 0x7FF) << 1)
    off = np.where(off & 0x400000, off - 0x800000, off)
    tgt = idx * 2 + 4 + off + ROM_BASE
    return [int(i) * 2 + ROM_BASE for i in idx[tgt == (target & ~1)]]


def find_arm_routines(rom, min_run=6):
    """Likely ARM routine starts: an 'stmfd sp!, {...}' (0xE92Dxxxx) followed by a run of always-executed ARM
    instructions. GBA games are mostly Thumb, so ARM code is usually speed-critical routines copied to RAM."""
    w = np.frombuffer(rom.data[: rom.size & ~3], dtype="<u4")
    starts = np.nonzero((w >> 16) == 0xE92D)[0]
    out = []
    for i in starts:
        run = w[i:i + min_run]
        if len(run) == min_run and ((run >> 28) == 0xE).sum() >= min_run - 1:
            out.append(int(i) * 4 + ROM_BASE)
    return out


def discover_decoders(rom, src_addr, src_len, candidates=None, max_instructions=3_000_000, tolerance=8,
                      skips=(0,), orders=("src,dest",)):
    """Run every candidate routine on the data at src_addr and keep those that read the data to (nearly) its end and
    write output. candidates: [(address, thumb)]; default: every ARM routine start. skips: bytes to skip at the start
    (e.g. 1 for a type byte). orders: 'src,dest' (r0=src, r1=dest, r2=&src) or 'dest,src'.
    Returns [(routine, thumb, skip, order, bytes written, bytes read)]."""
    from .emu import EWRAM, Gba
    g = Gba(rom)
    dest, slot = EWRAM + 0x10000, EWRAM + 0x100
    hits = []
    cands = candidates if candidates is not None else [(a, False) for a in find_arm_routines(rom)]
    for c, thumb in cands:
        for skip in skips:
            src = src_addr + skip
            for order in orders:
                g.write(dest, b"\0" * 0x20000)
                g.write(slot, src.to_bytes(4, "little"))
                args = (src, dest, slot, 0) if order == "src,dest" else (dest, src, 0, 0)
                try:
                    _, read, written = g.call_tracking(c, args, (src, src_len + 0x100), (dest, 0x20000),
                                                       thumb=thumb, max_instructions=max_instructions)
                except (RuntimeError, Exception):
                    continue
                if written > 0 and abs(read - (src_len - skip)) <= tolerance:
                    hits.append((c, thumb, skip, order, written, read))
    return hits


def decompile(rom, addresses, create=True, timeout=60, arm_size=0):
    """Decompile the functions containing each address. Returns [(address, function name, entry, C text)].

    arm_size: treat [address, address+arm_size) as ARM code (clearing any Thumb disassembly there) before decompiling.
    """
    from . import ghidra as g
    pyghidra = g.start_ghidra()
    from java.math import BigInteger
    from ghidra.app.decompiler import DecompInterface
    from ghidra.program.flatapi import FlatProgramAPI

    gdir = rom.workspace / "ghidra"
    project = pyghidra.open_project(str(gdir), rom.slug, create=False)
    out = []
    try:
        with pyghidra.program_context(project, "/" + rom.slug) as program:
            monitor = pyghidra.task_monitor()
            flat = FlatProgramAPI(program, monitor)
            A = program.getAddressFactory().getDefaultAddressSpace().getAddress
            dec = DecompInterface()
            dec.openProgram(program)
            changed = False
            with pyghidra.transaction(program, "gbax decompile"):
                for addr in addresses:
                    a = A(addr & ~1)
                    if arm_size:
                        end = A((addr & ~3) + arm_size - 1)
                        for f in list(program.getFunctionManager().getFunctionsOverlapping(
                                program.getAddressFactory().getAddressSet(a, end))):
                            program.getFunctionManager().removeFunction(f.getEntryPoint())
                        program.getListing().clearCodeUnits(a, end, False)
                        ctx = program.getProgramContext()
                        ctx.setValue(ctx.getRegister("TMode"), a, end, BigInteger.ZERO)
                        flat.disassemble(a)
                        changed = True
                    fn = flat.getFunctionContaining(a)
                    if fn is None and create:
                        if program.getListing().getInstructionAt(a) is None:
                            flat.disassemble(a)
                        fn = flat.createFunction(a, None)
                        changed = changed or fn is not None
                    if fn is None:
                        out.append((addr, None, None, "// no function here"))
                        continue
                    res = dec.decompileFunction(fn, timeout, monitor)
                    text = res.getDecompiledFunction().getC() if res.decompileCompleted() else \
                        f"// decompile failed: {res.getErrorMessage()}"
                    out.append((addr, fn.getName(), fn.getEntryPoint().getOffset(), text))
            if changed:
                program.save("gbax decompile: created functions", monitor)
            dec.dispose()
    finally:
        project.close()
    return out
