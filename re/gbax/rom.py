"""Loading a ROM, its header, and its per-ROM workspace."""
import hashlib
import json
import re
import zlib
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAMES = ROOT / "games"
ROM_BASE = 0x08000000

# Hashes verified in this project; extend as more ROMs are confirmed.
KNOWN_SHA1 = {
    "41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc": "Pokemon FireRed (USA) v1.0",
    "dd5945db9b930750cb39d00c84da8571feebf417": "Pokemon FireRed (USA, Europe) Rev 1",
}

# Save-library ID strings Nintendo's SDK embeds; emulators use the same strings to pick the save type.
SAVE_IDS = (b"EEPROM_V", b"SRAM_V", b"SRAM_F_V", b"FLASH_V", b"FLASH512_V", b"FLASH1M_V")


@dataclass
class Rom:
    path: Path
    data: bytes
    title: str = ""
    code: str = ""
    maker: str = ""
    version: int = 0
    header_ok: bool = False
    sha1: str = ""
    crc32: str = ""
    extra: dict = field(default_factory=dict)

    @classmethod
    def load(cls, path):
        path = Path(path)
        data = path.read_bytes()
        r = cls(path=path, data=data)
        r.title = data[0xA0:0xAC].rstrip(b"\0").decode("ascii", "replace")
        r.code = data[0xAC:0xB0].decode("ascii", "replace")
        r.maker = data[0xB0:0xB2].decode("ascii", "replace")
        r.version = data[0xBC]
        chk = (-sum(data[0xA0:0xBD]) - 0x19) & 0xFF
        r.header_ok = chk == data[0xBD]
        r.sha1 = hashlib.sha1(data).hexdigest()
        r.crc32 = f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"
        return r

    @property
    def size(self):
        return len(self.data)

    @property
    def known_as(self):
        return KNOWN_SHA1.get(self.sha1)

    @property
    def slug(self):
        name = re.sub(r"[^A-Za-z0-9]+", "-", self.path.stem).strip("-")[:40]
        return f"{self.code}-{self.sha1[:8]}-{name}"

    @property
    def workspace(self):
        ws = GAMES / self.slug
        ws.mkdir(parents=True, exist_ok=True)
        return ws

    def save_types(self):
        found = []
        for sid in SAVE_IDS:
            i = self.data.find(sid)
            if i >= 0:
                m = re.match(rb"[A-Z0-9_]+V\d{3}", self.data[i:i + 20])
                found.append(m.group(0).decode() if m else sid.decode())
        return found

    def u32(self, off):
        return int.from_bytes(self.data[off:off + 4], "little")

    def write_json(self, name, obj):
        (self.workspace / name).write_text(json.dumps(obj, indent=2), encoding="utf-8")

    def read_json(self, name):
        p = self.workspace / name
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None
