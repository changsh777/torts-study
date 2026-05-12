"""
make_answer_key.py — quiz_data.json에서 answer_key.json 추출

answer_key.json 은 correct_answer + explanation 의 유일한 진실 소스(source of truth).
AI 스크립트는 절대 이 파일을 건드리지 않는다.
인간 또는 parse_quiz.py(PDF 파서)만 수정 가능.
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

QUIZ_DATA   = r'F:\mbe\_extracted\quiz_data.json'
ANSWER_KEY  = r'F:\mbe\_extracted\answer_key.json'

with open(QUIZ_DATA, encoding='utf-8') as f:
    data = json.load(f)

answer_key = {}
for section, questions in data.items():
    answer_key[section] = {}
    for q in questions:
        q_num = str(q['q_num'])
        answer_key[section][q_num] = {
            'correct_answer': q.get('correct_answer', ''),
            'explanation':    q.get('explanation', ''),
        }

with open(ANSWER_KEY, 'w', encoding='utf-8') as f:
    json.dump(answer_key, f, ensure_ascii=False, indent=2)

total = sum(len(v) for v in answer_key.values())
print(f'answer_key.json 생성 완료: {len(answer_key)}개 섹션, {total}개 문항')
for sec, qs in answer_key.items():
    print(f'  {sec}: {len(qs)}문항')
