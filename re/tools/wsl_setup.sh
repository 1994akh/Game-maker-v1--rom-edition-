#!/usr/bin/env bash
# Sets up the GBA build toolchain inside WSL (Ubuntu) and builds vanilla FireRed v1.0 from the pret decompilation.
# Run from Windows:  wsl -d Ubuntu -u root --cd ~ bash /mnt/c/Users/aaron/Documents/UnboundHack/tools/wsl_setup.sh
# Re-running is safe: completed steps are skipped.
set -euo pipefail

GBA=/opt/gba
OUT=/mnt/c/Users/aaron/Documents/UnboundHack/build
export DEBIAN_FRONTEND=noninteractive

echo "== apt packages"
apt-get update -qq
apt-get install -y -qq build-essential binutils-arm-none-eabi gcc-arm-none-eabi libnewlib-arm-none-eabi \
    git libpng-dev pkg-config python3 >/dev/null

mkdir -p "$GBA" "$OUT"
cd "$GBA"

echo "== pret/agbcc (the original GBA C compiler, needed for matching builds)"
[ -d agbcc ] || git clone -q https://github.com/pret/agbcc.git
[ -x agbcc/agbcc ] || (cd agbcc && ./build.sh >/dev/null)

echo "== pret/pokefirered"
[ -d pokefirered ] || git clone -q https://github.com/pret/pokefirered.git
[ -x pokefirered/tools/agbcc/bin/agbcc ] || (cd agbcc && ./install.sh ../pokefirered >/dev/null)

echo "== build FireRed v1.0 and Rev 1"
cd pokefirered
make -j"$(nproc)" firered >/dev/null
make -j"$(nproc)" firered_rev1 >/dev/null
sha1sum pokefirered.gba pokefirered_rev1.gba

cp pokefirered.gba "$OUT/pokefirered_v10.gba"
cp pokefirered.map "$OUT/pokefirered_v10.map" 2>/dev/null || true
cp pokefirered.elf "$OUT/pokefirered_v10.elf"
cp pokefirered_rev1.gba "$OUT/pokefirered_rev1.gba"
echo "== done; outputs in $OUT"
