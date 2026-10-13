"""Per-game knowledge, keyed by the header's game code. Generic commands consult this when it has an entry."""
from .codecs import golden_sun

# Game code -> codec module. A codec module provides Decoder(rom) with classify(addr, size) -> (status, data).
CODECS = {
    "AGSE": golden_sun,  # Golden Sun (USA, Europe)
    "AGFE": golden_sun,  # Golden Sun: The Lost Age (USA, Europe)
}


def codec_for(rom):
    return CODECS.get(rom.code)
