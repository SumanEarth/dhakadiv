#!/usr/bin/env python3
"""
Regenerate data.json from the source Excel file.

Usage:
    pip install pandas openpyxl
    python3 convert.py dhaka-div-maps.xlsx

Expects two columns: FolderPath, FileName.
Writes data.json next to this script (folders de-duplicated to keep the
file small — folder paths repeat for every file inside them).
"""
import sys
import json
import pandas as pd

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 convert.py <source.xlsx>")
        sys.exit(1)

    src = sys.argv[1]
    df = pd.read_excel(src).fillna("")

    folders = sorted(df["FolderPath"].unique())
    fidx = {f: i for i, f in enumerate(folders)}
    files = [[fidx[r.FolderPath], r.FileName] for r in df.itertuples()]

    out = {"folders": folders, "files": files}
    with open("data.json", "w", encoding="utf-8") as fp:
        json.dump(out, fp, ensure_ascii=False, separators=(",", ":"))

    print(f"Wrote data.json — {len(files)} files across {len(folders)} folders")

if __name__ == "__main__":
    main()
