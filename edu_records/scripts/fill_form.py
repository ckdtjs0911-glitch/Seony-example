"""누적 교육 기록(data/<연도>.json)을 원본 양식에 채워 Word 파일을 만든다.

사용법:
  python3 fill_form.py <연도> [출력 경로]

원본 양식은 건드리지 않고 복사본에 교육 행(교육일자·교육명·교육시간·교육기관·비고)만 채운다.
글자 서식은 각 칸의 기존 문단 서식(맑은 고딕 등)을 그대로 따른다.
직원 한 명의 교육이 양식의 빈 행(12행)보다 많으면 마지막 행을 같은 서식으로 복제해 늘린다.
"""
import copy
import json
import sys
from datetime import date
from pathlib import Path

import docx
from docx.oxml.ns import qn

BASE = Path(__file__).resolve().parent.parent
HEADER_ROW = 11  # '교 육 일 자 | 교 육 명 | ...' 행
NAME_ROW, NAME_COL = 1, 4
FIELDS = ["date_text", "course", "hours", "institution", "note"]


def unique_cells(row):
    seen, out = set(), []
    for c in row.cells:
        if id(c._tc) not in seen:
            seen.add(id(c._tc))
            out.append(c)
    return out


def set_text(cell, text):
    p = cell.paragraphs[0]
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    if not text:
        return
    run = p.add_run(text)
    ppr = p._p.pPr
    mark = ppr.find(qn("w:rPr")) if ppr is not None else None
    if mark is not None:
        run._r.insert(0, copy.deepcopy(mark))


def main():
    year = int(sys.argv[1])
    cfg = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
    data = json.loads((BASE / "data" / f"{year}.json").read_text(encoding="utf-8"))
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else (
        BASE / "output" / f"UIT-F601-03_개인교육훈련기록표_{year}_{date.today():%Y%m%d}.docx")

    doc = docx.Document(BASE / cfg["template"])
    for emp in cfg["employees"]:
        table = doc.tables[emp["table_index"]]
        name = table.rows[NAME_ROW].cells[NAME_COL].text.replace(" ", "")
        if name != emp["name"]:
            sys.exit(f"양식 {emp['table_index']}번 표의 성명({name})이 설정({emp['name']})과 다름")
        recs = [r for r in data["records"] if r["employee"] == emp["name"]]
        rows = table.rows[HEADER_ROW + 1:]
        while len(rows) < len(recs):
            last = rows[-1]._tr
            new = copy.deepcopy(last)
            last.addnext(new)
            rows = table.rows[HEADER_ROW + 1:]
        for rec, row in zip(recs, rows):
            for cell, key in zip(unique_cells(row), FIELDS):
                set_text(cell, rec.get(key, ""))
        print(f"{emp['name']}: {len(recs)}건")

    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out)
    print(out)


if __name__ == "__main__":
    main()
