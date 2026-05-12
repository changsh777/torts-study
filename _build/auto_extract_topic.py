"""
auto_extract_topic.py — UDSL PPT 슬라이드 → 토픽 curated.json 자동 생성

원칙 (환각 0):
  - 슬라이드 영문 텍스트: raw 그대로
  - 슬라이드 한국어 코멘트: 그대로 (= 김윤상 정리본 추정)
  - Rule Statement: torts_rules_raw.json (김윤상 docx) 그대로
  - Claude 의역·요약·추가 작성 금지
  - 0회독 r0-txt 도입 한 줄만 슬라이드 첫 한국어 코멘트 또는 영문 정의 그대로
"""
import json, re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

NOTES_PATH = r'F:\mbe\_extracted\udsl_ppt\class01_notes.json'
RULES_PATH = r'F:\mbe\_extracted\torts_rules_raw.json'
OUT_DIR    = r'F:\mbe\_extracted\udsl_ppt'

# 토픽별 슬라이드 영역 + Rule docx 인덱스
TOPICS = [
    {
        'key': 'battery',
        'label': 'Battery (폭행)',
        'stars': 'Class 1 ★★★★★',
        'slide_range': (28, 71),
        'rule_idx': [2, 3, 4, 5, 6, 7],
        'mcq_slide_starts': [48, 51, 54, 57, 60, 62, 64],  # Hypothetical 1~7 시작 슬라이드
    },
    {
        'key': 'assault',
        'label': 'Assault (협박)',
        'stars': 'Class 1 ★★★★',
        'slide_range': (72, 87),
        'rule_idx': [8],
        'mcq_slide_starts': [],  # auto-detect
    },
    {
        'key': 'fi',
        'label': 'False Imprisonment (불법감금)',
        'stars': 'Class 1 ★★★★',
        'slide_range': (88, 116),
        'rule_idx': [9, 10, 11, 12],
        'mcq_slide_starts': [],
    },
    {
        'key': 'iied',
        'label': 'IIED (정신적 고통의 고의)',
        'stars': 'Class 1 ★★★',
        'slide_range': (117, 134),
        'rule_idx': [13, 14],
        'mcq_slide_starts': [],
    },
    {
        'key': 'trespass_land',
        'label': 'Trespass to Land (토지 침입) — 도입',
        'stars': 'Class 1 ★★',
        'slide_range': (135, 149),
        'rule_idx': [15, 16],
        'mcq_slide_starts': [],
    },
]

KOR_RE = re.compile(r'[가-힣]')

def is_korean_line(text):
    return bool(KOR_RE.search(text))

def split_lang(texts):
    """텍스트 리스트를 영어/한국어 라인으로 분리. 슬라이드 한 장 안에서."""
    en, ko = [], []
    for t in texts:
        t = t.strip()
        if not t: continue
        if is_korean_line(t):
            ko.append(t)
        else:
            en.append(t)
    return en, ko

def detect_mcq_slide(slide):
    """이 슬라이드가 객관식 문제인지."""
    text = '\n'.join(slide['texts'])
    has_hypo = bool(re.search(r'Hypothetical\s*\d', text, re.I)) or 'Practice Question' in text
    has_yn = ('Yes' in text and 'No' in text and len(text) > 40)
    has_abcd_options = bool(re.search(r'\([A-D]\)\s', text)) or text.count('A.') + text.count('B.') >= 2
    return has_hypo and (has_yn or has_abcd_options)

def group_subsections(slides_in_topic, mcq_slide_starts):
    """
    같은 첫 줄 제목 연속 슬라이드를 한 sub-section으로.
    mcq 슬라이드는 별도 분리.
    """
    mcq_slides = []
    body_slides = []
    for s in slides_in_topic:
        if detect_mcq_slide(s) or 'Hypothetical' in (s['texts'][0] if s['texts'] else ''):
            mcq_slides.append(s)
        else:
            body_slides.append(s)

    # body slides을 첫 줄 제목 기준으로 그룹핑
    sub_sections = []
    cur = None
    for s in body_slides:
        title = s['texts'][0].strip() if s['texts'] else '(제목 없음)'
        # 제목 정규화 (공백, 특수문자 일부 제거)
        norm = re.sub(r'[\s ]+', ' ', title).strip()
        if cur and cur['_norm'] == norm:
            cur['slides'].append(s['slide'])
            cur['raw_texts'].extend(s['texts'][1:])
            if s['notes']:
                cur['notes'] += '\n' + s['notes']
        else:
            if cur:
                sub_sections.append(cur)
            cur = {
                '_norm': norm,
                'title': title,
                'slides': [s['slide']],
                'raw_texts': list(s['texts'][1:]),  # 첫 줄(=제목) 제외
                'notes': s['notes'],
            }
    if cur:
        sub_sections.append(cur)

    # 각 sub-section의 본문 영/한 분리
    out_subs = []
    for sec in sub_sections:
        en, ko = split_lang(sec['raw_texts'])
        notes_en, notes_ko = split_lang(sec['notes'].split('\n')) if sec['notes'] else ([], [])
        en_text = '\n'.join(en).strip()
        ko_text = '\n'.join(ko).strip()
        # title 자체에 한국어가 섞이면 영문/한국어 분리
        title_en = sec['title']
        title_ko = ''
        if is_korean_line(sec['title']):
            # 제목 내 한국어 추출
            kor_chars = ''.join(c for c in sec['title'] if is_korean_line(c) or c in ' ,.()/')
            title_ko = kor_chars.strip()
        out_subs.append({
            'title_en': title_en,
            'title_ko': title_ko,
            'slides': sec['slides'],
            'content_en': en_text,
            'content_ko': ko_text,
            'notes_en': '\n'.join(notes_en).strip(),
            'notes_ko': '\n'.join(notes_ko).strip(),
        })

    # mcq 그룹핑 — 같은 Hypothetical 번호 연속 슬라이드
    mcq_items = []
    cur_mcq = None
    for s in mcq_slides:
        text_joined = '\n'.join(s['texts'])
        m = re.search(r'Hypothetical\s*(\d)', text_joined, re.I)
        hypo_num = m.group(1) if m else None
        if cur_mcq and cur_mcq.get('hypo_num') == hypo_num:
            cur_mcq['slides'].append(s['slide'])
            cur_mcq['raw_texts'].extend(s['texts'])
            if s['notes']:
                cur_mcq['notes'] += '\n' + s['notes']
        else:
            if cur_mcq:
                mcq_items.append(cur_mcq)
            cur_mcq = {
                'hypo_num': hypo_num,
                'slides': [s['slide']],
                'raw_texts': list(s['texts']),
                'notes': s['notes'] or '',
            }
    if cur_mcq:
        mcq_items.append(cur_mcq)

    # mcq 영/한 분리
    out_mcq = []
    for item in mcq_items:
        en_lines, ko_lines = split_lang(item['raw_texts'])
        # 옵션 자동 검출 (Yes/No 또는 A/B/C/D)
        en_text = '\n'.join(en_lines)
        ko_text = '\n'.join(ko_lines)
        opts = []
        # Yes/No 패턴
        if 'Yes' in en_text.split('\n') and 'No' in en_text.split('\n'):
            opts = [
                {'label': 'A', 'text': 'Yes', 'correct': None},
                {'label': 'B', 'text': 'No',  'correct': None},
            ]
        # ABCD 패턴
        else:
            for letter in 'ABCD':
                m = re.search(rf'(?:^|\n)\s*\(?{letter}\)?\.?\s*([^\n]+)', en_text)
                if m:
                    opts.append({'label': letter, 'text': m.group(1).strip(), 'correct': None})
        out_mcq.append({
            'id': f'q{item["hypo_num"] or len(out_mcq)+1}',
            'hypo_num': item['hypo_num'],
            'slides': item['slides'],
            'q_en_raw': en_text,
            'q_ko_raw': ko_text,
            'options': opts,
            'notes': item['notes'],
        })

    return out_subs, out_mcq

def main():
    with open(NOTES_PATH, 'r', encoding='utf-8') as f:
        all_notes = json.load(f)
    with open(RULES_PATH, 'r', encoding='utf-8') as f:
        rules = json.load(f)

    for topic in TOPICS:
        key = topic['key']
        s_start, s_end = topic['slide_range']
        slides = [s for s in all_notes if s_start <= s['slide'] <= s_end]
        sub_sections, mcq_items = group_subsections(slides, topic['mcq_slide_starts'])

        # rule statements (idx별)
        rule_lines = [{'idx': i, 'text': rules[i]} for i in topic['rule_idx'] if 0 <= i < len(rules)]

        # 한국어 도입 (슬라이드 첫 한국어 코멘트가 있다면 그것, 아니면 비움 — 환각 X)
        ko_intro_candidate = ''
        for s in slides:
            for t in s['texts']:
                if is_korean_line(t) and len(t) > 30:
                    ko_intro_candidate = t.strip()
                    break
            if ko_intro_candidate:
                break

        out = {
            '_comment': f'UDSL Class 1 — {topic["label"]} (자동 추출, 환각 0 원칙)',
            '_principle': 'UDSL 슬라이드 raw 텍스트 그대로 + 김윤상 Rule docx 그대로. Claude 의역 X.',
            'topic_key': key,
            'topic_label': topic['label'],
            'stars': topic['stars'],
            'slide_range': topic['slide_range'],
            'ko_intro_candidate': ko_intro_candidate,
            'rule_lines': rule_lines,
            'sub_sections': sub_sections,
            'udsl_quiz_raw': mcq_items,
        }
        out_path = os.path.join(OUT_DIR, f'class01_{key}_curated.json')
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f'✓ {key:<14} sub-sections={len(sub_sections):>2}, mcq={len(mcq_items):>2}, rule={len(rule_lines)} → {out_path}')

if __name__ == '__main__':
    main()
