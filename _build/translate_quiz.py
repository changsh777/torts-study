"""
translate_quiz.py — UDSL Torts 퀴즈 영→한 번역 (Ollama EXAONE)
quiz_data.json 의 q_ko · exp_ko 필드를 채워서 덮어씀

사용법:
  python F:\mbe\_build\translate_quiz.py          # 전체 번역
  python F:\mbe\_build\translate_quiz.py --cls cl2  # 특정 클래스만
  python F:\mbe\_build\translate_quiz.py --force    # 기번역도 재번역

Mac Mini Ollama: http://192.168.0.141:11434
모델: exaone3.5:7.8b
"""
import sys, json, time, re, argparse, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

QUIZ_DATA  = r'F:\mbe\_extracted\quiz_data.json'
OLLAMA_URL = 'http://192.168.0.141:11434/api/generate'
MODEL      = 'exaone3.5:7.8b'
TIMEOUT    = 120  # 초

SYSTEM_PROMPT = (
    "[SYSTEM] 당신은 미국 불법행위법(Torts) 전문 한국어 번역가입니다. "
    "주어진 영문 텍스트를 정확하고 자연스러운 한국어로 번역하세요. "
    "법률 용어는 처음 등장 시 한영 병기: 예) 폭행(battery), 과실(negligence). "
    "번역문만 출력하세요. 설명, 영어 원문, 따옴표 없이.[/SYSTEM]"
)

def call_exaone(text: str) -> str:
    """Ollama EXAONE API 호출"""
    prompt = f"{SYSTEM_PROMPT}\n\n번역할 텍스트:\n{text}\n\n한국어 번역:"
    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 1024},
    }).encode('utf-8')
    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        resp = json.loads(r.read())
    result = resp.get('response', '').strip()
    # prefix 잔존 제거: "한국어 번역: " 등
    result = re.sub(r'^(?:한국어\s*번역[:：]?\s*|번역[:：]?\s*)', '', result).strip()
    # EXAONE 추가 주석 제거: "*단어 (번역): ..." 형태의 glossary footnote
    result = re.sub(r'\n\*[A-Za-z가-힣].*$', '', result, flags=re.DOTALL).strip()
    # 빈 줄 여러 개 → 단일 줄바꿈
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result

def translate_quiz(quiz_data: dict, target_cls=None, force=False):
    total = 0
    for cls_key, questions in quiz_data.items():
        if target_cls and cls_key != target_cls:
            continue
        print(f'\n── {cls_key} ({len(questions)}문제) ──')
        for q in questions:
            q_num = q['q_num']
            need_q   = force or not q.get('q_ko', '').strip()
            need_exp = force or not q.get('exp_ko', '').strip()

            if need_q and q.get('q_text', '').strip():
                print(f'  Q{q_num} 문제 번역...', end=' ', flush=True)
                try:
                    q['q_ko'] = call_exaone(q['q_text'])
                    print(f'✓  ({len(q["q_ko"])}자)')
                    total += 1
                    time.sleep(0.5)
                except Exception as e:
                    print(f'✗ {e}')

            if need_exp and q.get('explanation', '').strip():
                print(f'  Q{q_num} 해설 번역...', end=' ', flush=True)
                try:
                    q['exp_ko'] = call_exaone(q['explanation'])
                    print(f'✓  ({len(q["exp_ko"])}자)')
                    total += 1
                    time.sleep(0.5)
                except Exception as e:
                    print(f'✗ {e}')

        # 클래스 단위 중간 저장 (중단돼도 유실 없음)
        json.dump(quiz_data, open(QUIZ_DATA, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2)
        print(f'  → {cls_key} 중간 저장 완료')

    return total

def main():
    parser = argparse.ArgumentParser(description='퀴즈 EXAONE 번역')
    parser.add_argument('--cls',   default=None,  help='cl1~cl8 또는 practice')
    parser.add_argument('--force', action='store_true', help='기번역 항목도 재번역')
    args = parser.parse_args()

    # Ollama 연결 확인
    try:
        urllib.request.urlopen('http://192.168.0.141:11434/api/tags', timeout=5)
        print(f'✅ Ollama 연결 확인 ({MODEL})')
    except Exception as e:
        print(f'❌ Ollama 연결 실패: {e}')
        print('   Mac Mini (192.168.0.141:11434) 가 실행 중인지 확인하세요')
        sys.exit(1)

    quiz_data = json.load(open(QUIZ_DATA, 'r', encoding='utf-8'))
    n = translate_quiz(quiz_data, target_cls=args.cls, force=args.force)

    json.dump(quiz_data, open(QUIZ_DATA, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)
    print(f'\n✅ 번역 완료: {n}건 → {QUIZ_DATA}')
    print('다음 단계: python F:\\mbe\\_build\\builder_v8.py')

if __name__ == '__main__':
    main()
