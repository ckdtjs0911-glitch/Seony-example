# M2 / UroInsight CheckUp — 전립선 MRI AI 분석 SaMD 규제 근거 정리

> 전립선 MRI 딥러닝 분석 디지털의료기기(SaMD)의 기술문서 성능시험 항목·시험기준·근거문헌을 정리한 학습용 문서.
> 제조사: ㈜유로인사이트 / 제품: M2 (M2 1.0) / 제품코드: B1ABXA1 / 디지털의료기기 제조신고 D 제신 26-100호

---

## 0. 제품 개요

- **사용목적**: 전립선 MRI 영상(T2 강조영상, ADC 지도, 고b값 DWI)을 입력받아, 딥러닝(3차원 합성곱 신경망, 3D CNN)으로
  1) 전립선 세부구조 자동 분할(Segmentation) 및 구역별·전체 부피(cm³)·PSAD 산출
  2) 임상적으로 유의한 전립선암(csPCa) 의심 병변의 위치·범위·부피 산출
  → 영상의학과·비뇨의학과 전문의의 진단 보조 (확진·조직검사 대체 아님)
- **분할 구역**: 말초대(PZ, Peripheral zone), 이행대(TZ, Transition zone), 정낭(SV, Seminal vesicle), 전립선 전체(WG, Whole gland)

---

## 1. 핵심 개념 (지표·용어)

### 1.1 분할 정확도 지표

- **DSC (Dice Similarity Coefficient, 다이스 계수)**
  - 정의: `DSC = 2|P∩G| ÷ (|P|+|G|)` (P=예측 마스크, G=참조표준 마스크)
  - 두 분할 영역이 **얼마나 겹치는가(overlap)**. 0~1, **높을수록 우수**.
- **ASSD (Average Symmetric Surface Distance, 평균 대칭 표면거리)**
  - 예측 경계와 참조표준 경계 간 **양방향 대칭 평균 표면거리(mm)**. **낮을수록 우수**.
  - ASD(평균 표면거리)·MSD·ABD(평균 경계거리, Average Boundary Distance)는 모두 ASSD와 **동일 계열** 지표 (단위 mm).
  - 지표 정의·산출 표준 출처: PROMISE12 챌린지 [Litjens et al., Med Image Anal. 2014].
- **DSC vs ASSD**: DSC는 "겹침(넓이)" 관점, ASSD는 "경계(테두리) 거리" 관점. 보는 각도가 다름.

### 1.2 구역 명칭

- WG = Whole gland (전립선 전체) = 대략 TZ + PZ (+ CG 등)
- TZ = Transition zone (이행대)
- CG = Central gland (중심샘) = 이행대(TZ) + 중심대(central zone). **논문에 따라 TZ 대신 CG로 보고** → 규격의 TZ에 대응.
- PZ = Peripheral zone (말초대) — 분할 난이도가 가장 높아 정확도가 낮게 나오는 경향.
- SV = Seminal vesicle (정낭) — 작고 분할이 어려워 거리지표 편차 큼 → 보통 거리 기준 판정에서 제외.

### 1.3 병변 검출 지표 (csPCa)

- **민감도(Sensitivity)** = TP/(TP+FN) — 실제 암을 암으로 맞히는 비율
- **특이도(Specificity)** = TN/(TN+FP) — 암이 아닌 것을 아니라고 맞히는 비율
- **민감도-특이도 상충**: 전립선 MRI/AI csPCa 검출은 **민감도는 높고(~0.85~0.90) 특이도는 낮은(~0.5~0.7)** 경향 → **특이도 ≥0.81이 달성의 병목**.

### 1.4 PI-RADS

- Prostate Imaging–Reporting and Data System. 전립선 MRI로 csPCa 가능성을 **1~5점**으로 매기는 국제 표준.
- 1(매우 낮음)~5(매우 높음). 보통 **≥3 또는 ≥4를 양성(생검 권고) 기준점**으로 사용.

### 1.5 글리슨 등급군 (Gleason Grade Group, GG 1~5)

- 전립선암 **공격성(악성도)** 등급 (조직검사 기반, ISUP 2014).
- GG1(≤6, 거의 무해) / GG2(3+4) / GG3(4+3) / GG4(8) / GG5(9~10, 매우 공격적).
- **csPCa 정의**: 보통 **GG ≥ 2** 또는 **GG ≥ 3**. (GG1은 능동감시 → 비-csPCa)

### 1.6 라디오믹스(Radiomics)

- MRI 영상에서 **밝기·질감(texture)·모양 등 수백~수천 개 정량적 특징을 자동 추출**해 머신러닝으로 분석하는 기법 ("영상을 숫자 데이터로 변환").
- **딥러닝(CNN)과 차이**: 라디오믹스는 사람이 정의한 수식으로 특징 추출 후 ML, 딥러닝은 특징을 스스로 학습. (M2는 딥러닝 방식)

### 1.7 저널 등급 (근거 자료 등급)

- **SCI / SCIE (Science Citation Index / Expanded)**: Web of Science 등재, Impact Factor 보유. 최상위 근거. (현재 SCI·SCIE 통합 → SCIE = SCI급)
- **ESCI (Emerging Sources Citation Index)**: WoS 하위, IF 없음.
- **Scopus**: WoS와 별개 색인 (CiteScore). SCIE·ESCI보다 낮은 단계로 간주.

---

## 2. 시험항목 2 — 전립선 구역(zone) 분할 및 부피 산출

### 2.1 시험기준 (두 가지 관점이 문서 내 혼재했음 — 반드시 통일 필요)

**(A) DSC 기준** (최종 채택 방향):
- 전립선 전체(WG): **DSC ≥ 0.94**
- 이행대(TZ): **DSC ≥ 0.85**
- 말초대(PZ): **DSC ≥ 0.85**

**(B) ASSD 기준** (초기 검토안, 이후 DSC로 전환):
- WG ≤ 1.3 mm / TZ ≤ 1.6 mm / PZ ≤ 1.3 mm

> ⚠️ 주의: 한 문서 안에 DSC와 ASSD가 섞여 있으면 본문·근거자료가 상충. **하나로 통일**해야 함. (최종: DSC 채택)

### 2.2 DSC 기준 근거 문헌 (SCIE)

| No. | 문헌 | 저널(등재)·연도 | 대표 DSC | 근거 대상 |
|---|---|---|---|---|
| [1] | Zabihollahy F, et al. | Medical Physics (SCIE)·2019 | WG 0.9533 / CG 0.9375 / PZ 0.8678 (T2W) | **전 구역** (1순위) |
| [2] | Bardis MD, et al. | Radiol Imaging Cancer (RSNA)·2021 | WG 0.940 / TZ 0.910 / PZ 0.774 | 전체·이행대 |
| [3] | Xu L, et al. | Insights into Imaging (SCIE)·2023 | CG 0.909 / PZ 0.844 | 이행대(CG) + 다기관 임상검증 |
| [4] | Rundo L, et al. (USE-Net) | Neurocomputing (SCIE)·2019 | CG 0.937 / PZ 0.919 (최고치) | 말초대(PZ) 보강 |

**기준별 충족 매핑**:
- WG ≥0.94 → Zabihollahy 0.9533 · Bardis 0.940
- TZ ≥0.85 → Bardis 0.910 · Zabihollahy(CG) 0.9375 · Xu(CG) 0.909
- PZ ≥0.85 → Zabihollahy 0.8678 · Rundo 0.919

**핵심 발견**: WG≥0.94 **그리고** PZ≥0.85를 **한 논문에서 모두** 충족하는 건 사실상 **Zabihollahy 2019 유일** (2개 독립 종합 리뷰로 교차확인). PZ는 문헌 평균 DSC ~0.79로 낮아 0.85 넘는 연구가 드묾.

### 2.3 논문별 Dice 결과 요약

- **Zabihollahy 2019 (Med Phys, 225명, 두 개 U-Net)**: T2W — WG 0.9533 / CG 0.9375 / PZ 0.8678 ; ADC — WG 0.9209 / CG 0.8989 / PZ 0.8610
- **Bardis 2021 (Radiol Imaging Cancer, 242명)**: WG 0.940(IQR 0.930–0.961) / TZ 0.910(0.894–0.938) / PZ 0.774(0.727–0.832). (부피 Pearson r = 0.981/0.992/0.927)
- **Xu 2023 (Insights into Imaging, 다기관)**: 내부 CG 0.909·PZ 0.844 / 외부공개 0.889·0.755 / 외부민간 0.869·0.764. (WG·TZ 라벨 없음, CG=TZ 대응)
- **Rundo 2019 (Neurocomputing, 다기관 3셋)**: 최고 CG 0.937 / PZ 0.919 (데이터셋별 PZ 0.80~0.92 편차)

### 2.4 참고: 세 구역 모두 보고하는 비-SCIE 논문

- Gaudiano 계열 아님. 예: "Multi-label semantic segmentation of the prostate gland", Discover Artificial Intelligence(**Scopus**, 非SCIE)·2024 — WG ~0.91 / CG 0.75 / PZ 0.67. (세 구역 보고하나 값 낮음)
- Cuocolo R, et al. (J Magn Reson Imaging, SCIE·2021): WG 0.91 / TZ 0.87 / PZ 0.71 (DSC) — TZ만 기준 충족.
- Litjens 2014 (PROMISE12, Med Image Anal): **전립선 전체만**, TZ·PZ 없음 → **시험방법(지표 정의) 근거**로 활용.
- AJR 2020 (고려대, Lee DK et al.): 전립선 전체 DSC 0.8712 / TZ 0.7648 — 국내 MRI 벤치마크(회사 CT 0.85 대비 MRI 0.87) 인용용.

### 2.5 시험방법 (DSC 기준, 8단계)

1. 학습 미사용 전립선 MRI 데이터셋(T2W, n≥200, 가능시 외부기관 포함) 준비
2. 영상의학 전문의 2인 이상 합의로 전립선 전체·이행대·말초대 수기 분할 → 참조표준(GT) 마스크 확보
3. 제품 구역 분할 실행 → 전립선 전체·이행대·말초대 자동 분할·표시 확인
4. 구역별·전체 부피(cm³) 정량 산출·표시 확인
5. 각 영상·각 구역에서 예측 vs 참조표준 간 DSC 산출
6. 전체 데이터셋 구역별 평균 DSC(평균±표준편차, 95% 신뢰구간) 산출
7. 평균 DSC가 시험기준(WG ≥0.94 / TZ ≥0.85 / PZ ≥0.85) 충족 여부 판정
8. PSA 입력 시 PSAD(= PSA ÷ 전립선 전체 부피) 산출 확인

> 정낭(SV)은 분할·표시·부피만 확인, DSC 합격 판정 대상에서 제외.

---

## 3. 시험항목 3 — 전립선암 의심 병변(csPCa) 분할 및 부피 산출

### 3.1 시험기준

- 구역 분할 완료된 전립선 영역 내에서 csPCa 의심 병변이 분할·표시되고 병변 부피(cm³) 산출.
- **병변 분할 DSC ≥ 0.78** (병변 양성 증례, 예측 vs 전문의 참조표준).
- **병변 유무 판정 (참조표준=조직검사 결과 대비) 민감도 ≥ 78% · 특이도 ≥ 81%.**

> ⚠️ 문서 내 불일치 주의: 일부 위치에 "민감도 85%·특이도 75%"가 남아 있어 "78%/81%"와 충돌 → 통일 필요.

### 3.2 민감도·특이도 근거 문헌

| No. | 문헌 | 저널(등재)·연도 | 민감도 | 특이도 | 비고 |
|---|---|---|---|---|---|
| [주] | Wu H, et al. (Bian Y 교신) | **Nature Communications (SCIE)·2025** | 0.97 | 0.88 | 전립선 MRI 자동 csPCa 검출, **실사용(post-implementation)** 기준 |
| [보조] | Gaudiano C, et al. | **Cancers (Basel, SCIE)·2022** | 0.84 | 0.84 | MRI(ADC) **라디오믹스**, csPCa(GG≥3) 분류, 참조표준=생검, 시험셋 50례 |
| [제외] | Zhao Y, et al. | Prostate Cancer Prostatic Dis (SCIE) | — | — | 메타분석. 민감도·특이도 동시 충족 못함(특이도 0.73, CI상단 0.81) |

**핵심**: 민감도 ≥78%는 대부분 충족(쉬움), **특이도 ≥81%가 관문**. SCIE급에서 두 조건 동시 충족은 **Wu/Bian 2025(실사용 0.97/0.88)**와 **Gaudiano 2022(84%/84%)** 두 편.

**중요 단서(인용 시 명시)**:
- Wu/Bian 2025: 0.97/0.88은 **AI를 임상 워크플로우(PI-RADS≥3)에 통합한 실사용 배치** 조건. **AI 단독 외부검증(TCIA)은 0.75/0.76**으로 기준 미달. → "실사용 기준 0.97/0.88"로 조건 명시 인용.
- Gaudiano 2022: **이미 발견된 PI-RADS≥3 병변 중 csPCa(GG≥3) 분류** 모델(검출 아님), 라디오믹스(딥러닝 아님), 표본 작음.
- **제품(M2)의 특이도 0.81은 반드시 자체 검증 데이터로 확증** (문헌만으로 일반화 지양).

### 3.3 근거 인용 (복붙용)

```
[1] Wu H, et al. Automated MRI system for clinically significant prostate cancer detection:
    development, validation and real-world implementation. Nature Communications. 2025;16:11583.
    doi:10.1038/s41467-025-66593-z
[2] Gaudiano C, et al. Beyond Multiparametric MRI and towards Radiomics to Detect Prostate Cancer:
    A Machine Learning Model to Predict Clinically Significant Lesions. Cancers (Basel). 2022;14(24):6156.
    doi:10.3390/cancers14246156
```

### 3.4 시험방법 (요지)

1. 학습 미사용 시험 데이터셋(csPCa 양성·음성 포함) + 각 증례 참조표준(조직검사) 확보
2. 구역 분할 완료 상태에서 csPCa 병변 검출 실행 → 병변 분할·표시 + 병변 부피(cm³) 산출 확인
3. 판정 기준(임계값) 적용해 병변 유무(양성/음성) 판정
4. 참조표준 대조로 TP·FP·FN·TN 집계
5. 민감도·특이도(각 95% CI) 산출
6. 시험기준(민감도 ≥78%·특이도 ≥81%) 충족 여부 확인 (+ 병변 양성 증례 평균 DSC ≥0.78 확인)

---

## 4. 시험항목 1 — 전립선 MRI 영상 입력 및 시퀀스 분류 (요약)

- 시험기준: MRI 파일 정상 입력/업로드 + 촬영 시퀀스(T2강조/ADC/고b값 DWI) 자동 분류 → 분석가능 형식(NIfTI) 변환.
- 시험방법: ① 영상(3개 시퀀스 포함) 준비·업로드 ② 정상 등록 확인 ③ 시퀀스별 올바른 자동 분류 + NIfTI 변환 확인.

---

## 5. 규제 조문 — 근거자료 인정 근거

**「디지털의료제품 허가·인증·신고·심사 및 평가 등에 관한 규정」(식약처, 2026-54)**

- **제26조제1항제4호가목4)** = SCI 또는 SCIE 등재 전문학회지에 게재된 논문을 (독립형 디지털의료기기소프트웨어의) **임상시험 등 평가 자료로 인정**한다는 조항.
  - 계층: 제26조(첨부서류의 요건) > ①항(독립형 SW 심사 첨부서류) > 4호(임상시험 등 평가에 관한 자료) > 가목(일반사항) > 4)
  - (내장형이면 제2항 → 제26조제2항제4호가목4))
- **읽는 법**: SCI(E) 논문은 임상시험 자료로 인정되나, 그 논문이 "나목 세부사항"(대상자 선정·제외기준, 유효성·안전성 평가기준·방법, 임상결과, 분석·평가)의 **내용 요건**을 갖춰야 실제 인정. → 형식(SCIE 등재)만으로 끝 아님.
- M2 근거 논문은 모두 SCIE 등재로 형식 요건 충족. 보수적으로는 **문헌(4호) + 제품 자체 임상적 성능시험 자료(1호)** 병행 제시가 안전.

---

## 6. 전체 결론 요약

1. **구역 분할(항목 2)**: DSC 기준(WG≥0.94·TZ≥0.85·PZ≥0.85) 채택. 근거는 Zabihollahy(전 구역)·Bardis·Xu·Rundo(SCIE). PZ≥0.85가 문헌상 가장 까다로움 → 제품 실측 확인 필수.
2. **병변 검출(항목 3)**: 민감도≥78%·특이도≥81%. 근거는 Wu/Bian 2025(실사용 0.97/0.88)·Gaudiano 2022(84%/84%). **특이도 0.81은 제품 파일럿 데이터로 확증**.
3. **지표 정의 표준**: PROMISE12(Litjens 2014) 준용.
4. **문서 내 기준 불일치(DSC/ASSD, 85·75 / 78·81) 통일**이 선결 과제.
5. **규제 인정 근거**: 제26조제1항제4호가목4) (SCI/SCIE 논문 인정) — 단, 세부사항 내용요건 충족 전제.

---

*본 문서는 규제 컨설팅 작업 내용을 학습·참고용으로 정리한 것이며, 최종 인허가 판단은 식약처 심사부서 및 RA 전문가의 공식 확인을 따라야 함.*
