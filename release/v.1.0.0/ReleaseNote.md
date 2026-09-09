# Release v.1.0.0

## Tiny Tapeout IHP 26b - Initial Release

**Date:** 2026-09-09
**Process:** IHP SG13G2

### Release Contents

- `gds/TT2609.oas` - Final chip layout (OAS format) with fill and seal ring
- `netlist/tt_ihp_wrapper.nl.v` - Gate-level Verilog netlist
- `netlist/tt_ihp_wrapper.v` - Powered Verilog netlist

### Verification Status

| Check                 | Status                             |
| --------------------- | ---------------------------------- |
| DRC (KLayout)         | PASS                               |
| Metal density         | PASS                               |
| Zero-area polygons    | PASS (none found)                  |
| LVS (Netgen)          | PASS - "Circuits match uniquely"   |
| Gate-level simulation | PASS (test_factory_test, test_rom) |

### Design Summary

- Die: 3600 x 5000 um
- Grid: 12 x 20 tiles (240 project slots)
- Top cell: TT2609
- User projects: 36 (shuttle open until 2026-09-21)
- Built from: https://github.com/TinyTapeout/tinytapeout-ihp-26b (commit 34848a7)
- Build workflow: https://github.com/TinyTapeout/tinytapeout-ihp-26b/actions/runs/34266123820
