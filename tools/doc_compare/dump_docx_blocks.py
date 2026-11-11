"""docx 문단·표를 순서대로 뽑고 LibreOffice PDF 기준 쪽 번호를 붙인다.

사용법: python dump_docx_blocks.py 원본.docx 원본.pdf 결과.json
"""
import sys, json, re, subprocess
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
doc = Document(sys.argv[1])
blocks = []
for el in doc.element.body.iterchildren():
    tag = el.tag.split('}')[1]
    if tag == 'p':
        t = Paragraph(el, doc).text.strip()
        if t: blocks.append({"t": "p", "text": t})
    elif tag == 'tbl':
        tb = Table(el, doc)
        rows = []
        for r in tb.rows:
            cells = []
            prev = None
            for c in r.cells:
                if c._tc is prev: continue
                prev = c._tc
                cells.append(c.text.strip())
            rows.append(cells)
        blocks.append({"t": "tbl", "rows": rows})
# page mapping via pdftotext
pages = []
n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', sys.argv[2]], capture_output=True, text=True).stdout).group(1))
for i in range(1, n + 1):
    txt = subprocess.run(['pdftotext', '-f', str(i), '-l', str(i), '-layout', sys.argv[2], '-'], capture_output=True, text=True).stdout
    pages.append(re.sub(r'\s+', '', txt))
cur = 0
for b in blocks:
    key = re.sub(r'\s+', '', b["text"] if b["t"] == "p" else ''.join(''.join(r) for r in b["rows"]))[:12]
    for j in range(cur, n):
        if key and key in pages[j]:
            cur = j; break
    b["page"] = cur + 1
json.dump(blocks, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
for i, b in enumerate(blocks):
    s = b["text"] if b["t"] == "p" else "[TBL] " + " | ".join(b["rows"][0])
    print(i, f"p{b['page']}", s[:70])
