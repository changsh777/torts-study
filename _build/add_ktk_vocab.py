import sys, re
sys.stdout.reconfigure(encoding='utf-8')

# ── vocab tag CSS ──
VOCAB_CSS = """
/* KTK 문제별 어휘 태그 */
.ktk-vt-wrap{margin-top:.6rem;border-top:1px dashed #d0b8f0;padding-top:.45rem;display:flex;flex-wrap:wrap;gap:.3rem;align-items:center;}
.ktk-vt-lbl{font-size:.62rem;font-weight:700;color:#7a5c00;background:#fdf6e3;padding:.15rem .45rem;border-radius:3px;white-space:nowrap;}
.ktk-vt{font-size:.72rem;border:1px solid #c5cae9;border-radius:12px;padding:.15rem .55rem;cursor:pointer;background:#f5f5ff;position:relative;user-select:none;}
.ktk-vt:hover{background:#e8eaff;}
.ktk-vt-ko{color:#555;margin-left:.25rem;}
.ktk-vt-def{display:none;position:absolute;bottom:calc(100% + 4px);left:0;background:#fff;border:1px solid #c5cae9;border-radius:6px;padding:.4rem .6rem;font-size:.72rem;line-height:1.5;color:#222;z-index:99;min-width:200px;max-width:280px;box-shadow:0 2px 8px rgba(0,0,0,.12);}
.ktk-vt.open .ktk-vt-def{display:block;}
"""

# ── vocab word definitions (word, korean, definition) ──
VOCAB = {
    'taunting/heckler': ('야유·조롱 / 야유꾼', '조롱하기·야유하기. "heckler"(야유꾼)와 세트. Dylan Q24: 의도(intent)는 해를 입히려는 게 아니라 접촉 행위의 의도만 있으면 OK.'),
    'imminent': ('임박한, 즉각적인', '"I\'ll hurt you tomorrow" ≠ imminent. 지금 당장(now)이어야 assault 성립. 미래 협박은 해당 없음.'),
    'apprehension': ('두려움, 우려', 'Assault 핵심 요건. 실제 두려움이 아니라 합리적인 심리적 인식(reasonable apprehension)이면 충분.'),
    'provocation': ('도발, 자극', '"without any provocation" = D가 먼저 자극한 게 아님. 시험에서 \'아무 이유 없이\'를 나타내는 표현.'),
    'hallucination': ('환각, 환청', '정신질환 + 환각 → 의도(intent) 항변? NO. 불법행위법에서 정신질환은 원칙적으로 방어사유 불인정.'),
    'encroachment': ('(경계선) 침범', '재산 경계를 넘어 구조물 설치 = trespass. 경계선을 몰랐어도 의도적으로 그 위치에 지었으면 intent 성립.'),
    'ordinance': ('조례 (지방 법령)', '지자체가 만든 규정. Negligence per se: 조례 위반 → 그 조례가 예방하려던 피해 + 보호 대상 원고여야 성립.'),
    'foreseeable': ('예견 가능한', 'Proximate cause: 피해가 breach의 예견 가능한 결과여야 함. 예견 불가능 → superseding cause → proximate cause 단절.'),
    'contemporaneously': ('동시에, 그 순간에', 'NIED bystander 3요건 중 하나. 사고 현장에서 "그 순간" 목격해야 함. 전화 통보 후 나중에 도착 = 불충족.'),
    'indivisible': ('불가분의', 'Joint & several liability 적용 조건. 여러 D의 과실이 하나의 나눌 수 없는 피해를 초래 → 각자 전액 책임.'),
    'insolvent': ('지급불능, 파산', '"Yes, only if County is insolvent" = 틀린 선지 패턴. J&S는 상대방 지급능력과 무관하게 전액 청구 가능.'),
    'altercation': ('언쟁, 몸싸움', '구두 다툼~신체 충돌 포함. 고용주 대위책임: intentional tort도 scope of employment 내이면 성립 가능.'),
    'vicarious liability': ('대위/간접 책임', 'Respondeat superior: 고용인이 업무 범위 내에서 한 불법행위 → 고용주 책임. "업무 범위" 여부가 핵심.'),
    'scope of employment': ('업무 범위', '고용인의 행위가 업무 목적·수행 중이어야 함. Frolic(완전 이탈) = X. Detour(소폭 이탈) = O.'),
    'anesthetized': ('마취된', '수술 동의는 범위가 있음. Medic 동의 → Surgeon 집도 = consent 범위 초과 → battery. 결과가 좋아도 consent 없으면 battery.'),
    'privity': ('계약 당사자 관계', 'Strict products liability: privity 불요. 제조자→유통→판매자 어디서나 고소 가능. 최종 구매자가 아닌 Annie도 제소 가능.'),
    'defamatory': ('명예훼손적인', '진술이 합리적 제3자 기준으로 P의 평판을 해치면 defamatory. 1가지 해석만 → 법원이 law 문제로 판단.'),
    'appropriation': ('성명·초상 도용', '동의 범위를 초과한 상업적 사용. 사진 촬영 동의 ≠ 광고 사용 동의. Privacy tort 4가지 중 하나.'),
    'invitee': ('초대 방문자 (상업적)', '가장 높은 주의의무. 검사(inspect) + 경고(warn) 의무. 최초 무단침입자도 점원이 존재 허락 → invitee 지위로 전환.'),
    'malfunction / defect': ('오작동 / 결함', 'Manufacturing defect: 특정 제품이 설계와 다름. Design defect: 전 제품라인 위험 → RAD 필요. Failure to warn: 경고 부재.'),
    'negligently': ('부주의하게, 과실로', '"George was driving negligently" = 과실 운전. 상대방 과실이 있어도 negligence per se 분석은 별개 (ordinance 목적 기준).'),
    'verdict / JNOV': ('평결 / 평결불구판결', 'JNOV: 합리적 배심원이 그 결론에 도달할 수 없을 때만 인용. 증거가 있으면 배심원 평결 존중 → JNOV 기각.'),
}

def make_tag(key):
    ko, defn = VOCAB[key]
    safe_defn = defn.replace("'", "&#39;").replace('"', '&quot;')
    return (f'<span class="ktk-vt" onclick="this.classList.toggle(\'open\')">'
            f'<strong>{key}</strong><span class="ktk-vt-ko">{ko}</span>'
            f'<span class="ktk-vt-def">{defn}</span></span>')

def wrap_tags(words):
    tags = ''.join(make_tag(w) for w in words if w in VOCAB)
    return (f'\n<div class="ktk-vt-wrap"><span class="ktk-vt-lbl">📌 어휘</span>'
            f'{tags}</div>')

# ── problem → vocab mapping (by answer badge text as anchor) ──
# Each entry: (unique text in explain, vocab word list)
PROBLEM_VOCAB = [
    # Q24 Dylan battery
    ('Dylan deliberately threw the ball', ['taunting/heckler', 'imminent']),
    # Q33 George/Paula transferred intent
    ('George need not have intended to shoot Paula', ['provocation']),
    # Q37 Pamela/Davis hallucination
    ('Mental illness is generally not a defense', ['hallucination', 'provocation']),
    # Q23 Phill assault
    ("Dacty's conditional threat created a reasonable apprehension", ['apprehension', 'imminent']),
    # Q39 Daniel trespass to land
    ('Daniel intentionally built the garage at that location', ['encroachment']),
    # Q45 David parents
    ('David\'s parents would be liable for Paul\'s injury if they knew', ['foreseeable']),
    # Q25 Donna ordinance
    ('fire hydrant ordinance is designed to ensure fire hydrant access', ['ordinance', 'negligently']),
    # Q47 Darcy JNOV
    ('enough evidence in favor of Darcy which demonstrates', ['verdict / JNOV']),
    # Q46 Helen NIED
    ('she did not witness the accident contemporaneously', ['contemporaneously']),
    # Q55 Parker joint liability
    ('Parker may collect the entire $100,000 from Trainco alone', ['indivisible', 'insolvent']),
    # Q75 blender
    ('The consumer does not need to prove that Omega Plus was negligent', ['malfunction / defect']),
    # Q101 tractor auctioneer
    ('auctioneer is not in the business of selling tractors', ['privity']),
    # Q34 Jack defamation
    ('negligent publication element would be satisfied', ['defamatory']),
    # Q105 Actress appropriation
    ('Actress consented only to being photographed', ['appropriation']),
    # Q32 premises invitee
    ('his status changed to an invitee', ['invitee']),
    # Q63 Miller respondeat
    ('unprovoked intentional battery arising from a seating dispute', ['altercation', 'vicarious liability', 'scope of employment']),
    # Q104 Player consent
    ('The scope of Player\'s consent did not extend to Surgeon', ['anesthetized']),
]

with open(r'F:\mbe\index.html', encoding='utf-8') as f:
    content = f.read()

# ── 1. Add CSS ──
css_anchor = '/* KTK 교재 이론 섹션 */'
count = content.count(css_anchor)
print(f'CSS anchor: {count}')
if count == 1:
    content = content.replace(css_anchor, VOCAB_CSS + '\n' + css_anchor)
    print('CSS inserted')

# ── 2. Add vocab tags to each problem ──
inserted = 0
for anchor_text, words in PROBLEM_VOCAB:
    tag_html = wrap_tags(words)
    # Find the explain div containing this text, insert before its closing </div>
    # Pattern: anchor_text ... </div>\n</div>\n</div> (exp-text div → explain div → card div)
    idx = content.find(anchor_text)
    if idx == -1:
        print(f'WARN: not found: {anchor_text[:40]}')
        continue
    # Find the ktk-prac-exp-text closing div after this anchor
    close_search = content.find('</div>\n</div>\n</div>', idx)
    if close_search == -1:
        print(f'WARN: closing not found after: {anchor_text[:40]}')
        continue
    # Insert vocab tags right before the triple-close
    insert_pos = close_search
    # Check if vocab tag already there
    if content[max(0,insert_pos-20):insert_pos+5].find('ktk-vt-wrap') != -1:
        print(f'SKIP (already done): {anchor_text[:40]}')
        continue
    content = content[:insert_pos] + tag_html + '\n' + content[insert_pos:]
    inserted += 1
    print(f'OK: {anchor_text[:40]}')

print(f'\nTotal inserted: {inserted}')

with open(r'F:\mbe\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('DONE')
