"""
builder_v8.py — MBE Torts 단권화 v8
5-section 통합: 쉬운설명 + 이미지 + 개념설명 + 문제풀이 + IRAC Rule

원칙:
  - v4_base 콘텐츠 100% 유지 (SVG · 쉬운설명 · MCQ)
  - 개념설명: UDSL 슬라이드 raw 그대로 (환각 0)
  - Rule Statement: 김윤상 docx 그대로 (환각 0)
  - Class 1 먼저, 검수 후 2~8 추가
"""
import json, os, re, sys, base64, io
sys.stdout.reconfigure(encoding='utf-8')

try:
    from PIL import Image as PILImage
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

V4_BASE    = r'F:\mbe\_archive\Torts_단권화_v4_base.html'
IMG_CLS    = r'F:\mbe\_extracted\image_classification.json'
CURATED    = r'F:\mbe\_extracted\udsl_ppt'
RULES_PATH = r'F:\mbe\_extracted\torts_rules_raw.json'
OUT           = r'F:\mbe\Torts_단권화_v8.html'       # 내 것 (images/ 폴더 필요)
OUT_SHARE     = r'F:\mbe\Torts_단권화_v8_공유.html'  # 공유용 (단독 실행 파일)
IMG_DIR_SHARE = r'F:\mbe\images'

# IIED·Trespass는 슬라이드 추출 실패 → 교재(v4) 동일 케이스 직접 사용
FALLBACK_QUIZ = {
    'class01_iied_curated.json': {
        'q_ko_raw': '상관 Darla가 2개월에 걸쳐 팀 회의에서 부하직원 Evan의 말더듬을 반복적으로 조롱하고 흉내냈으며 "당신 같은 사람은 공개석상에서 말하면 안 된다"고 했다. Evan은 심각한 불안 증세로 상담 치료를 받게 됐다. Darla가 IIED로 liable한가?',
        'q_en_raw': 'Over two months, supervisor Darla repeatedly mocked employee Evan\'s stutter in team meetings, imitated him in front of coworkers, and said "People like you shouldn\'t be allowed to speak in public." Evan developed severe anxiety and began therapy. Is Darla liable for IIED?',
    },
    'class01_trespass_land_curated.json': {
        'q_ko_raw': 'Paula 소유의 시골 땅에 Daniel이 허락 없이 들어가 우연히 착지한 자신의 드론을 수거한 후 수분 내에 떠났다. 토지에 피해는 없었다. Daniel이 Trespass to Land로 liable한가?',
        'q_en_raw': 'Daniel entered Paula\'s rural property without permission to retrieve his drone that had accidentally landed there, then left within a few minutes. No damage was caused to the land. Is Daniel liable for trespass to land?',
    },
}

# ── Class 1 토픽 설정 ──────────────────────────────────────
CL1 = [
    {'title': 'Battery (폭행)',
     'curated': 'class01_battery_curated.json',
     'img_keys': []},
    {'title': 'Assault (협박)',
     'curated': 'class01_assault_curated.json',
     'img_keys': []},
    {'title': 'False Imprisonment (불법감금)',
     'curated': 'class01_fi_curated.json',
     'img_keys': []},
    {'title': 'IIED — Intentional Infliction of Emotional Distress',
     'curated': 'class01_iied_curated.json',
     'img_keys': []},
    {'title': 'Trespass to Land (토지 침입) — 기초',
     'curated': 'class01_trespass_land_curated.json',
     'img_keys': []},
]

# Class 2~8 이미지 매핑 (개념설명·Rule은 추후 추가)
CL28_IMG = {
    'Conversion & Trespass to Chattel':                         ['conversion'],
    'Defenses — Consent (동의)':                                 ['consent'],
    'Defenses — Self-Defense, Defense of Property, Necessity':  ['necessity', 'duress'],
    'Negligence — 4 Elements':                                  ['negligence_heading', 'breach', 'breach_child', 'res_ipsa'],
    '특수 Duty — 토지 점유자의 의무':                                 ['duty_special', 'duty_premises', 'respondeat'],
    'Causation — Actual + Proximate':                           ['causation', 'eggshell'],
    'Defenses to Negligence':                                   ['comp_neg'],
    'Strict Liability (엄격책임)':                                ['strict_liability', 'pl_design', 'pl_manufacturing', 'pl_warning'],
    'Property Torts — Trespass & Nuisance':                     ['property_torts', 'nuisance'],
    'Privacy Torts & Defamation':                               ['privacy', 'defamation'],
}

IMG_LABELS = {
    'ko_info': '🇰🇷 한글 개념도', 'en_info': '🇺🇸 English Concept',
    'ko_prac': '🇰🇷 한글 사례',   'en_prac': '🇺🇸 English Case',
    'ko_prac2':'🇰🇷 한글 사례 2', 'en_prac2':'🇺🇸 English Case 2',
}

# ── anchor_id → 어느 cls 탭에 속하는지 ────────────────────────
ANCHOR_CLS = {
    'tp-battery':       'cl1', 'tp-assault':      'cl1',
    'tp-fi':            'cl1', 'tp-iied':         'cl1',
    'tp-trespass-land': 'cl1', 'tp-conversion':   'cl2',
    'tp-consent':       'cl2', 'tp-defenses':     'cl2',
    'tp-negligence':    'cl3', 'tp-duty':         'cl3',
    'tp-causation':     'cl4', 'tp-defenses-neg': 'cl5',
    'tp-strict-liability':'cl6','tp-property-torts':'cl7',
    'tp-privacy':       'cl8',
}

# ── 토픽 Anchor ID (tp-hd id 속성 & 퀴즈 링크 공유) ──────────
TOPIC_ANCHORS = {
    'Battery (폭행)':                                            'tp-battery',
    'Assault (협박)':                                            'tp-assault',
    'False Imprisonment (불법감금)':                              'tp-fi',
    'IIED — Intentional Infliction of Emotional Distress':       'tp-iied',
    'Trespass to Land (토지 침입) — 기초':                        'tp-trespass-land',
    'Conversion & Trespass to Chattel':                          'tp-conversion',
    'Defenses — Consent (동의)':                                  'tp-consent',
    'Defenses — Self-Defense, Defense of Property, Necessity':   'tp-defenses',
    'Negligence — 4 Elements':                                   'tp-negligence',
    '특수 Duty — 토지 점유자의 의무':                               'tp-duty',
    'Causation — Actual + Proximate':                            'tp-causation',
    'Defenses to Negligence':                                    'tp-defenses-neg',
    'Strict Liability (엄격책임)':                                'tp-strict-liability',
    'Property Torts — Trespass & Nuisance':                      'tp-property-torts',
    'Privacy Torts & Defamation':                                'tp-privacy',
}

# ── 퀴즈 Q → 토픽 링크 매핑 [(anchor_id, 표시 레이블), ...] ────
QUIZ_TOPIC_LINKS = {
    # Class 1
    ('cl1', 1): [('tp-assault',        'Assault')],
    ('cl1', 2): [('tp-battery',        'Battery')],
    ('cl1', 3): [('tp-battery',        'Battery')],
    # Class 2
    ('cl2', 1): [('tp-trespass-land',  'Trespass to Land')],
    ('cl2', 2): [('tp-conversion',     'Conversion')],
    ('cl2', 3): [('tp-conversion',     'Trespass to Chattel')],
    ('cl2', 4): [('tp-defenses',       'Defenses — Duress')],
    ('cl2', 5): [('tp-defenses',       'Defense of Property')],
    ('cl2', 6): [('tp-defenses',       'Necessity')],
    # Class 3
    ('cl3', 1): [('tp-negligence',     'Negligence — Breach')],
    ('cl3', 2): [('tp-negligence',     'Negligence per se')],
    ('cl3', 3): [('tp-negligence',     'Negligence — Duty')],
    # Class 4
    ('cl4', 1): [('tp-causation',      'Causation')],
    ('cl4', 2): [('tp-causation',      'But-for / NESS Test')],
    ('cl4', 3): [('tp-causation',      'Alternative Liability')],
    # Class 5
    ('cl5', 1): [('tp-defenses-neg',   'Comparative Negligence')],
    ('cl5', 2): [('tp-defenses-neg',   'Pure Comparative Neg.')],
    ('cl5', 3): [('tp-defenses-neg',   'Modified Comparative')],
    # Class 6
    ('cl6', 1): [('tp-strict-liability','Strict Liability')],
    ('cl6', 2): [('tp-strict-liability','Products Liability')],
    ('cl6', 3): [('tp-strict-liability','Products Liability')],
    # Class 7
    ('cl7', 1): [('tp-property-torts', 'Nuisance')],
    ('cl7', 2): [('tp-property-torts', 'Nuisance')],
    ('cl7', 3): [('tp-property-torts', 'Trespass to Land')],
    # Class 8
    ('cl8', 1): [('tp-privacy',        'Defamation')],
    ('cl8', 2): [('tp-privacy',        'Privacy Torts')],
    ('cl8', 3): [('tp-privacy',        'Defamation')],
}

EXTRA_CSS = '''
/* ── KTK 문제풀이 탭 (v2: 텍스트 문제 → 클릭 → 해설+이미지) ── */
.ktk-prac-block{border:1.5px solid #c9b8e8;border-radius:8px;overflow:hidden;margin-bottom:1rem;}
.ktk-prac-cl-hd{background:#2d2060;color:#fff;font-size:.75rem;font-weight:700;
  padding:.35rem 1rem;letter-spacing:.5px;}
.ktk-prac-card{border-top:1px solid #e0d0f0;padding:.7rem 1rem .8rem;}
.ktk-prac-q-num{font-size:.7rem;font-weight:700;color:#4a2d7a;margin-bottom:.3rem;}
.ktk-prac-q-text{font-size:.82rem;line-height:1.75;color:#222;margin-bottom:.5rem;}
.ktk-prac-opt{font-size:.8rem;padding:.2rem .5rem;margin:.15rem 0;border-radius:3px;
  background:#f9f9f7;border:1px solid #e0e0e0;}
.ktk-prac-btn{width:100%;background:#4a2d7a;color:#fff;border:none;border-radius:4px;
  padding:.4rem;font-size:.73rem;font-weight:700;cursor:pointer;
  margin-top:.55rem;letter-spacing:.4px;display:block;}
.ktk-prac-btn:hover{background:#3a1d6a;}
.ktk-prac-explain{display:none;margin-top:.6rem;border-top:1.5px dashed #d0b8f0;padding-top:.6rem;}
.ktk-prac-explain.kp-open{display:block;}
.ktk-prac-answer-badge{display:inline-block;background:#1a6a1a;color:#fff;
  font-weight:700;font-size:.75rem;padding:.2rem .6rem;border-radius:3px;margin-bottom:.4rem;}
.ktk-prac-exp-text{font-size:.8rem;line-height:1.75;color:#222;margin-bottom:.6rem;}
/* 구형 호환 (이미지 탭용 스타일 유지) */
.ktk-prac-topic-hd{font-size:.76rem;font-weight:700;color:#3d1880;margin-bottom:.4rem;}
.ktk-prac-sub-lbl{font-size:.64rem;font-weight:700;color:#7a5c00;letter-spacing:.4px;
  text-transform:uppercase;margin:.5rem 0 .25rem;padding:.15rem .5rem;
  background:#fdf6e3;border-radius:3px;display:inline-block;}
.ktk-prac-cols{display:flex;gap:.5rem;}
.ktk-prac-col{flex:1;min-width:0;text-align:center;}
.ktk-prac-col-hd{font-size:.6rem;font-weight:700;padding:.12rem .4rem;
  border-radius:3px;display:inline-block;margin-bottom:.3rem;}
.ktk-prac-col-hd.ko{color:#1a4d8f;background:#e8f0fc;}
.ktk-prac-col-hd.en{color:#1a6a1a;background:#e8f5e8;}
.ktk-prac-img{width:100%;border-radius:4px;border:1px solid #ddd;display:block;margin-bottom:.25rem;}
.ktk-prac-exp-row{display:flex;gap:0;align-items:flex-start;}
.ktk-prac-exp-ko{flex:1;min-width:0;border-right:1.5px solid #e8d080;}
.ktk-prac-exp-en{flex:1;min-width:0;}
.ktk-prac-exp-tag{font-size:.6rem;font-weight:700;padding:.2rem .5rem;
  display:inline-block;margin:.3rem .5rem .1rem;border-radius:3px;}
.ktk-prac-exp-tag.ko{color:#1a4d8f;background:#e8f0fc;}
.ktk-prac-exp-tag.en{color:#1a6a1a;background:#e8f5e8;}
.ktk-prac-exp-body{font-size:.76rem;line-height:1.72;padding:.2rem .7rem .5rem;color:#222;}

/* ── Jenspark 이미지 ── */
.jenspark-wrap{background:#f5f0fb;border:1.5px solid #c9b8e8;border-top:none;
  padding:.75rem 1.1rem 1rem;}
.jenspark-lbl{font-size:.58rem;font-weight:700;letter-spacing:1.1px;color:#6a3d9a;
  text-transform:uppercase;margin-bottom:.6rem;}
.jenspark-imgs{display:grid;grid-template-columns:1fr 1fr;gap:.9rem;align-items:start;}
.topic-fig{margin:0;display:flex;flex-direction:column;}
.topic-cap{font-size:.7rem;color:#555;margin-bottom:.25rem;font-weight:600;}
.topic-img{max-width:100%;max-height:480px;width:100%;height:auto;
  border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.1);display:block;object-fit:contain;}
.topic-img.ko-img{border:2px solid #4a8f4a;}
.topic-img.en-img{border:2px solid var(--acc);}
.topic-fig-empty{min-height:1px;}
@media(max-width:780px){.jenspark-imgs{grid-template-columns:1fr;}.topic-fig-empty{display:none;}}

/* ── 개념설명 (UDSL 1회독) ── */
.udsl-wrap{border:1px solid var(--brd);border-top:none;background:#fcfcfa;}
.udsl-hd{background:#2c4a6e;color:#fff;padding:.55rem 1.1rem;font-size:.8rem;
  font-weight:700;display:flex;align-items:center;gap:8px;}
.udsl-bdg{font-size:.6rem;background:var(--acc2);color:#fff;padding:2px 7px;
  border-radius:10px;}
.udsl-sub{border-bottom:1px solid var(--brd);padding:.6rem 1.1rem;}
.udsl-sub:last-child{border-bottom:none;}
.udsl-sub-hd{font-size:.8rem;font-weight:700;color:var(--acc);margin-bottom:.45rem;
  display:flex;align-items:baseline;gap:.5rem;}
.udsl-slide-ref{font-size:.65rem;color:#aaa;font-weight:400;margin-left:auto;}
.udsl-cols{display:grid;grid-template-columns:1fr 1fr;gap:.6rem;}
.udsl-en{background:#eef4f9;padding:.45rem .7rem;border-radius:4px;
  font-size:.82rem;line-height:1.65;}
.udsl-ko{background:#fef9ec;padding:.45rem .7rem;border-radius:4px;
  font-size:.82rem;line-height:1.65;}
.udsl-lang{font-size:.6rem;font-weight:700;color:#888;margin-bottom:.2rem;}
@media(max-width:700px){.udsl-cols{grid-template-columns:1fr;}}

/* ── Rule + IRAC (3회독) ── */
.rule-irac-wrap{border:1px solid var(--brd);border-top:none;overflow:hidden;}
.rule-irac-hd{background:#1a2c1a;color:#fff;padding:.6rem 1.1rem;font-size:.82rem;
  font-weight:700;display:flex;align-items:center;gap:8px;}
.ri-bdg{font-size:.6rem;background:var(--gold);color:#1a1a00;padding:2px 7px;
  border-radius:10px;}
.rule-stmt{background:var(--acc);color:#fff;padding:.7rem 1.2rem;
  border-left:5px solid var(--acc2);}
.rule-lbl{font-size:.6rem;font-weight:700;letter-spacing:1px;opacity:.65;margin-bottom:4px;}
.rule-item{font-family:"Source Serif 4",serif;font-style:italic;
  font-size:.87rem;line-height:1.7;margin:.3rem 0;}
.rule-item b{color:var(--gold);font-style:normal;}
.irac-practice{padding:.8rem 1.1rem;background:#f9f9f7;}
.irac-p-hd{font-size:.7rem;font-weight:700;color:#2d6a2d;letter-spacing:.8px;
  text-transform:uppercase;margin-bottom:.6rem;}
.irac-slot{margin:.4rem 0;border-radius:5px;overflow:hidden;}
.irac-slot-lbl{font-size:.68rem;font-weight:700;padding:.3rem .7rem;color:#fff;}
.li-i{background:var(--acc2);}
.li-r{background:var(--acc);}
.li-a{background:#2d6a2d;}
.li-c{background:#7a3d8c;}
.irac-slot-hint{font-size:.78rem;color:#666;padding:.4rem .7rem;
  background:#fff;border:1px solid var(--brd);border-top:none;line-height:1.6;}
.irac-fact{background:#fff;border:1px solid #c0d4c0;border-radius:5px;
  padding:.6rem .9rem;margin-bottom:.7rem;}
.irac-fact-lbl{font-size:.6rem;font-weight:700;color:#2d6a2d;letter-spacing:.8px;
  text-transform:uppercase;margin-bottom:.4rem;}
.irac-fact-ko{font-size:.84rem;line-height:1.75;margin-bottom:.35rem;font-weight:500;}
.irac-fact-en{font-size:.78rem;color:#555;font-style:italic;line-height:1.65;}

/* ── 퀴즈 섹션 ── */
.quiz-mega-wrap{margin:2.5rem 0 1rem;border:2px solid #2c4a6e;border-radius:8px;overflow:hidden;}
.quiz-mega-hd{background:#2c4a6e;color:#fff;padding:.8rem 1.3rem;font-size:1rem;
  font-weight:700;letter-spacing:.5px;}
.quiz-cls-block{border-bottom:1.5px solid #c5d4e6;}
.quiz-cls-block:last-child{border-bottom:none;}
.quiz-cls-hd{background:#e8f0f8;color:#1a2c45;padding:.55rem 1.2rem;
  font-size:.85rem;font-weight:700;border-bottom:1px solid #c5d4e6;}
.quiz-lang-tag{padding:.35rem 1.2rem;font-size:.7rem;font-weight:700;
  letter-spacing:.8px;text-transform:uppercase;}
.quiz-lang-en{background:#e8f4e8;color:#1a4a1a;border-bottom:1px solid #c0d8c0;}
.quiz-lang-ko{background:#fef4e0;color:#4a3000;border-bottom:1px solid #e8d88a;margin-top:.25rem;}
.quiz-q-wrap{padding:.8rem 1.2rem 1rem;border-bottom:1px solid #dde6f0;}
.quiz-q-wrap:last-child{border-bottom:none;}
.quiz-q-num{font-size:.68rem;font-weight:700;color:#2c4a6e;letter-spacing:.8px;
  text-transform:uppercase;margin-bottom:.3rem;}
.quiz-q-text{font-size:.87rem;line-height:1.75;color:#111;margin-bottom:.65rem;}
.quiz-opts{display:flex;flex-direction:column;gap:.3rem;margin-bottom:.7rem;}
.quiz-opt{font-size:.84rem;line-height:1.6;padding:.3rem .6rem;
  background:#f5f8fc;border:1px solid #d0dce8;border-radius:4px;}
.quiz-opt-lbl{font-weight:700;color:#2c4a6e;margin-right:.3rem;}
.quiz-reveal{margin-top:.2rem;}
.quiz-reveal summary{cursor:pointer;font-size:.78rem;font-weight:700;color:#2c7a2c;
  padding:.35rem .7rem;background:#e8f4e8;border:1px solid #90c890;border-radius:4px;
  list-style:none;user-select:none;}
.quiz-reveal summary::-webkit-details-marker{display:none;}
.quiz-reveal[open] summary{background:#c8e8c8;border-color:#5a9a5a;}
.quiz-exp{background:#fff;border:1px solid #90c890;border-top:none;
  border-radius:0 0 4px 4px;padding:.7rem 1rem;font-size:.83rem;line-height:1.75;color:#222;}

/* ── 퀴즈 탭 인터랙티브 ── */
.quiz-opt{cursor:pointer;transition:background .12s,border-color .12s;}
.quiz-opt:hover:not(.locked){background:#e8f0fc;border-color:#8aaad8;}
.quiz-opt.right{background:#d4f0d4!important;border-color:#4a9a4a!important;}
.quiz-opt.wrong{background:#f0d4d4!important;border-color:#9a4a4a!important;}
.quiz-opt.right .quiz-opt-lbl::after{content:' ✓';color:#1a6a1a;}
.quiz-opt.wrong .quiz-opt-lbl::after{content:' ✗';color:#6a1a1a;}
.quiz-opt.reveal-correct{background:#e8f5e8!important;border-color:#70b070!important;}
.quiz-exp-panel{display:none;background:#fff;border:1px solid #90c890;
  border-radius:0 0 4px 4px;padding:.7rem 1rem;font-size:.83rem;line-height:1.75;}
.quiz-q-wrap.answered .quiz-exp-panel{display:block;}

/* ── iOS Safari 터치 클릭 픽스 ── */
/* touch-action:none = iOS가 스크롤 제스처로 삼키지 않음 */
.ctab{touch-action:none;user-select:none;-webkit-tap-highlight-color:rgba(0,0,0,.08);}
.ctabs{-webkit-overflow-scrolling:touch;}
.quiz-opt{touch-action:none;user-select:none;-webkit-tap-highlight-color:rgba(0,0,0,.06);}
.mbt{touch-action:manipulation;-webkit-tap-highlight-color:rgba(255,255,255,.15);}

/* ── KTK 교재 이론 섹션 ── */
.ktk-wrap{margin:1.5rem 0;border:1.5px solid #c5a028;border-radius:8px;overflow:hidden;}
.ktk-hd{background:#7a5c00;color:#fff;font-size:.8rem;font-weight:700;padding:.5rem 1rem;}
.ktk-topic{border-top:1px solid #e8d080;}
.ktk-topic:first-of-type{border-top:none;}
.ktk-topic-hd{background:#fdf6e3;color:#5a4000;font-size:.78rem;font-weight:700;
  padding:.4rem 1rem;border-bottom:1px solid #e8d080;}
.ktk-lang-tag{font-size:.68rem;font-weight:700;padding:.25rem .8rem;
  display:inline-block;margin:.4rem .6rem .1rem;}
.ktk-ko{color:#1a4d8f;background:#e8f0fc;border-radius:3px;}
.ktk-en{color:#1a6a1a;background:#e8f5e8;border-radius:3px;}
.ktk-body{font-size:.82rem;line-height:1.75;padding:.5rem 1rem 1rem;color:#222;}
.ktk-body h3{font-size:.85rem;font-weight:700;color:#5a4000;margin:.6rem 0 .3rem;}
.ktk-body h4{font-size:.8rem;font-weight:700;color:#4a5a00;margin:.5rem 0 .2rem;}
.ktk-body ul{margin:.3rem 0 .3rem 1.2rem;padding:0;}
.ktk-body li{margin:.15rem 0;}
.ktk-body p{margin:.3rem 0;}
.ktk-sep{border:none;border-top:1px dashed #d0c080;margin:.6rem 0;}
/* ── KTK 2열 병렬 레이아웃 ── */
.ktk-cols{display:flex;align-items:flex-start;gap:0;}
.ktk-col{flex:1;min-width:0;}
.ktk-col-ko{border-right:1.5px solid #e8d080;}
.ktk-col-ko .ktk-body,.ktk-col-ko .jenspark-wrap{border-right:none;}
.ktk-col-single{width:100%;}

/* ── 퀴즈 → 개념도 링크 뱃지 ── */
.quiz-topic-link{display:inline-flex;align-items:center;gap:2px;
  font-size:.63rem;font-weight:700;color:#6a3d9a;text-decoration:none;
  background:#f5f0fb;border:1px solid #c9b8e8;border-radius:3px;
  padding:1px 6px;margin-left:.5rem;vertical-align:middle;
  transition:background .15s;}
.quiz-topic-link:hover{background:#e0d0f5;border-color:#9a60d0;}
'''

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

# ── 렌더 함수들 ──────────────────────────────────────────

def _img_fig(fn, img_type):
    """단일 이미지 figure 태그. fn이 없으면 빈 칸 유지용 div."""
    if not fn:
        return '<div class="topic-fig-empty"></div>\n'
    lbl = IMG_LABELS[img_type]
    cls = 'ko-img' if img_type.startswith('ko') else 'en-img'
    return (f'<figure class="topic-fig">'
            f'<figcaption class="topic-cap">{lbl}</figcaption>'
            f'<img class="topic-img {cls}" src="images/{fn}" loading="lazy" alt="{lbl}">'
            f'</figure>\n')

def render_jenspark(img_keys, img_data):
    """한글(좌) / 영문(우) 2열 그리드. ko-en 쌍 단위로 출력해 어긋남 방지."""
    figures = ''
    for key in img_keys:
        imgs = img_data.get(key, {})
        for suffix in ['info', 'prac', 'prac2']:
            ko_fn = imgs.get(f'ko_{suffix}')
            en_fn = imgs.get(f'en_{suffix}')
            if not ko_fn and not en_fn:
                continue
            figures += _img_fig(ko_fn, f'ko_{suffix}')
            figures += _img_fig(en_fn, f'en_{suffix}')
    if not figures: return ''
    return (f'<div class="jenspark-wrap">\n'
            f'<div class="jenspark-lbl">🖼 Jenspark 개념 이미지 — 한글(좌) · 영문(우)</div>\n'
            f'<div class="jenspark-imgs">\n{figures}</div>\n</div>\n')

def render_udsl(curated):
    subs = curated.get('sub_sections', [])
    if not subs: return ''
    rows = ''
    for sec in subs:
        en = esc(sec.get('content_en','')).replace('\n','<br>')
        ko = esc(sec.get('content_ko','')).replace('\n','<br>')
        title_en = esc(sec.get('title_en',''))
        slides_str = ', '.join(map(str, sec.get('slides',[])))
        ko_col = (f'<div class="udsl-ko"><div class="udsl-lang">🇰🇷 KO</div>{ko}</div>'
                  if ko else '')
        cols_cls = 'udsl-cols' if ko else ''
        rows += (f'<div class="udsl-sub">'
                 f'<div class="udsl-sub-hd">{title_en}'
                 f'<span class="udsl-slide-ref">slide {slides_str}</span></div>'
                 f'<div class="{cols_cls}">'
                 f'<div class="udsl-en"><div class="udsl-lang">🇺🇸 EN</div>{en}</div>'
                 f'{ko_col}</div></div>\n')
    return (f'<div class="udsl-wrap">\n'
            f'<div class="udsl-hd">📖 개념설명 — UDSL 슬라이드 원문 (raw)'
            f'<span class="udsl-bdg">1회독</span></div>\n'
            f'{rows}</div>\n')

def render_rule_irac(rule_lines, topic_label, quiz_item=None):
    if not rule_lines: return ''

    # Rule Statement
    items = ''
    for rl in rule_lines:
        items += f'<div class="rule-item"><b>#{rl["idx"]}.</b> {esc(rl["text"])}</div>\n'

    # Fact Pattern
    fact_html = ''
    if quiz_item:
        en = esc(quiz_item.get('q_en_raw', '')).replace('\n', '<br>')
        ko = esc(quiz_item.get('q_ko_raw', '')).replace('\n', '<br>')
        fact_html = (
            f'<div class="irac-fact">'
            f'<div class="irac-fact-lbl">📋 Fact Pattern (교재 Hypothetical)</div>'
            f'<div class="irac-fact-ko">{ko}</div>'
            f'<div class="irac-fact-en">{en}</div>'
            f'</div>\n'
        )

    # I/R/A/C 슬롯
    irac_slots = ''
    for letter, lbl_cls, hint in [
        ('I', 'li-i', '어떤 법적 쟁점이 문제되는가?'),
        ('R', 'li-r', '적용할 Rule: 위 Rule Statement 핵심 요소'),
        ('A', 'li-a', '각 요소를 Fact에 대입: 충족 / 불충족 근거'),
        ('C', 'li-c', '결론 — liable / not liable, 이유 한 줄'),
    ]:
        irac_slots += (
            f'<div class="irac-slot">'
            f'<div class="irac-slot-lbl {lbl_cls}">{letter}</div>'
            f'<div class="irac-slot-hint">{hint}</div>'
            f'</div>\n'
        )

    return (
        f'<div class="rule-irac-wrap">\n'
        f'<div class="rule-irac-hd">⚖ Rule Statement + IRAC 연습'
        f'<span class="ri-bdg">3회독</span></div>\n'
        f'<div class="rule-stmt">'
        f'<div class="rule-lbl">RULE STATEMENT — 김윤상 정리본 그대로</div>'
        f'{items}</div>\n'
        f'<div class="irac-practice">'
        f'<div class="irac-p-hd">✍ IRAC 연습 — {esc(topic_label)}</div>'
        f'{fact_html}'
        f'{irac_slots}</div>\n'
        f'</div>\n'
    )

# ── 퀴즈 렌더 ────────────────────────────────────────────

QUIZ_CLASS_LABELS = {
    'cl1': 'Class 1 Quiz — Intentional Torts I (Battery · Assault · FI · IIED)',
    'cl2': 'Class 2 Quiz — Intentional Torts II + Defenses',
    'cl3': 'Class 3 Quiz — Negligence (Duty + Breach)',
    'cl4': 'Class 4 Quiz — Negligence (Causation + Harm)',
    'cl5': 'Class 5 Quiz — Defenses to Negligence + Vicarious',
    'cl6': 'Class 6 Quiz — Strict Liability + Products Liability',
    'cl7': 'Class 7 Quiz — Property Torts',
    'cl8': 'Class 8 Quiz — Defamation + Privacy',
    'practice': 'Practice Questions — 종합 실전 (20문제)',
}

def join_lines(s):
    """PDF 줄바꿈(word-wrap artifact) → 자연스러운 공백 연결. 단락 구분(\n\n)은 <p> 태그로."""
    if not s: return ''
    # 단락 분리 기준: 두 줄 이상 연속 줄바꿈
    paras = re.split(r'\n{2,}', s)
    result = []
    for p in paras:
        # 같은 단락 안 줄바꿈은 공백으로
        result.append(esc(p.replace('\n', ' ').strip()))
    return '</p><p>'.join(result)

def render_quiz_question(q, lang='en', topic_links=None):
    q_num = q['q_num']
    raw_text = q['q_text'] if lang == 'en' else (q.get('q_ko') or q['q_text'])
    raw_exp  = q['explanation'] if lang == 'en' else (q.get('exp_ko') or q['explanation'])
    q_text  = f'<p>{join_lines(raw_text)}</p>'
    exp_txt = (f'<p>{join_lines(raw_exp)}</p>' if raw_exp
               else '<em style="color:#888">해설 없음</em>')

    opts_html = ''
    for opt in q['options']:
        text = esc(opt['text']).replace('\n', ' ').strip()
        opts_html += (f'<div class="quiz-opt">'
                      f'<span class="quiz-opt-lbl">{opt["label"]}.</span> {text}</div>\n')

    lang_icon = '🇺🇸' if lang == 'en' else '🇰🇷'

    # 개념도 링크 뱃지
    link_badges = ''
    if topic_links:
        for anchor_id, label in topic_links:
            link_badges += (f'<a href="#{anchor_id}" class="quiz-topic-link">'
                            f'↑ {esc(label)}</a>')

    return (
        f'<div class="quiz-q-wrap">\n'
        f'<div class="quiz-q-num">{lang_icon} Question {q_num}{link_badges}</div>\n'
        f'<div class="quiz-q-text">{q_text}</div>\n'
        f'<div class="quiz-opts">{opts_html}</div>\n'
        f'<details class="quiz-reveal">\n'
        f'<summary>정답 · 해설 보기 ▼</summary>\n'
        f'<div class="quiz-exp">{exp_txt}</div>\n'
        f'</details>\n'
        f'</div>\n'
    )

def render_quiz_section(quiz_data):
    out = '<div class="quiz-mega-wrap">\n'
    out += '<div class="quiz-mega-hd">📝 UDSL 퀴즈 — 4회독 후 실전 점검</div>\n'

    for cls_key in ['cl1','cl2','cl3','cl4','cl5','cl6','cl7','cl8','practice']:
        questions = quiz_data.get(cls_key, [])
        if not questions: continue
        label = QUIZ_CLASS_LABELS.get(cls_key, cls_key)
        out += f'<div class="quiz-cls-block">\n'
        out += f'<div class="quiz-cls-hd">{label} ({len(questions)}문제)</div>\n'

        # ① 영문 원본
        out += '<div class="quiz-lang-tag quiz-lang-en">🇺🇸 English Version</div>\n'
        for q in questions:
            links = QUIZ_TOPIC_LINKS.get((cls_key, q['q_num']))
            out += render_quiz_question(q, lang='en', topic_links=links)

        # ② 한글 번역 (q_ko 필드 있을 때만)
        has_ko = any(q.get('q_ko','').strip() for q in questions)
        if has_ko:
            out += '<div class="quiz-lang-tag quiz-lang-ko">🇰🇷 한글 번역 연습</div>\n'
            for q in questions:
                if q.get('q_ko','').strip():
                    links = QUIZ_TOPIC_LINKS.get((cls_key, q['q_num']))
                    out += render_quiz_question(q, lang='ko', topic_links=links)

        out += '</div>\n'

    out += '</div>\n'
    return out

# ── 퀴즈 탭용 인터랙티브 렌더 ────────────────────────────────

QUIZ_TAB_JS = '''
<script>
/* ── 퀴즈 인터랙티브 ── */
function pickOpt(el){
  const wrap=el.closest('.quiz-q-wrap');
  if(wrap.classList.contains('answered')) return;
  wrap.classList.add('answered');
  const correct=wrap.dataset.correct||'';
  wrap.querySelectorAll('.quiz-opt').forEach(opt=>{
    opt.classList.add('locked');
    const lbl=opt.querySelector('.quiz-opt-lbl').textContent.replace('.','').trim();
    if(lbl===correct) opt.classList.add('right');
    else if(opt===el) opt.classList.add('wrong');
  });
}

/* ── 개념 태그: 탭 전환 + 스크롤 ── */
function gotoTopic(anchorId, clsId){
  showCls(clsId);
  setTimeout(()=>{
    const el=document.getElementById(anchorId);
    if(el) el.scrollIntoView({behavior:'smooth', block:'start'});
  }, 80);
  return false;
}

/* ── iOS Safari 터치 픽스 ──
   핵심: touchstart를 passive:false + preventDefault → iOS가 touchcancel 안 쏨
   touch-action:none (CSS) + preventDefault(touchstart) 이중 방어
   touchend에서 8px 이내 이동만 탭으로 판정, 직접 함수 호출 */
(function(){
  function tapFix(selector, action){
    document.querySelectorAll(selector).forEach(function(el){
      var sx=0, sy=0;
      el.addEventListener('touchstart',function(e){
        sx=e.touches[0].clientX; sy=e.touches[0].clientY;
        e.preventDefault(); // iOS가 스크롤 제스처로 채가는 것 차단
      },{passive:false});
      el.addEventListener('touchend',function(e){
        var dx=Math.abs(e.changedTouches[0].clientX-sx);
        var dy=Math.abs(e.changedTouches[0].clientY-sy);
        if(dx>8||dy>8) return;
        action(el);
      });
    });
  }
  /* 클래스 탭 */
  tapFix('.ctab', function(el){
    var m=(el.getAttribute('onclick')||'').match(/showCls\('([^']+)'\)/);
    if(m) showCls(m[1]);
  });
  /* 퀴즈 보기 */
  tapFix('.quiz-opt', function(el){ pickOpt(el); });
  /* 모드 버튼 */
  tapFix('.mbt', function(el){
    var m=(el.getAttribute('onclick')||'').match(/setMode\((\d+)\)/);
    if(m) setMode(parseInt(m[1]));
  });
})();

/* ── KTK 문제풀이 답·해설 토글 ── */
function toggleKtkExp(btn){
  var card=btn.closest('.ktk-prac-card');
  var panel=card.querySelector('.ktk-prac-explain');
  var isOpen=panel.classList.contains('kp-open');
  panel.classList.toggle('kp-open',!isOpen);
  btn.textContent=isOpen?'📖 답·해설 보기':'📗 답·해설 닫기';
}
</script>
'''

QUIZ_CLASS_LABELS_KO = {
    'cl1': 'Class 1 — Intentional Torts I',
    'cl2': 'Class 2 — Intentional Torts II + Defenses',
    'cl3': 'Class 3 — Negligence (Duty + Breach)',
    'cl4': 'Class 4 — Causation + Harm',
    'cl5': 'Class 5 — Defenses to Negligence',
    'cl6': 'Class 6 — Strict Liability + Products',
    'cl7': 'Class 7 — Property Torts',
    'cl8': 'Class 8 — Defamation + Privacy',
}

def render_interactive_question(q, cls_key, lang='ko'):
    """퀴즈 탭용: 클릭→정답/오답. lang='ko'|'en'"""
    q_num   = q['q_num']
    correct = q.get('correct_answer', '')

    if lang == 'ko':
        icon    = '🇰🇷'
        q_text  = f'<p>{join_lines(q.get("q_ko") or q["q_text"])}</p>'
        exp_raw = q.get('exp_ko') or q.get('explanation', '')
    else:
        icon    = '🇺🇸'
        q_text  = f'<p>{join_lines(q["q_text"])}</p>'
        exp_raw = q.get('explanation', '')

    exp_html = (f'<p>{join_lines(exp_raw)}</p>' if exp_raw
                else '<em style="color:#888">해설 없음</em>')

    # 개념 링크 뱃지 (탭 전환 JS 사용)
    link_badges = ''
    for anchor_id, label in (QUIZ_TOPIC_LINKS.get((cls_key, q_num)) or []):
        target_cls = ANCHOR_CLS.get(anchor_id, 'cl1')
        link_badges += (f'<a href="#{anchor_id}" '
                        f'onclick="return gotoTopic(\'{anchor_id}\',\'{target_cls}\')" '
                        f'class="quiz-topic-link">↑ {esc(label)}</a>')

    opts_html = ''
    for opt in q['options']:
        text = esc(opt['text']).replace('\n', ' ').strip()
        opts_html += (f'<div class="quiz-opt" onclick="pickOpt(this)">'
                      f'<span class="quiz-opt-lbl">{opt["label"]}.</span> {text}</div>\n')

    return (
        f'<div class="quiz-q-wrap" data-correct="{correct}">\n'
        f'<div class="quiz-q-num">{icon} Q{q_num}{link_badges}</div>\n'
        f'<div class="quiz-q-text">{q_text}</div>\n'
        f'<div class="quiz-opts">{opts_html}</div>\n'
        f'<div class="quiz-exp-panel">{exp_html}</div>\n'
        f'</div>\n'
    )

def render_quiz_tabs(quiz_data):
    """cls id='quiz' 섹션 (cl1~cl8 — 한글 먼저, 영문 뒤)"""
    out = '<div class="cls" id="quiz">\n'
    out += '<div style="padding:.6rem 1rem .2rem;font-size:.75rem;color:#666">※ 보기를 클릭하면 정답/오답이 표시됩니다. 개념 태그(↑)를 클릭하면 해당 토픽으로 이동합니다.</div>\n'
    for cls_key in ['cl1','cl2','cl3','cl4','cl5','cl6','cl7','cl8']:
        qs = quiz_data.get(cls_key, [])
        if not qs: continue
        label = QUIZ_CLASS_LABELS_KO.get(cls_key, cls_key)
        out += f'<div class="quiz-cls-block">\n'
        out += f'<div class="quiz-cls-hd">{label} ({len(qs)}문제)</div>\n'
        # ① 한글 먼저
        out += '<div class="quiz-lang-tag quiz-lang-ko">🇰🇷 한글</div>\n'
        for q in qs:
            out += render_interactive_question(q, cls_key, lang='ko')
        # ② 영문 뒤
        out += '<div class="quiz-lang-tag quiz-lang-en">🇺🇸 English</div>\n'
        for q in qs:
            out += render_interactive_question(q, cls_key, lang='en')
        out += '</div>\n'
    out += '</div>\n'
    return out

KTK_DATA = r'F:\mbe\_extracted\ktk_data.json'

TOPIC_LABELS_KO = {
    'battery':             'Battery (폭행)',
    'assault':             'Assault (협박)',
    'false_imprisonment':  'False Imprisonment (불법감금)',
    'iied':                'IIED / NIED (감정적 고통)',
    'trespass_land':       'Trespass to Land (토지 침해)',
    'conversion':          'Conversion & Trespass to Chattel',
    'defenses_intentional':'Defenses (동의·자기방어·필요성)',
    'negligence_duty':     'Negligence — Duty & Breach',
    'negligence_general':  'Negligence 개요',
    'causation':           'Causation (인과관계)',
    'defenses_neg':        'Defenses to Negligence',
    'strict_liability':    'Strict Liability (엄격책임)',
    'products_liability':  'Products Liability (제조물책임)',
    'nuisance':            'Nuisance (방해행위)',
    'defamation':          'Defamation (명예훼손)',
    'privacy':             'Privacy Torts (프라이버시)',
}

# KTK 토픽 → 이미지 키 매핑 (해당 토픽 내용 바로 아래 이미지 배치)
KTK_IMG_MAP = {
    'battery':              ['battery', 'transferred_intent'],
    'assault':              ['assault'],
    'false_imprisonment':   ['fi'],
    'iied':                 ['iied'],
    'trespass_land':        ['trespass_land'],
    'conversion':           ['conversion'],
    'defenses_intentional': ['consent', 'necessity', 'duress'],
    'negligence_duty':      ['duty_special', 'duty_premises', 'respondeat'],
    'negligence_general':   ['negligence_heading', 'breach', 'breach_child', 'res_ipsa'],
    'causation':            ['causation', 'eggshell'],
    'defenses_neg':         ['comp_neg'],
    'strict_liability':     ['strict_liability'],
    'products_liability':   ['pl_design', 'pl_manufacturing', 'pl_warning'],
    'nuisance':             ['nuisance', 'property_torts'],
    'defamation':           ['defamation'],
    'privacy':              ['privacy'],
}

def render_ktk_imgs(keys: list, lang: str, img_data: dict) -> str:
    """KTK 섹션 하단 인라인 이미지 (lang='ko' or 'en')"""
    figures = ''
    for key in keys:
        imgs = img_data.get(key, {})
        for img_type in [f'{lang}_info', f'{lang}_prac', f'{lang}_prac2']:
            fn = imgs.get(img_type)
            if not fn:
                continue
            lbl = IMG_LABELS[img_type]
            cls = 'ko-img' if lang == 'ko' else 'en-img'
            figures += (f'<figure class="topic-fig">'
                        f'<figcaption class="topic-cap">{lbl}</figcaption>'
                        f'<img class="topic-img {cls}" src="images/{fn}" loading="lazy" alt="{lbl}">'
                        f'</figure>\n')
    if not figures:
        return ''
    return (f'<div class="jenspark-wrap ktk-imgs">\n'
            f'<div class="jenspark-lbl">🖼 Jenspark 개념 이미지</div>\n'
            f'<div class="jenspark-imgs">\n{figures}</div>\n</div>\n')

def render_ktk_section(cl_key: str, ktk_data: dict, img_data: dict = None) -> str:
    """KTK 한글 + 영문 이론을 챕터별 HTML로 렌더링 (이미지 인라인 삽입)"""
    ko_topics = ktk_data.get('ko', {}).get(cl_key, {})
    en_topics = ktk_data.get('en', {}).get(cl_key, {})
    all_topics = sorted(set(list(ko_topics.keys()) + list(en_topics.keys())))
    if not all_topics:
        return ''

    out = '<div class="ktk-wrap">\n'
    out += '<div class="ktk-hd">📖 KTK 교재 이론</div>\n'

    for topic in all_topics:
        label = TOPIC_LABELS_KO.get(topic, topic)
        ko_text = ko_topics.get(topic, '')
        en_text = en_topics.get(topic, '')
        if not ko_text and not en_text:
            continue

        img_keys = KTK_IMG_MAP.get(topic, [])

        out += f'<div class="ktk-topic">\n'
        out += f'<div class="ktk-topic-hd">{label}</div>\n'

        # ── 2열 병렬: 좌=한글, 우=영문 ──
        both = ko_text and en_text

        if both:
            out += '<div class="ktk-cols">\n'

        # ── 좌열: 한글 ──
        if ko_text:
            col_cls = 'ktk-col ktk-col-ko' if both else 'ktk-col-single'
            out += f'<div class="{col_cls}">\n'
            out += '<div class="ktk-lang-tag ktk-ko">🇰🇷 한글 이론</div>\n'
            ko_html = md_to_html(ko_text)
            out += f'<div class="ktk-body ktk-body-ko">{ko_html}</div>\n'
            if img_data and img_keys:
                ko_imgs = render_ktk_imgs(img_keys, 'ko', img_data)
                if ko_imgs:
                    out += ko_imgs
            out += '</div>\n'

        # ── 우열: 영문 ──
        if en_text:
            col_cls = 'ktk-col ktk-col-en' if both else 'ktk-col-single'
            out += f'<div class="{col_cls}">\n'
            out += '<div class="ktk-lang-tag ktk-en">🇺🇸 English Theory</div>\n'
            en_html = md_to_html(en_text)
            out += f'<div class="ktk-body ktk-body-en">{en_html}</div>\n'
            if img_data and img_keys:
                en_imgs = render_ktk_imgs(img_keys, 'en', img_data)
                if en_imgs:
                    out += en_imgs
            out += '</div>\n'

        if both:
            out += '</div>\n'  # .ktk-cols 닫기

        out += '</div>\n'  # .ktk-topic 닫기

    out += '</div>\n'
    return out

def md_to_html(text: str) -> str:
    """최소한의 마크다운 → HTML 변환"""
    import html as html_mod
    lines = text.split('\n')
    result = []
    in_ul = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_ul:
                result.append('</ul>')
                in_ul = False
            result.append('')
            continue
        # 제목 (### 이하만)
        if stripped.startswith('### '):
            if in_ul: result.append('</ul>'); in_ul = False
            result.append(f'<h4>{html_mod.escape(stripped[4:])}</h4>')
        elif stripped.startswith('## '):
            if in_ul: result.append('</ul>'); in_ul = False
            result.append(f'<h3>{html_mod.escape(stripped[3:])}</h3>')
        # 구분선
        elif stripped.startswith('---'):
            if in_ul: result.append('</ul>'); in_ul = False
            result.append('<hr class="ktk-sep">')
        # 리스트 항목
        elif stripped.startswith(('- ', '* ', '• ')):
            if not in_ul:
                result.append('<ul>')
                in_ul = True
            item = stripped[2:].strip()
            item = apply_inline(html_mod.escape(item))
            result.append(f'<li>{item}</li>')
        elif re.match(r'^\d+\.\s', stripped):
            if not in_ul:
                result.append('<ul>')
                in_ul = True
            item = re.sub(r'^\d+\.\s', '', stripped)
            item = apply_inline(html_mod.escape(item))
            result.append(f'<li>{item}</li>')
        else:
            if in_ul: result.append('</ul>'); in_ul = False
            line_html = apply_inline(html_mod.escape(stripped))
            result.append(f'<p>{line_html}</p>')
    if in_ul:
        result.append('</ul>')
    return '\n'.join(result)

def apply_inline(text: str) -> str:
    """굵게(**), 기울임(*) 인라인 변환"""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*',     r'<em>\1</em>',         text)
    return text

def inject_ktk_content(html: str, ktk_data: dict, img_data: dict = None) -> str:
    """cl1~cl8 각 챕터 내 UDSL 퀴즈 앞에 KTK 이론 삽입"""
    cls_keys = ['cl1','cl2','cl3','cl4','cl5','cl6','cl7','cl8']
    inserted = 0
    for i, cls_key in enumerate(cls_keys):
        ktk_html = render_ktk_section(cls_key, ktk_data, img_data)
        if not ktk_html:
            print(f'  ⚠ {cls_key} KTK 내용 없음')
            continue

        # 퀴즈 블록(quiz-mega-wrap) 바로 앞에 삽입
        # 없으면 챕터 cls div 끝 바로 앞에 삽입
        if i < len(cls_keys) - 1:
            next_cls = cls_keys[i + 1]
            next_pos = html.find(f'<div id="{next_cls}"')
            inject_pos = html.rfind('<div class="quiz-mega-wrap">', 0, next_pos)
            if inject_pos < 0:
                inject_pos = html.rfind('</div>', 0, next_pos)
        else:
            script_pos = html.rfind('<script>')
            inject_pos = html.rfind('<div class="quiz-mega-wrap">', 0, script_pos)
            if inject_pos < 0:
                inject_pos = html.rfind('</div>', 0, script_pos)

        if inject_pos < 0:
            print(f'  ⚠ {cls_key} inject 위치 못 찾음')
            continue

        html = html[:inject_pos] + ktk_html + html[inject_pos:]
        topics = list(ktk_data.get('ko',{}).get(cls_key,{}).keys()) + \
                 [t for t in ktk_data.get('en',{}).get(cls_key,{}).keys()
                  if t not in ktk_data.get('ko',{}).get(cls_key,{})]
        print(f'  ✓ {cls_key} KTK 삽입 ({len(set(topics))}토픽)')
        inserted += 1
    return html

def inject_quiz_into_chapters(html, quiz_data):
    """cl1~cl8 각 챕터 cls div 끝에 해당 클래스 퀴즈 삽입"""
    cls_keys = ['cl1','cl2','cl3','cl4','cl5','cl6','cl7','cl8']
    for i, cls_key in enumerate(cls_keys):
        qs = quiz_data.get(cls_key, [])
        if not qs: continue
        label = QUIZ_CLASS_LABELS_KO.get(cls_key, cls_key)

        # 퀴즈 블록 (한글 → 영문)
        qblock  = f'<div class="quiz-mega-wrap">\n'
        qblock += f'<div class="quiz-mega-hd">📝 {label} 퀴즈</div>\n'
        qblock += '<div class="quiz-cls-block">\n'
        qblock += '<div class="quiz-lang-tag quiz-lang-ko">🇰🇷 한글</div>\n'
        for q in qs:
            qblock += render_interactive_question(q, cls_key, lang='ko')
        qblock += '<div class="quiz-lang-tag quiz-lang-en">🇺🇸 English</div>\n'
        for q in qs:
            qblock += render_interactive_question(q, cls_key, lang='en')
        qblock += '</div>\n</div>\n'

        # cls div 닫힘 바로 앞에 inject
        if i < len(cls_keys) - 1:
            next_pos = html.find(f'<div id="{cls_keys[i+1]}"')
            inject_pos = html.rfind('</div>', 0, next_pos)
        else:
            # cl8: 마지막 <script> 블록 앞의 </div>
            script_pos = html.rfind('<script>')
            inject_pos = html.rfind('</div>', 0, script_pos)

        if inject_pos < 0:
            print(f'  ⚠ {cls_key} inject 위치 못 찾음')
            continue
        html = html[:inject_pos] + qblock + html[inject_pos:]
        print(f'  ✓ 퀴즈 {cls_key} → 챕터 내 삽입 ({len(qs)}문제)')
    return html

IMG_KEY_LABELS = {
    'battery':           'Battery (폭행)',
    'transferred_intent':'Transferred Intent (전이된 의도)',
    'assault':           'Assault (협박)',
    'fi':                'False Imprisonment (불법감금)',
    'iied':              'IIED (고의적 정신적 피해)',
    'trespass_land':     'Trespass to Land (토지 침해)',
    'conversion':        'Conversion (동산 침탈)',
    'consent':           'Defense: Consent (동의)',
    'necessity':         'Defense: Necessity (필요성)',
    'duress':            'Defense: Duress (강박)',
    'duty_special':      'Special Duty (특별의무)',
    'duty_premises':     'Premises Duty (부지 의무)',
    'respondeat':        'Respondeat Superior',
    'negligence_heading':'Negligence Overview (과실 개요)',
    'breach':            'Breach of Duty (의무위반)',
    'breach_child':      'Child Standard (아동 기준)',
    'res_ipsa':          'Res Ipsa Loquitur',
    'causation':         'Causation (인과관계)',
    'eggshell':          'Eggshell Skull Rule',
    'comp_neg':          'Comparative Negligence (비교과실)',
    'strict_liability':  'Strict Liability (엄격책임)',
    'pl_design':         'Design Defect (설계결함)',
    'pl_manufacturing':  'Manufacturing Defect (제조결함)',
    'pl_warning':        'Warning Defect (경고결함)',
    'informed_consent':  'Informed Consent (설명의무)',
    'nuisance':          'Nuisance (방해행위)',
    'property_torts':    'Property Torts',
    'defamation':        'Defamation (명예훼손)',
    'privacy':           'Privacy Torts (프라이버시)',
}

KTK_CL_TOPICS = [
    ('Class 1 — Intentional Torts I',
     ['battery', 'assault', 'false_imprisonment', 'iied', 'trespass_land']),
    ('Class 2 — Intentional Torts II',
     ['conversion', 'defenses_intentional']),
    ('Class 3 — Negligence',
     ['negligence_duty', 'negligence_general']),
    ('Class 4 — Causation',
     ['causation']),
    ('Class 5 — Defenses to Negligence',
     ['defenses_neg']),
    ('Class 6 — Strict Liability + Products',
     ['strict_liability', 'products_liability']),
    ('Class 7 — Property Torts',
     ['nuisance']),
    ('Class 8 — Defamation + Privacy',
     ['defamation', 'privacy']),
]

def _ktk_prac_theory(topic_key, ko_all, en_all):
    """토픽 키에 해당하는 KTK 이론 텍스트 (ko, en) 반환"""
    ko_text, en_text = '', ''
    for topics in ko_all.values():
        if topic_key in topics:
            ko_text = topics[topic_key]
            break
    for topics in en_all.values():
        if topic_key in topics:
            en_text = topics[topic_key]
            break
    return ko_text, en_text

def render_ktk_prac_tab(ktk_prac_data, img_data):
    """cls id='ktk_prac' 섹션 — KTK 문제풀이 탭 (텍스트 문제 → 클릭 → 해설+이미지)

    ktk_prac_data: ktk_prac_data.json 로드 결과
      { topic_key: [{"q_num":N, "q_text":"...", "options":[...],
                     "correct_answer":"A", "explanation":"..."}, ...], ... }
    img_data: image_classification.json topic_mapping
    """
    out = '<div class="cls" id="ktk_prac">\n'
    out += ('<div style="padding:.6rem 1rem .2rem;font-size:.75rem;color:#666">'
            'KTK 문제풀이 — 팩트패턴 분석 후 ▼ 버튼으로 정답·해설 확인</div>\n')

    # 토픽 순서: KTK_CL_TOPICS의 순서를 따름 (cl_label, topic_keys)
    # ktk_prac_data의 키만 포함된 토픽을 순서대로 렌더링
    seen_topics = set()
    ordered_topic_keys = []
    for _cl_label, topic_keys in KTK_CL_TOPICS:
        for tk in topic_keys:
            if tk in ktk_prac_data and tk not in seen_topics:
                ordered_topic_keys.append(tk)
                seen_topics.add(tk)
    # KTK_CL_TOPICS에 없는 토픽 뒤에 추가 (respondeat 등)
    for tk in ktk_prac_data:
        if tk not in seen_topics:
            ordered_topic_keys.append(tk)

    # 클래스 구분 헤더 삽입용 매핑: topic_key → cl_label
    topic_to_cl = {}
    for cl_label, topic_keys in KTK_CL_TOPICS:
        for tk in topic_keys:
            topic_to_cl[tk] = cl_label

    current_cl = None
    for topic_key in ordered_topic_keys:
        questions = ktk_prac_data.get(topic_key, [])
        if not questions:
            continue

        cl_label = topic_to_cl.get(topic_key, 'Other')
        label    = TOPIC_LABELS_KO.get(topic_key, topic_key)

        # 새 클래스 블록 시작
        if cl_label != current_cl:
            if current_cl is not None:
                out += '</div>\n'  # 이전 .ktk-prac-block 닫기
            out += '<div class="ktk-prac-block">\n'
            out += f'<div class="ktk-prac-cl-hd">◆ {cl_label}</div>\n'
            current_cl = cl_label

        # 토픽 내 문제들
        for q in questions:
            q_num       = q.get('q_num', 0)
            q_text      = esc(q.get('q_text', '')).replace('\n', '<br>')
            options     = q.get('options', [])
            correct     = q.get('correct_answer', '')
            explanation = esc(q.get('explanation', '')).replace('\n', '<br>')

            out += '<div class="ktk-prac-card">\n'
            # 문제 번호 + 토픽 뱃지
            out += (f'<div class="ktk-prac-q-num">Q{q_num} '
                    f'<span style="font-weight:400;color:#888;font-size:.65rem">— {esc(label)}</span>'
                    f'</div>\n')
            # 팩트패턴
            if q_text:
                out += f'<div class="ktk-prac-q-text">{q_text}</div>\n'
            else:
                out += '<div class="ktk-prac-q-text" style="color:#aaa">(팩트패턴 준비 중)</div>\n'
            # MCQ 옵션
            for opt in options:
                opt_text = esc(opt.get('text', '')).replace('\n', ' ')
                out += f'<div class="ktk-prac-opt">({opt["label"]}) {opt_text}</div>\n'

            # 답·해설 버튼
            out += '<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>\n'

            # ── 숨겨진 해설 패널 ──────────────────────────────────────
            out += f'<div class="ktk-prac-explain" data-correct="{esc(correct)}">\n'

            # 정답 뱃지
            if correct:
                out += f'<div class="ktk-prac-answer-badge">정답: ({correct})</div>\n'

            # 해설 텍스트
            if explanation:
                out += f'<div class="ktk-prac-exp-text">{explanation}</div>\n'
            else:
                out += '<div class="ktk-prac-exp-text" style="color:#aaa">(해설 준비 중)</div>\n'

            # 해당 토픽 Jenspark prac 이미지 (있으면)
            img_keys = KTK_IMG_MAP.get(topic_key, [])
            if img_keys and img_data:
                figures = ''
                for img_key in img_keys:
                    imgs = img_data.get(img_key, {})
                    for img_type in ['ko_prac', 'en_prac', 'ko_prac2', 'en_prac2']:
                        fn = imgs.get(img_type)
                        if not fn:
                            continue
                        lbl = IMG_LABELS.get(img_type, img_type)
                        cls = 'ko-img' if img_type.startswith('ko') else 'en-img'
                        figures += (f'<figure class="topic-fig">'
                                    f'<figcaption class="topic-cap">{esc(lbl)}</figcaption>'
                                    f'<img class="topic-img {cls}" src="images/{fn}" '
                                    f'loading="lazy" alt="{esc(lbl)}">'
                                    f'</figure>\n')
                if figures:
                    out += ('<div class="jenspark-wrap" style="margin-top:.5rem">\n'
                            '<div class="jenspark-lbl">Jenspark 개념 이미지</div>\n'
                            f'<div class="jenspark-imgs">\n{figures}</div>\n</div>\n')

            out += '</div>\n'  # .ktk-prac-explain
            out += '</div>\n'  # .ktk-prac-card

    # 마지막 블록 닫기
    if current_cl is not None:
        out += '</div>\n'  # .ktk-prac-block

    out += '</div>\n'  # .cls#ktk_prac
    return out


def render_practice_tab(quiz_data):
    """cls id='practice' 섹션 (Practice 20문제 — 한글 먼저, 영문 뒤)"""
    qs = quiz_data.get('practice', [])
    out = '<div class="cls" id="practice">\n'
    out += '<div style="padding:.6rem 1rem .2rem;font-size:.75rem;color:#666">종합 실전 20문제 — 보기 클릭 시 정답/오답 표시</div>\n'
    out += '<div class="quiz-cls-block">\n'
    out += f'<div class="quiz-cls-hd">Practice Questions — 종합 실전 ({len(qs)}문제)</div>\n'
    # ① 한글 먼저
    out += '<div class="quiz-lang-tag quiz-lang-ko">🇰🇷 한글</div>\n'
    for q in qs:
        out += render_interactive_question(q, 'practice', lang='ko')
    # ② 영문 뒤
    out += '<div class="quiz-lang-tag quiz-lang-en">🇺🇸 English</div>\n'
    for q in qs:
        out += render_interactive_question(q, 'practice', lang='en')
    out += '</div>\n</div>\n'
    return out

# ── 단답형 Hypo 탭 ───────────────────────────────────────

HYPO_CSS = """
/* ── 단답형 Hypo 탭 ── */
.hypo-wrap{margin:0;padding:0;}
.hypo-cl-block{border-bottom:2px solid #b8cce4;margin-bottom:0;}
.hypo-cl-block:last-child{border-bottom:none;}
.hypo-cl-hd{background:#1e3a5f;color:#fff;padding:.6rem 1.2rem;font-size:.82rem;
  font-weight:700;letter-spacing:.3px;cursor:pointer;user-select:none;
  display:flex;justify-content:space-between;align-items:center;}
.hypo-cl-hd .hypo-cl-count{font-size:.7rem;font-weight:400;opacity:.8;}
.hypo-cl-body{display:none;}
.hypo-cl-body.open{display:block;}
.hypo-card{border-bottom:1px solid #d8e6f0;padding:.8rem 1.2rem;}
.hypo-card:last-child{border-bottom:none;}
.hypo-card-num{font-size:.65rem;font-weight:700;color:#1e3a5f;letter-spacing:.6px;
  text-transform:uppercase;margin-bottom:.3rem;}
.hypo-card-title{font-size:.76rem;font-weight:700;color:#444;margin-bottom:.4rem;}
.hypo-q{font-size:.84rem;line-height:1.78;color:#111;white-space:pre-wrap;
  background:#f8f9fb;border-left:3px solid #4a7ab5;padding:.5rem .8rem;
  border-radius:0 4px 4px 0;margin-bottom:.5rem;}
.hypo-ans-toggle{cursor:pointer;font-size:.75rem;font-weight:700;color:#1e6a1e;
  background:#e8f4e8;border:1px solid #90c890;border-radius:4px;
  padding:.25rem .7rem;display:inline-block;margin-bottom:.1rem;}
.hypo-ans-toggle:hover{background:#d0ead0;}
.hypo-ans{display:none;margin-top:.4rem;background:#f0f8f0;
  border:1px solid #90c890;border-radius:4px;padding:.6rem .9rem;
  font-size:.82rem;line-height:1.78;color:#111;white-space:pre-wrap;}
.hypo-ans.open{display:block;}
"""

CL_LABELS = {
    'cl1': 'Class 1 — Intentional Torts I',
    'cl2': 'Class 2 — Intentional Torts II',
    'cl3': 'Class 3 — Negligence',
    'cl4': 'Class 4 — Causation & Harm',
    'cl5': 'Class 5 — Defenses & Vicarious Liability',
    'cl6': 'Class 6 — Strict Liability & Products Liability',
    'cl7': 'Class 7 — Property Torts',
    'cl8': 'Class 8 — Defamation & Privacy',
}

def render_hypo_tab(hypo_data: dict) -> str:
    """단답형 Hypo 탭 전체 HTML"""
    out = '<div class="cls" id="hypo">\n'
    out += '<div style="padding:.6rem 1.2rem .2rem;font-size:.75rem;color:#555">'
    total = sum(len(v) for v in hypo_data.values())
    out += f'PPT 교재 수업 사례 ({total}문제) — 클릭하면 교재 해설 펼침</div>\n'
    out += '<div class="hypo-wrap">\n'

    for cl_key in ['cl1','cl2','cl3','cl4','cl5','cl6','cl7','cl8']:
        hypos = hypo_data.get(cl_key, [])
        if not hypos:
            continue
        label = CL_LABELS.get(cl_key, cl_key)
        out += f'<div class="hypo-cl-block">\n'
        out += (f'<div class="hypo-cl-hd" onclick="toggleHypoCl(this)">'
                f'{label}<span class="hypo-cl-count">{len(hypos)}개</span></div>\n')
        out += '<div class="hypo-cl-body">\n'

        for i, h in enumerate(hypos, 1):
            hid = h.get('id', f'{cl_key}-h{i}')
            title = h.get('title', '')
            q_text = h.get('question', '').strip()
            ans_text = h.get('answer', '').strip()

            # 제목이 질문 텍스트 첫 줄과 같으면 중복 제거
            q_lines = q_text.split('\n')
            if q_lines and q_lines[0].strip() == title.strip():
                q_text = '\n'.join(q_lines[1:]).strip()

            out += f'<div class="hypo-card">\n'
            out += f'<div class="hypo-card-num">Q{i}</div>\n'
            if title:
                out += f'<div class="hypo-card-title">{title}</div>\n'
            out += f'<div class="hypo-q">{q_text}</div>\n'

            if ans_text:
                out += (f'<div class="hypo-ans-toggle" '
                        f'onclick="toggleHypoAns(this)">▶ 교재 해설 보기</div>\n')
                out += f'<div class="hypo-ans">{ans_text}</div>\n'
            else:
                out += '<div style="font-size:.72rem;color:#888;font-style:italic">해설: 교재 다음 슬라이드 참고</div>\n'

            out += '</div>\n'  # hypo-card

        out += '</div>\n'  # hypo-cl-body
        out += '</div>\n'  # hypo-cl-block

    out += '</div>\n</div>\n'  # hypo-wrap, cls
    return out

HYPO_JS = """
function toggleHypoCl(el){
  const body = el.nextElementSibling;
  body.classList.toggle('open');
  el.style.background = body.classList.contains('open') ? '#2c5480' : '';
}
function toggleHypoAns(el){
  const ans = el.nextElementSibling;
  const isOpen = ans.classList.toggle('open');
  el.textContent = isOpen ? '▼ 교재 해설 닫기' : '▶ 교재 해설 보기';
}
"""

# ── tp-hd anchor 주입 ────────────────────────────────────

def add_topic_anchors(html):
    """TOPIC_ANCHORS 매핑대로 tp-hd 태그에 id 속성 추가"""
    tp_hd_re = re.compile(r'<div class="tp-hd"[^>]*>')
    for title, anchor_id in TOPIC_ANCHORS.items():
        title_span = f'<span class="tp-t">{title}</span>'
        pos = html.find(title_span)
        if pos < 0:
            continue
        # 이 title 바로 앞에 있는 tp-hd 태그 찾기
        last_m = None
        for m in tp_hd_re.finditer(html, 0, pos):
            last_m = m
        if not last_m:
            continue
        old_tag = last_m.group()
        if 'id=' in old_tag:
            continue  # 이미 id 있음
        new_tag = old_tag[:-1] + f' id="{anchor_id}">'
        html = html[:last_m.start()] + new_tag + html[last_m.end():]
    return html

# ── 주입 함수 ─────────────────────────────────────────────

def inject_at(html, search_from, marker, content, before=True):
    pos = html.find(marker, search_from)
    if pos < 0: return html, False
    if before:
        return html[:pos] + content + html[pos:], True
    else:
        end = pos + len(marker)
        return html[:end] + content + html[end:], True

def find_r0_end(html, search_from):
    """search_from 이후 첫 번째 <div class="r0"> 닫힘 직후 위치 반환"""
    r0_pos = html.find('<div class="r0">', search_from)
    if r0_pos < 0:
        return -1
    depth = 0
    i = r0_pos
    limit = min(r0_pos + 50000, len(html))
    while i < limit:
        if html[i:i+4] == '<div':
            depth += 1
            i += 4
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                return i + 6   # </div> 닫힘 직후
            i += 6
        else:
            i += 1
    return -1

def process_topic(html, topic_cfg, img_data):
    title = topic_cfg['title']
    title_marker = f'<span class="tp-t">{title}</span>'
    title_pos = html.find(title_marker)
    if title_pos < 0:
        print(f'  ⚠ 제목 없음: {title}')
        return html

    curated_path = os.path.join(CURATED, topic_cfg['curated'])
    curated = json.load(open(curated_path, 'r', encoding='utf-8'))

    # 1) Jenspark 이미지 → r0 섹션(~가 뭐냐면) 닫힌 뒤에
    img_block = render_jenspark(topic_cfg['img_keys'], img_data)
    if img_block:
        r0_end = find_r0_end(html, title_pos)
        if r0_end > 0:
            html = html[:r0_end] + img_block + html[r0_end:]
            print(f'  ✓ 이미지  {title[:35]}')
        else:
            html, ok = inject_at(html, title_pos, '<div class="r0-lbl">', img_block)
            if ok: print(f'  ✓ 이미지(fb)  {title[:35]}')

    # 2) 개념설명 — 사용 안 함 (v4 내용 그대로)

    # 3) Rule + IRAC → 다음 tp-hd 앞에 (또는 class div 끝)
    quiz_items = curated.get('udsl_quiz_raw', [])
    if not quiz_items:
        quiz_items = [FALLBACK_QUIZ.get(topic_cfg['curated'])] if topic_cfg['curated'] in FALLBACK_QUIZ else []
        quiz_items = [q for q in quiz_items if q]
    quiz_item = quiz_items[0] if quiz_items else None
    rule_block = render_rule_irac(curated.get('rule_lines', []), curated.get('topic_label', title), quiz_item)
    if rule_block:
        # 이 토픽 이후 다음 tp-hd 위치
        next_tp = html.find('<div class="tp-hd">', title_pos + len(title_marker))
        if next_tp < 0:
            next_tp = html.find('</div>', title_pos + len(title_marker) + 500)
        if next_tp > 0:
            html = html[:next_tp] + rule_block + html[next_tp:]
            print(f'  ✓ Rule    {title[:35]}')

    return html

# ── 공유용: 이미지 base64 embed ────────────────────────────

def build_share(html: str):
    """PNG → WebP(q=85) base64 embed → 단독 실행 HTML"""
    if not HAS_PIL:
        print('\n⚠ Pillow 없어서 공유용 빌드 스킵 (pip install Pillow)')
        return

    print('\n== 공유용 빌드 (이미지 embed) ==')
    pattern = re.compile(r'src="images/([^"]+\.png)"')
    unique  = sorted(set(pattern.findall(html)))
    cache   = {}

    for fn in unique:
        path = os.path.join(IMG_DIR_SHARE, fn)
        if not os.path.exists(path):
            print(f'  ⚠ 없음: {fn}')
            continue
        buf = io.BytesIO()
        PILImage.open(path).save(buf, format='WEBP', quality=85)
        b64 = base64.b64encode(buf.getvalue()).decode('ascii')
        cache[fn] = f'data:image/webp;base64,{b64}'

    html_out = pattern.sub(
        lambda m: f'src="{cache[m.group(1)]}"' if m.group(1) in cache else m.group(0),
        html
    )

    with open(OUT_SHARE, 'w', encoding='utf-8') as f:
        f.write(html_out)

    mb = os.path.getsize(OUT_SHARE) / 1024 / 1024
    print(f'✅ 공유용: {OUT_SHARE}  ({mb:.1f} MB)')

# ── 메인 ──────────────────────────────────────────────────

QUIZ_DATA     = r'F:\mbe\_extracted\quiz_data.json'
ANSWER_KEY    = r'F:\mbe\_extracted\answer_key.json'
KTK_PRAC_DATA = r'F:\mbe\_extracted\ktk_prac_data.json'
HYPO_DATA     = r'F:\mbe\_extracted\hypo_data.json'

def apply_answer_key(quiz_data):
    """answer_key.json으로 quiz_data의 correct_answer+explanation을 덮어씀.
    AI 스크립트가 quiz_data.json의 정답을 오염시켜도 빌드 시 자동 복원됨."""
    try:
        answer_key = json.load(open(ANSWER_KEY, 'r', encoding='utf-8'))
    except FileNotFoundError:
        print('⚠ answer_key.json 없음 — make_answer_key.py 먼저 실행하세요')
        return quiz_data
    patched = 0
    for section, questions in quiz_data.items():
        ak_section = answer_key.get(section, {})
        for q in questions:
            q_num = str(q['q_num'])
            if q_num in ak_section:
                ak = ak_section[q_num]
                if (q.get('correct_answer') != ak['correct_answer'] or
                        q.get('explanation') != ak['explanation']):
                    q['correct_answer'] = ak['correct_answer']
                    q['explanation']    = ak['explanation']
                    patched += 1
    if patched:
        print(f'🔒 answer_key.json 적용: {patched}개 문항 정답 복원')
    else:
        print(f'✅ answer_key.json 검증 통과 ({sum(len(v) for v in quiz_data.values())}문항 일치)')
    return quiz_data

def main():
    with open(V4_BASE, 'r', encoding='utf-8') as f:
        html = f.read()
    img_data  = json.load(open(IMG_CLS,  'r', encoding='utf-8'))['topic_mapping']
    quiz_data = json.load(open(QUIZ_DATA, 'r', encoding='utf-8'))
    quiz_data = apply_answer_key(quiz_data)
    try:
        ktk_data  = json.load(open(KTK_DATA,  'r', encoding='utf-8'))
        print(f'✅ KTK 데이터 로드 완료')
    except FileNotFoundError:
        ktk_data  = {'ko': {}, 'en': {}}
        print(f'⚠ KTK 데이터 없음 (ktk_parser.py 먼저 실행)')
    try:
        ktk_prac_data = json.load(open(KTK_PRAC_DATA, 'r', encoding='utf-8'))
        total_prac = sum(len(v) for v in ktk_prac_data.values())
        print(f'✅ KTK 문제풀이 데이터 로드 완료 ({total_prac}문제)')
    except FileNotFoundError:
        ktk_prac_data = {}
        print(f'⚠ KTK 문제풀이 데이터 없음 (ktk_prac_parser.py 먼저 실행)')

    # 타이틀
    html = html.replace(
        '<title>Torts 단권화 — KTK Academy 2026</title>',
        '<title>MBE Torts 단권화 v8</title>')
    html = re.sub('Torts 단권화 — KTK Academy 2026', 'MBE Torts 단권화 v8', html)

    # CSS 추가
    html = html.replace('</style>', EXTRA_CSS + '</style>', 1)

    # ── Class 1: 5-section 완성 (Rule만, 이미지는 KTK 섹션 내 배치) ──
    print('== Class 1 ==')
    for t in CL1:
        html = process_topic(html, t, img_data)

    # ── KTK 이론 → 각 챕터 내 삽입 (이미지 인라인 포함) ──────────────────────────
    print('\n== KTK 이론 + 이미지 → 챕터 내 삽입 ==')
    html = inject_ktk_content(html, ktk_data, img_data)

    # ── UDSL 퀴즈 → 각 챕터 내 삽입 ─────────────────────────
    print('\n== UDSL 퀴즈 → 챕터 내 삽입 ==')
    html = inject_quiz_into_chapters(html, quiz_data)

    # ── Practice 탭 + KTK 탭 추가 ───────────────────────────
    # 1) ctab 버튼: Practice + KTK 문제 두 개 추가
    html = html.replace(
        "onclick=\"showCls('cl8')\">Class 8 — Privacy &amp; Defamation</div>",
        "onclick=\"showCls('cl8')\">Class 8 — Privacy &amp; Defamation</div>\n"
        "  <div class=\"ctab\" onclick=\"showCls('practice')\">🎯 Practice</div>\n"
        "  <div class=\"ctab\" onclick=\"showCls('ktk_prac')\">📋 KTK 문제</div>",
        1
    )
    # 2) showCls ids 배열 (practice + ktk_prac 추가)
    html = html.replace(
        "const ids=['cl1','cl2','cl3','cl4','cl5','cl6','cl7','cl8'];",
        "const ids=['cl1','cl2','cl3','cl4','cl5','cl6','cl7','cl8','practice','ktk_prac'];",
        1
    )
    # 3) Practice 탭 cls 섹션 주입
    prac_tab_html = render_practice_tab(quiz_data)
    body_close = html.rfind('</body>')
    html = html[:body_close] + prac_tab_html + html[body_close:]
    print(f'  ✓ Practice 탭 (20문제)')
    # 4) KTK 문제 탭 cls 섹션 주입
    ktk_prac_html = render_ktk_prac_tab(ktk_prac_data, img_data)
    body_close = html.rfind('</body>')
    html = html[:body_close] + ktk_prac_html + html[body_close:]
    # 5) 인터랙티브 JS 삽입 (</body> 바로 앞) — toggleKtkExp 포함
    body_close = html.rfind('</body>')
    html = html[:body_close] + QUIZ_TAB_JS + html[body_close:]
    total_prac_q = sum(len(v) for v in ktk_prac_data.values())
    print(f'  ✓ KTK 문제 탭 ({len(ktk_prac_data)}토픽 / {total_prac_q}문제)')

    # ── tp-hd anchor ID 주입 ──
    html = add_topic_anchors(html)
    anchored = sum(1 for a in TOPIC_ANCHORS.values() if f'id="{a}"' in html)
    print(f'\n== Anchor ID ==')
    print(f'  ✓ {anchored}/{len(TOPIC_ANCHORS)}개 토픽에 id 추가됨')

    # ── 구 퀴즈 섹션 (하단 append) 제거 → 탭으로 이전됨 ──
    # render_quiz_section은 탭 구조로 대체됨

    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(html)

    kb = os.path.getsize(OUT) // 1024
    print(f'\n✅ 내 것: {OUT}  ({kb} KB)')

    # ── 공유용 standalone 빌드 ──────────────────────────────
    build_share(html)

if __name__ == '__main__':
    main()
