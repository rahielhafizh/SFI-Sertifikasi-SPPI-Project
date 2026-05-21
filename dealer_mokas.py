#!/usr/bin/env python3

import os
import re
from openpyxl import load_workbook

SRC_PATH = r"C:\EL\REPORT_SPPI\src\DB-OWNER-DEALER.xlsx"
DEST_DIR = r"C:\EL\REPORT_SPPI\asset"
DEST_PATH = os.path.join(DEST_DIR, "DB-OWNER-DEALER-MODIFIED.xlsx")
SHEET_NAME = "DBN"

PRE_TITLE_MAP: dict[str, str] = {
    "PROF": "Prof.",
    "DR": "Dr.",
    "IR": "Ir.",
    "DRS": "Drs.",
    "DRA": "Dra.",
    "H": "H.",
    "HJ": "Hj.",
    "HM": "H.M.",
    "NY": "Ny.",
    "TN": "Tn.",
    "RR": "Rr.",
}

POST_DEGREE_MAP: dict[str, str] = {
    "SE": "S.E",
    "SH": "S.H",
    "ST": "S.T",
    "SI": "S.I",
    "SIP": "S.I.P",
    "SSOS": "S.Sos",
    "SKOM": "S.Kom",
    "SAG": "S.Ag",
    "SPD": "S.Pd",
    "SKM": "S.K.M",
    "SFARM": "S.Farm",
    "SKEP": "S.Kep",
    "SGZ": "S.Gz",
    "SP": "S.P",
    "AMD": "A.Md",
    "MM": "M.M",
    "MT": "M.T",
    "MSI": "M.Si",
    "MPD": "M.Pd",
    "MH": "M.H",
    "MBA": "M.B.A",
    "PHD": "Ph.D",
    "MKES": "M.Kes",
    "MKOM": "M.Kom",
    "MSC": "M.Sc",
    "MAK": "M.Ak",
    "AK": "Ak",
    "CPA": "C.P.A",
    "CFP": "C.F.P",
    "CIA": "C.I.A",
    "NS": "Ns",
}

POST_DEGREE_PAIR_MAP: dict[tuple[str, str], str] = {
    ("S", "KOM"): "S.Kom",
    ("S", "IK"): "S.I.K",
    ("S", "KED"): "S.Ked",
    ("S", "AB"): "S.A.B",
    ("S", "HUT"): "S.Hut",
    ("S", "IKOM"): "S.I.Kom",
    ("S", "SOS"): "S.Sos",
    ("S", "PD"): "S.Pd",
    ("A", "MD"): "A.Md",
    ("M", "GZ"): "M.Gz",
    ("M", "SC"): "M.Sc",
}

BALINESE_SECONDARY: frozenset[str] = frozenset(
    {
        "DEWA",
        "GUSTI",
        "KETUT",
        "MADE",
        "NENGAH",
        "WAYAN",
        "GEDE",
        "GDE",
        "KADEK",
        "KOMANG",
        "NYOMAN",
        "PUTU",
        "BAGUS",
        "ALIT",
        "LUH",
        "AGUNG",
        "COKORDA",
    }
)


def _key(token: str) -> str:
    return token.replace(".", "").upper()


def _is_initial(token: str) -> bool:
    core = token.rstrip(".")
    return len(core) == 1 and core.isalpha()


def normalize_dealer_name(raw: str) -> str:
    if not isinstance(raw, str):
        return raw
    return raw.strip().upper()


def normalize_owner_name(raw: str) -> str:
    if not isinstance(raw, str):
        return raw

    raw = raw.strip()
    if not raw:
        return raw

    tokens: list[str] = [t for t in re.split(r"[\s,]+", raw) if t]
    if not tokens:
        return raw

    pre_titles: list[str] = []
    post_degrees: list[str] = []

    while tokens and _key(tokens[0]) in PRE_TITLE_MAP:
        pre_titles.append(PRE_TITLE_MAP[_key(tokens.pop(0))])

    while tokens:
        consumed = False
        if len(tokens) >= 2:
            pair = (_key(tokens[-2]), _key(tokens[-1]))
            if pair in POST_DEGREE_PAIR_MAP:
                post_degrees.insert(0, POST_DEGREE_PAIR_MAP[pair])
                tokens.pop()
                tokens.pop()
                consumed = True
        if not consumed and _key(tokens[-1]) in POST_DEGREE_MAP:
            post_degrees.insert(0, POST_DEGREE_MAP[_key(tokens.pop())])
            consumed = True
        if not consumed:
            break

    name_parts: list[str] = []
    for idx, token in enumerate(tokens):
        k = _key(token)
        if k in PRE_TITLE_MAP:
            name_parts.append(PRE_TITLE_MAP[k])
        elif _is_initial(token):
            core = token.rstrip(".").upper()
            if (
                core == "I"
                and idx == 0
                and len(tokens) > 1
                and _key(tokens[1]) in BALINESE_SECONDARY
            ):
                name_parts.append("I")
            else:
                name_parts.append(core + ".")
        else:
            name_parts.append(token.title())

    result = " ".join(pre_titles + name_parts)
    if post_degrees:
        result += ", " + ", ".join(post_degrees)

    return result


def _build_column_index(sheet, targets: list[str]) -> dict[str, int]:
    col_map: dict[str, int] = {}
    for cell in sheet[1]:
        header = str(cell.value).strip() if cell.value is not None else ""
        if header in targets:
            col_map[header] = cell.column
    missing = [c for c in targets if c not in col_map]
    if missing:
        raise ValueError(
            f"Required column(s) not found in sheet '{sheet.title}': {missing}"
        )
    return col_map


def process_dbn_sheet(sheet) -> None:
    col_map = _build_column_index(sheet, ["DEALER_NAME", "OWNER_NAME"])
    dealer_col = col_map["DEALER_NAME"]
    owner_col = col_map["OWNER_NAME"]

    for row in sheet.iter_rows(min_row=2):
        dealer_cell = row[dealer_col - 1]
        owner_cell = row[owner_col - 1]

        if dealer_cell.value is not None:
            dealer_cell.value = normalize_dealer_name(str(dealer_cell.value))

        if owner_cell.value is not None:
            owner_cell.value = normalize_owner_name(str(owner_cell.value))


def main() -> None:
    if not os.path.isfile(SRC_PATH):
        raise FileNotFoundError(f"Source file not found: {SRC_PATH}")

    os.makedirs(DEST_DIR, exist_ok=True)

    wb = load_workbook(SRC_PATH)

    if SHEET_NAME not in wb.sheetnames:
        raise ValueError(f"Sheet '{SHEET_NAME}' not found. Available: {wb.sheetnames}")

    process_dbn_sheet(wb[SHEET_NAME])
    wb.save(DEST_PATH)
    print(f"Completed. Output written to:\n  {DEST_PATH}")


if __name__ == "__main__":
    main()
