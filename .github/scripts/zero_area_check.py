#!/usr/bin/env python3
"""Report zero-area polygons on SG13G2 drawing layers.

Report-only counterpart of ``zero.py`` from
https://github.com/IHP-GmbH/Open-Silicon-MPW/tree/main/March-2026/submitted-tmp
(the foundry strips such polygons during submission processing). Accepts any
layout format KLayout can read (GDS, OAS, ...) and exits non-zero when at
least one zero-area polygon is found.

Usage:
    python3 zero_area_check.py <layout> [--cell TOP] [--report report.txt]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import klayout.db as db

# (layer, datatype) pairs checked by the foundry.
LAYER_SPECS = [
    (1, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (14, 0), (19, 0),
    (20, 0), (27, 0), (29, 0), (30, 0), (31, 0), (32, 0), (36, 0), (44, 0),
    (49, 0), (50, 0), (66, 0), (67, 0), (72, 0), (73, 0), (74, 0), (75, 0),
    (77, 0), (83, 0), (84, 0), (125, 0), (126, 0), (128, 0), (129, 0),
    (132, 0), (133, 0), (134, 0), (146, 0),
]


def is_zero_area(shape: db.Shape) -> bool:
    if shape.is_box():
        b = shape.box
        return b.width() == 0 or b.height() == 0
    if shape.is_path():
        p = shape.path
        return p.width == 0 or p.polygon().area() == 0
    if shape.is_polygon():
        return shape.polygon.area() == 0
    if shape.is_simple_polygon():
        return shape.simple_polygon.area() == 0
    return False


def scan(layout: db.Layout, top: db.Cell | None) -> tuple[int, dict[str, int], dict[str, int]]:
    layer_indices = {}
    for layer, datatype in LAYER_SPECS:
        li = layout.find_layer(layer, datatype)
        if li is not None and li >= 0:
            layer_indices[f"{layer}/{datatype}"] = li

    cells = layout.each_cell()
    if top is not None:
        wanted = {top.cell_index()} | set(top.called_cells())
        cells = (layout.cell(ci) for ci in sorted(wanted))

    total = 0
    by_layer: dict[str, int] = {}
    by_cell: dict[str, int] = {}
    for cell in cells:
        for key, li in layer_indices.items():
            n = sum(1 for s in cell.shapes(li).each() if is_zero_area(s))
            if n:
                total += n
                by_layer[key] = by_layer.get(key, 0) + n
                by_cell[cell.name] = by_cell.get(cell.name, 0) + n
    return total, by_layer, by_cell


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("layout", type=Path)
    ap.add_argument("--cell", help="top cell (default: scan every cell)")
    ap.add_argument("--report", type=Path, help="write the report to this file")
    args = ap.parse_args()

    layout = db.Layout()
    layout.read(str(args.layout))
    top = None
    if args.cell:
        top = layout.cell(args.cell)
        if top is None:
            print(f"Error: cell '{args.cell}' not found in {args.layout}", file=sys.stderr)
            return 2

    total, by_layer, by_cell = scan(layout, top)

    lines = [
        "Zero-area polygon check",
        f"Layout: {args.layout}",
        f"Top cell: {args.cell or '(all cells)'}",
        f"Total zero-area polygons: {total}",
        "",
        "Counts by layer:",
    ]
    lines += [f"- {k}: {by_layer[k]}" for k in sorted(by_layer)] or ["- none"]
    lines += ["", "Counts by cell:"]
    lines += [f"- {k}: {by_cell[k]}" for k in sorted(by_cell)] or ["- none"]
    text = "\n".join(lines) + "\n"
    print(text, end="")
    if args.report:
        args.report.write_text(text, encoding="utf-8")

    print(f"Number of zero-area polygons: {total}")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
