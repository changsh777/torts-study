"""
auto_extract_class.py — Class 2~8 PPT → 통째 curated.json (간이 처리)
각 Class 한 토픽으로 묶음 (사용자 검수 후 세분화 가능).
"""
import json, re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r'F:\mbe\_extracted\udsl_ppt'
RULES_PATH = r'F:\mbe\_extracted\torts_rules_raw.json'
KOR_RE = re.compile(r'[가-힣]')

CLASSES = [
    {'cls':'cl2', 'notes':'class02_notes.json', 'key':'cl2_intent_defenses', 'label':'Class 2 — 의도 II (Trespass·Conversion) + Defenses', 'stars':'Class 2 ★★★', 'rule_idx':[15,16,17,18,19,20,21,22,23,24,25,26]},
    {'cls':'cl3', 'notes':'class03_notes.json', 'key':'cl3_neg_duty_breach',  'label':'Class 3 — Negligence I (Duty + Breach)',           'stars':'Class 3 ★★★★★','rule_idx':[27,28,29,30,31,32,33,34,35,36,37,38,39,40]},
    {'cls':'cl4', 'notes':'class04_notes.json', 'key':'cl4_causation_harm',   'label':'Class 4 — Negligence II (Causation + Harm)',      'stars':'Class 4 ★★★★','rule_idx':[41,42,43,44,45,46,47,48,49,50,51]},
    {'cls':'cl5', 'notes':'class05_notes.json', 'key':'cl5_neg_defenses',     'label':'Class 5 — Defenses to Negligence + Multi-D + Vicarious','stars':'Class 5 ★★★★','rule_idx':[52,53,54,55,56,57,58]},
    {'cls':'cl6', 'notes':'class06_notes.json', 'key':'cl6_strict_liability', 'label':'Class 6 — Strict Liability + Products Liability',  'stars':'Class 6 ★★★','rule_idx':[59,60,61,62,63]},
    {'cls':'cl7', 'notes':'class07_notes.json', 'key':'cl7_property_torts',   'label':'Class 7 — Property Torts (Trespass to Land + Nuisance)','stars':'Class 7 ★★★','rule_idx':[64]},
    {'cls':'cl8', 'notes':'class08_notes.json', 'key':'cl8_defam_privacy',    'label':'Class 8 — Defamation + Privacy Torts',             'stars':'Class 8 ★★★★','rule_idx':[65,66,67,68,69,70]},
]

def is_korean(t):
    return bool(KOR_RE.search(t))

def split_lang(texts):
    en, ko = [], []
    for t in texts:
        t = t.strip()
        if not t: continue
        (ko if is_korean(t) else en).append(t)
    return en, ko

def detect_mcq(slide):
    text = '\n'.join(slide['texts'])
    has_hypo = bool(re.search(r'Hypothetical\s*\d', text, re.I)) or 'Practice Question' in text
    has_yn = ('Yes' in text.split('\n') and 'No' in text.split('\n'))
    has_abcd = bool(re.search(r'(?:^|\n)\s*\(?[A-D]\)?\.?\s+\w', text))
    return has_hypo and (has_yn or has_abcd)

def main():
    rules = json.load(open(RULES_PATH, 'r', encoding='utf-8'))
    for cl in CLASSES:
        notes = json.load(open(os.path.join(OUT_DIR, cl['notes']), 'r', encoding='utf-8'))

        body, mcqs = [], []
        for s in notes:
            if detect_mcq(s) or 'Hypothetical' in (s['texts'][0] if s['texts'] else ''):
                mcqs.append(s)
            else:
                body.append(s)

        # body 그룹핑 (같은 첫 줄 연속)
        subs, cur = [], None
        for s in body:
            title = s['texts'][0].strip() if s['texts'] else '(제목 없음)'
            norm = re.sub(r'\s+', ' ', title)
            if cur and cur['_norm'] == norm:
                cur['slides'].append(s['slide'])
                cur['raw'].extend(s['texts'][1:])
                if s['notes']: cur['notes'] += '\n' + s['notes']
            else:
                if cur: subs.append(cur)
                cur = {'_norm':norm, 'title':title, 'slides':[s['slide']], 'raw':list(s['texts'][1:]), 'notes':s['notes']}
        if cur: subs.append(cur)

        out_subs = []
        for sec in subs:
            en, ko = split_lang(sec['raw'])
            tk = ''
            if is_korean(sec['title']):
                tk = ''.join(c for c in sec['title'] if is_korean(c) or c in ' ,.()/-').strip()
            out_subs.append({
                'title_en': sec['title'],
                'title_ko': tk,
                'slides': sec['slides'],
                'content_en': '\n'.join(en).strip(),
                'content_ko': '\n'.join(ko).strip(),
                'notes_en': '', 'notes_ko': '',
            })

        # mcq 그룹핑
        out_mcq, cur_q = [], None
        for s in mcqs:
            text = '\n'.join(s['texts'])
            m = re.search(r'Hypothetical\s*(\d)', text, re.I)
            num = m.group(1) if m else None
            if cur_q and cur_q['hypo_num'] == num:
                cur_q['slides'].append(s['slide'])
                cur_q['raw'].extend(s['texts'])
                if s['notes']: cur_q['notes'] += '\n' + s['notes']
            else:
                if cur_q: out_mcq.append(cur_q)
                cur_q = {'hypo_num':num, 'slides':[s['slide']], 'raw':list(s['texts']), 'notes':s['notes'] or ''}
        if cur_q: out_mcq.append(cur_q)

        mcq_final = []
        for i, item in enumerate(out_mcq):
            en_lines, ko_lines = split_lang(item['raw'])
            en_text = '\n'.join(en_lines)
            ko_text = '\n'.join(ko_lines)
            opts = []
            if 'Yes' in en_text.split('\n') and 'No' in en_text.split('\n'):
                opts = [{'label':'A','text':'Yes','correct':None}, {'label':'B','text':'No','correct':None}]
            else:
                for letter in 'ABCD':
                    m = re.search(rf'(?:^|\n)\s*\(?{letter}\)?\.?\s*([^\n]+)', en_text)
                    if m: opts.append({'label':letter, 'text':m.group(1).strip()[:300], 'correct':None})
            mcq_final.append({
                'id': f'q{i+1}',
                'hypo_num': item['hypo_num'],
                'slides': item['slides'],
                'q_en_raw': en_text,
                'q_ko_raw': ko_text,
                'options': opts,
                'notes': item['notes'],
            })

        # ko_intro
        ko_intro = ''
        for s in notes:
            for t in s['texts']:
                if is_korean(t) and len(t) > 30:
                    ko_intro = t.strip()
                    break
            if ko_intro: break

        rule_lines = [{'idx':i, 'text':rules[i]} for i in cl['rule_idx'] if 0 <= i < len(rules)]

        out = {
            '_comment': f'UDSL {cl["label"]} (자동 추출)',
            'topic_key': cl['key'],
            'topic_label': cl['label'],
            'stars': cl['stars'],
            'class': cl['cls'],
            'ko_intro_candidate': ko_intro,
            'rule_lines': rule_lines,
            'sub_sections': out_subs,
            'udsl_quiz_raw': mcq_final,
        }
        out_path = os.path.join(OUT_DIR, f'{cl["cls"]}_curated.json')
        json.dump(out, open(out_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print(f'✓ {cl["cls"]} {cl["key"]:<26} subs={len(out_subs):>3} mcq={len(mcq_final):>2} rule={len(rule_lines)} → {out_path}')

if __name__ == '__main__':
    main()
