"""Build a Ghidra project for any GBA ROM from gbax's findings (scan seeds, signature names, blobs, BIOS stubs)."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GBA_MEMORY = [  # name, start, size, permissions
    ("BIOS", 0x00000000, 0x4000, "rx"), ("EWRAM", 0x02000000, 0x40000, "rwx"), ("IWRAM", 0x03000000, 0x8000, "rwx"),
    ("IO", 0x04000000, 0x400, "rw"), ("PALETTE", 0x05000000, 0x400, "rw"), ("VRAM", 0x06000000, 0x18000, "rw"),
    ("OAM", 0x07000000, 0x400, "rw"),
]


def start_ghidra():
    os.environ.setdefault("JAVA_HOME", str(next((ROOT / "apps").glob("jdk-21*"))))
    os.environ.setdefault("GHIDRA_INSTALL_DIR", str(next((ROOT / "apps").glob("ghidra_*_PUBLIC"))))
    import pyghidra
    if not pyghidra.started():
        pyghidra.start()
    return pyghidra


def reset_handler_arm_range(data):
    """The header's first word is an ARM branch to the reset handler; return the ARM-looking run it lands in."""
    w0 = int.from_bytes(data[0:4], "little")
    if w0 >> 24 != 0xEA:
        return None
    imm = w0 & 0xFFFFFF
    if imm & 0x800000:
        imm -= 0x1000000
    tgt = 8 + imm * 4
    end = tgt
    while end < min(len(data), tgt + 0x400) and data[end + 3] >> 4 == 0xE:
        end += 4
    return (tgt, end) if end > tgt else None


def build(rom, scan_result, sig_matches, inferred, analyze=False, rebuild=False):
    pyghidra = start_ghidra()
    from java.math import BigInteger
    from ghidra.app.util.opinion import BinaryLoader
    from ghidra.program.flatapi import FlatProgramAPI
    from ghidra.program.model.symbol import SourceType

    gdir = rom.workspace / "ghidra"
    gdir.mkdir(exist_ok=True)
    name = rom.slug
    monitor = pyghidra.task_monitor()
    project = pyghidra.open_project(str(gdir), name, create=True)
    stats = {}
    try:
        df = project.getProjectData().getFile("/" + name)
        if df is not None and rebuild:
            df.delete()
            df = None
        if df is None:
            with pyghidra.program_loader().project(project).source(str(rom.path)).name(name) \
                    .loaders(BinaryLoader.class_).language("ARM:LE:32:v4t").compiler("default").load() as res:
                p = res.getPrimaryDomainObject()
                with pyghidra.transaction(p, "Rebase"):
                    p.setImageBase(p.getAddressFactory().getDefaultAddressSpace().getAddress(0x08000000), True)
                res.save(monitor)
            fresh = True
        else:
            fresh = False

        with pyghidra.program_context(project, "/" + name) as program:
            if fresh:
                flat = FlatProgramAPI(program, monitor)
                A = program.getAddressFactory().getDefaultAddressSpace().getAddress
                ctx, st, mem = program.getProgramContext(), program.getSymbolTable(), program.getMemory()
                tmode = ctx.getRegister("TMode")
                base = 0x08000000

                def mode(s, e, thumb):
                    ctx.setValue(tmode, A(base + s), A(base + e - 1), BigInteger.ONE if thumb else BigInteger.ZERO)

                def ns(n):
                    return st.getOrCreateNameSpace(program.getGlobalNamespace(), n, SourceType.IMPORTED)

                def func(off, fname=None, namespace=None):
                    a = A(base + off)
                    if program.getListing().getInstructionAt(a) is None:
                        flat.disassemble(a)
                    fn = flat.getFunctionAt(a) or flat.createFunction(a, fname)
                    if fn and fname:
                        fn.setName(fname, SourceType.IMPORTED)
                        if namespace:
                            fn.setParentNamespace(namespace)
                    return fn is not None

                with pyghidra.transaction(program, "gbax: memory map, modes, names"):
                    rb = mem.getBlock(A(base))
                    rb.setName("ROM")
                    rb.setWrite(False)
                    rb.setExecute(True)
                    for bname, s, size, perms in GBA_MEMORY:
                        b = mem.createUninitializedBlock(bname, A(s), size, False)
                        b.setRead("r" in perms)
                        b.setWrite("w" in perms)
                        b.setExecute("x" in perms)
                        b.setVolatile(bname == "IO")
                    mode(0, rom.size, True)
                    mode(0, 4, False)
                    arm = reset_handler_arm_range(rom.data)
                    if arm:
                        mode(arm[0], arm[1], False)
                    for n_, _, off, size, thumb, unique in sig_matches:
                        if unique and not thumb:
                            mode(off, off + size, False)

                    flat.addEntryPoint(A(base))
                    flat.createLabel(A(base), "RomHeader_Entry", True)
                    flat.disassemble(A(base))
                    if arm:
                        func(arm[0], "ResetHandler")

                    sdk = ns("SDK")
                    named = 0
                    for n_, obj, off, size, thumb, unique in sig_matches:
                        if unique and func(off, n_, sdk):
                            named += 1
                    stats["SDK functions named"] = named
                    for n_, addr in inferred.items():
                        if 0x08000000 <= addr < 0x08000000 + rom.size or 0x02000000 <= addr < 0x03008000:
                            st.createLabel(A(addr), n_, sdk, SourceType.IMPORTED)
                    stats["SDK data labels inferred"] = len(inferred)
                    bios = ns("BIOS")
                    for bname, off in scan_result["bios_stubs"].items():
                        func(off, bname, bios)
                    stats["BIOS stubs named"] = len(scan_result["bios_stubs"])
                    seeds = 0
                    for off in scan_result["function_seeds"]:
                        if func(int(off)):
                            seeds += 1
                    stats["functions from call/pointer seeds"] = seeds
                    for off, kind, size, clen, _ in scan_result["blobs"]:
                        a = A(base + off)
                        if program.getListing().getInstructionAt(a) is None:
                            flat.createLabel(a, f"{kind}_{base + off:08X}", True)
                            flat.setPreComment(a, f"{kind} compressed, {clen} -> {size} bytes")
                    stats["compressed blobs labelled"] = len(scan_result["blobs"])
                program.save("gbax import", monitor)
            if analyze:
                pyghidra.analyze(program, monitor)
                program.save("gbax auto-analysis", monitor)
            fm = program.getFunctionManager()
            stats["functions total"] = fm.getFunctionCount()
    finally:
        project.close()
    return gdir / f"{name}.gpr", stats
