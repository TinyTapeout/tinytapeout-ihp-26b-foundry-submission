# Tiny Tapeout IHP 26b - IHP Open-Silicon MPW Submission

Multi-Project Carrier (MPC) chip for the IHP SG13G2 Open-Silicon MPW September 2026 run.

## Overview

Tiny Tapeout IHP 26b is an educational ASIC that aggregates user-submitted
chip designs onto a single die manufactured on the **IHP SG13G2** 130nm BiCMOS process.
The current release contains 36 user projects (built 2026-09-08; the shuttle closes on 2026-09-21).

- **Category:** Mixed-Signal
- **Subcategory:** Multi Project Carrier (MPC)
- **Process:** IHP SG13G2
- **Die size:** 3600 x 5000 um
- **Top cell:** `TT2609`
- **Grid:** 12 x 20 tiles (240 user project slots)
- **License:** Apache-2.0

## Design Source

The chip design source is at: https://github.com/TinyTapeout/tinytapeout-ihp-26b

The design flow uses:
- **LibreLane** for RTL-to-GDS compilation
- **Yosys** for synthesis
- **OpenROAD** for place and route
- **Magic** for SPICE extraction
- **Netgen** for LVS verification
- **KLayout** for DRC and GDS streamout

## Physical Verification

LVS was verified during the chip build using Netgen (SPICE extracted via Magic
compared against the Verilog netlist). Result: `Circuits match uniquely.`

DRC, metal density and a zero-area polygon check are verified via GitHub Actions
using the IHP SG13G2 PDK scripts (see `.github/workflows/verification.yml`).

## Updating the Release

The `Update TT2609 release` workflow (`.github/workflows/update.yml`) downloads the
`foundry_submission` artifact from the latest successful `gds` run of the source
repository and commits the refreshed layout and netlists under `release/v.1.0.0/`.

## Links

- Source repository: https://github.com/TinyTapeout/tinytapeout-ihp-26b
- Tiny Tapeout: https://tinytapeout.com
- IHP SG13G2 PDK: https://github.com/IHP-GmbH/IHP-Open-PDK
