"""
parse_quiz.py — UDSL-Torts_Quiz Answers_2026S.pdf 파싱
출력: quiz_data.json
구조: {class: [{q_num, q_text, options:[{label,text}], correct_answer, explanation, q_ko, exp_ko}]}

correct_answer 추출 전략:
  PDF의 정답은 빨간 글씨 (1.0, 0.0, 0.0) + Bold 로 표기됨.
  각 컬럼에서 "Question N" 이후 처음 등장하는 빨간 [A-D]. 글자를 정답으로 인식.
  → AI 추론 없이 순수 PDF 파싱. hallucination 원천 차단.
"""
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')
import pdfplumber

PDF = r'F:\mbe\udsl퀴즈\UDSL-Torts_Quiz Answers_2026S.pdf'
OUT = r'F:\mbe\_extracted\quiz_data.json'

RED_COLOR = (1.0, 0.0, 0.0)   # 정답 표시 색상


# ── 1단계: 텍스트 기반 문제 파싱 ──────────────────────────────────────────

# 전체 텍스트 추출 (좌→우 컬럼 순서)
blocks = []
with pdfplumber.open(PDF) as pdf:
    for page in pdf.pages:
        w = page.width
        for col in [page.within_bbox((0, 0, w/2, page.height)),
                    page.within_bbox((w/2, 0, w, page.height))]:
            t = col.extract_text()
            if t and t.strip():
                blocks.append(t.strip())

full = '\n'.join(blocks)

# Class 섹션 분리
SECTION_RE = re.compile(
    r'(Class \d+ Quiz|Practice Questions)\s*\n?(.*?)(?=Class \d+ Quiz|Practice Questions|$)',
    re.DOTALL
)
sections = {}
for m in SECTION_RE.finditer(full):
    key = m.group(1).strip()
    body = m.group(2).strip()
    sections[key] = body

def parse_questions(text):
    # Question N 으로 분리
    parts = re.split(r'(?=Question\s+\d+\b)', text)
    questions = []
    for part in parts:
        part = part.strip()
        if not part or not re.match(r'Question\s+\d+', part):
            continue
        # 문제 번호
        m = re.match(r'Question\s+(\d+)\s*\n?(.*)', part, re.DOTALL)
        if not m:
            continue
        q_num = int(m.group(1))
        rest = m.group(2).strip()

        # 옵션 A~D 분리
        opt_pattern = re.compile(r'\n([A-D])\.\s+')
        opt_positions = [(mm.start(), mm.group(1)) for mm in opt_pattern.finditer(rest)]

        if len(opt_positions) >= 2:
            q_text = rest[:opt_positions[0][0]].strip()
            options = []
            for i, (pos, label) in enumerate(opt_positions):
                end = opt_positions[i+1][0] if i+1 < len(opt_positions) else None
                opt_body = rest[pos:end] if end else rest[pos:]
                opt_text = re.sub(r'^\n[A-D]\.\s*', '', opt_body).strip()
                options.append({'label': label, 'text': opt_text})

            # 마지막 옵션에서 해설 분리:
            # 패턴1: "답변 문장.\n해설..." → ".\n" 위치에서 분리
            # 패턴2: "Both A and B\n해설..." → 단답형, 첫 \n[A-Z] 에서 분리
            explanation = ''
            if options:
                last_text = options[-1]['text']
                # 패턴1: 마침표+줄바꿈
                m_boundary = re.search(r'\.\n', last_text)
                if m_boundary:
                    options[-1]['text'] = last_text[:m_boundary.start() + 1].strip()
                    explanation = last_text[m_boundary.end():].strip()
                else:
                    # 패턴2: 단답형 — 줄바꿈+대문자 (새 문장 시작)
                    m_boundary2 = re.search(r'\n([A-Z])', last_text)
                    if m_boundary2:
                        options[-1]['text'] = last_text[:m_boundary2.start()].strip()
                        explanation = last_text[m_boundary2.start() + 1:].strip()
        else:
            q_text = rest.strip()
            options = []
            explanation = ''

        questions.append({
            'q_num': q_num,
            'q_text': q_text,
            'options': options,
            'correct_answer': '',   # 2단계에서 채워짐
            'explanation': explanation,
            'q_ko': '',             # 번역 슬롯
            'exp_ko': '',
        })

    return questions

result = {}
for sec_key, body in sections.items():
    qs = parse_questions(body)
    # cls 키 정규화
    m = re.search(r'Class (\d+)', sec_key)
    if m:
        cls = f'cl{m.group(1)}'
    else:
        cls = 'practice'
    result[cls] = qs
    print(f'{sec_key}: {len(qs)}문제')


# ── 2단계: 색상 기반으로 correct_answer(빨강) + explanation(파랑) 추출 ────

BLUE_COLOR = (0.2, 0.4, 1.0)   # 학교 해설 교안 색상

def extract_colored_content(pdf_path):
    """
    PDF 색상 기반 추출:
      빨간 텍스트 (1.0,0.0,0.0) → correct_answer (정답 선지 글자)
      파란 텍스트 (0.2,0.4,1.0) → explanation (학교 해설 교안)

    컬럼별 순서 처리로 Question N → RED답 → BLUE교안 순서를 정확히 매핑.

    반환: {
      section_key: {
        q_num_int: {
          'correct_answer': 'A'|'B'|'C'|'D',
          'explanation': '...'
        }
      }
    }
    """
    data = {}
    current_section = None
    current_q = None

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            w_total = page.width
            for x0, x1 in [(0, w_total/2), (w_total/2, w_total)]:
                col = page.within_bbox((x0, 0, x1, page.height))
                words = col.extract_words(extra_attrs=['non_stroking_color'])

                i = 0
                while i < len(words):
                    w = words[i]
                    txt = w['text']

                    # 섹션 헤더 감지: Class N Quiz
                    if (txt == 'Class' and i+2 < len(words)
                            and words[i+1]['text'].isdigit()
                            and words[i+2]['text'] == 'Quiz'):
                        current_section = f'cl{words[i+1]["text"]}'
                        data.setdefault(current_section, {})
                        i += 3
                        continue

                    # 섹션 헤더 감지: Practice Questions
                    if txt == 'Practice' and i+1 < len(words) and words[i+1]['text'] == 'Questions':
                        current_section = 'practice'
                        data.setdefault(current_section, {})
                        i += 2
                        continue

                    # Question N 감지
                    if (txt == 'Question' and i+1 < len(words)
                            and words[i+1]['text'].isdigit()):
                        current_q = int(words[i+1]['text'])
                        i += 2
                        continue

                    # 빨간 [A-D]. 감지 → correct_answer (처음 나온 것만)
                    if (current_section and current_q is not None
                            and w.get('non_stroking_color') == RED_COLOR
                            and re.match(r'^[A-D]\.$', txt)):
                        q_dict = data[current_section].setdefault(current_q, {})
                        if 'correct_answer' not in q_dict:
                            q_dict['correct_answer'] = txt[0]  # 'A','B','C','D'

                    # 파란 텍스트 → explanation (해당 Question의 교안)
                    elif (current_section and current_q is not None
                            and w.get('non_stroking_color') == BLUE_COLOR):
                        q_dict = data[current_section].setdefault(current_q, {})
                        prev = q_dict.get('explanation', '')
                        q_dict['explanation'] = (prev + ' ' + txt).strip()

                    i += 1

    return data

print('\n정답·교안 추출 중 (빨강=정답, 파랑=교안)...')
colored = extract_colored_content(PDF)

# 추출 결과를 result에 병합
merged_ans = 0
merged_exp = 0
missing_ans = 0
for sec, qs in result.items():
    sec_data = colored.get(sec, {})
    for q in qs:
        qn = q['q_num']
        q_colored = sec_data.get(qn, {})
        if q_colored.get('correct_answer'):
            q['correct_answer'] = q_colored['correct_answer']
            merged_ans += 1
        else:
            missing_ans += 1
            print(f'  ⚠ 정답 없음: {sec}_Q{qn}')
        if q_colored.get('explanation'):
            q['explanation'] = q_colored['explanation']   # 파란색이 우선
            merged_exp += 1

print(f'정답 병합: {merged_ans}문항 / 교안 병합: {merged_exp}문항 / 정답 없음: {missing_ans}문항')


# ── 3단계: 저장 ──────────────────────────────────────────────────────────

# 기존 quiz_data.json에서 q_ko / exp_ko 보존 (번역 손실 방지)
import os
if os.path.exists(OUT):
    with open(OUT, encoding='utf-8') as f:
        old_data = json.load(f)
    for sec, qs in result.items():
        old_qs = {q['q_num']: q for q in old_data.get(sec, [])}
        for q in qs:
            old = old_qs.get(q['q_num'])
            if old:
                if old.get('q_ko'):
                    q['q_ko'] = old['q_ko']
                if old.get('exp_ko'):
                    q['exp_ko'] = old['exp_ko']
    print('기존 번역 데이터(q_ko/exp_ko) 보존 완료')

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

total = sum(len(v) for v in result.values())
print(f'\n저장 완료: {OUT}')
print(f'총 {len(result)}섹션, {total}문항')
for sec, qs in result.items():
    answered = sum(1 for q in qs if q.get('correct_answer'))
    print(f'  {sec}: {len(qs)}문항 (정답추출: {answered}개)')
