const pptxgen = require("pptxgenjs");
const path = require("path");
const { applyTheme } = require("/root/.claude/skills/synced/c4b55892-d1d5-4503-b36e-45945c611b9d_d15f8a99-671c-47f4-a518-e00ca4cdd941/pptx/scripts/apply_theme.js");

const OUT = process.argv[2] || "deck.pptx";
const FONT = "Malgun Gothic";
const THEME = {
  name: "SaMD Edu",
  headFontFace: FONT,
  bodyFontFace: FONT,
  colors: {
    dk1: "262626", lt1: "FFFFFF", dk2: "44546A", lt2: "E5F4CE",
    accent1: "77AE26", accent2: "B08600", accent3: "44546A", accent4: "C00000",
    accent5: "FFE699", accent6: "F4C7C3", hlink: "44546A", folHlink: "7F7F7F",
  },
};
const GOLD = "B08600", SLATE = "44546A", LIGHT = "E5F4CE", GREEN = "77AE26", TXT = "262626", GRAY = "7F7F7F";
const OK = "E5F4CE", MID = "FFE699", BAD = "F4C7C3";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
pres.title = "사이버보안 위험관리 (Security Risk Management)";

pres.defineSlideMaster({
  title: "Section Cover",
  background: { color: "FFFFFF" },
});
pres.defineSlideMaster({
  title: "Content",
  background: { color: "FFFFFF" },
  slideNumber: { x: 12.4, y: 7.0, w: 0.5, h: 0.3, fontSize: 10, color: GRAY, fontFace: FONT },
});

pres.addSection({ title: "01 사이버보안 위험관리" });
const SEC = "01 사이버보안 위험관리";

// helpers
function tag(slide, text) {
  slide.addText(text, {
    shape: pres.ShapeType.roundRect, rectRadius: 0.28, x: 0.5, y: 0.4, w: 4.2, h: 0.6,
    fill: { color: SLATE }, line: { color: SLATE }, color: "FFFFFF", fontSize: 20, bold: true,
    align: "center", valign: "middle", isTextBox: true, objectName: "Title tag",
  });
}
function purpose(slide, text) {
  slide.addText("목적", {
    shape: pres.ShapeType.roundRect, rectRadius: 0.12, x: 0.5, y: 1.3, w: 1.1, h: 1.0,
    fill: { color: GREEN }, line: { color: GREEN }, color: "FFFFFF", fontSize: 16, bold: true,
    align: "center", valign: "middle", isTextBox: true, objectName: "Purpose label",
  });
  slide.addText(text, {
    shape: pres.ShapeType.roundRect, rectRadius: 0.12, x: 1.75, y: 1.3, w: 11.08, h: 1.0,
    fill: { color: LIGHT }, line: { color: LIGHT }, color: TXT, fontSize: 16,
    align: "left", valign: "middle", margin: [4, 14, 4, 14], isTextBox: true, objectName: "Purpose box",
  });
}
function box(slide, text, o) {
  slide.addText(text, Object.assign({
    shape: pres.ShapeType.roundRect, rectRadius: 0.1, fill: { color: "FFFFFF" },
    line: { color: SLATE, width: 1 }, color: TXT, fontSize: 14, align: "center", valign: "middle",
    margin: [3, 8, 3, 8], isTextBox: true,
  }, o));
}
function arrow(slide, x, y, w, h, opts = {}) {
  slide.addShape(pres.ShapeType.line, Object.assign({
    x, y, w, h, line: { color: opts.color || SLATE, width: 2, endArrowType: "triangle" },
  }, opts.flipH ? { flipH: true } : {}, opts.flipV ? { flipV: true } : {}));
}

// ---------- Slide 1: section cover ----------
{
  const s = pres.addSlide({ masterName: "Section Cover", sectionTitle: SEC });
  s.addShape(pres.ShapeType.rtTriangle, { x: 9.6, y: 3.9, w: 3.73, h: 3.6, fill: { color: "D9D9D9" }, line: { color: "D9D9D9" }, flipH: true, objectName: "Deco triangle" });
  s.addShape(pres.ShapeType.rtTriangle, { x: 11.0, y: 5.3, w: 2.33, h: 2.2, fill: { color: "BFBFBF" }, line: { color: "BFBFBF" }, flipH: true, objectName: "Deco triangle" });
  s.addShape(pres.ShapeType.rtTriangle, { x: 0, y: 0, w: 2.2, h: 2.0, fill: { color: "EDEDED" }, line: { color: "EDEDED" }, flipV: true, objectName: "Deco triangle" });
  s.addText("01", { x: 1.2, y: 1.7, w: 3, h: 1.2, fontSize: 72, bold: true, color: GOLD, margin: 0, isTextBox: true });
  s.addText("사이버보안 위험관리", { x: 1.2, y: 2.95, w: 10, h: 1.0, fontSize: 50, bold: true, color: TXT, margin: 0, isTextBox: true });
  s.addShape(pres.ShapeType.line, { x: 1.2, y: 4.1, w: 6.2, h: 0, line: { color: GOLD, width: 3 } });
  s.addText("Security Risk Management — Safety와 Security의 통합 평가", {
    x: 1.2, y: 4.3, w: 9, h: 0.6, fontSize: 20, color: SLATE, margin: 0, isTextBox: true,
  });
  s.addNotes("이번 섹션은 보안 위협이 환자 안전 위해로 이어지는 경로를 위험관리 체계 안에서 어떻게 다룰지 정리한다. 핵심 과제는 두 가지다. 첫째, 안전 위험과 보안 위험을 함께 평가하는 매트릭스를 설계하는 것이다. 둘째, 의도적 공격의 발생 확률을 산정하기 어려운 상황에서 인증기관(Notified Body, NB)이 수용할 수 있는 위험 허용 논리를 세우는 것이다.");
}

// ---------- Slide 2: framework ----------
{
  const s = pres.addSlide({ masterName: "Content", sectionTitle: SEC });
  tag(s, "규격 프레임");
  purpose(s, "안전 위험관리(safety risk management)와 보안 위험관리(security risk management)를 별도 프로세스로 운영하되, 보안 위험이 위해(harm)로 이어질 수 있으면 안전 위험관리로 넘겨 함께 평가한다.");

  const laneY = 2.7, stepY0 = 3.45, stepH = 0.58, gap = 0.2;
  const lanes = [
    { x: 0.5, head: "보안 위험관리\nAAMI TIR57:2016/(R)2019", steps: ["자산(asset) 식별", "위협(threat)·취약점(vulnerability) 분석", "보안 위험 평가", "보안 통제(security control)"] },
    { x: 8.03, head: "안전 위험관리\nISO 14971:2019", steps: ["위험원(hazard) 식별", "위해 상황(hazardous situation) 분석", "위험 평가", "위험 통제(risk control)"] },
  ];
  for (const L of lanes) {
    box(s, L.head, { x: L.x, y: laneY, w: 4.8, h: 0.62, fill: { color: SLATE }, line: { color: SLATE }, color: "FFFFFF", bold: true, fontSize: 14, objectName: "Lane header" });
    L.steps.forEach((t, i) => {
      const y = stepY0 + i * (stepH + gap);
      box(s, t, { x: L.x + 0.4, y, w: 4.0, h: stepH, objectName: "Lane step" });
      if (i < 3) arrow(s, L.x + 2.4, y + stepH, 0, gap);
    });
  }
  // middle connectors
  box(s, "MDCG 2019-16 Rev.1\n부록 I · 상호 연계", { x: 5.5, y: laneY, w: 2.33, h: 0.62, fill: { color: GREEN }, line: { color: GREEN }, color: "FFFFFF", bold: true, fontSize: 13, objectName: "Link header" });
  const yA = stepY0 + 2 * (stepH + gap) + stepH / 2; // security risk eval -> safety risk eval
  arrow(s, 4.9, yA, 3.53, 0, { color: GOLD });
  s.addText("안전에 영향을 주는\n보안 위험 전달", { x: 5.4, y: yA - 0.72, w: 2.53, h: 0.62, fontSize: 12, color: TXT, align: "center", valign: "bottom", margin: 0, isTextBox: true });
  const yB = stepY0 + 3 * (stepH + gap) + stepH / 2; // safety control -> security
  arrow(s, 4.9, yB, 3.53, 0, { color: GOLD, flipH: true });
  s.addText("위험 통제의 보안 영향 전달", { x: 5.4, y: yB + 0.08, w: 2.53, h: 0.5, fontSize: 12, color: TXT, align: "center", valign: "top", margin: 0, isTextBox: true });

  s.addText("보조 참조: ISO/TR 24971:2020 부록 F(보안 관련 위험관리 지침), EU MDR 부속서 I 17.2·17.4·18.8항(정보보안·무단 접근 방지 요구사항)", {
    x: 0.5, y: 6.75, w: 11.6, h: 0.35, fontSize: 11, color: GRAY, margin: 0, isTextBox: true,
  });
  s.addNotes("ISO 14971 자체는 보안 위험 평가 방법을 자세히 다루지 않는다. 그래서 AAMI TIR57이 ISO 14971의 구조를 그대로 가져와 보안 위험관리에 적용하는 방법을 제시한다(후속 규격: ANSI/AAMI SW96:2023). MDCG 2019-16 부록 I은 두 프로세스가 서로 결과를 주고받아야 한다는 관계를 보여준다. 유럽 심사에서 TIR57은 정합 규격(harmonised standard)이 아니지만, 최신 기술 수준(state of the art)을 보여주는 근거로 흔히 인용된다.");
}

// ---------- Slide 3: integrated matrix ----------
{
  const s = pres.addSlide({ masterName: "Content", sectionTitle: SEC });
  tag(s, "통합 평가 매트릭스");
  purpose(s, "보안 위험을 먼저 공격 가능성(exploitability)과 영향(impact)으로 평가하고, 환자 안전에 영향을 주는 항목만 안전 매트릭스로 넘겨 위해의 심각도(severity)로 다시 평가한다.");

  // flow (left)
  box(s, [{ text: "1단계 · 보안 평가", options: { bold: true, breakLine: true } }, { text: "공격 가능성 × 기밀성·무결성·가용성(CIA) 영향" }],
    { x: 0.5, y: 2.75, w: 3.3, h: 0.95, objectName: "Step 1" });
  arrow(s, 2.15, 3.7, 0, 0.3);
  s.addText("환자 안전에\n영향이 있는가?", { shape: pres.ShapeType.diamond, x: 0.75, y: 4.0, w: 2.8, h: 1.2, fill: { color: LIGHT }, line: { color: GREEN, width: 1.5 }, fontSize: 13, bold: true, color: TXT, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "Decision" });
  arrow(s, 3.55, 4.6, 0.6, 0);
  s.addText("아니오", { x: 3.55, y: 4.22, w: 0.65, h: 0.3, fontSize: 11, color: GRAY, align: "center", margin: 0, isTextBox: true });
  box(s, "보안 위험으로만 관리함\n(데이터 보호 등)", { x: 4.15, y: 4.2, w: 1.75, h: 0.8, fontSize: 12, line: { color: GRAY, width: 1 }, objectName: "No branch" });
  arrow(s, 2.15, 5.2, 0, 0.35);
  s.addText("예", { x: 2.25, y: 5.2, w: 0.4, h: 0.3, fontSize: 11, color: GRAY, margin: 0, isTextBox: true });
  box(s, [{ text: "2단계 · 안전 평가", options: { bold: true, breakLine: true } }, { text: "공격 가능성 × 위해 심각도 → 허용 여부 판정" }],
    { x: 0.5, y: 5.55, w: 3.3, h: 0.95, fill: { color: SLATE }, line: { color: SLATE }, color: "FFFFFF", objectName: "Step 2" });

  // matrix (right)
  const hdr = (t) => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: SLATE }, align: "center", valign: "middle" } });
  const c = (t) => ({ text: t, options: { fill: { color: t === "허용" ? OK : t === "허용 불가" ? BAD : MID }, align: "center", valign: "middle" } });
  const rowh = (t) => ({ text: t, options: { bold: true, fill: { color: "F2F2F2" }, align: "left", valign: "middle" } });
  const rows = [
    [hdr("심각도 \\ 공격 가능성"), hdr("낮음"), hdr("중간"), hdr("높음")],
    [rowh("치명(Catastrophic)"), c("추가 통제 검토"), c("허용 불가"), c("허용 불가")],
    [rowh("중대(Critical)"), c("추가 통제 검토"), c("추가 통제 검토"), c("허용 불가")],
    [rowh("심각(Serious)"), c("허용"), c("추가 통제 검토"), c("허용 불가")],
    [rowh("경미(Minor)"), c("허용"), c("허용"), c("추가 통제 검토")],
    [rowh("무시 가능(Negligible)"), c("허용"), c("허용"), c("허용")],
  ];
  s.addTable(rows, { x: 6.4, y: 2.75, w: 6.43, colW: [2.23, 1.4, 1.4, 1.4], rowH: 0.58, fontSize: 13, fontFace: FONT, color: TXT, border: { type: "solid", pt: 1, color: "FFFFFF" }, objectName: "Risk matrix" });
  s.addText("예시. 실제 등급과 판정 기준은 위험관리 계획서(risk management plan)에 미리 정의함", {
    x: 6.4, y: 6.4, w: 6.43, h: 0.35, fontSize: 11, color: GRAY, margin: 0, isTextBox: true,
  });
  s.addNotes("안전 매트릭스의 확률 축을 공격 가능성 축으로 바꾸는 것이 핵심이다. 우발적 고장은 확률로 평가하지만, 의도적 공격은 확률을 신뢰성 있게 산정하기 어렵다. 그래서 같은 매트릭스 틀을 유지하면서 축만 정성적 공격 가능성으로 바꾼다. 축의 등급 수와 판정 칸은 위험관리 계획서에서 미리 정하고, 평가 후에 바꾸지 않는다.");
}

// ---------- Slide 4: exploitability ----------
{
  const s = pres.addSlide({ masterName: "Content", sectionTitle: SEC });
  tag(s, "공격 가능성 산정");
  purpose(s, "의도적 공격은 과거 데이터로 발생 확률을 추정하기 어렵다. 따라서 공격에 필요한 조건을 점수화한 공격 가능성(exploitability)으로 확률 축을 대신한다.");

  const H = (t) => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: SLATE }, align: "center", valign: "middle" } });
  const F = (t) => ({ text: t, options: { bold: true, fill: { color: "F2F2F2" }, valign: "middle" } });
  const V = (t) => ({ text: t, options: { valign: "middle" } });
  s.addTable([
    [H("공격 잠재력 요소"), H("낮은 점수(쉬움)"), H("높은 점수(어려움)")],
    [F("소요 시간(elapsed time)"), V("1일 이내"), V("수개월 이상")],
    [F("전문성(expertise)"), V("일반인"), V("여러 분야 전문가")],
    [F("제품 정보(knowledge of TOE)"), V("공개 정보"), V("기밀 정보")],
    [F("접근 기회(window of opportunity)"), V("원격·무제한"), V("물리적 접근·제한적")],
    [F("장비(equipment)"), V("일반 장비"), V("맞춤 제작 장비")],
  ], { x: 0.5, y: 2.75, w: 7.6, colW: [3.4, 2.1, 2.1], rowH: 0.56, fontSize: 14, fontFace: FONT, color: TXT, border: { type: "solid", pt: 1, color: "D9D9D9" }, objectName: "Attack potential table" });
  s.addText("근거: ISO/IEC 18045 공격 잠재력(attack potential) 산정 요소", { x: 0.5, y: 6.25, w: 7.6, h: 0.35, fontSize: 11, color: GRAY, margin: 0, isTextBox: true });

  // right: score -> grade
  const rx = 8.6, rw = 4.23;
  s.addText("점수 합계 → 등급 변환", { x: rx, y: 2.75, w: rw, h: 0.45, fontSize: 16, bold: true, color: SLATE, margin: 0, isTextBox: true });
  [["낮은 합계", "공격 가능성 높음", BAD], ["중간 합계", "공격 가능성 중간", MID], ["높은 합계", "공격 가능성 낮음", OK]].forEach(([a, b, col], i) => {
    const y = 3.3 + i * 0.68;
    s.addText(a, { x: rx, y, w: 1.4, h: 0.52, fontSize: 13, color: TXT, align: "left", valign: "middle", margin: 0, isTextBox: true });
    arrow(s, rx + 1.35, y + 0.26, 0.45, 0);
    s.addText(b, { shape: pres.ShapeType.roundRect, rectRadius: 0.2, x: rx + 1.9, y, w: 2.33, h: 0.52, fill: { color: col }, line: { color: col }, fontSize: 13, bold: true, color: TXT, align: "center", valign: "middle", margin: 0, isTextBox: true });
  });
  box(s, [{ text: "대안: CVSS", options: { bold: true, breakLine: true } }, { text: "공격 가능성 지표(exploitability metrics)를 쓸 수 있음. 단, 환자 위해 심각도는 별도로 평가함" }],
    { x: rx, y: 5.4, w: rw, h: 1.2, fontSize: 13, align: "left", valign: "middle", margin: [4, 10, 4, 10], line: { color: GRAY, width: 1 }, objectName: "CVSS note" });
  s.addNotes("확률을 억지로 숫자로 만들면 심사에서 근거를 묻는 질문에 답하기 어렵다. 공격 잠재력 요소는 공격자가 실제로 들여야 하는 시간, 지식, 장비를 기준으로 하므로 재현 가능하고 설명하기 쉽다. 점수가 높을수록 공격에 더 많은 자원이 필요하므로 공격 가능성은 낮아진다. CVSS는 취약점의 기술적 심각도 지표이므로 환자 위해 심각도를 대신하지 못한다. 어떤 체계를 쓰든 점수와 등급 변환 기준을 위험관리 계획서에 고정해 두어야 한다.");
}

// ---------- Slide 5: acceptability argument ----------
{
  const s = pres.addSlide({ masterName: "Content", sectionTitle: SEC });
  tag(s, "위험 허용 논리");
  purpose(s, "확률 대신 \"사전 기준 + 최악 가정 + 통제 효과 검증 + 시판 후 감시\"를 하나의 논리로 묶어 잔여 위험(residual risk)이 허용 가능함을 보인다.");

  const cards = [
    ["기준 사전 정의", "위험관리 계획서에 공격 가능성 등급, 매트릭스, 허용 기준을 평가 전에 정해 둠"],
    ["최악 가정", "공격 가능성 평가 전에는 공격이 성공한다고 가정하고 위해 심각도를 평가함"],
    ["통제 효과 검증", "인증·암호화·무결성 검증 등 통제 적용 후 공격 가능성을 재평가하고 침투 시험(penetration testing)으로 확인함"],
    ["시판 후 감시", "취약점 모니터링, SBOM(소프트웨어 자재 명세서), 패치 계획으로 변화를 추적하고 재평가함"],
  ];
  const w = 2.85, g = 0.31, y = 2.75, h = 2.4;
  cards.forEach(([t, d], i) => {
    const x = 0.5 + i * (w + g);
    s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.12, fill: { color: "FFFFFF" }, line: { color: "D9D9D9", width: 1 }, shadow: { type: "outer", color: "000000", opacity: 0.12, blur: 4, offset: 2, angle: 90 }, objectName: `Step card ${i + 1}` });
    s.addText(String(i + 1), { shape: pres.ShapeType.ellipse, x: x + 0.2, y: y + 0.2, w: 0.55, h: 0.55, fill: { color: GREEN }, line: { color: GREEN }, color: "FFFFFF", fontSize: 16, bold: true, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText(t, { x: x + 0.85, y: y + 0.2, w: w - 1.0, h: 0.55, fontSize: 16, bold: true, color: SLATE, valign: "middle", margin: 0, isTextBox: true });
    s.addText(d, { x: x + 0.2, y: y + 0.95, w: w - 0.4, h: h - 1.1, fontSize: 14, color: TXT, valign: "top", margin: 0, isTextBox: true });
    if (i < 3) arrow(s, x + w + 0.03, y + h / 2, g - 0.06, 0, { color: GOLD });
  });
  s.addText([
    { text: "결론  ", options: { bold: true, color: GOLD } },
    { text: "잔여 위험이 허용 기준을 넘으면 추가 통제를 적용한다. 더 줄일 수 없는 개별 위험은 이익-위험 분석(benefit-risk analysis, ISO 14971:2019 7.4항)으로 판단하고, 전체 잔여 위험은 8항에 따라 평가한다." },
  ], { shape: pres.ShapeType.roundRect, rectRadius: 0.12, x: 0.5, y: 5.5, w: 12.33, h: 0.95, fill: { color: "FFFFFF" }, line: { color: SLATE, width: 1.5 }, fontSize: 14, color: TXT, valign: "middle", margin: [4, 14, 4, 14], isTextBox: true, objectName: "Conclusion" });
  s.addNotes("NB가 가장 먼저 확인하는 것은 기준을 평가 결과에 맞춰 바꾸지 않았는가이다. 그래서 기준을 계획서에 미리 고정하는 것이 출발점이다. 다음으로 확률을 낮게 잡아 위험을 줄였다는 인상을 피하기 위해 최악 가정에서 시작한다. 통제의 효과는 침투 시험 같은 객관적 증거로 보이고, 공격 가능성은 시간이 지나면 변하므로 시판 후 감시 계획으로 논리를 닫는다. EU MDR은 위험을 가능한 한 줄일 것(as far as possible)을 요구하므로(EN ISO 14971:2019+A11:2021 부속서 ZA 참조), 경제성만을 이유로 통제를 생략했다는 인상을 주지 않아야 한다.");
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
