"""gbax: a GBA ROM extraction toolkit.

Works on any GBA ROM, with optional per-game knowledge layered on top. Every command writes into a per-ROM workspace
(games/<CODE>-<sha1 prefix>/) so results from different games sit side by side.

Commands (python -m gbax <command> ROM ...):
  identify   header, hashes, save type, BIOS calls used, sound engine, known-game match
  scan       map the ROM: pointers, pointer tables, compressed blobs, code seeds, free space
  sigs       name known SDK/library functions by fingerprint (built from a decomp ELF)
  extract    decompress blobs and render graphics previews to PNG
  palettes   pair graphics with palettes and write colour PNGs plus an HTML gallery
  ghidra     build a Ghidra project with the GBA memory map and every recovered name
  all        identify + scan + sigs + extract + ghidra
  refs       find code that loads an address, and BL calls to it
  decompile  Ghidra decompilation of the functions at given addresses (--arm SIZE for ARM routines)
  sigs-build build a fingerprint database from a decomp's ELF + map + ROM

Library use: gbax.emu.Gba(rom).call(addr, args) runs a game's own routine (e.g. a custom decompressor) on an
emulated ARM7. Per-game codecs live in gbax/codecs and are registered in gbax/profiles.py.
"""
