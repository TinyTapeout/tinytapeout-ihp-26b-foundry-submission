# Tiny Tapeout IHP 26b - Design Specification

## 1. Overview

Tiny Tapeout IHP 26b is a multi-project carrier (MPC) chip designed for the
IHP SG13G2 130nm BiCMOS process. It enables educational and research access to
silicon fabrication by aggregating many small user designs onto a single die.

## 2. Process Technology

- **Foundry:** IHP
- **Process:** SG13G2 (130nm BiCMOS)
- **Metal stack:** 5 thin metals + 2 thick top metals
- **PDK version:** `e16d00b7b26a93956563c373b782f54dd4d77a7f`

## 3. Physical Design

| Parameter                  | Value                         |
| -------------------------- | ----------------------------- |
| Die width                  | 3600 um                       |
| Die height                 | 5000 um                       |
| Core area                  | [425, 425] to [3175, 4575] um |
| Tile width (block.pitch)   | 217.44 um                     |
| Tile height (block.height) | 154.98 um                     |
| Grid dimensions            | 12 columns x 20 rows          |
| Total tiles                | 240                           |

### 3.1 Routing

- Metal1-Metal5: 480nm X pitch, 420nm Y pitch
- TopMetal1/2: 3400nm pitch
- Standard cell site: 480nm x 3780nm

### 3.2 Seal Ring

Seal ring is instantiated around the full die perimeter using the IHP SG13G2
seal ring generator (pycell4klayout-api).

### 3.3 Fill

Metal fill is generated using KLayout scripts to meet density requirements
for all metal layers.

## 4. Multiplexer Architecture

### 4.1 tt_ctrl (Address Controller)

Active-low select chain that routes control signals to the mux array.
Connected to pad ring GPIOs via Metal4/Metal3 custom routes.

### 4.2 tt_mux (Multiplexer Array)

Connects user project I/Os to the chip's external pins based on the
selected address. Each mux unit handles one column of tiles.

### 4.3 tt_top (Top-Level Wrapper)

Instantiates tt_ctrl, tt_mux grid, padring, and user project macros.
Custom routing connects all components via Metal4 vertical spines
and Metal5 horizontal links.

## 5. Verification

- **RTL simulation:** cocotb + iverilog (test_mux)
- **Gate-level simulation:** cocotb + iverilog 13 (test_mux_gl)
- **DRC:** KLayout (IHP SG13G2 rules) - PASS
- **Density:** KLayout density check - PASS
- **LVS:** Netgen (SPICE extraction via Magic) - PASS ("Circuits match uniquely")

## 6. EDA Tools

| Tool        | Purpose                                 |
| ----------- | --------------------------------------- |
| LibreLane   | RTL-to-GDS compilation flow             |
| Yosys       | Logic synthesis                         |
| OpenROAD    | Floorplanning, placement, routing, STA  |
| Magic       | SPICE extraction, DRC                   |
| Netgen      | LVS                                     |
| KLayout     | DRC, density check, GDS streamout, fill |
| iverilog 13 | Gate-level simulation                   |
| cocotb 2.x  | Testbench framework                     |
