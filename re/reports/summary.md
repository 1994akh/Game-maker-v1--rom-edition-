# ROM analysis

**Hack:** `Pokemon Unbound (v2.1.1.1).gba`  
size 33,554,432 bytes, SHA-1 `b4776b82a4c7915d0fadeaa27e013523f99dfd94`, title `POKEMON FIRE`, code `BPRE`, maker `01`, version 0

**Base:** `Pokemon - FireRed Version (USA, Europe) (Rev 1).gba`  
size 16,777,216 bytes, SHA-1 `dd5945db9b930750cb39d00c84da8571feebf417`, title `POKEMON FIRE`, code `BPRE`, maker `01`, version 1

## Changes inside the base ROM's address space
- 14,668,710 of 16,777,216 bytes differ (87.4%)
- spread over 301 regions covering 15,742,208 bytes (at 256-byte granularity)

## Space beyond the base ROM
- 16,777,216 bytes added past 0x1000000; about 16,328,617 of them in use

## Free space (0xFF runs of at least 256 bytes)
- total 1,683,585 bytes (1.61 MB) in 539 runs
- largest: 0x15FBC90 (344,944), 0x0B2B280 (150,912), 0x1FE6C64 (103,324), 0x01B2938 (34,940), 0x01ACD64 (20,504)

## Per-MB breakdown

| Range | Changed vs base | Free |
|---|---|---|
| 0x0000000 | 94.3% | 1,808 |
| 0x0100000 | 91.9% | 331,370 |
| 0x0200000 | 73.7% | 156,955 |
| 0x0300000 | 75.5% | 102,400 |
| 0x0400000 | 85.3% | 18,162 |
| 0x0500000 | 98.2% | 0 |
| 0x0600000 | 98.1% | 83,124 |
| 0x0700000 | 90.5% | 78,809 |
| 0x0800000 | 89.9% | 81,635 |
| 0x0900000 | 92.8% | 48,441 |
| 0x0A00000 | 97.1% | 0 |
| 0x0B00000 | 79.3% | 195,812 |
| 0x0C00000 | 94.4% | 48,395 |
| 0x0D00000 | 74.1% | 18,816 |
| 0x0E00000 | 64.7% | 69,259 |
| 0x0F00000 | 99.2% | 0 |
| 0x1000000 | added | 0 |
| 0x1100000 | added | 0 |
| 0x1200000 | added | 331 |
| 0x1300000 | added | 0 |
| 0x1400000 | added | 0 |
| 0x1500000 | added | 17,264 |
| 0x1600000 | added | 327,680 |
| 0x1700000 | added | 0 |
| 0x1800000 | added | 0 |
| 0x1900000 | added | 0 |
| 0x1A00000 | added | 0 |
| 0x1B00000 | added | 0 |
| 0x1C00000 | added | 0 |
| 0x1D00000 | added | 0 |
| 0x1E00000 | added | 0 |
| 0x1F00000 | added | 103,324 |
