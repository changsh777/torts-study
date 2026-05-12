"""
ktk_prac_parser.py — KTK 문제풀이 txt → ktk_prac_data.json 파서 (완전 재작성)

입력: F:\mbe\KTK\torts문제풀이_교정_dify.fixed.txt
출력: F:\mbe\_extracted\ktk_prac_data.json

구조:
  {
    "battery": [{"q_num":24, "q_text":"...", "options":[...], "correct_answer":"D", "explanation":"..."}, ...],
    "assault":  [...],
    ...
  }
"""
import re, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

SRC = r'F:\mbe\KTK\torts문제풀이_교정_dify.fixed.txt'
OUT = r'F:\mbe\_extracted\ktk_prac_data.json'

# ── Q번호 → 토픽 매핑 ────────────────────────────────────────
TOPIC_MAP = {
    23:  'assault',
    24:  'battery',
    25:  'negligence_general',
    32:  'duty_premises',
    33:  'battery',           # transferred intent
    34:  'defamation',
    37:  'battery',           # intentionally ill
    39:  'trespass_land',
    45:  'negligence_duty',
    46:  'defenses_neg',
    47:  'negligence_general',
    55:  'defenses_neg',
    63:  'respondeat',
    75:  'products_liability',
    101: 'products_liability',
    104: 'consent',
    105: 'privacy',
}

# ─────────────────────────────────────────────────────────────
# 헬퍼: 옵션 파싱
# ─────────────────────────────────────────────────────────────

def parse_options(body):
    """body 에서 (A)...(D) 옵션 추출. (q_text, options) 반환"""
    first_opt = re.search(r'^\([A-D]\)', body, re.MULTILINE)
    if first_opt:
        q_text   = body[:first_opt.start()].strip()
        opt_body = body[first_opt.start():]
    else:
        return body.strip(), []

    opt_pattern = re.compile(
        r'^\(([A-D])\)\s*(.*?)(?=^\([A-D]\)|\Z)',
        re.MULTILINE | re.DOTALL
    )
    options = []
    for mo in opt_pattern.finditer(opt_body):
        label    = mo.group(1)
        opt_text = mo.group(2).strip().replace('\n', ' ')
        opt_text = re.sub(r'  +', ' ', opt_text)
        options.append({'label': label, 'text': opt_text})
    return q_text, options


# ─────────────────────────────────────────────────────────────
# 1단계: ## [torts] Question N ... ***** 블록 파싱
# ─────────────────────────────────────────────────────────────

def parse_star_blocks(text):
    """
    ## [torts] Question N 헤더 + ***** 구분자 블록에서
    팩트패턴 + MCQ 추출.
    반환: {q_num: {'q_text': str, 'options': list}}
    """
    sections = text.split('*****')
    result = {}
    for sec in sections:
        m = re.search(r'## \[torts\] Question (\d+)', sec)
        if not m:
            continue
        q_num = int(m.group(1))
        body  = sec[m.end():].strip()
        # 메타 줄 제거
        body = re.sub(r'키워드:[^\n]*\n?', '', body)
        body = re.sub(r'출처:[^\n]*\n?', '', body)
        body = re.sub(r'\[문제\s*\d+\]\s*\n?', '', body)
        body = re.sub(r'^Ques(?:e?t?i?o?n?|ton)\s+\d+[^\n]*\n?', '', body,
                      flags=re.IGNORECASE | re.MULTILINE)
        body = body.strip()

        q_text, options = parse_options(body)

        # Q32, Q35처럼 OCR 깨진 경우: 옵션 없어도 일단 저장
        if q_text or options:
            result[q_num] = {'q_text': q_text, 'options': options}
    return result


# ─────────────────────────────────────────────────────────────
# 2단계: **[문제 N]** --- 블록 파싱 (섹션 4)
# ─────────────────────────────────────────────────────────────

def parse_bold_blocks(text):
    """
    **[문제 N]** 형식 팩트패턴 블록 추출.
    --- 구분자로 블록 분리.
    반환: {q_num: {'q_text': str, 'options': list}}
    """
    result = {}
    # --- 구분자로 분리
    chunks = re.split(r'\n---+\n', text)
    for chunk in chunks:
        chunk = chunk.strip()
        m = re.match(r'\*\*\[문제\s*(\d+)\]\*\*', chunk)
        if not m:
            continue
        q_num = int(m.group(1))

        # Q33: 파일의 **[문제 33]** 블록은 잘못 레이블된 내용 — 수동 보완 사용
        if q_num == 33:
            continue

        body  = chunk[m.end():].strip()
        # "Question N ..." 첫 줄 제거
        body = re.sub(r'^Question\s+\d+[^\n]*\n?', '', body,
                      flags=re.IGNORECASE)
        body = body.strip()

        # 해설 전용 블록 제외 (Correct/Incorrect/Court로 시작하는 경우)
        first_line = body.split('\n')[0].strip() if body else ''
        if re.match(r'^\([A-D]\)\s*(Correct|Incorrect|Court|No,|Yes,)',
                    first_line, re.IGNORECASE):
            continue

        q_text, options = parse_options(body)
        if q_text or options:
            result[q_num] = {'q_text': q_text, 'options': options}
    return result


# ─────────────────────────────────────────────────────────────
# 3단계: **질문 N 교정된 버전:** 블록 파싱 (Q101, Q104, Q105)
# ─────────────────────────────────────────────────────────────

def parse_corrected_blocks(text):
    """
    **질문 N 교정된 버전:** 블록 파싱.
    반환: (fact_dict, exp_dict)
    """
    fact_result = {}
    exp_result  = {}

    block_re = re.compile(
        r'\*\*질문\s+(\d+)\s+교정된\s+버전:\*\*\s*\n(.*?)(?=\*\*질문\s+\d+\s+교정|\Z)',
        re.DOTALL
    )
    for m in block_re.finditer(text):
        q_num = int(m.group(1))
        body  = m.group(2).strip()

        if q_num == 101:
            # 해설만 (팩트패턴 없음)
            correct_m = re.search(
                r'^\(([A-D])\)\s*(?:Correct|Collect)\b', body,
                re.MULTILINE | re.IGNORECASE
            )
            correct_answer = correct_m.group(1) if correct_m else 'C'
            if correct_m:
                exp_start = correct_m.start()
                next_inc  = re.search(
                    r'^\([A-D]\)\s*Incorrect', body[exp_start:],
                    re.MULTILINE | re.IGNORECASE
                )
                exp_block = (body[exp_start: exp_start + next_inc.start()]
                             if next_inc else body[exp_start:])
                exp_block = re.sub(
                    r'^\([A-D]\)\s*(?:Correct|Collect)[.\s]*', '',
                    exp_block, flags=re.IGNORECASE
                )
                explanation = re.sub(r'  +', ' ',
                                     exp_block.strip().replace('\n', ' '))
            else:
                explanation = re.sub(r'  +', ' ',
                                     body.strip().replace('\n', ' '))
            exp_result[101] = {
                'correct_answer': correct_answer,
                'explanation': explanation
            }

        elif q_num in (104, 105):
            # 팩트패턴 + MCQ 포함
            q_text, options = parse_options(body)
            fact_result[q_num] = {'q_text': q_text, 'options': options}

    return fact_result, exp_result


# ─────────────────────────────────────────────────────────────
# 4단계: 해설 파싱
#   4a: "Question N (Simulated/Summarized/Simplified/문제 제기)" 형식
#   4b: "[문제 N]\n질문 N (시뮬레이션 질문)" 한글 형식
#   4c: "(C) No, unless..." 단독 라인 형식 (Q34)
# ─────────────────────────────────────────────────────────────

def extract_explanation(block, q_num):
    """
    블록에서 정답 + 해설 추출.
    returns {'correct_answer': str, 'explanation': str}
    """
    # 정답 패턴 — Correct / Collect / Court held / No, / Yes,
    correct_m = re.search(
        r'^\(([A-D])\)\s*(?:Correct|Collect|Court\s+held|No,|Yes,)',
        block, re.MULTILINE | re.IGNORECASE
    )
    if not correct_m:
        # 한글 "수집" 패턴
        correct_m = re.search(r'^\(([A-D])\)\s*수집', block, re.MULTILINE)

    correct_answer = correct_m.group(1) if correct_m else ''

    if correct_m:
        exp_start = correct_m.start()
        next_opt  = re.search(
            r'^\([A-D]\)\s*(?:Incorrect|오류|Incorrect\.)',
            block[exp_start:], re.MULTILINE | re.IGNORECASE
        )
        exp_block = (block[exp_start: exp_start + next_opt.start()]
                     if next_opt else block[exp_start:])
        # 첫 줄 정답 라벨 제거
        exp_block = re.sub(
            r'^\([A-D]\)\s*(?:Correct|Collect|Court\s+held|No,|Yes,|수집)[.\s]*',
            '', exp_block, flags=re.IGNORECASE
        )
        explanation = re.sub(r'  +', ' ',
                              exp_block.strip().replace('\n', ' '))
    else:
        explanation = re.sub(r'  +', ' ',
                              block.strip().replace('\n', ' '))[:1000]

    return {'correct_answer': correct_answer, 'explanation': explanation}


def parse_explanations(text):
    """
    영문 해설 블록 파싱 — "Question N (Simulated/Summarized/...)" 헤더 형식.
    반환: {q_num: {'correct_answer': str, 'explanation': str}}
    """
    result = {}
    header_re = re.compile(
        r'Question\s+(\d+)\s*\([^)]*(?:Simulated|Summarized|Simplified|문제 제기)[^)]*\)',
        re.IGNORECASE
    )
    matches = list(header_re.finditer(text))
    for i, m in enumerate(matches):
        q_num = int(m.group(1))
        end   = matches[i+1].start() if i+1 < len(matches) else len(text)
        block = text[m.end():end].strip()
        result[q_num] = extract_explanation(block, q_num)
    return result


def parse_ko_explanations(text):
    """
    한글 해설 블록 파싱 — "[문제 N]\n질문 N (시뮬레이션 질문)" 형식.
    반환: {q_num: {'correct_answer': str, 'explanation': str}}
    """
    result = {}
    ko_re  = re.compile(
        r'\[문제\s*(\d+)\]\s*\n질문\s+\d+\s*\([^)]*시뮬레이션[^)]*\)'
    )
    matches = list(ko_re.finditer(text))
    for i, m in enumerate(matches):
        q_num = int(m.group(1))
        end   = matches[i+1].start() if i+1 < len(matches) else len(text)
        block = text[m.end():end].strip()
        result[q_num] = extract_explanation(block, q_num)
    return result


def parse_q34_explanation(text):
    """
    Q34: "(C) No, unless Jack should have reasonably foreseen..." 단독 라인.
    반환: {34: {'correct_answer': 'C', 'explanation': str}}
    """
    m = re.search(
        r'^\(([A-D])\)\s*(No,\s+unless\s+Jack[^\n]+)',
        text, re.MULTILINE
    )
    if m:
        return {34: {
            'correct_answer': m.group(1),
            'explanation': m.group(2).strip()
        }}
    return {}


# ─────────────────────────────────────────────────────────────
# 수동 보완 데이터 (파일에서 추출 불가한 항목)
# ─────────────────────────────────────────────────────────────

# Q23 — assault
Q23_FACT = {
    'q_text': (
        "Phill was the prominent plant manager for a corporation. Phill had received "
        "significant feedback from suppliers for every contract they had entered into. "
        "Daily, the president of the corporation found out about the feedback and fired "
        "Phill on the spot yelling 'Get out of this building! If I see you here in ten "
        "minutes I'll have the security force you out.' Phill left immediately. "
        "If Phill sues Dacty for assault, would Phill succeed?"
    ),
    'options': [
        {'label': 'A', 'text': 'No, because the guards never touched Phill.'},
        {'label': 'B', 'text': 'No, because Dacty gave Phill ten minutes to leave.'},
        {'label': 'C', 'text': 'Yes, if Dacty intended to cause Phill severe emotional distress.'},
        {'label': 'D', 'text': 'Yes, because Dacty threatened Phill with a hint of offensive bodily contact.'},
    ]
}
Q23_EXP = {
    'correct_answer': 'D',
    'explanation': (
        'Assault is an intentional act that creates a reasonable apprehension of '
        'imminent harmful or offensive contact. The defendant\'s words "I\'ll have the '
        'security force you out" combined with the time constraint created an immediate '
        'threat of offensive bodily contact. The assault does not require actual physical '
        'contact — the apprehension itself is sufficient. Therefore, Phill can succeed '
        'because Dacty\'s conditional threat created a reasonable apprehension of '
        'imminent offensive contact by the security force.'
    )
}

# Q24 — battery (해설만 수동 보완)
Q24_EXP = {
    'correct_answer': 'D',
    'explanation': (
        'Battery is the intentional infliction of harmful or offensive contact with '
        'the plaintiff\'s person. Intent for battery requires only that the defendant '
        'intended the act that caused the contact, not that defendant intended harm. '
        'Dylan intentionally threw the ball at the hecklers — even if he did not expect '
        'the ball to pass through the fence, a jury could find that his conduct of '
        'deliberately throwing toward the crowd was extreme and outrageous, and caused '
        'physical harm to Paoloxa. Therefore, the directed verdict in favor of Dylan '
        'should be reversed and remanded for jury determination.'
    )
}

# Q25 — negligence_general (해설만 수동 보완)
Q25_EXP = {
    'correct_answer': 'D',
    'explanation': (
        'Negligence per se applies when a statute is violated and: (1) the plaintiff is '
        'in the class the statute was designed to protect, and (2) the harm suffered is '
        'the type the statute was designed to prevent. A fire hydrant ordinance is designed '
        'to ensure fire hydrant access for firefighting — not to prevent traffic accidents. '
        'Paul was injured in a car collision, not a fire. Therefore, Donna\'s violation '
        'does not constitute negligence per se because preventing traffic accidents was '
        'not the purpose of the parking ordinance near fire hydrants.'
    )
}

# Q32 — duty_premises (OCR 깨짐 — 팩트패턴 손상)
Q32_FACT = {
    'q_text': '(팩트패턴 원문 손상 — 해설 참조)',
    'options': []
}
Q32_EXP = {
    'correct_answer': 'D',
    'explanation': (
        'An invitee is a person who enters onto defendant\'s land with express or implied '
        'invitation for a purpose relating to defendant\'s interests or activities, or '
        'where the land is held open to the public. Land possessors owe a duty to exercise '
        'reasonable care to prevent injuries to invitees and to inspect for hidden dangers. '
        'Although Peter initially trespassed when he entered the No Admittance area, the '
        'clerk consented to his presence, changing his status to an invitee. Therefore, '
        'Discount Store is vicariously liable for failure to exercise reasonable care.'
    )
}

# Q34 — defamation (팩트패턴 수동 보완)
Q34_FACT = {
    'q_text': (
        'Jack made a statement about his neighbor Tom at a private gathering. '
        'He did not intend for the statement to be overheard by others. However, '
        'a third party at the gathering overheard the statement and repeated it. '
        'If Tom sues Jack for defamation, will Tom prevail?'
    ),
    'options': [
        {'label': 'A', 'text': 'Yes, because the statement was defamatory per se.'},
        {'label': 'B', 'text': 'Yes, because the statement was published.'},
        {'label': 'C', 'text': 'No, unless Jack should have reasonably foreseen that his statement would be overheard by another person.'},
        {'label': 'D', 'text': 'No, because Tom was not present when the statement was made.'},
    ]
}
Q34_EXP = {
    'correct_answer': 'C',
    'explanation': (
        'Defamation requires: (1) a defamatory statement, (2) of or concerning plaintiff, '
        '(3) publication to a third party, (4) damage to reputation. Publication means '
        'intentional or negligent communication to a third party. If Jack did not intend '
        'for the statement to be overheard and could not reasonably foresee it would be, '
        'the publication element is not satisfied. Therefore, Tom can only prevail if '
        'Jack should have reasonably foreseen that the statement would be overheard.'
    )
}

# Q33 — battery: transferred intent (팩트패턴 수동 보완)
# 파일의 **[문제 33]** 블록은 잘못 레이블된 다른 문제의 내용임
Q33_FACT = {
    'q_text': (
        'George and Kyle were rivals who had a long-standing dispute. One day, George '
        'spotted Kyle on a crowded street and, intending to shoot Kyle, fired his gun. '
        'The bullet missed Kyle and instead struck Paula, an innocent bystander. '
        'Paula sues George for battery. Will Paula prevail?'
    ),
    'options': [
        {'label': 'A', 'text': "No, because Paula is not Kyle's accomplice."},
        {'label': 'B', 'text': "No, because George was acting in self-defense."},
        {'label': 'C', 'text': 'Yes, because under the transferred intent doctrine, George\'s intent to shoot Kyle transfers to Paula.'},
        {'label': 'D', 'text': 'No, because George did not intend to shoot Paula.'},
    ]
}
Q33_EXP_SUPP = {
    'correct_answer': 'C',
    'explanation': (
        'Battery is the intentional infliction of harmful or offensive contact with '
        'plaintiff\'s person. Under the transferred intent doctrine, intent may be '
        'transferred when defendant intends to commit battery but results in injuring an '
        'unintended victim. George intended to shoot Kyle — that intent transfers to Paula. '
        'Therefore, George is liable to Paula for battery even though he did not intend '
        'to shoot her, as long as he intended to shoot Kyle.'
    )
}

# Q37 — battery: intentionally ill (해설 수동 보완)
Q37_EXP = {
    'correct_answer': 'A',
    'explanation': (
        'Battery is the intentional infliction of harmful or offensive contact. '
        'The intent required is the intent to cause the contact — not intent to cause harm. '
        'Mental illness is generally not a defense to intentional torts in tort law. '
        'Davis\'s strongest defense is (A) that he did not understand his act was wrongful. '
        'While wrongfulness is technically irrelevant to battery intent under majority rule, '
        'on the MBE the "did not understand wrongful" framing is the recognized strongest '
        'defense for a mentally ill defendant — it directly attacks the volitional intent element '
        'most favorable to Davis given that (B) and (C) are factually unsupported (Davis did '
        'pick up a brick and intentionally struck Pamela), and (D) requires a reasonable belief '
        'of imminent attack which is not supported on these facts.'
    )
}

# Q39 — trespass_land (해설 수동 보완)
Q39_EXP = {
    'correct_answer': 'C',
    'explanation': (
        'Trespass to land requires: (1) a physical intrusion onto plaintiff\'s land, '
        '(2) intent to be on the land (not necessarily knowing it is another\'s), and '
        '(3) causation. The intent required is merely the intent to place the structure '
        'where it was placed — not intent to trespass. The fact that Daniel did not know '
        'the garage crossed the property line is irrelevant. Daniel intentionally built '
        'the garage at that location, so the trespass intent element is satisfied. '
        'Pamela succeeds because Daniel intentionally placed the garage there, regardless '
        'of whether he knew exactly where the property line was.'
    )
}

# Q45 — negligence_duty (팩트패턴 + 해설 수동 보완)
Q45_FACT = {
    'q_text': (
        'David, a teenager, had recently expressed to his parents that he intended '
        'to run out into traffic on the highway to harm himself. His parents did not take '
        'any steps to prevent him from leaving the house. David did run into the highway '
        'and was struck by a car driven by Paul, injuring Paul. Paul sues David\'s parents. '
        'Under which circumstances would David\'s parents be liable for Paul\'s injuries?'
    ),
    'options': [
        {'label': 'A', 'text': "If David's parents were negligent per se in failing to supervise their child."},
        {'label': 'B', 'text': 'If Paul suffered emotional distress from witnessing the accident.'},
        {'label': 'C', 'text': "If David's parents knew or should have known of the danger David posed to third persons and failed to exercise reasonable care to prevent it."},
        {'label': 'D', 'text': "If David's parents are vicariously liable for all of David's intentional torts as his guardians."},
    ]
}
Q45_EXP = {
    'correct_answer': 'C',
    'explanation': (
        'Although one generally has no duty to prevent another from injuring a third person, '
        'certain special relationships create such a duty — including parent-child, '
        'employer-employee, custodian-ward, and psychiatrist-patient. A parent who knew or '
        'should have known of the danger their child poses to a third person must exercise '
        'reasonable care to prevent the injury. Here, David\'s parents knew he intended to '
        'run into traffic. Therefore, they are liable to Paul if they knew of the danger '
        'and failed to take reasonable steps to prevent it.'
    )
}

# Q46 — defenses_neg / NIED bystander (팩트패턴 수동 보완)
Q46_FACT = {
    'q_text': (
        'Helen was at home when she received a phone call informing her that her son '
        'had just been struck by a negligently driven car outside their neighborhood. '
        'Helen rushed to the scene but arrived after the accident had occurred. '
        'Helen suffered severe emotional distress upon seeing her injured son. '
        'If Helen brings a claim for negligent infliction of emotional distress (NIED) '
        'against the driver, will Helen prevail?'
    ),
    'options': [
        {'label': 'A', 'text': 'Yes, because Helen suffered severe emotional distress.'},
        {'label': 'B', 'text': 'Yes, because Helen has a close familial relationship with the victim.'},
        {'label': 'C', 'text': 'No, because Helen did not witness the accident contemporaneously at the scene.'},
        {'label': 'D', 'text': 'No, because Helen was outside the zone of danger and does not satisfy bystander theory prerequisites.'},
    ]
}
Q46_EXP = {
    'correct_answer': 'D',
    'explanation': (
        'Negligent infliction of emotional distress (NIED) under the bystander theory '
        'requires plaintiff to: (1) be located near the scene of the accident, (2) suffer '
        'severe emotional distress, and (3) have a close relationship with the victim. '
        'Additionally, plaintiff must have directly witnessed the accident (not merely '
        'its aftermath). Helen was at home during the accident — outside the zone of danger '
        '— and did not witness it contemporaneously. Therefore, Helen does not satisfy '
        'the bystander theory prerequisites and cannot recover for NIED.'
    )
}

# Q47 — negligence_general / JNOV (팩트패턴 수동 보완)
Q47_FACT = {
    'q_text': (
        'Darcy parked her car on a street at night. She testified she did not park '
        'negligently and introduced evidence that juveniles had been seen tampering '
        'with cars in the neighborhood. Peter was injured when he tripped over Darcy\'s '
        'car in the dark. The jury returned a verdict for Darcy. Peter moves for a '
        'judgment notwithstanding the verdict (JNOV), arguing no reasonable jury could '
        'have found for Darcy. Should the court grant the JNOV?'
    ),
    'options': [
        {'label': 'A', 'text': "Yes, because Darcy's negligent parking was the legal cause of Peter's injuries."},
        {'label': 'B', 'text': "Yes, because the evidence of juvenile tampering was insufficient to excuse Darcy's negligence."},
        {'label': 'C', 'text': 'No, because there was sufficient evidence in favor of Darcy for a reasonable jury to reach its verdict.'},
        {'label': 'D', 'text': 'No, because Darcy was in a better position than Peter to explain the accident.'},
    ]
}
Q47_EXP = {
    'correct_answer': 'C',
    'explanation': (
        'A judgment notwithstanding the verdict (JNOV / judgment as a matter of law) '
        'is appropriate only when no reasonable jury could have reached the verdict. '
        'To establish negligence, plaintiff must prove: duty, breach, causation, and damages. '
        'Here, Darcy testified she did not park negligently and introduced evidence of '
        'juvenile tampering. This evidence was sufficient for a reasonable jury to find '
        'in Darcy\'s favor — the JNOV should be denied.'
    )
}

# Q55 — defenses_neg / joint & several (팩트패턴 수동 보완)
Q55_FACT = {
    'q_text': (
        'Parker was injured in an accident caused by the combined negligence of '
        'Trainco and County. The jury found Parker\'s damages to be $100,000, '
        'and apportioned fault at 60% to Trainco and 40% to County. '
        'Under joint and several liability, Parker seeks to recover the full '
        '$100,000 from Trainco alone. May Parker recover the full amount from Trainco?'
    ),
    'options': [
        {'label': 'A', 'text': 'Yes, because under joint and several liability, each tortfeasor is liable for the full amount of damages.'},
        {'label': 'B', 'text': 'Yes, but only if County is insolvent.'},
        {'label': 'C', 'text': 'No, because Parker can only recover from each defendant in proportion to their fault.'},
        {'label': 'D', 'text': 'No, because joint and several liability only applies when defendants acted in concert.'},
    ]
}
Q55_EXP = {
    'correct_answer': 'A',
    'explanation': (
        'Under joint and several liability, when multiple defendants\' negligence '
        'combines to cause a single indivisible injury, each defendant is liable '
        'for the full amount of plaintiff\'s damages. Parker can recover the full '
        '$100,000 from Trainco, leaving Trainco to seek contribution from County '
        'for County\'s 40% share. Comparative negligence affects the apportionment '
        'between defendants but does not limit plaintiff\'s right to recover the full '
        'amount from any one defendant under joint and several liability.'
    )
}

# Q63 — respondeat superior (팩트패턴 + 해설 수동 보완)
Q63_FACT = {
    'q_text': (
        'Miller, a flight attendant employed by Fly Airline, was involved in an '
        'altercation with a passenger during a flight. The altercation arose from '
        'a dispute over seating. Miller intentionally struck the passenger. '
        'The passenger sues both Miller and Fly Airline. '
        'Is Fly Airline liable for Miller\'s battery?'
    ),
    'options': [
        {'label': 'A', 'text': "Yes, because Miller was acting as Fly Airline's agent."},
        {'label': 'B', 'text': "Yes, because the incident occurred during the course of Miller's employment."},
        {'label': 'C', 'text': "No, unless Miller's use of force was within the scope of employment and for the employer's benefit."},
        {'label': 'D', 'text': 'No, because intentional torts can never be attributed to an employer.'},
    ]
}
Q63_EXP = {
    'correct_answer': 'C',
    'explanation': (
        'Under respondeat superior, an employer is vicariously liable for an employee\'s '
        'torts committed within the scope of employment. For intentional torts, an '
        'employer is liable only if the employee\'s conduct was within the scope of '
        'employment and at least partially motivated by a purpose to serve the employer. '
        'A flight attendant managing passenger disputes could fall within scope of '
        'employment, but an unprovoked intentional battery for personal reasons would '
        'not. Fly Airline is liable only if Miller\'s force was within the scope of '
        'employment and served the airline\'s interests.'
    )
}

# Q75 — products_liability / manufacturing defect (팩트패턴 + 해설 수동 보완)
Q75_FACT = {
    'q_text': (
        'A consumer purchased a blender manufactured by Omega Plus. While using '
        'the blender normally, the blade unexpectedly shattered, injuring the consumer. '
        'An investigation revealed that the specific blender had a metal defect in '
        'the blade introduced during the manufacturing process, though the design was '
        'otherwise sound. The consumer sues Omega Plus for strict products liability. '
        'Will the consumer prevail?'
    ),
    'options': [
        {'label': 'A', 'text': 'Yes, because the blender had a manufacturing defect that made it unreasonably dangerous.'},
        {'label': 'B', 'text': 'Yes, but only if the consumer can prove Omega Plus was negligent in its manufacturing process.'},
        {'label': 'C', 'text': 'No, because the design of the blender was not defective.'},
        {'label': 'D', 'text': 'No, because the consumer assumed the risk of using an electrical appliance.'},
    ]
}
Q75_EXP = {
    'correct_answer': 'A',
    'explanation': (
        'Under strict products liability (Restatement 2d, § 402A), a manufacturer who '
        'sells a product in a defective condition unreasonably dangerous to the user is '
        'strictly liable. A manufacturing defect exists when the product deviates from '
        'its intended design in a way that makes it unreasonably dangerous. Here, the '
        'blade had a metal defect introduced during manufacturing — even though the '
        'design was sound, this specific unit was defective. Strict liability does not '
        'require proof of negligence; therefore the consumer prevails.'
    )
}

# Q101 — products_liability / auctioneer (팩트패턴 수동 보완)
Q101_FACT = {
    'q_text': (
        'Player purchased a tractor at an auction conducted by an auctioneer. '
        'The tractor had a manufacturing defect that caused it to malfunction, '
        'injuring Player. The auctioneer regularly conducts auctions of various goods '
        'but is not in the business of selling tractors specifically. '
        'If Player brings a strict products liability claim against the auctioneer, '
        'will Player succeed?'
    ),
    'options': [
        {'label': 'A', 'text': 'Yes, because the auctioneer sold the defective tractor to Player.'},
        {'label': 'B', 'text': 'Yes, because the auctioneer was in the chain of distribution.'},
        {'label': 'C', 'text': 'No, because the auctioneer is not in the business of selling tractors and is not a proper defendant.'},
        {'label': 'D', 'text': "No, because the manufacturing defect was the manufacturer's fault, not the auctioneer's."},
    ]
}
Q101_EXP_SUPPLEMENT = {
    'correct_answer': 'C',
    'explanation': (
        'Under strict products liability, proper defendants include commercial suppliers '
        'at all levels of the distribution chain who are in the business of selling the '
        'product. An auctioneer who occasionally sells goods at auction but is not '
        'regularly in the business of selling tractors is not a proper defendant. '
        'Here, the auctioneer is not in the business of selling tractors — he merely '
        'facilitated the sale. Therefore, Player\'s strict liability claim against the '
        'auctioneer will fail.'
    )
}

# Q104 — consent (해설 수동 보완)
Q104_EXP = {
    'correct_answer': 'A',
    'explanation': (
        'Battery requires a harmful or offensive contact that is intentional. '
        'Consent is a defense to battery, but consent only covers the scope agreed to. '
        'Player consented to Medic performing the surgery, not Surgeon. '
        'The scope of Player\'s consent did not extend to Surgeon\'s performance of the '
        'operation. Therefore, Player prevails in the battery action against Surgeon '
        'because the contact exceeded the scope of Player\'s consent.'
    )
}

# Q105 — privacy / appropriation (해설 수동 보완)
Q105_EXP = {
    'correct_answer': 'D',
    'explanation': (
        'Appropriation (privacy tort) occurs when defendant uses plaintiff\'s name or '
        'likeness for commercial advantage without consent. Actress consented only to '
        'being photographed — not to use of the photo in commercial advertising. '
        'The photographer sold the photo to Winery without Actress\'s consent, and '
        'Winery used it in a national magazine advertisement. This constitutes '
        'appropriation unless Actress actually did enjoy Winery wine (which would imply '
        'an implied endorsement). Therefore, Actress prevails unless she did in fact '
        'enjoy Winery wine.'
    )
}


# ─────────────────────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────────────────────

def main():
    with open(SRC, 'r', encoding='utf-8') as f:
        raw = f.read()

    print(f'파일 로드: {len(raw)} 자')

    # 1단계: ***** 블록 파싱
    fact_stars = parse_star_blocks(raw)
    print(f'[1] ## 헤더 팩트패턴: {sorted(fact_stars.keys())}')

    # 2단계: **[문제 N]** 블록 파싱
    fact_bold = parse_bold_blocks(raw)
    print(f'[2] **[문제 N]** 팩트패턴: {sorted(fact_bold.keys())}')

    # 3단계: **질문 N 교정된 버전:** 파싱
    fact_corrected, exp_corrected = parse_corrected_blocks(raw)
    print(f'[3] 교정버전 팩트패턴: {sorted(fact_corrected.keys())}')
    print(f'[3] 교정버전 해설: {sorted(exp_corrected.keys())}')

    # 4단계: 해설 파싱
    exp_en = parse_explanations(raw)
    print(f'[4a] 영문 해설: {sorted(exp_en.keys())}')

    exp_ko = parse_ko_explanations(raw)
    print(f'[4b] 한글 해설: {sorted(exp_ko.keys())}')

    exp_q34 = parse_q34_explanation(raw)
    print(f'[4c] Q34 해설: {sorted(exp_q34.keys())}')

    # ── 팩트패턴 병합 (우선순위: stars > bold > corrected) ──
    all_facts = {}
    all_facts.update(fact_corrected)
    all_facts.update(fact_bold)
    all_facts.update(fact_stars)

    # ── 해설 병합 (우선순위: en > corrected > ko > q34) ──
    all_exps = {}
    all_exps.update(exp_ko)
    all_exps.update(exp_q34)
    all_exps.update(exp_corrected)
    all_exps.update(exp_en)  # 영문이 최우선

    # ── Q번호별 레코드 구성 ──
    q_records = {}

    # 파싱된 팩트패턴 적용
    for qn, fd in all_facts.items():
        q_records[qn] = {
            'q_num': qn,
            'q_text': fd['q_text'],
            'options': fd['options'],
            'correct_answer': '',
            'explanation': '',
        }

    # 파싱된 해설 적용
    for qn, ed in all_exps.items():
        if qn not in q_records:
            q_records[qn] = {
                'q_num': qn, 'q_text': '', 'options': [],
                'correct_answer': '', 'explanation': ''
            }
        q_records[qn]['correct_answer'] = ed['correct_answer']
        q_records[qn]['explanation']    = ed['explanation']

    # ── 수동 보완 fallback 적용 ──
    # (ff = fallback fact, fe = fallback explanation)
    fallbacks = {
        23:  (Q23_FACT,  Q23_EXP),
        24:  (None,      Q24_EXP),
        25:  (None,      Q25_EXP),
        32:  (Q32_FACT,  Q32_EXP),
        33:  (Q33_FACT,  Q33_EXP_SUPP),   # 파일 **[문제 33]** 내용은 오염 — 수동 보완
        34:  (Q34_FACT,  Q34_EXP),
        37:  (None,      Q37_EXP),
        39:  (None,      Q39_EXP),
        45:  (Q45_FACT,  Q45_EXP),
        46:  (Q46_FACT,  Q46_EXP),
        47:  (Q47_FACT,  Q47_EXP),
        55:  (Q55_FACT,  Q55_EXP),
        63:  (Q63_FACT,  Q63_EXP),
        75:  (Q75_FACT,  Q75_EXP),
        101: (Q101_FACT, Q101_EXP_SUPPLEMENT),
        104: (None,      Q104_EXP),
        105: (None,      Q105_EXP),
    }

    for qn, (ff, fe) in fallbacks.items():
        rec = q_records.get(qn, {
            'q_num': qn, 'q_text': '', 'options': [],
            'correct_answer': '', 'explanation': ''
        })
        # 팩트패턴 보완 (파싱 결과가 비어있을 때만)
        if ff and (not rec.get('q_text') or not rec.get('options')):
            rec['q_text']  = ff['q_text']
            rec['options'] = ff['options']
        # 해설 보완 (파싱 결과가 비어있을 때만)
        if fe:
            if not rec.get('explanation'):
                rec['explanation'] = fe['explanation']
            if not rec.get('correct_answer'):
                rec['correct_answer'] = fe['correct_answer']
        q_records[qn] = rec

    # ── Q3, Q35 스킵 (OCR 심하게 깨짐) ──
    skip_nums = {3, 35}

    # ── 토픽별 그루핑 ──
    topic_data = {}
    for qn, topic in TOPIC_MAP.items():
        if qn in skip_nums:
            print(f'  스킵 Q{qn} (OCR 손상)')
            continue
        if qn not in q_records:
            print(f'  ⚠ Q{qn} 레코드 없음 — 스킵')
            continue

        rec = q_records[qn]
        # 기본값 보장
        rec.setdefault('q_text', '')
        rec.setdefault('options', [])
        rec.setdefault('correct_answer', '')
        rec.setdefault('explanation', '')

        if topic not in topic_data:
            topic_data[topic] = []
        topic_data[topic].append(rec)

    # 토픽 내 정렬
    for topic in topic_data:
        topic_data[topic].sort(key=lambda r: r['q_num'])

    # ── 저장 ──
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(topic_data, f, ensure_ascii=False, indent=2)

    print(f'\n== 결과 요약 ==')
    total = 0
    for t, qs in sorted(topic_data.items()):
        nums = [q['q_num'] for q in qs]
        has_text  = sum(1 for q in qs if q['q_text'] and q['q_text'] != '(팩트패턴 원문 손상 — 해설 참조)')
        has_exp   = sum(1 for q in qs if q['explanation'])
        has_ans   = sum(1 for q in qs if q['correct_answer'])
        print(f'  {t}: {len(qs)}문제 Q{nums}  팩트패턴:{has_text}/{len(qs)}  해설:{has_exp}/{len(qs)}  정답:{has_ans}/{len(qs)}')
        total += len(qs)
    print(f'  총 {total}문제')
    print(f'\n저장 완료: {OUT}')


if __name__ == '__main__':
    main()
