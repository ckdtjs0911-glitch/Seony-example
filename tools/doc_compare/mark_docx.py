"""우리 문서(docx)에 비교 결과의 추가·수정 위치를 표시한 사본을 만든다.

사용법: python mark_docx.py 원본.docx 표시.json 결과.docx

표시.json 형식 (목록):
  {"anchor": "기준 문단의 앞부분 글자", "mode": "add" | "mod",
   "label": "짧은 제목", "lines": ["넣을 문장", ...], "memo": "선택"}
- anchor 문단 바로 뒤에 표시 문단을 넣는다. 원본 문단은 바꾸지 않는다.
- add(추가)는 파랑, mod(수정 제안)는 빨강으로 표시한다.
"""
import copy
import json
import re
import sys

from docx import Document
from docx.enum.text import WD_COLOR_INDEX
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

STYLE = {
    "add": ("[추가]", RGBColor(0x1D, 0x4E, 0xD8), WD_COLOR_INDEX.TURQUOISE),
    "mod": ("[수정 제안]", RGBColor(0xB4, 0x23, 0x18), WD_COLOR_INDEX.PINK),
}


def norm(s):
    return re.sub(r"\s+", "", s)


def insert_after(par, text, color, highlight, bold=False, size=None):
    new = copy.deepcopy(par._p)
    for child in list(new):
        if child.tag != qn("w:pPr"):
            new.remove(child)
    par._p.addnext(new)
    from docx.text.paragraph import Paragraph
    p = Paragraph(new, par._parent)
    r = p.add_run(text)
    r.font.color.rgb = color
    r.font.highlight_color = highlight
    r.font.bold = bold
    if size:
        r.font.size = Pt(size)
    return p


def main(src, spec_path, dst):
    doc = Document(src)
    spec = json.load(open(spec_path, encoding="utf-8"))
    pars = [p for p in doc.paragraphs]
    missing = []
    for item in spec:
        key = norm(item["anchor"])
        target = next((p for p in pars if norm(p.text).startswith(key)), None)
        if target is None:
            missing.append(item["anchor"])
            continue
        tag, color, hl = STYLE[item["mode"]]
        cur = insert_after(target, f"{tag} {item['label']}", color, hl, bold=True)
        for line in item["lines"]:
            cur = insert_after(cur, line, color, hl)
        if item.get("memo"):
            cur = insert_after(cur, f"※ {item['memo']}", color, hl, size=8)
    doc.save(dst)
    print(f"marked {len(spec) - len(missing)} / {len(spec)}")
    for m in missing:
        print("anchor not found:", m)


if __name__ == "__main__":
    main(*sys.argv[1:4])
