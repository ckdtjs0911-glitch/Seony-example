const pptxgen = require("pptxgenjs");
const path = require("path");
const { applyTheme } = require("/root/.claude/skills/synced/c4b55892-d1d5-4503-b36e-45945c611b9d_d15f8a99-671c-47f4-a518-e00ca4cdd941/pptx/scripts/apply_theme.js");

const OUT = process.argv[2] || "deck.pptx";
const DRAFT = process.argv[3] || path.join(__dirname, "draft.md");
// speaker notes come from the manuscript: the paragraph after each "**발표자 노트**"
const NOTES = require("fs").readFileSync(DRAFT, "utf8").split("**발표자 노트**").slice(1).map((b) => b.trim().split(/\n\s*\n|\n---/)[0].trim());
if (NOTES.length !== 5) throw new Error("expected 5 speaker notes in " + DRAFT);
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
    shape: pres.ShapeType.roundRect, rectRadius: 0.12, x: 0.5, y: 1.3, w: 1.1, h: 1.15,
    fill: { color: GREEN }, line: { color: GREEN }, color: "FFFFFF", fontSize: 16, bold: true,
    align: "center", valign: "middle", isTextBox: true, objectName: "Purpose label",
  });
  slide.addText(text, {
    shape: pres.ShapeType.roundRect, rectRadius: 0.12, x: 1.75, y: 1.3, w: 11.08, h: 1.15,
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
  s.addText("Security Risk Management — 안전(safety)과 보안(security)의 통합 평가", {
    x: 1.2, y: 4.3, w: 9, h: 0.6, fontSize: 20, color: SLATE, margin: 0, isTextBox: true,
  });
  s.addNotes(NOTES[0]);
}

// ---------- Slide 2: framework ----------
{
  const s = pres.addSlide({ masterName: "Content", sectionTitle: SEC });
  tag(s, "규격 프레임");
  purpose(s, "보안 위험에는 보안 특화 분석 방법을 쓰되, 하나의 위험관리 체계 안에서 안전 위험관리와 양방향으로 연계한다. 보안 위험이 안전이나 유효성에 영향을 주면 안전 위험평가에 포함한다.");

  const laneY = 2.7, stepY0 = 3.45, stepH = 0.58, gap = 0.2;
  const lanes = [
    { x: 0.5, head: "보안 위험관리\nAAMI TIR57:2016/(R)2023", steps: ["자산(asset) 식별", "위협(threat)·취약점(vulnerability) 분석", "보안 위험평가", "보안 통제(security control)"] },
    { x: 8.03, head: "안전 위험관리\nISO 14971:2019", steps: ["위험원(hazard) 식별", "위해상황(hazardous situation) 분석", "위험평가", "위험 통제(risk control)"] },
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
  box(s, "MDCG 2019-16 Rev.1\n§3.2 · 부록 IV", { x: 5.5, y: laneY, w: 2.33, h: 0.62, fill: { color: GREEN }, line: { color: GREEN }, color: "FFFFFF", bold: true, fontSize: 13, objectName: "Link header" });
  const yA = stepY0 + 2 * (stepH + gap) + stepH / 2; // security risk eval -> safety risk eval
  arrow(s, 4.9, yA, 3.53, 0, { color: GOLD });
  s.addText("안전·유효성 영향이 있으면\n안전 위험평가에 포함", { x: 5.4, y: yA - 0.72, w: 2.53, h: 0.62, fontSize: 12, color: TXT, align: "center", valign: "bottom", margin: 0, isTextBox: true });
  const yB = stepY0 + 3 * (stepH + gap) + stepH / 2; // safety control -> security
  arrow(s, 4.9, yB, 3.53, 0, { color: GOLD, flipH: true });
  s.addText("안전 통제의 보안 영향은\n보안 위험분석에 포함", { x: 5.4, y: yB - 0.6, w: 2.53, h: 0.52, fontSize: 12, color: TXT, align: "center", valign: "bottom", margin: 0, isTextBox: true });

  s.addText("보조 참조: ISO/TR 24971:2020 부록 F(보안 관련 위험관리 지침) · EU MDR 부속서 I 17.2항(정보보안을 포함한 소프트웨어 수명주기 개발), 17.4항(하드웨어·IT 네트워크·IT 보안 최소 요구사항), 18.8항(능동기기의 무단 접근 방지)", {
    x: 0.5, y: 6.55, w: 11.6, h: 0.55, fontSize: 11, color: GRAY, margin: 0, valign: "top", isTextBox: true,
  });
  s.addNotes(NOTES[1]);
}

// ---------- Slide 3: integrated matrix ----------
{
  const s = pres.addSlide({ masterName: "Content", sectionTitle: SEC });
  tag(s, "통합 평가 매트릭스");
  purpose(s, "보안 시나리오를 공격 가능성(exploitability)과 CIA 영향으로 먼저 평가한다. 안전·유효성에 영향을 주는 항목은 위해 경로를 분석해 공격 가능성과 위해 심각도(severity)의 조합으로 다시 판정한다.");

  // flow (left)
  box(s, [{ text: "1단계 · 보안 평가", options: { bold: true, breakLine: true } }, { text: "공격 가능성과 기밀성·무결성·가용성(CIA) 영향의 조합" }],
    { x: 0.5, y: 2.75, w: 3.3, h: 0.95, objectName: "Step 1" });
  arrow(s, 2.15, 3.7, 0, 0.3);
  s.addText("안전 또는 유효성에\n영향이 있는가?", { shape: pres.ShapeType.diamond, x: 0.75, y: 4.0, w: 2.8, h: 1.2, fill: { color: LIGHT }, line: { color: GREEN, width: 1.5 }, fontSize: 13, bold: true, color: TXT, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "Decision" });
  arrow(s, 3.55, 4.6, 0.6, 0);
  s.addText("아니오", { x: 3.55, y: 4.22, w: 0.65, h: 0.3, fontSize: 11, color: GRAY, align: "center", margin: 0, isTextBox: true });
  box(s, "보안 위험으로 관리함\n(위해 연결 여부는\n개별 판단함)", { x: 4.15, y: 4.13, w: 1.75, h: 0.95, fontSize: 12, line: { color: GRAY, width: 1 }, objectName: "No branch" });
  arrow(s, 2.15, 5.2, 0, 0.35);
  s.addText("예", { x: 2.25, y: 5.2, w: 0.4, h: 0.3, fontSize: 11, color: GRAY, margin: 0, isTextBox: true });
  box(s, [{ text: "2단계 · 안전 평가", options: { bold: true, breakLine: true } }, { text: "위해 경로 분석 후 공격 가능성·심각도 조합으로 판정" }],
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
  s.addText([
    { text: "제조사가 정하는 예시 방법이며, 등급·심각도 정의·판정 기준은 위험관리 계획서(risk management plan)에 미리 정의함", options: { breakLine: true } },
    { text: "\"허용\" 칸도 가능한 한 위험을 줄일 의무와 잔여 위험 검토가 적용됨" },
  ], {
    x: 6.4, y: 6.3, w: 6.43, h: 0.6, fontSize: 11, color: GRAY, margin: 0, valign: "top", isTextBox: true,
  });
  s.addNotes(NOTES[2]);
}

// ---------- Slide 4: exploitability ----------
{
  const s = pres.addSlide({ masterName: "Content", sectionTitle: SEC });
  tag(s, "공격 가능성 산정");
  purpose(s, "의도적 공격은 과거 데이터로 발생 확률을 추정하기 어렵다. 따라서 공격에 필요한 자원을 점수화하는 공인 방법으로 공격 가능성(exploitability)을 산정하고, 산정 근거를 계획서에 고정한다.");

  const H = (t) => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: SLATE }, align: "center", valign: "middle" } });
  const F = (t) => ({ text: t, options: { bold: true, fill: { color: "F2F2F2" }, valign: "middle" } });
  const V = (t) => ({ text: t, options: { valign: "middle" } });
  s.addTable([
    [H("공격 잠재력 요소"), H("낮은 점수(쉬움)"), H("높은 점수(어려움)")],
    [F("소요 시간(elapsed time)"), V("1일 이내"), V("수개월 이상")],
    [F("전문 기술 수준(specialist expertise)"), V("일반인"), V("여러 분야 전문가")],
    [F("설계·운용 지식(knowledge of the TOE)"), V("공개 정보"), V("엄격히 통제된 정보")],
    [F("기회의 창(window of opportunity)"), V("제약 없음"), V("매우 제한적")],
    [F("장비(equipment)"), V("일반 장비"), V("맞춤 제작 장비")],
  ], { x: 0.5, y: 2.75, w: 7.6, colW: [3.6, 2.0, 2.0], rowH: 0.56, fontSize: 14, fontFace: FONT, color: TXT, border: { type: "solid", pt: 1, color: "D9D9D9" }, objectName: "Attack potential table" });
  s.addText("근거: ISO/IEC 18045·CEM 공격 잠재력(attack potential) 요소. 적용 판본·점수표·등급 변환 기준은 계획서에 명시함", { x: 0.5, y: 6.25, w: 7.6, h: 0.55, valign: "top", fontSize: 11, color: GRAY, margin: 0, isTextBox: true });

  // right: score -> grade
  const rx = 8.6, rw = 4.23;
  s.addText("점수 합계 → 등급 변환", { x: rx, y: 2.75, w: rw, h: 0.45, fontSize: 16, bold: true, color: SLATE, margin: 0, isTextBox: true });
  [["낮은 합계", "공격 가능성 높음", BAD], ["중간 합계", "공격 가능성 중간", MID], ["높은 합계", "공격 가능성 낮음", OK]].forEach(([a, b, col], i) => {
    const y = 3.3 + i * 0.68;
    s.addText(a, { x: rx, y, w: 1.4, h: 0.52, fontSize: 13, color: TXT, align: "left", valign: "middle", margin: 0, isTextBox: true });
    arrow(s, rx + 1.35, y + 0.26, 0.45, 0);
    s.addText(b, { shape: pres.ShapeType.roundRect, rectRadius: 0.2, x: rx + 1.9, y, w: 2.33, h: 0.52, fill: { color: col }, line: { color: col }, fontSize: 13, bold: true, color: TXT, align: "center", valign: "middle", margin: 0, isTextBox: true });
  });
  box(s, [{ text: "대안: CVSS v3.1", options: { bold: true, breakLine: true } }, { text: "AV·AC·PR·UI 지표를 보조 입력으로 활용함", options: { breakLine: true } }, { text: "환자 위해 심각도는 별도로 평가함" }],
    { x: rx, y: 5.4, w: rw, h: 1.2, fontSize: 13, align: "left", valign: "middle", margin: [4, 10, 4, 10], line: { color: GRAY, width: 1 }, objectName: "CVSS note" });
  s.addNotes(NOTES[3]);
}

// ---------- Slide 5: acceptability argument ----------
{
  const s = pres.addSlide({ masterName: "Content", sectionTitle: SEC });
  tag(s, "위험 허용 논리");
  purpose(s, "확률 대신 사전 기준, 최악의 임상 결과 가정, 통제 효과의 객관적 증거, 시판 후 감시를 하나의 논리로 묶어 잔여 위험(residual risk)이 허용 가능함을 보인다.");

  const cards = [
    ["기준 사전 정의", "공격 가능성 등급, 심각도 정의, 매트릭스, 허용 기준을 평가 전에 계획서에 정해 둠"],
    ["최악 결과 가정", "공격이 성공한다고 보고, 합리적으로 예견 가능한 최악의 임상 결과와 가정을 기록함"],
    ["통제 효과 검증", "요구사항 시험·설계 검토·취약점 분석·침투 시험(penetration testing)으로 확인하고 범위·한계를 명시함"],
    ["시판 후 감시", "SBOM(소프트웨어 자재 명세서)을 바탕으로 취약점을 모니터링하고 패치 계획에 따라 재평가함"],
  ];
  const w = 2.85, g = 0.31, y = 2.75, h = 2.7;
  cards.forEach(([t, d], i) => {
    const x = 0.5 + i * (w + g);
    s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.12, fill: { color: "FFFFFF" }, line: { color: "D9D9D9", width: 1 }, shadow: { type: "outer", color: "000000", opacity: 0.12, blur: 4, offset: 2, angle: 90 }, objectName: `Step card ${i + 1}` });
    s.addText(String(i + 1), { shape: pres.ShapeType.ellipse, x: x + 0.2, y: y + 0.2, w: 0.55, h: 0.55, fill: { color: GREEN }, line: { color: GREEN }, color: "FFFFFF", fontSize: 16, bold: true, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText(t, { x: x + 0.85, y: y + 0.2, w: w - 1.0, h: 0.55, fontSize: 16, bold: true, color: SLATE, valign: "middle", margin: 0, isTextBox: true });
    s.addText(d, { x: x + 0.2, y: y + 0.9, w: w - 0.4, h: h - 1.0, fontSize: 14, color: TXT, valign: "top", margin: 0, isTextBox: true });
    if (i < 3) arrow(s, x + w + 0.03, y + h / 2, g - 0.06, 0, { color: GOLD });
  });
  s.addText([
    { text: "결론  ", options: { bold: true, color: GOLD } },
    { text: "기준을 넘으면 추가 통제를 적용한다. 추가 통제가 실행 가능하지 않은 개별 위험은 이익-위험 분석(benefit-risk analysis, ISO 14971:2019 7.4항)으로 판단하고, 이익을 입증하지 못하면 허용 불가로 남긴다. 전체 잔여 위험은 8항에 따라 평가한다." },
  ], { shape: pres.ShapeType.roundRect, rectRadius: 0.12, x: 0.5, y: 5.65, w: 12.33, h: 1.05, fill: { color: "FFFFFF" }, line: { color: SLATE, width: 1.5 }, fontSize: 14, color: TXT, valign: "middle", margin: [4, 14, 4, 14], isTextBox: true, objectName: "Conclusion" });
  s.addNotes(NOTES[4]);
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
