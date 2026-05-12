"""
builder_v7.py — UDSL 풀 콘텐츠 v7 빌더 (Class 1, 5 토픽)

원칙 (환각 0):
  - 슬라이드 raw 텍스트 그대로
  - 김윤상 Rule docx 그대로
  - 정답 미정인 옵션은 'selected' 회색 표시 (정답 추론 X)
"""
import re, json, os, sys

V4_BASE = r'F:\mbe\_archive\Torts_단권화_v4_base.html'
RULES   = r'F:\mbe\_extracted\torts_rules_raw.json'
IMG_CLS = r'F:\mbe\_extracted\image_classification.json'
OUT     = r'F:\mbe\Torts_단권화_v7.html'
CURATED_DIR = r'F:\mbe\_extracted\udsl_ppt'

# image_classification.json 키 alias (Class 2~8 topic_key → 이미지 키)
IMG_KEY_ALIAS = {
    'cl2_intent_defenses': 'consent',
    'cl3_neg_duty_breach':  'breach',
    'cl4_causation_harm':   'causation',
    'cl5_neg_defenses':     'comp_neg',
    'cl7_property_torts':   'property_torts',
    'cl8_defam_privacy':    'privacy',
    # cl6_strict_liability → 이미지 없음 (젠스파크 미생성)
}

CLASSES = {
    'cl1': [
        ('class01_battery',       1, 'Battery (폭행)'),
        ('class01_assault',       2, 'Assault (협박)'),
        ('class01_fi',            3, 'False Imprisonment (불법감금)'),
        ('class01_iied',          4, 'IIED (정신적 고통의 고의)'),
        ('class01_trespass_land', 5, 'Trespass to Land (토지 침입) — 도입'),
    ],
    'cl2': [('cl2', 1, 'Class 2 통합 (의도 II + Defenses)')],
    'cl3': [('cl3', 1, 'Class 3 통합 (Negligence Duty + Breach)')],
    'cl4': [('cl4', 1, 'Class 4 통합 (Causation + Harm)')],
    'cl5': [('cl5', 1, 'Class 5 통합 (Defenses to Negligence)')],
    'cl6': [('cl6', 1, 'Class 6 통합 (Strict Liability)')],
    'cl7': [('cl7', 1, 'Class 7 통합 (Property Torts)')],
    'cl8': [('cl8', 1, 'Class 8 통합 (Defamation + Privacy)')],
    'cl_async': [],
}

TAB_LABELS = {
    'cl1':'C1 의도 I', 'cl2':'C2 의도II/Def', 'cl3':'C3 Neg I', 'cl4':'C4 Neg II',
    'cl5':'C5 Defenses', 'cl6':'C6 SL', 'cl7':'C7 Property', 'cl8':'C8 Defam·Priv',
    'cl_async':'Async PL'
}

def read(p):
    with open(p, 'r', encoding='utf-8') as f: return f.read()
def write(p, s):
    with open(p, 'w', encoding='utf-8') as f: f.write(s)
def jread(p):
    with open(p, 'r', encoding='utf-8') as f: return json.load(f)

def render_figs(file_list, cls_prefix, label_prefix):
    if not file_list: return ''
    h = ''
    for f in file_list:
        h += f'<figure class="topic-fig"><figcaption class="topic-cap">{label_prefix}</figcaption><img class="topic-img {cls_prefix}" src="images/{f}" loading="lazy" alt="{label_prefix}"></figure>\n'
    return h

def esc_attr(s):
    return s.replace("'", "&#39;").replace('"', '&quot;')

def html_safe(s):
    """HTML 특수문자 escape (텍스트만)."""
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def render_topic_full(curated, num, img_data, rules):
    key = curated['topic_key']
    img_key = IMG_KEY_ALIAS.get(key, key)
    imgs = img_data.get(img_key, {})

    ko_figs = (
        render_figs([imgs['ko_info']] if 'ko_info' in imgs else [], 'info-ko', '🇰🇷 한글 개념도') +
        render_figs([imgs['ko_prac']] if 'ko_prac' in imgs else [], 'hypo-ko', '🇰🇷 한글 사례')
    )
    en_figs = (
        render_figs([imgs['en_info']] if 'en_info' in imgs else [], 'info-en', '🇺🇸 English Concept') +
        render_figs([imgs['en_prac']] if 'en_prac' in imgs else [], 'hypo-en', '🇺🇸 English Case')
    )

    ko_intro = curated.get('ko_intro_candidate', '')

    # sub-sections (슬라이드 텍스트 raw)
    sub_html = ''
    for sec in curated.get('sub_sections', []):
        title_en = html_safe(sec.get('title_en', '(제목 없음)'))
        title_ko = html_safe(sec.get('title_ko', ''))
        en = html_safe(sec.get('content_en', '')).replace('\n', '<br>')
        ko = html_safe(sec.get('content_ko', '')).replace('\n', '<br>')
        slides_str = ', '.join(map(str, sec.get('slides', [])))
        ko_part = f'<div class="udsl-sub-ko-body"><div class="udsl-lang-lbl">🇰🇷 KO (슬라이드 한국어 코멘트)</div>{ko}</div>' if ko else ''
        title_ko_part = f'<span class="udsl-sub-ko"> · {title_ko}</span>' if title_ko else ''
        sub_html += f'''
<div class="udsl-sub">
  <h3 class="udsl-sub-hd">{title_en}{title_ko_part} <span class="udsl-slide-ref">슬라이드 {slides_str}</span></h3>
  <div class="udsl-sub-body">
    <div class="udsl-sub-en"><div class="udsl-lang-lbl">🇺🇸 EN (UDSL slide raw)</div>{en}</div>
    {ko_part}
  </div>
</div>'''

    # Rule (김윤상 docx)
    rule_html = '<div class="r3 rule-box"><div class="rule-hd">⚖ Rule Statement (김윤상 정리본 그대로)</div>'
    for rl in curated.get('rule_lines', []):
        rule_html += f'<div class="rule-line"><b>#{rl["idx"]}:</b> {html_safe(rl["text"])}</div>'
    rule_html += '</div>'

    # UDSL 퀴즈 (raw)
    quiz_html = ''
    quiz_items = curated.get('udsl_quiz_raw', [])
    if quiz_items:
        quiz_html = '<div class="mcq-section-hd">📝 UDSL 객관식 — 슬라이드 그대로 <span class="mcq-bdg">옵션 클릭 → 표시</span></div>\n'
        for i, q in enumerate(quiz_items):
            qid = q.get('id') or f'q{i+1}'
            qid = re.sub(r'[^a-zA-Z0-9_]', '', qid) or f'q{i+1}'
            q_en = html_safe(q.get('q_en_raw', '')).replace('\n', '<br>')
            q_ko = html_safe(q.get('q_ko_raw', '')).replace('\n', '<br>')
            q_ko_part = f'<div class="q-ko">{q_ko}</div>' if q_ko else ''
            opts_html = ''
            for opt in q.get('options', []):
                correct = opt.get('correct')
                if correct is True:
                    correct_js = 'true'
                elif correct is False:
                    correct_js = 'false'
                else:
                    correct_js = 'null'
                label = html_safe(opt.get('label', ''))
                text = html_safe(opt.get('text', ''))
                opts_html += f'<div class="mcq-opt" onclick="ans(this,{correct_js},\'{key}_{qid}\')"><b>{label}</b>. {text}</div>'
            notes = html_safe(q.get('notes', '')).replace('\n', '<br>')
            notes_part = f'<div class="mcq-exp"><b>노트:</b> {notes}</div>' if notes else ''
            quiz_html += f'''
<div class="mcq-box" id="box_{key}_{qid}">
  <div class="mcq-q"><span class="mcq-qnum">Q{i+1}</span>
    <div class="mcq-q-body"><div class="q-en">{q_en}</div>{q_ko_part}</div>
  </div>
  <div class="mcq-opts">{opts_html}</div>
  {notes_part}
</div>'''

    ko_intro_safe = html_safe(ko_intro)
    ko_intro_part = f'<div class="r0-txt">{ko_intro_safe}</div>' if ko_intro else '<div class="r0-txt slot-empty">한국어 도입 자료 없음 (슬라이드 raw 한글 코멘트는 아래 sub-section에서 확인)</div>'

    return f'''
<div class="topic" data-topic="{key}">
  <div class="sec-hd"><span class="tp-n">{num}</span><span class="tp-t">{html_safe(curated["topic_label"])}</span><span class="tp-s">{html_safe(curated["stars"])}</span></div>

  <!-- 0회독: 한글 도식 + 한글 코멘트 -->
  <div class="r0 sec-ko-imgs"><div class="img-region">{ko_figs}</div></div>
  <div class="r0 sec-desc">
    <div class="r0-lbl">0회독 — 한국어 코멘트 (김윤상 슬라이드)</div>
    {ko_intro_part}
  </div>

  <!-- 1회독: 영문 도식 + UDSL 슬라이드 raw 본문 -->
  <div class="r1 sec-en-imgs"><div class="img-region">{en_figs}</div></div>
  <div class="r1 sec-content">{sub_html}</div>

  <!-- 3회독: Rule (김윤상 docx) -->
  {rule_html}

  <!-- 1회독: UDSL 퀴즈 (raw) -->
  <div class="r1 sec-quiz">{quiz_html}</div>

  <div class="oops-wrap" id="slot-oops-{key}">
    <div class="slot-empty">📕 오답 노트</div>
  </div>
</div>'''

def render_placeholder_class(label):
    return f'''<div class="topic placeholder">
  <div class="sec-hd"><span class="tp-n">⏳</span><span class="tp-t">{label}</span><span class="tp-s">미완료</span></div>
  <div class="r1" style="padding:2rem;text-align:center;color:#888;">
    <p>📋 다음 Class 진행 시 UDSL 슬라이드 추출 → curated.json → 빌드</p>
  </div>
</div>'''

def build():
    v4 = read(V4_BASE)
    rules = jread(RULES)
    img_data = jread(IMG_CLS)['topic_mapping']

    css = re.search(r'<style>(.*?)</style>', v4, re.DOTALL).group(1)
    extra_css = '''
.placeholder{opacity:.6;}
.udsl-sub{margin:1rem 0;border-left:3px solid var(--acc);padding:.6rem .9rem;background:#fafaf8;border-radius:5px;}
.udsl-sub-hd{margin:0 0 .5rem;color:var(--acc);font-size:.95rem;}
.udsl-sub-ko{font-weight:400;color:#666;font-size:.85rem;}
.udsl-slide-ref{float:right;font-size:.7rem;color:#999;font-weight:400;}
.udsl-sub-body{display:grid;grid-template-columns:1fr 1fr;gap:.8rem;}
.udsl-sub-en,.udsl-sub-ko-body{font-size:.85rem;line-height:1.6;}
.udsl-sub-en{background:#eef4f9;padding:.5rem .7rem;border-radius:4px;}
.udsl-sub-ko-body{background:#fef9ec;padding:.5rem .7rem;border-radius:4px;}
.udsl-lang-lbl{font-size:.68rem;color:#888;font-weight:700;margin-bottom:.3rem;}
@media (max-width:780px){.udsl-sub-body{grid-template-columns:1fr;}}

.rule-hd{font-size:.78rem;color:var(--gold);margin-bottom:.5rem;font-weight:700;}
.rule-line{font-size:.85rem;margin:.4rem 0;color:#eee;line-height:1.5;}
.rule-line b{color:var(--gold);}

.mcq-section-hd{background:#2c2c2a;color:#fff;padding:.55rem 1.1rem;font-size:.85rem;font-weight:700;display:flex;align-items:center;gap:8px;margin-top:1rem;border-radius:6px 6px 0 0;}
.mcq-bdg{font-size:.65rem;background:var(--acc2);padding:.15rem .5rem;border-radius:4px;}
.mcq-box{background:#fff;border:1px solid var(--brd);padding:.8rem 1rem;margin:.5rem 0;border-radius:6px;}
.mcq-q{display:flex;gap:.6rem;align-items:flex-start;margin-bottom:.6rem;}
.mcq-qnum{display:inline-block;background:var(--acc);color:#fff;padding:.15rem .5rem;border-radius:4px;font-size:.78rem;font-weight:700;flex-shrink:0;}
.mcq-q-body{flex:1;}
.q-en{font-weight:500;line-height:1.55;}
.q-ko{font-style:italic;color:#666;font-size:.85rem;line-height:1.5;margin-top:.3rem;}
.mcq-opts{display:flex;flex-direction:column;gap:.3rem;}
.mcq-opt{padding:.5rem .8rem;background:#fafaf8;border:1px solid #e0ddd5;border-radius:5px;cursor:pointer;font-size:.86rem;transition:background .15s;}
.mcq-opt:hover{background:#fff8e6;}
.mcq-opt.correct{background:#e7f5e2;border-color:#4a8f4a;color:#1b5e20;}
.mcq-opt.wrong{background:#fde7e7;border-color:#c8472a;color:#a52020;}
.mcq-opt.selected{background:#e8e8e8;border-color:#888;color:#333;}
.mcq-exp{display:none;background:#fff8e6;border-left:3px solid var(--gold);padding:.5rem .8rem;font-size:.82rem;line-height:1.55;margin-top:.5rem;border-radius:4px;}
.mcq-box[data-done] .mcq-exp{display:block;}

.img-region{margin:.6rem 0;display:flex;flex-direction:column;gap:.8rem;align-items:flex-start;}
.topic-fig{margin:0;display:flex;flex-direction:column;align-items:flex-start;max-width:520px;width:100%;}
.topic-cap{font-size:.78rem;color:#666;margin-bottom:.3rem;font-weight:600;}
.topic-img{max-width:520px;max-height:580px;width:100%;height:auto;display:block;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,.08);}
.topic-img.info-ko,.topic-img.hypo-ko{border:2px solid #4a8f4a;}
.topic-img.info-en,.topic-img.hypo-en{border:2px solid var(--acc);}
body.m0 .topic-img.info-en,body.m0 .topic-img.hypo-en{opacity:.15;}
body.m1 .topic-img{opacity:1;}
body.m2 .topic-img,body.m3 .topic-img{opacity:.18;}
body.m4 .img-region{display:none;}
body.mQE .img-region,body.mQK .img-region{display:none;}

.mbt-bar{position:fixed!important;top:62px;right:14px;z-index:60;display:flex!important;flex-direction:column;gap:4px;background:rgba(255,255,255,.97);border:1.5px solid var(--brd);border-radius:10px;padding:7px;box-shadow:0 4px 14px rgba(0,0,0,.12);width:118px;}
.mbt-bar .mbt{padding:.42rem .7rem;font-size:.78rem;border:1px solid #d0c7b3;background:#fafaf8;color:#333;border-radius:5px;cursor:pointer;text-align:left;width:100%;font-weight:500;}
.mbt-bar .mbt:hover{background:#fff8e6;border-color:var(--gold);}
.mbt-bar .mbt.on{background:var(--acc);color:#fff;border-color:var(--acc);font-weight:700;}
body{padding-right:144px;}
.ctabs{max-width:calc(100vw - 160px);}
@media (max-width:900px){body{padding-right:0;}.mbt-bar{position:sticky!important;top:54px;right:auto;flex-direction:row;width:100%;border-radius:0;}.mbt-bar .mbt{flex:1;text-align:center;font-size:.74rem;}.ctabs{max-width:100%;}}

.panel-quiz{display:none;padding:1rem .9rem 4rem;max-width:1060px;margin:0 auto;}
body.mQE .ctabs,body.mQK .ctabs{display:none!important;}
body.mQE .cls,body.mQK .cls{display:none!important;}
body.mQE .panel4,body.mQK .panel4{display:none!important;}
body.mQE .panel-quiz.qe,body.mQK .panel-quiz.qk{display:block!important;}
'''

    # JS
    v4_js = re.search(r'<script>(.*?)</script>', v4, re.DOTALL).group(1)
    v4_js = re.sub(r'function\s+setMode\s*\([^)]*\)\s*\{.*?\n\}\s*', '', v4_js, count=1, flags=re.DOTALL)
    v4_js = re.sub(r'function\s+showCls\s*\([^)]*\)\s*\{.*?\n\}\s*', '', v4_js, count=1, flags=re.DOTALL)
    v4_js = re.sub(r'function\s+ans\s*\([^)]*\)\s*\{.*?\n\}\s*', '', v4_js, count=1, flags=re.DOTALL)
    v4_js = re.sub(r'window\.onload\s*=\s*function\s*\(\s*\)\s*\{[^}]*\}\s*;?\s*', '', v4_js, flags=re.DOTALL)

    js = '<script>\n' + v4_js + '''
function setMode(n){
  document.body.className='m'+n;
  var btns=document.querySelectorAll('.mbt');
  btns.forEach(function(b){b.classList.remove('on');});
  var map={'0':0,'1':1,'2':2,'3':3,'4':4,'QE':5,'QK':6};
  var idx=map[String(n)];
  if(idx!==undefined&&btns[idx]) btns[idx].classList.add('on');
  if(n===4 && typeof buildFC==='function') buildFC();
}
function showCls(id){
  document.querySelectorAll('.cls').forEach(function(c){c.classList.remove('on');});
  var t=document.getElementById(id); if(t) t.classList.add('on');
  document.querySelectorAll('.ctab').forEach(function(b){b.classList.remove('on');});
  var ids=['cl1','cl2','cl3','cl4','cl5','cl6','cl7','cl8','cl_async'];
  var i=ids.indexOf(id); var btns=document.querySelectorAll('.ctab');
  if(i>=0&&btns[i]) btns[i].classList.add('on');
  window.scrollTo(0,0);
}
function ans(el, correct, qid){
  var box = document.getElementById('box_'+qid);
  if(!box || box.dataset.done) return;
  box.dataset.done = '1';
  box.querySelectorAll('.mcq-opt').forEach(function(o){
    o.style.pointerEvents = 'none';
  });
  if(correct === null){
    el.classList.add('selected');
  } else if(correct === true){
    el.classList.add('correct');
  } else {
    el.classList.add('wrong');
  }
}
window.onload=function(){setMode(1);showCls('cl1');};
</script>'''

    btn_bar = '''
<div class="mbt-bar">
  <button class="mbt" onclick="setMode(0)">0회독</button>
  <button class="mbt on" onclick="setMode(1)">1회독</button>
  <button class="mbt" onclick="setMode(2)">2회독</button>
  <button class="mbt" onclick="setMode(3)">3회독</button>
  <button class="mbt" onclick="setMode(4)">4회독 실전</button>
  <button class="mbt" onclick="setMode('QE')">퀴즈 영어</button>
  <button class="mbt" onclick="setMode('QK')">퀴즈 한글</button>
</div>'''

    tabs = '<div class="ctabs">'
    for ck, lbl in TAB_LABELS.items():
        on = ' on' if ck == 'cl1' else ''
        tabs += f'<button class="ctab{on}" onclick="showCls(\'{ck}\')">{lbl}</button>'
    tabs += '</div>'

    class_divs = ''
    for ck, topics in CLASSES.items():
        on = ' on' if ck == 'cl1' else ''
        body = ''
        if topics:
            for t in topics:
                key, num, label = t
                curated_path = os.path.join(CURATED_DIR, f'{key}_curated.json')
                if os.path.exists(curated_path):
                    curated = jread(curated_path)
                    body += render_topic_full(curated, num, img_data, rules)
                else:
                    body += render_placeholder_class(label)
        else:
            body = render_placeholder_class(TAB_LABELS.get(ck, ck))
        class_divs += f'<div id="{ck}" class="cls{on}">{body}</div>'

    panel4 = '<div class="panel4"><div style="text-align:center;padding:2rem;"><h2>4회독 — 플래시카드 (Class 1 검수 후)</h2></div></div>'
    quiz_qe = '<div class="panel-quiz qe"><div style="text-align:center;padding:2rem;"><h2>퀴즈 영어</h2><p>UDSL Hypo PDF 추출 후 빌드</p></div></div>'
    quiz_qk = '<div class="panel-quiz qk"><div style="text-align:center;padding:2rem;"><h2>퀴즈 한국어</h2><p>UDSL Hypo PDF 한글판 빌드</p></div></div>'

    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>MBE Torts 단권화 v7 — UDSL Class 1 풀</title>
<style>{css}{extra_css}</style>
</head>
<body class="m1">
<header style="background:var(--acc);color:#fff;padding:.7rem 1rem;position:sticky;top:0;z-index:50;box-shadow:0 2px 6px rgba(0,0,0,.15);">
  <h1 style="margin:0;font-size:1.1rem;">MBE Torts 단권화 v7 — UDSL Class 1 풀 콘텐츠 (raw, 환각 0)</h1>
  <div style="font-size:.78rem;opacity:.85;margin-top:2px;">DC Bar Legacy UBE July 2027 / UDSL VanZandt 2026</div>
</header>
{btn_bar}
{tabs}
{class_divs}
{panel4}
{quiz_qe}
{quiz_qk}
{js}
</body>
</html>'''

    write(OUT, html)
    print(f'OK built: {OUT} ({os.path.getsize(OUT)//1024} KB)')

if __name__ == '__main__':
    build()
