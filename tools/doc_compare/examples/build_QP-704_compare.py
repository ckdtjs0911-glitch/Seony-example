"""QP-704 비교 HTML 생성 예시 (doc_compare.md 4절 참고).

새 비교를 만들 때는 이 파일을 복사해 "sections" 부분(절별 원문 범위, 표시 문구, 비교 의견)만 바꾼다.
사용법: python build_QP-704_compare.py a_blocks.json 참고본.txt 참고본.xml 샘플.html 결과.html
  - a_blocks.json: dump_docx_blocks.py 출력
  - 참고본.txt / 참고본.xml: hwp5txt / hwp5proc xml 출력
  - 샘플.html: samples/doc-compare/QP-706_vs_QP-711_sample.html (스타일을 가져옴)
"""
import html
import json
import re
import sys

a_json, b_txt, b_xml, css_src, out = sys.argv[1:6]
A = json.load(open(a_json, encoding="utf-8"))
B_LINES = open(b_txt, encoding="utf-8").read().split("\n")
X = open(b_xml, encoding="utf-8").read()

# ---- reference tables from the HWP (T0..T7, in document order)
def hwp_tables():
    out = []
    for t in re.findall(r"<TableControl\b.*?</TableControl>", X, re.S):
        rows = {}
        for c in re.findall(r"<TableCell\b(.*?)</TableCell>", t, re.S):
            r = int(re.search(r'row="(\d+)"', c).group(1))
            col = int(re.search(r'col="(\d+)"', c).group(1))
            txt = "".join(re.findall(r"<Text[^>]*>([^<]*)</Text>", c)).strip()
            rows.setdefault(r, []).append((col, txt))
        out.append([[t for _, t in sorted(rows[r])] for r in sorted(rows)])
    return out

TBL = hwp_tables()
PLACEHOLDER_LINES = [i for i, l in enumerate(B_LINES, 1) if l.strip() == "<표>"]
TBL_AT = dict(zip(PLACEHOLDER_LINES, range(len(TBL))))

esc = html.escape


def mark(text, marks):
    s = esc(text)
    for sub, cls in marks:
        e = esc(sub)
        if e in s:
            s = s.replace(e, f'<span class="mk-{cls}">{e}</span>', 1)
    return s


def table_html(rows, marks=()):
    h = '<table class="src">'
    for r in rows:
        h += "<tr>" + "".join(f"<td>{mark(c, marks)}</td>" for c in r) + "</tr>"
    return h + "</table>"


MODS = {}  # block_index -> (tag, short text): 수정할 위치 표시 (반드시 반영 / 반영 권장)


def mod_mark(i):
    tag, text = MODS[i]
    return f'<p class="mod-mark"><span class="tag {tag}">{TAG[tag]}</span> {text} (→ 비교 의견)</p>'


def a_html(lo, hi, extra=None):
    """Blocks lo..hi (inclusive) of QP-704 with page markers. extra: {block_index: html after it}"""
    h, page, first = "", None, True
    for i in range(lo, hi + 1):
        b = A[i]
        if b["page"] != page:
            page = b["page"]
            h += f'<span class="pg706{" first" if first else ""}">p.{page}</span>'
            first = False
        if b["t"] == "p":
            h += f"<p>{esc(b['text'])}</p>"
        else:
            h += table_html(b["rows"])
        if i in MODS:
            h += mod_mark(i)
        if extra and i in extra:
            h += extra[i]
    return h


def b_html(ranges, marks=()):
    h = ""
    for lo, hi in ranges:
        for n in range(lo, hi + 1):
            line = B_LINES[n - 1]
            if n in TBL_AT:
                h += table_html(TBL[TBL_AT[n]], marks)
            elif line.strip():
                h += f"<p>{mark(line.strip(), marks)}</p>"
    return h


def pages(lo, hi):
    ps = sorted({A[i]["page"] for i in range(lo, hi + 1)})
    return f"704 p.{ps[0]}" + (f"–{ps[-1]}" if len(ps) > 1 else "")


EMPTY = '<p class="empty">— 해당 내용 없음 —</p>'
TAG = {"high": "수정·추가", "mid": "수정", "ok": "유지", "na": "선택"}
MODS.update({
    1: ("mid", "개정 일자·개정번호 정리"),
    5: ("high", "적용 대상(독립형 소프트웨어) 명시"),
    63: ("high", "PHASE-1 하드웨어 표현 정리"),
    75: ("mid", "아키텍처 구성(모듈·외부 연동·SOUP)으로 수정"),
    86: ("mid", "안전성 등급 정의 문장 수정"),
    100: ("mid", "\"H/W E/S승인\" 등 장비 표현 정리"),
    108: ("mid", "이력/버전 관리 시스템 조건 추가"),
    112: ("mid", "\"설계 사양을\" → \"요구사항을\""),
    139: ("mid", "(2) 번호 중복"),
    153: ("mid", "추적성 연결 대상 구체화"),
    157: ("mid", "\"양산용\" 표현 정리"),
    174: ("mid", "45일 이내 보고서 시점 확인"),
    177: ("high", "밸리데이션 보고서 작성·승인 주체 통일"),
    197: ("high", "배포 승인자 정리, 최종 배포 조건 추가"),
    211: ("high", "장비 운용파일 설명을 소프트웨어 제품에 맞게 수정"),
    212: ("high", "파일 이름·버전 표기 체계 수정"),
    225: ("high", "버전 체계와 올리는 기준"),
    232: ("mid", "\"고객이 원하는 경우\" 범위 정리"),
    249: ("mid", "양식 목록 보완, 번호 통일"),
})


def note(tags, title, bullets, ex=None, memo=None):
    h = "".join(f'<span class="tag {t}">{TAG[t]}</span> ' for t in tags)
    h += f"<br><b>{title}</b>"
    for b in bullets:
        h += f"<br>· {b}"
    if ex:
        h += f'<div class="ex"><b>예시문</b><br>{ex}</div>'
    if memo:
        h += f'<div class="ex-memo">※ {memo}</div>'
    return h


def arrow(text):
    return f'<p class="arrow-add">{text}</p>'


rows = []  # (id, title, cnt, pg, row_html)


def sec(sid, title, cnt, pg, a, b, nt, a_empty=False, b_empty=False):
    ac = f'<td class="txt">{a}</td>' if not a_empty else f'<td class="empty">— 해당 내용 없음 —{a}</td>'
    bc = f'<td class="txt">{b if not b_empty else EMPTY}</td>'
    pgs = f'<span class="pgsec">{pg}</span>' if pg else ""
    rows.append((sid, title, f'<tr class="sec" id="{sid}"><td colspan="3">{title} <span class="cnt">{cnt}</span>{pgs}</td></tr>'
                 f'<tr>{ac}{bc}<td class="nt">{nt}</td></tr>'))


# ===================== sections =====================
sec("r1", "1. 표지·개정 이력", "양쪽", pages(0, 1),
    a_html(0, 1), b_html([(1, 11)]),
    note(["mid"], "개정 정보 정리",
         ["결재란·제개정 이력의 \"2027.02.00\"을 실제 날짜로 확정함",
          "개정 이력은 Rev.1인데 머리글 개정번호는 0, 바닥글은 \"UIT-QP-704 (Rev.0)\"임 → 개정 이력에 맞게 고침",
          "참고본처럼 목차를 넣을지는 선택임"]))

sec("r2", "2. 목적", "양쪽", pages(2, 3),
    a_html(2, 3), b_html([(13, 14)], [("고객 및 법적으로 요구된 제반 조건에 대한", "add")]),
    note(["na"], "고객·법적 요구사항 언급 추가 (선택)",
         ["704 목적이 더 구체적이라 그대로 써도 됨",
          "참고본처럼 고객·법적 요구사항을 충족한다는 내용을 넣을 수 있음"],
         ex="본 절차서는 주식회사 유로인사이트(이하 ‘당사’라 한다.)의 S/W 개발 내부 프로세스를 규정하고, 고객 및 법적 요구사항을 충족하며 의료기기의 안전성을 확보하기 위해 S/W 개발, 배포, 유지보수 등이 관련 부서와의 협력 하에 효과적으로 이루어지도록 하는 데 그 목적이 있다."))

sec("r3", "3. 적용범위", "양쪽", pages(4, 5),
    a_html(4, 5), b_html([(16, 17)], [("제품 및 내장소프트웨어 및 단독 소프트웨어에 대한 개발 전반", "mod")]),
    note(["high"], "적용 대상 명시",
         ["\"품질보증업무 수행에 필요한 유효성 관리 업무\"만으로는 개발·배포·유지보수 전체에 적용되는지 분명하지 않음",
          "독립형 소프트웨어(SaMD)를 적용 대상으로 적음"],
         ex="본 절차서는 당사가 개발하는 독립형 소프트웨어(SaMD)의 개발, 검증 및 유효성 확인, 배포, 유지보수 전반에 적용한다.",
         memo="UroInsight CheckUp이 독립형 소프트웨어라는 것은 이전 UDI·통합정보 자료에서 확인한 내용임. 의료기기에 포함된 소프트웨어도 개발한다면 대상에 추가함"))

# ---- definitions table
def def_rows():
    r = []
    def row(a_title, a_body, a_pg, b_title, b_body, nt):
        ac = (f'<span class="pg706 first">p.{a_pg}</span><div class="dt">{esc(a_title)}</div>{esc(a_body)}' if a_title
              else '<p class="empty">— 해당 내용 없음 —</p>')
        bc = (f'<div class="dt">{b_title}</div>{b_body}' if b_title else '<p class="empty">— 해당 내용 없음 —</p>')
        r.append(f"<tr><td>{ac}</td><td>{bc}</td><td>{nt}</td></tr>")
    T = lambda i: A[i]["text"]
    row(T(7), T(8), 2, "", "", note(["mid"], "번호 중복·오타 수정",
        ["3.1이 두 번 나옴 → 이 항목부터 3.1~3.10으로 다시 매김",
         "오타 \"소프트웨어사\"를 \"소프트웨어가\"로 수정함"],
        ex="3.1 소프트웨어 설계 규격<br>소프트웨어가 어떤 기능을 어떻게 수행할 것인가를 설명한 것"))
    for i, j in [(9, 10), (11, 12), (13, 14), (15, 16), (17, 18), (19, 20), (21, 22), (23, 24)]:
        row(T(i), T(j), 2, "", "", note(["ok"], "그대로 유지", ["번호 정리 후 하나씩 밀림"]))
    row(T(25), T(26), 2, "", "", note(["mid"], "정의 보강",
        ["\"목적에 적합한 아이템의 버전\"은 뜻이 분명하지 않음",
         "특정 목적으로 내놓는 형상 항목의 특정 버전이라는 뜻으로 고침"],
        ex="3.10 배포(Release)<br>특정 목적으로 사용할 수 있도록 제공되는 형상 항목의 특정 버전",
        memo="IEC 62304의 release 정의를 참고한 문장임 [확인 필요: 규격 원문의 정의 문구]"))
    for lo, hi, title, tags, nt_title, bl in [
        (20, 21, "3.1 설계 및 개발 입력", ["na"], "추가 선택", ["설계 및 개발관리 절차서(UIT-QP-703)에 정의가 있으면 생략함"]),
        (22, 24, "3.2 설계 및 개발 출력", ["na"], "추가 선택", ["위와 같음"]),
        (25, 26, "3.3 설계 및 개발 도면", ["na"], "추가 불필요", ["하드웨어 도면 정의라 소프트웨어 절차서에는 필요 없음"]),
        (27, 28, "3.4 설계 및 개발 검증", ["mid"], "정의 추가 권장",
         ["704 본문에서 \"검증\"과 \"유효성 확인\"을 여러 번 쓰므로 두 용어를 정의함"]),
        (29, 30, "3.5 설계 및 개발 유효성 확인", ["mid"], "정의 추가 권장", ["위와 같음"]),
    ]:
        body = " ".join(l.strip() for l in B_LINES[lo - 1:hi] if l.strip())
        cls = "add" if tags == ["mid"] else None
        b_body = f'<span class="mk-add">{esc(body)}</span>' if cls else esc(body)
        b_title = f'<span class="mk-add">{esc(title)}</span>' if cls else esc(title)
        row("", "", 0, b_title, b_body, note(tags, nt_title, bl))
    return ('<tr><td colspan="3" class="inner"><table class="def"><tr><th>UIT-QP-704</th><th>참고본</th><th>비교 의견</th></tr>'
            + "".join(r) + "</table></td></tr>")

rows.append(("r4", "4. 용어의 정의",
             f'<tr class="sec" id="r4"><td colspan="3">4. 용어의 정의 <span class="cnt">704: 10개 · 참고본: 5개</span>'
             f'<span class="pgsec">{pages(6, 26)}</span></td></tr>' + def_rows()))

sec("r5", "5. 책임과 권한", "양쪽", pages(27, 54),
    a_html(27, 54, {27: arrow("➜ [704 p.2] 교체: 4.1~4.3 전체를 오른쪽 예시문(회사 상황에 맞춘 재배정)으로 바꿈")}),
    b_html([(32, 44)]),
    note(["high"], "회사 상황에 맞춰 재배정, 중복 삭제",
         ["개발팀장·S/W Project Leader가 없음 → 그 업무를 대표이사, S/W개발담당자, 품질관리팀으로 옮김(사용자 지정 배정)",
          "\"4.3 S/W개발담당자\"가 같은 내용으로 두 번 나옴 → 하나를 삭제함",
          "품질책임자는 4.4로 고침",
          "5장 본문의 개발팀장·S/W Project Leader도 이 배정에 맞게 바꿔야 함"],
         ex="4.1 대표이사<br>(1) 개발 계획서에 따라 Project별 인원 및 기능별 개발자 배정<br>(2) S/W 설계사양서 최종 승인<br>(3) 이력/버전 관리 시스템 검토<br>(4) S/W 배포기록서 승인<br>4.2 S/W개발담당자<br>(1) 담당 프로젝트의 기능별 S/W 설계사양서 목록 작성<br>(2) 개발하고자 하는 S/W 설계사양서 작성<br>(3) S/W 설계사양서에 준하여 S/W 구현<br>(4) S/W 버전 및 변경이력 기록<br>(5) S/W 개발 단계에서 발생하는 S/W 파일 및 문서 관리 및 보존<br>(6) 이력/버전 관리 시스템 선정<br>(7) S/W 유지보수 주관<br>(8) S/W 배포기록서 및 동작설명서 작성<br>(9) S/W 개발완료 보고서 작성<br>4.3 품질관리팀<br>(1) S/W 변경 이력 관리<br>4.4 품질책임자<br>(1) 전자기록, 전자서명 관리 및 소프트웨어 유효성 확인에 대한 총괄적인 책임과 권한<br>(2) 소프트웨어 개발 환경 및 자원 제공",
         memo="변경 이력의 \"기록\"(개발담당자)과 \"관리\"(품질관리팀)의 범위 구분 확인 필요"))

sec("r6", "6. S/W 유효성관리 원칙 (회귀시험·독립성)", "참고본만", "",
    arrow("➜ [704 p.9] 추가 위치: 5.1.15 (2) 유지보수 절차 5) 뒤에 회귀시험 항목 추가"),
    b_html([(47, 67)], [("S/W 개발자는 변경되지 않는 시스템의 취약한 부분이 악영향을 받지 않는다는 것을 입증하기", "add"),
                        ("S/W 유효성 검토가 다른 부분에 영향을 받지 않고 독립적인 평가가 이루어지도록 한다.", "add")]),
    note(["high"], "회귀시험 추가, 독립성은 일부 반영됨",
         ["704에는 변경 후 회귀시험 언급이 없음 → 유지보수 절차에 추가함",
          "독립 검토는 704의 설계 적격성 평가·통합 테스트 보고서(5.1.9 (4), 5.1.11 (7))에만 있음 → 시스템 테스트·밸리데이션 보고서에도 같은 원칙을 둘지 검토함"],
         ex="6) 회귀시험: S/W를 변경한 경우 변경 부분의 검증뿐 아니라 변경이 전체 S/W에 미치는 영향을 분석하고, 변경하지 않은 부분이 영향을 받지 않음을 확인하기 위한 회귀시험의 범위를 정하여 수행한다."),
    a_empty=True)

sec("r7", "7. 생명주기 모델", "양쪽", pages(80, 82),
    a_html(80, 82), b_html([(69, 80)]),
    note(["ok"], "V 모델 유지", ["704는 V 모델 그림으로 생명주기를 보여 줌",
                                 "유지보수 절(5.1.15)에 폐기까지 적혀 있어 참고본의 9단계를 따로 넣지 않아도 됨"]))

sec("r8", "8. 개발 계획 (PHASE-0)", "양쪽", pages(56, 98),
    a_html(56, 62, {62: arrow("➜ [704 p.4] 추가: 5.1.1 (6) 개발계획서 포함 항목 (오른쪽 예시문)")}) + a_html(87, 98), b_html([(82, 114)], [("1) S/W 주요기능", "add"), ("7) S/W 개발 단계", "add"),
                                                          ("8) S/W 개발 일정", "add"), ("9) S/W관련 위험관리", "add")]),
    note(["mid"], "개발계획서 포함 항목 추가",
         ["704는 개발계획서(UIT-F704-01) 승인 후 PL을 임명한다고만 하고, 계획서에 무엇을 적는지 정하지 않음",
          "밸리데이션 계획서(UIT-SVP-AAA) 10개 항목은 있음 → 개발계획서 항목도 정함"],
         ex="(6) 소프트웨어 개발계획서(UIT-F704-01)에는 최소한 다음 사항을 포함한다.<br>1) S/W 주요 기능 2) 개발 단계와 일정 3) 업무 분장과 자원 4) 개발 환경 및 도구 5) 단계별 산출물과 검토·승인 6) 위험관리 활동 7) 형상관리 및 문제 해결 방법",
         memo="[확인 필요: IEC 62304의 소프트웨어 개발 계획 요구 항목과 대조]"))

sec("r9", "9. 개발관리 시스템", "양쪽", pages(32, 108),
    a_html(32, 32) + a_html(108, 108), b_html([(116, 121)], [("2) 개발 결과물의 Upload, Download 및 수정에 대한 권한 부여가 가능할 것", "add")]),
    note(["mid"], "시스템 조건 추가",
         ["704는 개발팀장이 이력/버전 관리 시스템을 선정하고 반드시 쓰도록 했지만, 시스템이 갖출 조건이 없음",
          "권한 관리와 변경 이력 기록 조건을 추가함"],
         ex="(9) 소프트웨어 개발 과정에서 개발팀장이 선정한 이력/버전 관리 시스템을 반드시 사용해야 한다. 이 시스템은 개발 결과물을 한곳에 저장하고, 등록·수정 권한을 관리하며, 변경 이력을 남길 수 있어야 한다."))

sec("r10", "10. 개발과제 규격화 단계 (PHASE-1)", "704만", pages(63, 68),
    a_html(63, 68), "", note(["high"], "하드웨어 표현 정리",
        ["\"H/W 성능시험 S/W\", \"H/W승인용 S/W\", \"시험 시료\"는 장비 개발용 표현임",
         "독립형 소프트웨어에는 H/W 승인 단계가 없으므로 이 단계를 과제 규격화로 바꿈"],
        ex="5.1.2 개발과제 규격화 단계(PHASE-1)<br>(1) S/W Project Leader는 개발해야 할 세부 과제를 추출하고 과제별 담당자를 지정하며, 담당자는 과제별 S/W 설계사양서를 작성하여 개발팀장의 승인을 받는다.<br>(2) 개발 중 발견한 문제점은 소프트웨어 변경이력서(UIT-F704-02)에 따라 관리한다.",
        memo="H/W 연동 장비를 함께 개발하는 경우에는 기존 문구를 남김"), b_empty=True)

sec("r11", "11. 위험 분석", "양쪽", pages(69, 72),
    a_html(69, 72), b_html([(181, 192)]),
    note(["ok"], "그대로 유지 (확인 조건 있음)", ["위험분석관리 절차서(UIT-QP-705)를 따르고 위험관리 출력물을 설계 입력으로 다룸",
                               "확인 필요: 참고본의 위험 심각도 3단계와 704의 안전성 등급(5.1.5 (2))은 같은 분류가 아님 → 심각도 기준이 UIT-QP-705에 있는지 확인함"]))

sec("r12", "12. 소프트웨어 아키텍처", "양쪽", pages(73, 79),
    a_html(73, 79), b_html([(168, 168), (174, 175)], [("(9) 보조 프로그램(예, 운영시스템, 드라이버, 다른 응용 S/W)", "add")]),
    note(["mid"], "아키텍처 구성 수정",
         ["4계층(장치드라이버·하드웨어 계층)은 장비 내장 S/W용 구조임",
          "독립형 소프트웨어는 모듈 간 인터페이스, 외부 시스템(PACS 등) 연동, 외부 소프트웨어(SOUP)를 아키텍처에 적는 것이 중요함"],
         ex="(2) Software Architecture에는 다음을 포함한다.<br>1) 소프트웨어 모듈과 모듈 간 인터페이스<br>2) 외부 시스템(예: PACS)과의 인터페이스<br>3) 운영체제, 라이브러리 등 외부에서 가져온 소프트웨어(SOUP)와 그 버전 및 필요한 사양",
         memo="[확인 필요: IEC 62304 아키텍처 설계 요구사항과 대조]"))

sec("r13", "13. 소프트웨어 안전성 등급", "양쪽", pages(83, 86),
    a_html(83, 86), b_html([(132, 157)]),
    note(["mid"], "정의 문장 수정, 등급별 문서 기준 검토",
         ["704 표의 설명이 \"~를 입힌 경우\"로 되어 있어 이미 일어난 일처럼 읽힘 → \"~가 발생할 수 있는 경우\"로 고침",
          "참고본 표3처럼 등급별로 작성할 문서를 정할지 검토함. 다만 참고본 표1~3은 FDA 제출문서 가이드 방식으로 보이며 [확인 필요: 출처], 규격 요구사항으로 볼 근거는 없음"],
         ex="Class A: 소프트웨어 시스템의 고장이나 잠재적 결함으로 상해가 발생할 수 없는 경우<br>Class B: 중상이 아닌 상해가 발생할 수 있는 경우<br>Class C: 사망 또는 중상이 발생할 수 있는 경우",
         memo="[확인 필요: IEC 62304 안전 등급 정의와 개정판(AMD1:2015)의 분류 방법]"))

sec("r14", "14. 프로그래밍 및 디버깅 단계 (PHASE-2)", "704만", pages(99, 110),
    a_html(99, 110), "", note(["mid"], "하드웨어 표현 정리",
        ["\"H/W E/S승인\", \"장비의 설계변경\", \"장비의 S/W\"는 장비 개발용 표현임 → 소프트웨어 제품에 맞게 고침",
         "(5) \"특별히 H/W 설계변경의 기술적 사유를 ... 담당자에게 알린다\"는 주어가 없음 → 삭제하거나 주체를 적음"]),
    b_empty=True)

sec("r15", "15. 소프트웨어 요구사항 명세서 (SRS)", "양쪽", pages(111, 120),
    a_html(111, 120, {120: arrow("➜ [704 p.7] 추가: 5.1.7 (4) 추가 요구사항 처리 (오른쪽 예시문)")}), b_html([(123, 130)], [("7.3.2 연구개발부서장은 개발 중 및 개발완료 후 추가적으로 발생되는 소프트웨어 요구사항에 대", "add")]),
    note(["mid"], "문장 수정, 추가 요구사항 처리 추가",
         ["(1) \"설계 사양을 소프트웨어 요구사항 명세서에 문서화\" → SRS에는 설계가 아니라 요구사항을 적으므로 \"요구사항을\"으로 고침",
          "개발 중·후에 생긴 요구사항을 기록하고 SRS 갱신 여부를 판단하는 절차를 추가함"],
         ex="(4) 개발 중 또는 개발 완료 후 새로 생긴 요구사항은 기록하고, SRS와 관련 산출물의 갱신 필요 여부를 판단하여 반영한다."))

sec("r16", "16. 설계 명세서 (SDS) · 설계 적격성 평가", "양쪽", pages(121, 130),
    a_html(121, 130, {124: arrow("➜ [704 p.7] 추가: 5.1.8 (4) SDS 포함 항목 (오른쪽 예시문)")}), b_html([(159, 179)], [("(8) 오류, 정보 및 경고 메시지", "add"), ("(11) 보안수단 Security measures", "add"),
                                            ("(12) 외부업체로부터 연결 또는 S/W에 대한 SDK를 공급받는 경우 관련 정보", "add")]),
    note(["mid"], "SDS 포함 항목 추가",
         ["704는 SDS와 SRS의 추적성, 설계 적격성 평가는 충실함",
          "SDS에 무엇을 적는지 정하지 않음 → 알고리즘, 데이터 흐름, 오류 메시지, 외부 S/W 연동, 보안 수단을 추가함"],
         ex="(4) SDS에는 최소한 다음 사항을 포함한다.<br>1) 모듈별 논리 구조와 처리 단계(알고리즘)<br>2) 데이터 구조와 데이터 흐름<br>3) 오류·정보·경고 메시지<br>4) 외부 시스템 및 외부 소프트웨어(SDK 등)와의 인터페이스<br>5) 보안 수단(사용자 인증, 접근 제어, 데이터 보호 등)"))

sec("r17", "17. 소프트웨어 구현", "양쪽", pages(131, 135),
    a_html(131, 135, {135: arrow("➜ [704 p.8] 추가: 5.1.10 (5) 모듈(단위) 시험 항목 (18번 행 예시문)")}), b_html([(194, 196), (167, 167)], [("(2) 개발절차 및 코딩지침(또는 프로그래밍 절차", "add")]),
    note(["na"], "코딩 지침 추가 (선택)",
         ["704는 흐름도 작성과 구현, 개발 회의 검토가 있음",
          "참고본처럼 코딩 지침(코딩 규칙)을 따르도록 할 수 있음"]))

sec("r18", "18. 검증 (통합·시스템 테스트, 추적성)", "양쪽", pages(136, 153),
    a_html(136, 153),
    b_html([(197, 222)], [("5) 세부적인 설계를 위한 단위(모듈)시험", "add"), ("9) 단위(모듈)시험 실행", "add")]),
    note(["mid"], "단위 시험 절차 추가, 번호 수정",
         ["밸리데이션 보고서(5.1.16)에는 \"모듈 테스트\"가 있는데, 본문에 모듈(단위) 시험을 하는 절차가 없음 → 5.1.10에 추가함",
          "5.1.11 (2)가 두 번 나옴 → 번호를 다시 매김",
          "5.1.13 추적성은 포괄 문장만 있음 → 요구사항–설계–시험–위험통제를 연결한다고 구체적으로 적음",
          "확인 필요: 5.1.12 시스템 테스트를 밸리데이션 보고서에서 \"유효성 평가\"로 분류함 → 소프트웨어 시스템 시험(검증)과 설계 유효성 확인을 구분할지 확인함"],
         ex="(5) S/W개발담당자는 구현한 모듈(단위)별로 단위 시험을 수행하고 결과를 소프트웨어 검증 및 유효성 확인서(UIT-VVT-AAA)에 기록한다.",
         memo="문서번호는 26번 행에서 정리하는 번호(UIT-VVT-AAA 또는 UIT-VVT-MS01)로 맞춤"))

sec("r19", "19. 유효성 확인 · 품질인증 (PHASE-4)", "양쪽", pages(154, 157),
    a_html(154, 157, {157: arrow("➜ [704 p.9] 추가: 5.1.14 (4) 설계 및 개발 유효성 확인 (오른쪽 예시문)")}), b_html([(224, 235)], [("1) 관련문서 및 자료 검토", "add"), ("3) 테스트", "add")]),
    note(["mid"], "유효성 확인 방법 추가, 표현 정리",
         ["704는 품질 인증을 \"인증시험 적합 판정\"으로만 정함",
          "의도한 사용 환경에서 사용 목적을 충족하는지 확인하는 방법을 적음",
          "\"양산용 S/W\", \"사업개발팀에 양산자료로 등록\"은 장비 생산용 표현임 → \"출시용 S/W\" 등으로 고침"],
         ex="(4) 설계 및 개발 유효성 확인은 의도한 사용 환경 또는 이를 모사한 환경에서 S/W가 사용 목적과 사용자 요구사항을 충족하는지 확인하는 것으로, 설계 및 개발관리 절차서(UIT-QP-703)에 따라 수행한다."))

sec("r20", "20. 유지보수 · 변경 (PHASE-5)", "양쪽", pages(158, 175),
    a_html(158, 175, {165: arrow("➜ [704 p.9] 추가: 5.1.15 (2) 6) 회귀시험 (6번 행 예시문)")}), b_html([(237, 240), (61, 64)]),
    note(["mid"], "회귀시험 연결, 보고서 시점 확인",
         ["유지보수 절차(변경요청→영향 분석→계획→구현→검토)와 4유형은 충실함",
          "회귀시험 항목은 6번 행 예시문을 (2)에 추가함",
          "확인 필요: (7) \"제품 출시 후 45일 이내에 소프트웨어 밸리데이션 보고서 작성\" → 출시 전에 검증·유효성 확인을 끝낸다는 점과 보고서 정리 시점의 관계를 명확히 함"]))

sec("r21", "21. 소프트웨어 밸리데이션 보고서", "704만", pages(176, 195),
    a_html(176, 195), "", note(["high"], "작성·승인 주체 통일",
        ["5.1.15 (7)은 \"개발팀장 작성, 품질책임자 승인\", 5.1.16 (1)·(3)은 \"개발팀 담당자 작성, 대표이사 최종 승인\"임 → 하나로 정함",
         "(2) 10) \"소프트웨어 유효성 평가: 시스템 테스트\"는 18번 행 확인 사항과 함께 정리함"]),
    b_empty=True)

sec("r22", "22. 배포", "양쪽", pages(196, 221),
    a_html(196, 221), b_html([(279, 282)], [("소프트웨어 배포는 유효성 확인절차를 완료하고", "add"),
                                            ("배포 기록된 S/W와 설명서의 버전이 일치하", "add")]),
    note(["high"], "승인자 정리, 최종 배포 조건 추가",
         ["배포 승인자가 개발팀장(5.1.2·5.1.6·5.1.14), 품질책임자(5.1.11), 사업개발팀장(5.2.1), PL(4.2)로 곳마다 다름 → 개발 중 내부 배포와 최종(출시) 배포의 승인자를 나눠 정하고, 같은 기록서(UIT-F704-03)의 승인자가 서로 다른 것부터 정리함",
          "최종(출시) 배포는 검증·유효성 확인을 끝낸 뒤 한다는 조건과, 배포한 S/W와 사용설명서 버전이 같은지 확인하는 절차를 추가함",
          "5.2.2 (1) 2) 수신 부서장 재량으로 배포 용도 외 사용을 허용하는 문장은 허용 범위와 승인 조건을 정할지 검토함",
          "5.2.3 (2) \"장비 운용파일은 부트, 디바이스 드라이버, 네트웍 프로토콜...\"은 장비용 설명임 → 소프트웨어 제품에 맞게 고침",
          "띄어쓰기: \"5.2.3배포용\" → \"5.2.3 배포용\""],
         ex="5.2.1 출시용 S/W는 검증 및 유효성 확인을 완료한 후 배포하며, 배포 시 소프트웨어 배포 및 검증기록서(UIT-F704-03)를 작성하여 ○○의 승인을 받는다. 배포 후에는 배포한 S/W와 사용설명서의 버전이 일치하는지 확인하여 기록한다.",
         memo="○○에는 회사에서 정한 승인자를 넣음. 개발 중 내부 배포에는 이 조건을 적용하지 않음"))

sec("r23", "23. 버전 관리", "양쪽", pages(212, 232),
    a_html(212, 212) + a_html(222, 232),
    b_html([(243, 277)], [("S/W명 – 버전번호(1자리)  – 개정번호(2자리)  – 패치번호(1자리)", "mod"),
                          ("8.2 소프트웨어 버전 업그레이드 정책", "add"), ("1) 패치번호 업그레이드", "add"),
                          ("2) 개정번호 업그레이드", "add"), ("3) 버전번호 업그레이드", "add")]),
    note(["high"], "버전 체계 수정, 올리는 기준 추가",
         ["\"ABC00000_202000000_0x1000 Ver 1.0.0\"은 칩 모델명·생성일 기반이라 소프트웨어 제품과 맞지 않음",
          "예시 \"202000000\"(9자리)와 설명 \"20200000\"(8자리)이 다르고, \"0x1000\"을 소문자 알파벳이라고 설명함",
          "버전 숫자를 언제 올리는지 기준이 없음 → 참고본 8.2처럼 정함",
          "5.3.4 \"고객이 원하는 경우는 그에 따른다\"는 범위가 불분명함 → 삭제하거나 대상을 적음"],
         ex="5.3.1 S/W 버전은 \"주버전.부버전.패치\"(예: 1.0.0) 형식으로 표기하며, 다음 기준에 따라 올린다.<br>1) 주버전: 사용 목적, 주요 기능 또는 사용 방법이 바뀌어 사용설명서 개정이나 사용자 재교육이 필요한 경우에 올린다.<br>2) 부버전: 사용자 기능이 일부 바뀌지만 재교육이 필요 없는 경우에 올린다.<br>3) 패치: 기능 변경 없이 오류 수정·성능 개선만 하는 경우에 올린다.",
         memo="이전 엑셀 자료의 UDI 바코드는 (10)1.0(두 자리), 의료기기통합정보 버전은 1.1.X(패치 자리를 X로 둔 것으로 보임)라 서로 다름 → 바코드와 통합정보에 몇 자리까지 쓸지 함께 정함 [확인 필요]"))

sec("r24", "24. 백업 · 프로세스 모니터링 · 매뉴얼", "704만", pages(233, 242),
    a_html(233, 242), "", note(["ok", "na"], "유지, 백업 매체만 정리 (선택)",
        ["참고본에 없는 704의 좋은 항목임",
         "\"CD 및 서버\" → 실제 쓰는 저장 매체(서버, 외부 저장소 등)로 바꿀 수 있음"]),
    b_empty=True)

sec("r25", "25. 관련문서", "양쪽", pages(243, 247),
    a_html(243, 247, {247: arrow("➜ [704 p.14] 추가: 6.5~6.9 관련 규격·절차서 (오른쪽 예시문)")}), b_html([(284, 287)], [("· IEC 62304 Software validation", "add")]),
    note(["mid"], "관련 규격·절차서 추가",
         ["소프트웨어 생명주기 규격과 본문에서 참조하는 절차서가 빠짐",
          "참고본의 \"IEC 62304 Software validation\"은 정확한 규격 이름이 아님"],
         ex="6.5 IEC 62304 의료기기 소프트웨어 — 소프트웨어 생명주기 프로세스<br>6.6 ISO 14971:2019 의료기기 — 위험관리의 의료기기 적용<br>6.7 설계 및 개발관리 절차서(UIT-QP-703)<br>6.8 위험분석관리 절차서(UIT-QP-705)<br>6.9 사용적합성 절차서(UIT-QP-706)",
         memo="[확인 필요: 적용하는 IEC 62304의 판·개정사항(예: 2006+AMD1:2015)]"))

sec("r26", "26. 양식 및 기록", "양쪽", pages(248, 249),
    a_html(248, 249), b_html([(303, 305)]),
    note(["mid"], "양식 목록 보완",
         ["본문에 나오지만 목록에 없는 문서: 밸리데이션 계획서(UIT-SVP-AAA), 밸리데이션 보고서(UIT-SVR-AAA), S/W 문제점 목록, 개발 회의록, 동작설명서",
          "번호 표기가 다름: 본문 \"UIT-SRS-AAA\" / 목록 \"UIT-SRS-MS01\" → 한 가지로 맞춤",
          "참고본처럼 시험계획서·버전관리대장 등을 따로 둘지는 선택임"]))

# ===================== page =====================
css = re.search(r"<style>(.*?)</style>", open(css_src, encoding="utf-8").read(), re.S).group(1)
nav = "".join(f'<a href="#{sid}">{title}</a>' for sid, title, _ in rows)
legend = ('<p class="legend"><span class="pg706" style="margin:0">p.N</span> 704 쪽(LibreOffice 변환 기준, 14쪽) &nbsp;'
          '<span class="arrow-add" style="display:inline-block;margin:0">➜ 704 추가 위치</span> &nbsp;<span class="mod-mark" style="display:inline-block;margin:0"><span class="tag high">수정·추가</span>/<span class="tag mid">수정</span> 704 수정 위치</span> &nbsp;<b>참고본 표시</b> '
          '(수정 항목의 비교 의견 칸에는 <b style="color:#b42318">예시문</b> 포함): <span class="mk-mod">빨강</span> = 704의 기존 내용을 이 문구 방향으로 수정 &nbsp; '
          '<span class="mk-add">파랑</span> = 704에 없어서 이 내용을 추가 &nbsp;|&nbsp; <span class="tag high">수정·추가</span> 반드시 반영 &nbsp; '
          '<span class="tag mid">수정</span> 반영 권장 &nbsp; <span class="tag ok">유지</span> 현행 유지 &nbsp; <span class="tag na">선택</span> 필요 시 반영 · '
          '704 원문은 docx에서, 참고본은 hwp에서 추출했어요. 참고본의 줄바꿈은 원문 그대로이고, 머리글은 표지 행에 넣었어요. 참고본의 &lt;그림&gt;은 hwp에서 그림을 뽑지 못한 자리예요.</p>')
page = f"""<!doctype html>
<html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>UIT-QP-704 ↔ 참고본 전체 문서 대조</title>
<style>{css}
.mod-mark{{color:#b42318;background:#fde8e4;border:1px dashed #b42318;border-radius:5px;padding:4px 9px;margin:6px 0;font-size:13px;font-weight:bold}}
.mod-mark .tag{{margin:0 4px 0 0}}</style>
</head>
<body><div class="wrap">
<h1>소프트웨어 관리 절차서 전체 문서 대조</h1>
<p class="sub">왼쪽: UIT-QP-704 소프트웨어 관리 (Rev.1 개정 중, docx · 14쪽) · 가운데: 참고본 소프트웨어 개발관리 절차서 (hwp, 회사명 XXXX 견본) · 오른쪽: 비교 의견 (704 기준)</p>
<nav>{nav}</nav>
{legend}
<table class="main">
<colgroup><col class="c1"><col class="c2"><col class="c3"></colgroup>
<thead><tr><th>UIT-QP-704 (원문)</th><th>참고본 (원문)</th><th>비교 의견</th></tr></thead>
<tbody>
{''.join(r for _, _, r in rows)}
</tbody></table>
</div></body></html>
"""
open(out, "w", encoding="utf-8").write(page)
print("sections", len(rows))
