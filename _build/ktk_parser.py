"""
ktk_parser.py — KTK 교재 텍스트 파싱 + cl1~cl8 매핑 + EXAONE OCR 정제
입력: F:\mbe\KTK\torts한글_교정_dify.fixed.txt
      F:\mbe\KTK\torts영문_교정_dify.fixed.txt
출력: F:\mbe\_extracted\ktk_data.json

사용법:
  python F:\mbe\_build\ktk_parser.py            # 전체 파싱 + 정제
  python F:\mbe\_build\ktk_parser.py --no-llm   # 정제 없이 파싱만
  python F:\mbe\_build\ktk_parser.py --cl cl3   # 특정 챕터만
"""
import sys, re, json, time, argparse, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

KO_FILE  = r'F:\mbe\KTK\torts한글_교정_dify.fixed.txt'
EN_FILE  = r'F:\mbe\KTK\torts영문_교정_dify.fixed.txt'
OUT_FILE = r'F:\mbe\_extracted\ktk_data.json'

OLLAMA_URL = 'http://192.168.0.141:11434/api/generate'
MODEL      = 'exaone3.5:7.8b'

# ── 토픽 키워드 (내용 기반 감지) ──────────────────────────────────
TOPIC_KEYS = [
    ('battery',            ['battery', '배터리', '폭행', 'INTENT FOR BATTERY', 'harmful contact', 'offensive contact']),
    ('assault',            ['assault', '협박', 'apprehension', 'imminent']),
    ('false_imprisonment', ['false imprisonment', '불법감금', 'shopkeeper', '상점주인', '상점 주인', 'confinement']),
    ('iied',               ['iied', 'emotional distress', '감정적 고통', '정서적 고통', 'outrageous', 'nied', 'negligent infliction']),
    ('trespass_land',      ['trespass to land', '토지 침입', '토지침입', 'entry onto land']),
    ('conversion',         ['conversion', 'trespass to chattel', '동산 침해', '동산침해', 'chattel']),
    ('defenses_intentional',['consent', '동의', 'self-defense', '자기 방어', 'necessity', '필요성', 'privilege', 'shopkeeper privilege', 'defense of property']),
    ('negligence_duty',    ['duty of care', 'reasonable person', '주의의무', 'breach of duty', 'standard of care', '합리적인 사람']),
    ('negligence_general', ['negligence', '과실', 'elements of negligence', '과실의 요소']),
    ('causation',          ['causation', 'but-for', 'proximate cause', 'actual cause', '인과관계', 'superseding cause', 'intervening']),
    ('defenses_neg',       ['contributory negligence', 'comparative negligence', 'assumption of risk', '기여과실', '비교과실', '위험인수']),
    ('strict_liability',   ['strict liability', '엄격책임', 'abnormally dangerous', 'ultrahazardous', 'wild animal']),
    ('products_liability', ['product liability', '제품 책임', 'manufacturing defect', 'design defect', 'warning defect', '제조물 책임']),
    ('nuisance',           ['nuisance', '방해행위', 'public nuisance', 'private nuisance', '공적 방해', '사적 방해']),
    ('defamation',         ['defamation', '명예훼손', 'libel', 'slander', 'defamatory', 'publication of']),
    ('privacy',            ['privacy', '프라이버시', 'intrusion', 'false light', 'appropriation', 'public disclosure']),
]

# ── 토픽 → cl 매핑 ───────────────────────────────────────────────
CL_MAP = {
    'cl1': ['battery', 'assault', 'false_imprisonment', 'iied', 'trespass_land'],
    'cl2': ['conversion', 'defenses_intentional'],
    'cl3': ['negligence_duty', 'negligence_general'],
    'cl4': ['causation'],
    'cl5': ['defenses_neg'],
    'cl6': ['strict_liability', 'products_liability'],
    'cl7': ['nuisance'],
    'cl8': ['defamation', 'privacy'],
}

CL_LABELS = {
    'cl1': 'Class 1 — Intentional Torts I',
    'cl2': 'Class 2 — Intentional Torts II + Defenses',
    'cl3': 'Class 3 — Negligence (Duty + Breach)',
    'cl4': 'Class 4 — Causation + Harm',
    'cl5': 'Class 5 — Defenses to Negligence',
    'cl6': 'Class 6 — Strict Liability + Products',
    'cl7': 'Class 7 — Property Torts',
    'cl8': 'Class 8 — Defamation + Privacy',
}

# ── OCR 정제 (정규식 기본) ─────────────────────────────────────────
OCR_FIXES = [
    (r'Queson\b',          'Question'),
    (r'Questoin\b',        'Question'),
    (r'pllán\b',           'plan'),
    (r'Daⅽt[yу]\b',        'Dacty'),
    (r'Paoloλ[aα]\b',      'Paola'),
    (r'[∴∵∶·˙]',           ''),
    (r'[:;][\'\"]\s*[:;]', ''),
    (r'\n{4,}',            '\n\n\n'),
    (r'[ \t]{3,}',         ' '),
    # 메타데이터 헤더 제거
    (r'^##.*\n(?:과목|유형|키워드):.*\n?', '', re.MULTILINE),
    (r'^(?:과목|유형|키워드):.*\n?', '', re.MULTILINE),
]

def basic_clean(text: str) -> str:
    for fix in OCR_FIXES:
        if len(fix) == 2:
            text = re.sub(fix[0], fix[1], text)
        else:
            text = re.sub(fix[0], fix[1], text, flags=fix[2])
    return text.strip()

# ── EXAONE 정제 (고품질) ──────────────────────────────────────────
CLEAN_PROMPT = (
    "다음 미국 불법행위법(Torts) 교재 텍스트는 OCR 스캔 결과물입니다. "
    "다음 작업을 수행하세요:\n"
    "1. OCR 오류 수정 (깨진 단어, 이상한 특수문자 제거)\n"
    "2. 불완전한 문장 자연스럽게 보완\n"
    "3. 법률 용어 한영 병기 유지 (예: 과실(negligence))\n"
    "4. 원본 내용과 구조 최대한 보존\n"
    "5. 정제된 텍스트만 출력 (설명 없이)\n\n"
    "텍스트:\n"
)

def call_exaone(text: str) -> str:
    if len(text) < 50:
        return text
    prompt = CLEAN_PROMPT + text[:2000]
    payload = json.dumps({
        'model': MODEL, 'prompt': prompt, 'stream': False,
        'options': {'temperature': 0.1, 'num_predict': 2000},
    }).encode('utf-8')
    req = urllib.request.Request(
        OLLAMA_URL, data=payload,
        headers={'Content-Type': 'application/json'}, method='POST',
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        resp = json.loads(r.read())
    result = resp.get('response', '').strip()
    result = re.sub(r'^(?:정제된\s*텍스트[:：]?\s*|수정된\s*텍스트[:：]?\s*)', '', result).strip()
    return result if result else text

# ── 토픽 감지 ─────────────────────────────────────────────────────
def detect_topic(text: str) -> str | None:
    low = text.lower()
    for topic, keys in TOPIC_KEYS:
        if any(k.lower() in low for k in keys):
            return topic
    return None

def topic_to_cl(topic: str) -> str | None:
    for cl, topics in CL_MAP.items():
        if topic in topics:
            return cl
    return None

# ── 섹션 분리 + 파싱 ──────────────────────────────────────────────
def parse_file(filepath: str, lang: str, use_llm: bool, target_cl: str | None) -> dict:
    """파일 → {cl: {topic: [text, ...]}} 구조"""
    with open(filepath, encoding='utf-8') as f:
        raw = f.read()

    sections = re.split(r'\n(?=## )', raw)
    result = {f'cl{i}': {} for i in range(1, 9)}
    stats = {'total': len(sections), 'matched': 0, 'skipped': 0}

    for i, sec in enumerate(sections, 1):
        topic = detect_topic(sec)
        if not topic:
            stats['skipped'] += 1
            continue
        cl = topic_to_cl(topic)
        if not cl:
            stats['skipped'] += 1
            continue
        if target_cl and cl != target_cl:
            continue

        # 기본 정제
        cleaned = basic_clean(sec)
        if len(cleaned) < 80:
            continue  # 너무 짧은 섹션 무시

        # LLM 정제
        if use_llm:
            print(f'  [{i:3d}/{stats["total"]}] {lang} {cl}/{topic} LLM 정제...', end=' ', flush=True)
            try:
                cleaned = call_exaone(cleaned)
                print(f'✓ ({len(cleaned)}자)')
                time.sleep(0.3)
            except Exception as e:
                print(f'✗ {e}')
        else:
            print(f'  [{i:3d}/{stats["total"]}] {lang} {cl}/{topic} ({len(cleaned)}자)')

        if topic not in result[cl]:
            result[cl][topic] = []
        result[cl][topic].append(cleaned)
        stats['matched'] += 1

    print(f'  → {lang}: {stats["matched"]}/{stats["total"]}개 매핑 ({stats["skipped"]}개 스킵)')
    return result

# ── 병합: 같은 cl+topic의 텍스트를 하나로 합침 ────────────────────
def merge_sections(data: dict) -> dict:
    merged = {}
    for cl, topics in data.items():
        merged[cl] = {}
        for topic, texts in topics.items():
            # 중복 제거 후 합치기
            seen = set()
            unique = []
            for t in texts:
                key = t[:100]
                if key not in seen:
                    seen.add(key)
                    unique.append(t)
            merged[cl][topic] = '\n\n---\n\n'.join(unique)
    return merged

# ── 메인 ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='KTK 파서')
    parser.add_argument('--no-llm', action='store_true', help='EXAONE 정제 스킵')
    parser.add_argument('--cl', default=None, help='특정 챕터만 (cl1~cl8)')
    args = parser.parse_args()

    use_llm = not args.no_llm
    target_cl = args.cl

    if use_llm:
        try:
            urllib.request.urlopen('http://192.168.0.141:11434/api/tags', timeout=5)
            print(f'✅ Ollama 연결 확인 ({MODEL})')
        except Exception as e:
            print(f'❌ Ollama 연결 실패: {e}')
            print('   --no-llm 옵션으로 정제 없이 실행하세요')
            sys.exit(1)

    # 기존 데이터 로드 (재시작 시 이어쓰기)
    try:
        existing = json.load(open(OUT_FILE, encoding='utf-8'))
        print(f'기존 데이터 로드: {OUT_FILE}')
    except FileNotFoundError:
        existing = {'ko': {}, 'en': {}}

    print(f'\n── 한글 파일 파싱 ──')
    ko_raw = parse_file(KO_FILE, 'KO', use_llm, target_cl)
    ko_merged = merge_sections(ko_raw)

    print(f'\n── 영문 파일 파싱 ──')
    en_raw = parse_file(EN_FILE, 'EN', use_llm, target_cl)
    en_merged = merge_sections(en_raw)

    # 기존 데이터와 병합
    for cl in [f'cl{i}' for i in range(1, 9)]:
        if cl not in existing['ko']:
            existing['ko'][cl] = {}
        if cl not in existing['en']:
            existing['en'][cl] = {}
        for topic, text in ko_merged.get(cl, {}).items():
            if target_cl and cl != target_cl:
                continue
            existing['ko'][cl][topic] = text
        for topic, text in en_merged.get(cl, {}).items():
            if target_cl and cl != target_cl:
                continue
            existing['en'][cl][topic] = text

    json.dump(existing, open(OUT_FILE, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    print(f'\n✅ 파싱 완료: {OUT_FILE}')
    print('\n=== 결과 요약 ===')
    for cl in [f'cl{i}' for i in range(1, 9)]:
        ko_topics = list(existing['ko'].get(cl, {}).keys())
        en_topics = list(existing['en'].get(cl, {}).keys())
        label = CL_LABELS.get(cl, cl)
        print(f'{cl} ({label[:30]}):')
        print(f'  KO: {ko_topics}')
        print(f'  EN: {en_topics}')

    print('\n다음 단계: python F:\\mbe\\_build\\builder_v8.py')


if __name__ == '__main__':
    main()
