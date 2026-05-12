import sys
sys.stdout.reconfigure(encoding='utf-8')

vocab_panel = """<div class="p4-panel" id="p4p-vocab">
<style>
.voc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:7px;margin:6px 0 10px;}
.voc-card{border:1px solid #c5cae9;border-radius:6px;padding:8px 10px;cursor:pointer;user-select:none;transition:.15s;}
.voc-card:hover{background:#f0f4ff;}
.voc-en{font-weight:700;color:#1a1a8c;font-size:10.5pt;}
.voc-ko{font-size:9.5pt;color:#555;margin-top:2px;}
.voc-def{font-size:9pt;color:#222;margin-top:5px;line-height:1.55;border-top:1px dashed #c5cae9;padding-top:4px;display:none;}
.voc-card.open .voc-def{display:block;}
.voc-cat{font-size:9pt;font-weight:700;color:#fff;background:#3949ab;padding:3px 9px;border-radius:4px;margin:10px 0 4px;display:inline-block;}
</style>
<p style="font-size:.8rem;color:#555;margin-bottom:6px;">📌 카드 클릭 → 정의 펼쳐짐</p>

<span class="voc-cat">Intentional Torts</span>
<div class="voc-grid">
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Assault</div><div class="voc-ko">폭행(위협)</div><div class="voc-def">Intentional act causing plaintiff's reasonable apprehension of imminent harmful or offensive contact.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Battery</div><div class="voc-ko">구타(접촉)</div><div class="voc-def">Intentional act causing harmful or offensive contact with plaintiff's person.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">False Imprisonment</div><div class="voc-ko">불법 감금</div><div class="voc-def">Intentional confinement within bounded area without consent and no reasonable means of escape.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">IIED</div><div class="voc-ko">고의적 정신적 고통</div><div class="voc-def">Intentional/reckless extreme and outrageous conduct causing severe emotional distress.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Transferred Intent</div><div class="voc-ko">전이 의도</div><div class="voc-def">Intent to commit one tort transfers to actual tort committed, even against unintended victim.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Single / Dual Intent</div><div class="voc-ko">단일/이중 의도</div><div class="voc-def">Single (majority): intent to do the act. Dual (minority): intent to act AND to cause harm.</div></div>
</div>

<span class="voc-cat">Property Torts</span>
<div class="voc-grid">
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Trespass to Land</div><div class="voc-ko">토지 침입</div><div class="voc-def">Intentional physical entry onto land possessed by another. No damage required.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Trespass to Chattel</div><div class="voc-ko">동산 침입</div><div class="voc-def">Intentional interference with another's possession of personal property. Intermeddling itself suffices.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Conversion</div><div class="voc-ko">변취</div><div class="voc-def">Serious intentional interference with another's chattel. Full value owed. Duration/extent matters.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Private Necessity</div><div class="voc-ko">사적 긴급피난</div><div class="voc-def">Privilege to interfere with another's property to prevent greater harm. Must compensate for actual damage.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Public Necessity</div><div class="voc-ko">공적 긴급피난</div><div class="voc-def">Privilege to destroy private property to prevent public disaster. No compensation owed.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Deadly Force (Property)</div><div class="voc-ko">재산보호 + 치명력</div><div class="voc-def">Deadly force may NEVER be used solely to protect property. Only to protect persons from imminent death/serious harm.</div></div>
</div>

<span class="voc-cat">Negligence</span>
<div class="voc-grid">
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Duty of Care</div><div class="voc-ko">주의의무</div><div class="voc-def">Obligation to act as a reasonably prudent person toward foreseeable plaintiffs (Palsgraf majority).</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Negligence per se</div><div class="voc-ko">법령 위반 과실</div><div class="voc-def">(1) statute violated; (2) plaintiff in protected class; (3) harm = type statute designed to prevent. All 3 met = breach shown.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Hand Formula (B&lt;PL)</div><div class="voc-ko">핸드 공식</div><div class="voc-def">Breach when Burden &lt; Probability x gravity of harm. Defines standard of care (breach), NOT causation.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">But-For Test</div><div class="voc-ko">가정적 원인</div><div class="voc-def">Injury would not have occurred but for defendant's breach. Primary actual causation test.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Substantial Factor Test</div><div class="voc-ko">실질적 요인</div><div class="voc-def">Used when multiple independent sufficient causes. Defendant liable if conduct was substantial factor in harm.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Alternative Causation</div><div class="voc-ko">대체 인과관계</div><div class="voc-def">2+ negligent Ds, only one caused harm, P can't identify who → burden shifts to each D to prove non-causation.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Proximate Cause</div><div class="voc-ko">근접 원인</div><div class="voc-def">Harm must be foreseeable result of breach. Superseding intervening cause breaks the chain.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Eggshell Plaintiff Rule</div><div class="voc-ko">달걀껍데기 원고</div><div class="voc-def">Defendant takes plaintiff as found. Liable for full extent of harm even if plaintiff's vulnerability was unforeseeable.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Res Ipsa Loquitur</div><div class="voc-ko">사실 자체가 말한다</div><div class="voc-def">(1) harm doesn't occur without negligence; (2) D had exclusive control; (3) P not contributorily negligent → negligence inferred.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Emergency Doctrine</div><div class="voc-ko">긴급 상황 원칙</div><div class="voc-def">Person facing sudden emergency not of own making is held to what a reasonable person would do in that emergency.</div></div>
</div>

<span class="voc-cat">Defenses to Negligence</span>
<div class="voc-grid">
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Contributory Negligence</div><div class="voc-ko">기여과실 (구법)</div><div class="voc-def">Any plaintiff negligence = complete bar. Minority rule.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Modified Comparative Negligence</div><div class="voc-ko">수정 비교과실</div><div class="voc-def">Plaintiff recovers proportionally UNLESS fault &gt; defendant's (or &gt;=50%). Majority rule.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Pure Comparative Negligence</div><div class="voc-ko">순수 비교과실</div><div class="voc-def">Plaintiff always recovers, reduced by own %. No bar even at 99% fault.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Assumption of Risk</div><div class="voc-ko">위험 인수</div><div class="voc-def">Plaintiff knowingly and voluntarily assumes a known risk. Complete or partial bar.</div></div>
</div>

<span class="voc-cat">Strict Liability &amp; Products</span>
<div class="voc-grid">
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Abnormally Dangerous Activity</div><div class="voc-ko">비정상적 위험 활동</div><div class="voc-def">(1) inherently high risk; (2) unusual for community; (3) injury from that danger. Force of nature = NO defense.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Manufacturing Defect</div><div class="voc-ko">제조 결함</div><div class="voc-def">Specific product departs from intended design specs. Compare to manufacturer's own blueprint.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Design Defect</div><div class="voc-ko">설계 결함</div><div class="voc-def">Entire product line unreasonably dangerous. Requires reasonable alternative design (RAD). Irreducibly unsafe = no RAD = no design defect claim.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Failure to Warn</div><div class="voc-ko">경고 결함</div><div class="voc-def">Knew/should have known risk + failed to warn. Warning does NOT cure design defect. Causation: plaintiff would have heeded.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Privity (Products)</div><div class="voc-ko">계약 당사자 관계</div><div class="voc-def">NOT required. Any foreseeable user or bystander can sue entire distribution chain.</div></div>
</div>

<span class="voc-cat">Nuisance &amp; Privacy</span>
<div class="voc-grid">
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Private Nuisance</div><div class="voc-ko">사적 방해</div><div class="voc-def">Substantial + unreasonable interference with use/enjoyment of land. Coming to nuisance = NOT a defense.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Public Nuisance</div><div class="voc-ko">공적 방해</div><div class="voc-def">Unreasonable interference with right common to general public. Private citizen needs harm "different in kind" to have standing.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Appropriation</div><div class="voc-ko">성명·초상 도용</div><div class="voc-def">Using plaintiff's name/likeness without consent for defendant's own purpose.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">False Light</div><div class="voc-ko">허위 사실 공표</div><div class="voc-def">Publicizes false information about plaintiff that is highly offensive to reasonable person.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Intrusion upon Seclusion</div><div class="voc-ko">사생활 침입</div><div class="voc-def">Intentional intrusion on private affairs, highly offensive. Photographing in PUBLIC = NOT intrusion.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Public Disclosure of Private Facts</div><div class="voc-ko">사적 사실 공개</div><div class="voc-def">Publicizes private facts, highly offensive. Defense: legitimate public interest → must prove actual malice.</div></div>
</div>

<span class="voc-cat">Defamation &amp; Damages</span>
<div class="voc-grid">
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Defamation per se</div><div class="voc-ko">당연 명예훼손</div><div class="voc-def">Crime of moral turpitude / loathsome disease / business misconduct / sexual misconduct. Damages presumed.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Actual Malice</div><div class="voc-ko">실제 악의</div><div class="voc-def">Knowledge of falsity OR reckless disregard for truth. Required for public figures.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Survival Action</div><div class="voc-ko">소송 승계</div><div class="voc-def">Decedent's own claims survive death. Estate brings claim (e.g., pain and suffering before death).</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Wrongful Death</div><div class="voc-ko">불법사망 소송</div><div class="voc-def">Survivors recover for THEIR OWN loss: consortium, guidance, financial support.</div></div>
<div class="voc-card" onclick="this.classList.toggle('open')"><div class="voc-en">Loss of Consortium</div><div class="voc-ko">배우자 동거 손해</div><div class="voc-def">Spouse's claim for lost companionship, services, affection due to partner's injury or death.</div></div>
</div>
</div>"""

with open(r'F:\mbe\index.html', encoding='utf-8') as f:
    content = f.read()

old = '</div>\n</div>\n<div id="cl1"'
new = '</div>\n' + vocab_panel + '\n</div>\n<div id="cl1"'
count = content.count(old)
print(f'match: {count}')
if count == 1:
    content = content.replace(old, new)
    with open(r'F:\mbe\index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('vocab done')
else:
    print('no unique match')
