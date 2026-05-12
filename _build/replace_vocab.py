import sys
sys.stdout.reconfigure(encoding='utf-8')

new_vocab = '''<div class="p4-panel" id="p4p-vocab">
<style>
/* vocab panel */
.vp-sec{margin:0 0 14px;}
.vp-sec-hd{font-size:.72rem;font-weight:700;color:#fff;background:#3949ab;padding:3px 10px;border-radius:4px;display:inline-block;margin:10px 0 6px;}
.vp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:6px;}
.vp-card{border:1px solid #c5cae9;border-radius:6px;padding:7px 10px;cursor:pointer;user-select:none;transition:.15s;background:#fff;}
.vp-card:hover{background:#f0f4ff;}
.vp-en{font-weight:700;color:#1a1a8c;font-size:10pt;}
.vp-ko{font-size:9pt;color:#555;margin-top:1px;}
.vp-ex{font-size:8.5pt;color:#333;margin-top:5px;border-top:1px dashed #c5cae9;padding-top:4px;display:none;line-height:1.55;}
.vp-card.open .vp-ex{display:block;}
/* essay phrases */
.ep-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:6px;}
.ep-card{border:1px solid #b2dfdb;border-radius:6px;padding:7px 10px;cursor:pointer;user-select:none;background:#fff;transition:.15s;}
.ep-card:hover{background:#e0f7fa;}
.ep-phrase{font-weight:700;color:#00695c;font-size:9.5pt;}
.ep-ko{font-size:9pt;color:#555;margin-top:1px;}
.ep-ex{font-size:8.5pt;color:#333;margin-top:5px;border-top:1px dashed #b2dfdb;padding-top:4px;display:none;line-height:1.55;}
.ep-card.open .ep-ex{display:block;}
</style>
<p style="font-size:.75rem;color:#555;margin:4px 0 2px;">📌 카드 클릭 → 예시·설명 펼침</p>

<div class="vp-sec">
<span class="vp-sec-hd">📖 팩트패턴 독해 어휘</span>
<div class="vp-grid">

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">apprehension</div><div class="vp-ko">두려움, 우려 (신체 접촉에 대한)</div>
<div class="vp-ex">Assault requires P's <em>apprehension</em> of imminent contact — not fear of future harm.<br>→ 즉각적인 접촉에 대한 심리적 인식. 실제 두려움 필요 없음.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">imminent</div><div class="vp-ko">임박한, 즉각적인</div>
<div class="vp-ex">"I'll hurt you tomorrow" = NOT <em>imminent</em>.<br>→ 미래 협박은 assault 불성립. 지금 당장(now)이어야 함.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">confinement</div><div class="vp-ko">구금, 감금</div>
<div class="vp-ex">False imprisonment requires intentional <em>confinement</em> with no reasonable escape.<br>→ 합리적 탈출 방법이 있으면 불성립.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">outrageous</div><div class="vp-ko">극도로 터무니없는, 상식을 벗어난</div>
<div class="vp-ex">IIED needs "extreme and <em>outrageous</em>" conduct — mere rudeness ≠ outrageous.<br>→ 무례함·모욕은 부족. 사회 상식을 완전히 벗어난 행위만 해당.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">provocation</div><div class="vp-ko">도발, 자극</div>
<div class="vp-ex">"Without any <em>provocation</em>..." = D acted without P doing anything first.<br>→ 시험에서 '정당한 이유 없이'를 표현할 때 자주 등장.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">encroachment</div><div class="vp-ko">침범, (경계선) 침입</div>
<div class="vp-ex">Building a garage 1 foot over the property line = trespass by <em>encroachment</em>.<br>→ Trespass to land: 의도적 위치에 지었으면 경계선 몰라도 성립.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">ordinance</div><div class="vp-ko">조례 (지방법)</div>
<div class="vp-ex">City <em>ordinance</em> prohibiting parking near hydrants → negligence per se if violated.<br>→ 연방법(statute)과 구별. 지자체가 만든 규정.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">foreseeable</div><div class="vp-ko">예견 가능한</div>
<div class="vp-ex">Proximate cause requires the harm be <em>foreseeable</em> at the time of breach.<br>→ 예견 불가능한 피해 → proximate cause 단절 가능.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">contemporaneously</div><div class="vp-ko">동시에, 그 순간에</div>
<div class="vp-ex">NIED bystander: P must witness the accident <em>contemporaneously</em>, not arrive after.<br>→ 전화로 소식 듣고 나중에 도착 = 요건 미충족.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">indivisible</div><div class="vp-ko">불가분의 (나눌 수 없는)</div>
<div class="vp-ex">Joint &amp; several liability applies when injury is <em>indivisible</em> between multiple Ds.<br>→ 한 명에게 전액 청구 가능 → 기여금 구상권 행사.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">insolvent</div><div class="vp-ko">지급불능, 파산 상태</div>
<div class="vp-ex">"Yes, but only if County is <em>insolvent</em>" = wrong answer (J&amp;S doesn't require insolvency).<br>→ Joint &amp; several: 다른 D가 지급능력 있어도 전액 청구 가능.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">altercation</div><div class="vp-ko">언쟁, 몸싸움</div>
<div class="vp-ex">"An <em>altercation</em> arose from a seating dispute" — flight attendant battery hypo.<br>→ 구두 다툼부터 신체 충돌까지 포함. intentional tort 문제에 자주 등장.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">chattel</div><div class="vp-ko">동산 (개인 재산)</div>
<div class="vp-ex">Trespass to <em>chattel</em> = intermeddling with personal property. Compare: conversion.<br>→ 부동산(land) 제외 개인 소유물 전체. 자동차·가방 등 포함.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">taunting / heckler</div><div class="vp-ko">야유하기 / 야유꾼</div>
<div class="vp-ex">"Spectators were <em>taunting</em> the pitcher… one of the <em>hecklers</em> was struck."<br>→ Dylan Q24 팩트패턴 핵심 단어. intent = 접촉 의도만 있으면 OK.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">rebuttable presumption</div><div class="vp-ko">반증 가능한 추정</div>
<div class="vp-ex">Res ipsa creates a <em>rebuttable presumption</em> of negligence — D can still rebut it.<br>→ 반박 증거 없으면 과실 추정. "inference" vs "conclusive" 구별.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">invitee / licensee / trespasser</div><div class="vp-ko">초대방문자 / 허락방문자 / 무단침입자</div>
<div class="vp-ex"><em>Invitee</em>: highest duty (inspect + warn). <em>Licensee</em>: warn of known dangers. <em>Trespasser</em>: no willful/wanton harm.<br>→ 방문자 지위가 의무 수준 결정.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">vicarious liability</div><div class="vp-ko">대위/간접 책임</div>
<div class="vp-ex">Employer's <em>vicarious liability</em> for employee's tort = respondeat superior.<br>→ 고용인의 행위가 scope of employment 내 → 고용주 책임.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">privity</div><div class="vp-ko">계약 당사자 관계</div>
<div class="vp-ex">Strict products liability: <em>privity</em> NOT required. Any foreseeable user can sue.<br>→ "Annie didn't buy from manufacturer" 는 틀린 선지의 패턴.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">defamatory statement</div><div class="vp-ko">명예를 훼손하는 진술</div>
<div class="vp-ex">A statement is <em>defamatory</em> if it tends to harm P's reputation in the community.<br>→ Publication = 제3자에게 전달(의도적·과실). Tom이 없어도 성립.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">notwithstanding</div><div class="vp-ko">~에도 불구하고</div>
<div class="vp-ex">"<em>Notwithstanding</em> the warning sign, Rocker drove up the driveway."<br>→ 에세이·팩트패턴 모두 자주 등장. "despite" = 동의어.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">verdict / JNOV</div><div class="vp-ko">평결 / 평결 불구 판결</div>
<div class="vp-ex">JNOV = judgment <em>notwithstanding the verdict</em>: judge overrides jury when no reasonable jury could decide that way.<br>→ Darcy Q47: 합리적 배심원이 다른 결론 낼 수 없어야 JNOV 인용.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">scope of employment</div><div class="vp-ko">업무 범위 (고용 범위)</div>
<div class="vp-ex">Employer liable only if employee acted within <em>scope of employment</em>.<br>→ 출퇴근 중 사고(frolic)는 제외. 업무 관련 detour는 포함.</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">anesthetized</div><div class="vp-ko">마취된</div>
<div class="vp-ex">"Once Player was <em>anesthetized</em>, Medic asked Surgeon to perform the surgery."<br>→ 동의 범위 초과 → battery 성립 (Q104).</div></div>

<div class="vp-card" onclick="this.classList.toggle('open')">
<div class="vp-en">malfunction / defect</div><div class="vp-ko">오작동 / 결함</div>
<div class="vp-ex">Manufacturing <em>defect</em>: specific unit deviates from design (blender blade).<br>Design <em>defect</em>: entire product line dangerous → RAD needed.</div></div>

</div><!-- /vp-grid -->
</div><!-- /vp-sec -->

<div class="vp-sec">
<span class="vp-sec-hd">✍️ 에세이 필수 표현</span>
<div class="ep-grid">

<div class="ep-card" onclick="this.classList.toggle('open')">
<div class="ep-phrase">The issue is whether [D] is liable for [tort]</div>
<div class="ep-ko">Issue 시작 공식</div>
<div class="ep-ex">예: "The issue is whether Dylan is liable for battery when he intentionally threw the ball toward the stands."</div></div>

<div class="ep-card" onclick="this.classList.toggle('open')">
<div class="ep-phrase">Under [rule], a plaintiff must show…</div>
<div class="ep-ko">Rule 도입 공식</div>
<div class="ep-ex">예: "Under battery, a plaintiff must show (1) an intentional act (2) causing harmful or offensive contact (3) with the plaintiff's person."</div></div>

<div class="ep-card" onclick="this.classList.toggle('open')">
<div class="ep-phrase">Here / In the case at bar</div>
<div class="ep-ko">Application 시작 — 본 사안에서</div>
<div class="ep-ex">"<em>Here</em>, Dylan deliberately threw the ball toward the hecklers." — 팩트를 법리에 적용할 때 시작하는 표현.</div></div>

<div class="ep-card" onclick="this.classList.toggle('open')">
<div class="ep-phrase">Therefore / Thus / Accordingly</div>
<div class="ep-ko">결론 도출 — 따라서</div>
<div class="ep-ex">"<em>Therefore</em>, Dylan is liable for battery." / "<em>Accordingly</em>, P will prevail." — Conclusion 마무리.</div></div>

<div class="ep-card" onclick="this.classList.toggle('open')">
<div class="ep-phrase">However / Nevertheless / Nonetheless</div>
<div class="ep-ko">역접 — 그러나</div>
<div class="ep-ex">"<em>However</em>, the fact that Dylan did not expect the ball to pierce the fence does not negate his intent." — 반론 제거 시 사용.</div></div>

<div class="ep-card" onclick="this.classList.toggle('open')">
<div class="ep-phrase">Although / While / Even though</div>
<div class="ep-ko">양보 — ~이지만 / ~에도 불구하고</div>
<div class="ep-ex">"<em>Although</em> Daniel did not know the garage crossed the property line, he intentionally built it at that location."</div></div>

<div class="ep-card" onclick="this.classList.toggle('open')">
<div class="ep-phrase">This element is satisfied because…</div>
<div class="ep-ko">요소 충족 확인</div>
<div class="ep-ex">"<em>This element is satisfied because</em> Dylan intended to make contact with the hecklers when he threw the ball."</div></div>

<div class="ep-card" onclick="this.classList.toggle('open')">
<div class="ep-phrase">This element is not met because…</div>
<div class="ep-ko">요소 미충족 확인</div>
<div class="ep-ex">"<em>This element is not met because</em> Helen did not witness the accident contemporaneously — she arrived only after the fact."</div></div>

<div class="ep-card" onclick="this.classList.toggle('open')">
<div class="ep-phrase">D will argue that… / P will counter that…</div>
<div class="ep-ko">양측 주장 제시</div>
<div class="ep-ex">"<em>D will argue that</em> the warning sign was sufficient to cut off liability. <em>P will counter that</em> assumption of risk does not bar recovery here."</div></div>

<div class="ep-card" onclick="this.classList.toggle('open')">
<div class="ep-phrase">On balance / On the whole / In sum</div>
<div class="ep-ko">종합 결론</div>
<div class="ep-ex">"<em>On balance</em>, because all elements are satisfied and no valid defense applies, P will likely prevail on the battery claim."</div></div>

<div class="ep-card" onclick="this.classList.toggle('open')">
<div class="ep-phrase">absent [X] / but for [X]</div>
<div class="ep-ko">~이 없었다면 / ~가 아니었다면</div>
<div class="ep-ex">"<em>But for</em> Donna's illegal parking, Paul would not have been injured." — 인과관계 분석 핵심 표현.</div></div>

<div class="ep-card" onclick="this.classList.toggle('open')">
<div class="ep-phrase">prima facie case</div>
<div class="ep-ko">일응의 입증 / 표면상 유효한 청구</div>
<div class="ep-ex">"To establish a <em>prima facie case</em> of negligence, P must prove duty, breach, causation, and damages."</div></div>

<div class="ep-card" onclick="this.classList.toggle('open')">
<div class="ep-phrase">in light of / given that</div>
<div class="ep-ko">~을 고려하면 / ~이기 때문에</div>
<div class="ep-ex">"<em>In light of</em> the jury's finding, no reasonable jury could have found for Darcy." — 사실 인정을 근거로 논리 전개.</div></div>

<div class="ep-card" onclick="this.classList.toggle('open')">
<div class="ep-phrase">Moreover / Furthermore / In addition</div>
<div class="ep-ko">추가 논거 — 더욱이 / 게다가</div>
<div class="ep-ex">"<em>Moreover</em>, even if intent is disputed, the transferred intent doctrine would apply." — 논거 보강 시 사용.</div></div>

<div class="ep-card" onclick="this.classList.toggle('open')">
<div class="ep-phrase">to the extent that / insofar as</div>
<div class="ep-ko">~하는 한도 내에서</div>
<div class="ep-ex">"<em>To the extent that</em> Miller's conduct was motivated by a purpose to serve the employer, liability may attach." — 조건부 결론.</div></div>

<div class="ep-card" onclick="this.classList.toggle('open')">
<div class="ep-phrase">it is important to note that…</div>
<div class="ep-ko">주목할 점은 ~이다</div>
<div class="ep-ex">"<em>It is important to note that</em> a warning does not cure a design defect under products liability." — 오답 유도 포인트를 짚을 때.</div></div>

</div><!-- /ep-grid -->
</div><!-- /vp-sec -->

</div>'''

with open(r'F:\mbe\index.html', encoding='utf-8') as f:
    content = f.read()

# Find the old p4p-vocab div and replace its contents
# The div starts with <div class="p4-panel" id="p4p-vocab">
# and ends with </div> before the next closing div (</div></div></div>)

# Find start
start_marker = '<div class="p4-panel" id="p4p-vocab">'
end_marker = '\n</div>\n</div>\n</div>\n<div id="cl1"'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

print(f'start: {start_idx}, end: {end_idx}')

if start_idx == -1 or end_idx == -1:
    print('ERROR: markers not found')
else:
    old = content[start_idx:end_idx]
    print(f'replacing {len(old)} chars')
    content = content[:start_idx] + new_vocab + content[end_idx:]
    with open(r'F:\mbe\index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('DONE')
