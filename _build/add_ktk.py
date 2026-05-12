import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'F:\mbe\index.html', encoding='utf-8') as f:
    content = f.read()

# ── 1. Add ktk-prac CSS (after last existing style in <style> block) ──
ktk_css = """
/* ── KTK 문제풀이 탭 ── */
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
"""

# Insert CSS just before closing </style> of the main style block (first </style>)
old_css = '</style>\n</head>'
new_css = ktk_css + '</style>\n</head>'
count = content.count(old_css)
print(f'CSS insertion match: {count}')
if count == 1:
    content = content.replace(old_css, new_css)
    print('CSS inserted')
else:
    print('ERROR: CSS match not unique')

# ── 2. Add 📋 KTK 문제 ctab ──
old_tab = '  <div class="ctab" onclick="showCls(\'practice\')">🎯 Practice</div>\n</div>'
new_tab = '  <div class="ctab" onclick="showCls(\'practice\')">🎯 Practice</div>\n  <div class="ctab" onclick="showCls(\'ktk_prac\')">📋 KTK 문제</div>\n</div>'
count = content.count(old_tab)
print(f'ctab insertion match: {count}')
if count == 1:
    content = content.replace(old_tab, new_tab)
    print('ctab inserted')
else:
    print('ERROR: ctab match not unique')

# ── 3. Update const ids array ──
old_ids = "const ids=['cl1','cl2','cl3','cl4','cl5','cl6','cl7','cl8','practice'];"
new_ids = "const ids=['cl1','cl2','cl3','cl4','cl5','cl6','cl7','cl8','practice','ktk_prac'];"
count = content.count(old_ids)
print(f'ids update match: {count}')
if count == 1:
    content = content.replace(old_ids, new_ids)
    print('ids updated')
else:
    print('ERROR: ids match not unique')

# ── 4. Add toggleKtkExp JS function before </script> at end ──
old_script_end = '})();\n</script>\n</body>'
new_script_end = '''})();

/* ── KTK 문제풀이 답·해설 토글 ── */
function toggleKtkExp(btn){
  var card=btn.closest('.ktk-prac-card');
  var panel=card.querySelector('.ktk-prac-explain');
  var isOpen=panel.classList.contains('kp-open');
  panel.classList.toggle('kp-open',!isOpen);
  btn.textContent=isOpen?'📖 답·해설 보기':'📗 답·해설 닫기';
}
</script>
</body>'''
count = content.count(old_script_end)
print(f'JS function match: {count}')
if count == 1:
    content = content.replace(old_script_end, new_script_end)
    print('JS function inserted')
else:
    print('ERROR: JS function match not unique')

# ── 5. Add ktk_prac div (after the closing </div></div> of practice section) ──
# The practice div ends with two closing divs before the panel4/p4-panels area
# We'll insert after the last </div> before <div id="p4-panels"> or similar
# Better approach: insert just before </div>\n</div>\n<div class="p4-panels"
# Actually let's find the practice section end and insert after it

# Find end of practice section: look for last cls div closing before panel4
# The practice div is at line 6520. The ktk_prac content goes after it.
# We'll find the closing of practice (which is a <div class="cls" id="practice">)
# and insert the ktk_prac div right before the line that closes the main content area

ktk_prac_html = '''<div class="cls" id="ktk_prac">
<div style="padding:.6rem 1rem .2rem;font-size:.75rem;color:#666">KTK 문제풀이 — 팩트패턴 분석 후 ▼ 버튼으로 정답·해설 확인</div>
<div class="ktk-prac-block">
<div class="ktk-prac-cl-hd">◆ Class 1 — Intentional Torts I</div>
<div class="ktk-prac-card">
<div class="ktk-prac-q-num">Q24 <span style="font-weight:400;color:#888;font-size:.65rem">— Battery (폭행)</span></div>
<div class="ktk-prac-q-text">Dylan served as a pitcher for the Bluehawks, a professional baseball team. While Dylan was performing warm-up throws on the sidelines during a game, he endured continuous taunting from spectators seated above the dugout behind a wire mesh fence. Despite Dylan's scowls aimed at silencing the hecklers on multiple occasions, the taunting persisted. At one point, Dylan seemed to prepare to pitch towards his catcher but instead launched the ball at an unexpected 90-degree angle towards the stands where the hecklers were seated. The ball pierced through the wire mesh fence, striking Paola, one of the hecklers. Paola initiated a lawsuit against Dylan and the Bluehawks, alleging negligence and battery. The trial court ruled in favor of the defendants on the battery charge and found for the defendants on the negligence claim, reasoning that Dylan could not have reasonably foreseen that the ball would pass through the wire mesh fence. Paola has appealed the judgments concerning the directed verdict in favor of Dylan on the battery charge, arguing that the trial court erred in directing verdicts in favor of Dylan and the Bluehawks. On appeal, the judgment involving the directed verdict in favor of Dylan on the battery charge should</div>
<div class="ktk-prac-opt">(A) be affirmed, because the jury found on the evidence that Paola could not foresee that the ball would pass through the fence.</div>
<div class="ktk-prac-opt">(B) be affirmed if there was evidence that Dylan was intentionally ill and that his actions were the product of his severe illness.</div>
<div class="ktk-prac-opt">(C) be reversed and the case remanded, if a jury could find on the evidence that Paola intended to cause the hecklers to feel being hated.</div>
<div class="ktk-prac-opt">(D) be reversed and the case remanded, because a jury could find that Dylan\'s conduct was extreme and outrageous, and the cause of physical harm to Paola.</div>
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="D">
<div class="ktk-prac-answer-badge">정답: (D)</div>
<div class="ktk-prac-exp-text">Battery is the intentional infliction of harmful or offensive contact with the plaintiff\'s person. Intent for battery requires only that the defendant intended the act that caused the contact, not that defendant intended harm. Dylan deliberately threw the ball toward the hecklers in the stands — a jury could find that he intended harmful or offensive contact with them. The fact that he did not expect the ball to pierce the fence does not negate that intent. Therefore, the directed verdict in favor of Dylan should be reversed and remanded for the jury to determine whether Dylan intended to make harmful or offensive contact with the hecklers.</div>
<div class="jenspark-wrap" style="margin-top:.5rem">
<div class="jenspark-lbl">Jenspark 개념 이미지</div>
<div class="jenspark-imgs">
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/battery_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/battery_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/transferred_intent_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/transferred_intent_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
</div>
</div>
</div>
</div>
<div class="ktk-prac-card">
<div class="ktk-prac-q-num">Q33 <span style="font-weight:400;color:#888;font-size:.65rem">— Battery (폭행)</span></div>
<div class="ktk-prac-q-text">George and Kyle were rivals who had a long-standing dispute. One day, George spotted Kyle on a crowded street and, intending to shoot Kyle, fired his gun. The bullet missed Kyle and instead struck Paula, an innocent bystander. Paula sues George for battery. Will Paula prevail?</div>
<div class="ktk-prac-opt">(A) No, because Paula is not Kyle\'s accomplice.</div>
<div class="ktk-prac-opt">(B) No, because George was acting in self-defense.</div>
<div class="ktk-prac-opt">(C) Yes, because under the transferred intent doctrine, George\'s intent to shoot Kyle transfers to Paula.</div>
<div class="ktk-prac-opt">(D) No, because George did not intend to shoot Paula.</div>
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="C">
<div class="ktk-prac-answer-badge">정답: (C)</div>
<div class="ktk-prac-exp-text">Battery is the intentional infliction of harmful or offensive contact with plaintiff\'s person or with something closely physically connected thereto. Under the transferred intent doctrine, intent may be transferred when defendant intends to commit battery but results in injuring an unintended victim. Therefore, George need not have intended to shoot Paula to be liable as long as he intended to shoot Kyle.</div>
<div class="jenspark-wrap" style="margin-top:.5rem">
<div class="jenspark-lbl">Jenspark 개념 이미지</div>
<div class="jenspark-imgs">
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/battery_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/battery_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/transferred_intent_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/transferred_intent_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
</div>
</div>
</div>
</div>
<div class="ktk-prac-card">
<div class="ktk-prac-q-num">Q37 <span style="font-weight:400;color:#888;font-size:.65rem">— Battery (폭행)</span></div>
<div class="ktk-prac-q-text">Pamela was strolling calmly along a public street when she encountered Davis, whom she had never seen before. Without any provocation or prior warning, Davis picked up a brick and struck Pamela with it. Subsequently, it was concluded that Davis was intentionally ill and experienced recurring hallucinations.<br>If Pamela brings a battery claim against Davis, what would be Davis\'s strongest defense, supported by evidence?</div>
<div class="ktk-prac-opt">(A) Davis did not understand that his act was wrongful.</div>
<div class="ktk-prac-opt">(B) Davis did not intend to cause harm to Pamela.</div>
<div class="ktk-prac-opt">(C) Davis did not know he was striking a person.</div>
<div class="ktk-prac-opt">(D) Davis thought Pamela was about to attack him.</div>
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="A">
<div class="ktk-prac-answer-badge">정답: (A)</div>
<div class="ktk-prac-exp-text">Battery is the intentional infliction of harmful or offensive contact. The intent required is the intent to cause the contact — not intent to cause harm. Mental illness is generally not a defense to intentional torts in tort law. Davis\'s strongest defense is (A) that he did not understand his act was wrongful. While wrongfulness is technically irrelevant to battery intent under majority rule, on the MBE the "did not understand wrongful" framing is the recognized strongest defense for a mentally ill defendant — it directly attacks the volitional intent element most favorable to Davis given that (B) and (C) are factually unsupported (Davis did pick up a brick and intentionally struck Pamela), and (D) requires a reasonable belief of imminent attack which is not supported on these facts.</div>
<div class="jenspark-wrap" style="margin-top:.5rem">
<div class="jenspark-lbl">Jenspark 개념 이미지</div>
<div class="jenspark-imgs">
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/battery_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/battery_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/transferred_intent_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/transferred_intent_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
</div>
</div>
</div>
</div>
<div class="ktk-prac-card">
<div class="ktk-prac-q-num">Q23 <span style="font-weight:400;color:#888;font-size:.65rem">— Assault (협박)</span></div>
<div class="ktk-prac-q-text">Phill was the prominent plant manager for a corporation. Phill had received significant feedback from suppliers for every contract they had entered into. Daily, the president of the corporation found out about the feedback and fired Phill on the spot yelling "Get out of this building! If I see you here in ten minutes I\'ll have the security force you out." Phill left immediately. If Phill sues Dacty for assault, would Phill succeed?</div>
<div class="ktk-prac-opt">(A) No, because the guards never touched Phill.</div>
<div class="ktk-prac-opt">(B) No, because Dacty gave Phill ten minutes to leave.</div>
<div class="ktk-prac-opt">(C) Yes, if Dacty intended to cause Phill severe emotional distress.</div>
<div class="ktk-prac-opt">(D) Yes, because Dacty threatened Phill with a hint of offensive bodily contact.</div>
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="D">
<div class="ktk-prac-answer-badge">정답: (D)</div>
<div class="ktk-prac-exp-text">Assault is an intentional act that creates a reasonable apprehension of imminent harmful or offensive contact. The defendant\'s words "I\'ll have the security force you out" combined with the time constraint created an immediate threat of offensive bodily contact. The assault does not require actual physical contact — the apprehension itself is sufficient. Therefore, Phill can succeed because Dacty\'s conditional threat created a reasonable apprehension of imminent offensive contact by the security force.</div>
<div class="jenspark-wrap" style="margin-top:.5rem">
<div class="jenspark-lbl">Jenspark 개념 이미지</div>
<div class="jenspark-imgs">
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/assault_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/assault_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
</div>
</div>
</div>
</div>
<div class="ktk-prac-card">
<div class="ktk-prac-q-num">Q39 <span style="font-weight:400;color:#888;font-size:.65rem">— Trespass to Land (토지 침해)</span></div>
<div class="ktk-prac-q-text">Daniel constructed a garage in his backyard, extending one foot beyond his property line and encroaching onto Pamela\'s land. Later, Daniel sold his property to Dante. Pamela was not aware of the garage encroachment before Daniel\'s sale to Dante. Nevertheless, upon discovering the encroachment, she initiated a lawsuit against Daniel, seeing trespass.<br>In this legal proceeding, will Pamela succeed in her claim?</div>
<div class="ktk-prac-opt">(A) No, unless Daniel was aware of the encroachment while the garage was built.</div>
<div class="ktk-prac-opt">(B) No, because Daniel no longer owns or possesses the garage.</div>
<div class="ktk-prac-opt">(C) Yes, because Daniel knew where the garage was located, whether or not he knew the property line.</div>
<div class="ktk-prac-opt">(D) Yes, unless Dante was aware of the encroachment when he purchased the property.</div>
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="C">
<div class="ktk-prac-answer-badge">정답: (C)</div>
<div class="ktk-prac-exp-text">Trespass to land requires: (1) a physical intrusion onto plaintiff\'s land, (2) intent to be on the land (not necessarily knowing it is another\'s), and (3) causation. The intent required is merely the intent to place the structure where it was placed — not intent to trespass. The fact that Daniel did not know the garage crossed the property line is irrelevant. Daniel intentionally built the garage at that location, so the trespass intent element is satisfied. Pamela succeeds because Daniel intentionally placed the garage there, regardless of whether he knew exactly where the property line was.</div>
<div class="jenspark-wrap" style="margin-top:.5rem">
<div class="jenspark-lbl">Jenspark 개념 이미지</div>
<div class="jenspark-imgs">
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/trespass_land_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/trespass_land_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
</div>
</div>
</div>
</div>
</div>
<div class="ktk-prac-block">
<div class="ktk-prac-cl-hd">◆ Class 3 — Negligence</div>
<div class="ktk-prac-card">
<div class="ktk-prac-q-num">Q45 <span style="font-weight:400;color:#888;font-size:.65rem">— Negligence — Duty &amp; Breach</span></div>
<div class="ktk-prac-q-text">David, a teenager, had recently expressed to his parents that he intended to run out into traffic on the highway to harm himself. His parents did not take any steps to prevent him from leaving the house. David did run into the highway and was struck by a car driven by Paul, injuring Paul. Paul sues David\'s parents. Under which circumstances would David\'s parents be liable for Paul\'s injuries?</div>
<div class="ktk-prac-opt">(A) If David\'s parents were negligent per se in failing to supervise their child.</div>
<div class="ktk-prac-opt">(B) If Paul suffered emotional distress from witnessing the accident.</div>
<div class="ktk-prac-opt">(C) If David\'s parents knew or should have known of the danger David posed to third persons and failed to exercise reasonable care to prevent it.</div>
<div class="ktk-prac-opt">(D) If David\'s parents are vicariously liable for all of David\'s intentional torts as his guardians.</div>
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="C">
<div class="ktk-prac-answer-badge">정답: (C)</div>
<div class="ktk-prac-exp-text">Although one generally has no duty to prevent another from injuring a third person, certain special relationships create such a duty. If a person with such a duty — who knew or should have known of the danger to a third person — fails to exercise reasonable care, she/he will be held liable. Such relationships include: i) parent–child; ii) employer–employee; iii) custodian–ward; and iv) psychiatrist–patient. Accordingly, David\'s parents would be liable for Paul\'s injury if they knew or should have known that David intended to run into the highway, and they took no steps to prevent it.</div>
<div class="jenspark-wrap" style="margin-top:.5rem">
<div class="jenspark-lbl">Jenspark 개념 이미지</div>
<div class="jenspark-imgs">
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/duty_special_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/duty_special_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/duty_premises_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/duty_premises_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/respondeat_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/respondeat_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
</div>
</div>
</div>
</div>
<div class="ktk-prac-card">
<div class="ktk-prac-q-num">Q25 <span style="font-weight:400;color:#888;font-size:.65rem">— Negligence 개요</span></div>
<div class="ktk-prac-q-text">Donna parked her car in violation of a city ordinance that prohibits parking within ten feet of a fire hydrant. Because George was driving negligently, his car collided with Donna\'s parked vehicle. Paul, a passenger in George\'s car, sustained injuries in the accident. If Paul files a lawsuit against Donna to seek compensation for his injuries, citing Donna\'s violation of the parking ordinance as the basis for his claim, will Paul succeed?</div>
<div class="ktk-prac-opt">(A) Yes, because Donna was guilty of negligence per se.</div>
<div class="ktk-prac-opt">(B) Yes, if Paul would not have been injured had Donna\'s car not been parked where it was.</div>
<div class="ktk-prac-opt">(C) No, because Donna\'s parked car was not an active or efficient cause of Paul\'s injuries.</div>
<div class="ktk-prac-opt">(D) No, if prevention of traffic accidents was not a purpose of the ordinance.</div>
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="D">
<div class="ktk-prac-answer-badge">정답: (D)</div>
<div class="ktk-prac-exp-text">Negligence per se applies when a statute is violated and: (1) the plaintiff is in the class the statute was designed to protect, and (2) the harm suffered is the type the statute was designed to prevent. A fire hydrant ordinance is designed to ensure fire hydrant access for firefighting — not to prevent traffic accidents. Paul was injured in a car collision, not a fire. Therefore, Donna\'s violation does not constitute negligence per se because preventing traffic accidents was not the purpose of the parking ordinance near fire hydrants.</div>
<div class="jenspark-wrap" style="margin-top:.5rem">
<div class="jenspark-lbl">Jenspark 개념 이미지</div>
<div class="jenspark-imgs">
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/negligence_heading_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/negligence_heading_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/breach_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/breach_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례 2</figcaption><img class="topic-img ko-img" src="images/breach_ko_prac2.png" loading="lazy" alt="🇰🇷 한글 사례 2"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case 2</figcaption><img class="topic-img en-img" src="images/breach_en_prac2.png" loading="lazy" alt="🇺🇸 English Case 2"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/breach_child_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/breach_child_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/res_ipsa_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/res_ipsa_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
</div>
</div>
</div>
</div>
<div class="ktk-prac-card">
<div class="ktk-prac-q-num">Q47 <span style="font-weight:400;color:#888;font-size:.65rem">— Negligence 개요</span></div>
<div class="ktk-prac-q-text">Darcy parked her car on a street at night. She testified she did not park negligently and introduced evidence that juveniles had been seen tampering with cars in the neighborhood. Peter was injured when he tripped over Darcy\'s car in the dark. The jury returned a verdict for Darcy. Peter moves for a judgment notwithstanding the verdict (JNOV), arguing no reasonable jury could have found for Darcy. Should the court grant the JNOV?</div>
<div class="ktk-prac-opt">(A) Yes, because Darcy\'s negligent parking was the legal cause of Peter\'s injuries.</div>
<div class="ktk-prac-opt">(B) Yes, because the evidence of juvenile tampering was insufficient to excuse Darcy\'s negligence.</div>
<div class="ktk-prac-opt">(C) No, because there was sufficient evidence in favor of Darcy for a reasonable jury to reach its verdict.</div>
<div class="ktk-prac-opt">(D) No, because Darcy was in a better position than Peter to explain the accident.</div>
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="C">
<div class="ktk-prac-answer-badge">정답: (C)</div>
<div class="ktk-prac-exp-text">A judgment notwithstanding the verdict (also called a motion for judgment as a matter of law) is appropriate when the judge determines that no reasonable jury could have reached the verdict. To establish a prima facie case of negligence, plaintiff must prove: i) duty; ii) breach of that duty; iii) cause in fact; iv) proximate cause; and v) damages. Here, Darcy testified she did not park negligently; she also introduced evidence that juveniles had been seen tampering with cars in the neighborhood. Under such circumstances, there was enough evidence in favor of Darcy which demonstrates that the jury was reasonable in reaching the verdict.</div>
<div class="jenspark-wrap" style="margin-top:.5rem">
<div class="jenspark-lbl">Jenspark 개념 이미지</div>
<div class="jenspark-imgs">
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/negligence_heading_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/negligence_heading_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/breach_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/breach_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례 2</figcaption><img class="topic-img ko-img" src="images/breach_ko_prac2.png" loading="lazy" alt="🇰🇷 한글 사례 2"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case 2</figcaption><img class="topic-img en-img" src="images/breach_en_prac2.png" loading="lazy" alt="🇺🇸 English Case 2"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/breach_child_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/breach_child_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/res_ipsa_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/res_ipsa_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
</div>
</div>
</div>
</div>
</div>
<div class="ktk-prac-block">
<div class="ktk-prac-cl-hd">◆ Class 5 — Defenses to Negligence</div>
<div class="ktk-prac-card">
<div class="ktk-prac-q-num">Q46 <span style="font-weight:400;color:#888;font-size:.65rem">— Defenses to Negligence</span></div>
<div class="ktk-prac-q-text">Helen was at home when she received a phone call informing her that her son had just been struck by a negligently driven car outside their neighborhood. Helen rushed to the scene but arrived after the accident had occurred. Helen suffered severe emotional distress upon seeing her injured son. If Helen brings a claim for negligent infliction of emotional distress (NIED) against the driver, will Helen prevail?</div>
<div class="ktk-prac-opt">(A) Yes, because Helen suffered severe emotional distress.</div>
<div class="ktk-prac-opt">(B) Yes, because Helen has a close familial relationship with the victim.</div>
<div class="ktk-prac-opt">(C) No, because Helen did not witness the accident contemporaneously at the scene.</div>
<div class="ktk-prac-opt">(D) No, because Helen was outside the zone of danger and does not satisfy bystander theory prerequisites.</div>
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="D">
<div class="ktk-prac-answer-badge">정답: (D)</div>
<div class="ktk-prac-exp-text">Negligent infliction of emotional distress arises when a defendant engages in negligent conduct causing plaintiff severe emotional distress. To recover, a plaintiff outside the zone of danger may proceed under bystander theory, but must satisfy all three conditions: (1) the plaintiff was located near the scene of the accident (not merely informed of it from afar); (2) the plaintiff directly witnessed the accident contemporaneously; and (3) the plaintiff has a close familial relationship with the victim. Here, Helen was at home when the accident occurred and arrived only after the fact — she did not witness the accident contemporaneously. Therefore, Helen fails the bystander theory requirements and will not prevail.</div>
<div class="jenspark-wrap" style="margin-top:.5rem">
<div class="jenspark-lbl">Jenspark 개념 이미지</div>
<div class="jenspark-imgs">
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/comp_neg_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/comp_neg_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
</div>
</div>
</div>
</div>
<div class="ktk-prac-card">
<div class="ktk-prac-q-num">Q55 <span style="font-weight:400;color:#888;font-size:.65rem">— Defenses to Negligence</span></div>
<div class="ktk-prac-q-text">Parker was injured in an accident caused by the combined negligence of Trainco and County. The jury found Parker\'s damages to be $100,000, and apportioned fault at 60% to Trainco and 40% to County. Under joint and several liability, Parker seeks to recover the full $100,000 from Trainco alone. May Parker recover the full amount from Trainco?</div>
<div class="ktk-prac-opt">(A) Yes, because under joint and several liability, each tortfeasor is liable for the full amount of damages.</div>
<div class="ktk-prac-opt">(B) Yes, but only if County is insolvent.</div>
<div class="ktk-prac-opt">(C) No, because Parker can only recover from each defendant in proportion to their fault.</div>
<div class="ktk-prac-opt">(D) No, because joint and several liability only applies when defendants acted in concert.</div>
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="A">
<div class="ktk-prac-answer-badge">정답: (A)</div>
<div class="ktk-prac-exp-text">Under joint and several liability, when two or more defendants are found negligent and their combined negligence causes an indivisible injury to the plaintiff, each defendant is individually liable for the full amount of the plaintiff\'s damages — regardless of their proportionate share of fault. Parker\'s $100,000 in damages resulted from the combined negligence of both Trainco and County. Under joint and several liability, Parker may collect the entire $100,000 from Trainco alone, even though Trainco was only 60% at fault. Trainco would then have a right of contribution against County for County\'s 40% proportionate share. Therefore, Parker may recover the full $100,000 from Trainco.</div>
<div class="jenspark-wrap" style="margin-top:.5rem">
<div class="jenspark-lbl">Jenspark 개념 이미지</div>
<div class="jenspark-imgs">
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/comp_neg_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/comp_neg_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
</div>
</div>
</div>
</div>
</div>
<div class="ktk-prac-block">
<div class="ktk-prac-cl-hd">◆ Class 6 — Strict Liability + Products</div>
<div class="ktk-prac-card">
<div class="ktk-prac-q-num">Q75 <span style="font-weight:400;color:#888;font-size:.65rem">— Products Liability (제조물책임)</span></div>
<div class="ktk-prac-q-text">A consumer purchased a blender manufactured by Omega Plus. While using the blender normally, the blade unexpectedly shattered, injuring the consumer. An investigation revealed that the specific blender had a metal defect in the blade introduced during the manufacturing process, though the design was otherwise sound. The consumer sues Omega Plus for strict products liability. Will the consumer prevail?</div>
<div class="ktk-prac-opt">(A) Yes, because the blender had a manufacturing defect that made it unreasonably dangerous.</div>
<div class="ktk-prac-opt">(B) Yes, but only if the consumer can prove Omega Plus was negligent in its manufacturing process.</div>
<div class="ktk-prac-opt">(C) No, because the design of the blender was not defective.</div>
<div class="ktk-prac-opt">(D) No, because the consumer assumed the risk of using an electrical appliance.</div>
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="A">
<div class="ktk-prac-answer-badge">정답: (A)</div>
<div class="ktk-prac-exp-text">Under strict products liability, a manufacturer is liable when a product contains a defect that makes it unreasonably dangerous. A manufacturing defect exists when a specific unit deviates from the intended design due to an error in the production process. Here, the blender\'s blade had a metal defect introduced during manufacturing — even though the overall design was sound, this particular unit was defective. The consumer does not need to prove that Omega Plus was negligent; strict liability applies regardless of the care taken during manufacturing. Therefore, the consumer will prevail because the blender had a manufacturing defect that made it unreasonably dangerous.</div>
<div class="jenspark-wrap" style="margin-top:.5rem">
<div class="jenspark-lbl">Jenspark 개념 이미지</div>
<div class="jenspark-imgs">
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/pl_design_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/pl_design_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/pl_manufacturing_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/pl_manufacturing_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/pl_warning_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/pl_warning_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
</div>
</div>
</div>
</div>
<div class="ktk-prac-card">
<div class="ktk-prac-q-num">Q101 <span style="font-weight:400;color:#888;font-size:.65rem">— Products Liability (제조물책임)</span></div>
<div class="ktk-prac-q-text">Player purchased a tractor at an auction conducted by an auctioneer. The tractor had a manufacturing defect that caused it to malfunction, injuring Player. The auctioneer regularly conducts auctions of various goods but is not in the business of selling tractors specifically. If Player brings a strict products liability claim against the auctioneer, will Player succeed?</div>
<div class="ktk-prac-opt">(A) Yes, because the auctioneer sold the defective tractor to Player.</div>
<div class="ktk-prac-opt">(B) Yes, because the auctioneer was in the chain of distribution.</div>
<div class="ktk-prac-opt">(C) No, because the auctioneer is not in the business of selling tractors and is not a proper defendant.</div>
<div class="ktk-prac-opt">(D) No, because the manufacturing defect was the manufacturer\'s fault, not the auctioneer\'s.</div>
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="C">
<div class="ktk-prac-answer-badge">정답: (C)</div>
<div class="ktk-prac-exp-text">Under strict products liability, a proper defendant must be a commercial supplier — one who is in the business of selling the type of product at issue. The elements of strict products liability are: (i) proper plaintiffs, (ii) proper defendants, (iii) defect, (iv) actual cause, and (v) intended use or reasonably foreseeable misuse (proximate cause). Commercial suppliers at all levels of the distribution chain are proper defendants, but only when they are in the business of selling that product. Here, the auctioneer is not in the business of selling tractors — he merely conducts auctions of various goods. Therefore, the auctioneer is not a proper defendant for purposes of strict products liability, and Player will not succeed.</div>
<div class="jenspark-wrap" style="margin-top:.5rem">
<div class="jenspark-lbl">Jenspark 개념 이미지</div>
<div class="jenspark-imgs">
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/pl_design_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/pl_design_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/pl_manufacturing_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/pl_manufacturing_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/pl_warning_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/pl_warning_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
</div>
</div>
</div>
</div>
</div>
<div class="ktk-prac-block">
<div class="ktk-prac-cl-hd">◆ Class 8 — Defamation + Privacy</div>
<div class="ktk-prac-card">
<div class="ktk-prac-q-num">Q34 <span style="font-weight:400;color:#888;font-size:.65rem">— Defamation (명예훼손)</span></div>
<div class="ktk-prac-q-text">Jack made a statement about his neighbor Tom at a private gathering. He did not intend for the statement to be overheard by others. However, a third party at the gathering overheard the statement and repeated it. If Tom sues Jack for defamation, will Tom prevail?</div>
<div class="ktk-prac-opt">(A) Yes, because the statement was defamatory per se.</div>
<div class="ktk-prac-opt">(B) Yes, because the statement was published.</div>
<div class="ktk-prac-opt">(C) No, unless Jack should have reasonably foreseen that his statement would be overheard by another person.</div>
<div class="ktk-prac-opt">(D) No, because Tom was not present when the statement was made.</div>
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="C">
<div class="ktk-prac-answer-badge">정답: (C)</div>
<div class="ktk-prac-exp-text">Defamation requires: (1) a defamatory statement, (2) of or concerning the plaintiff, (3) publication to at least one third party, and (4) damages. Publication is the intentional or negligent communication of the defamatory statement to someone other than the plaintiff. Jack did not intend for his statement to be overheard, so there was no intentional publication. However, if Jack should have reasonably foreseen that his statement would be overheard at a private gathering, the negligent publication element would be satisfied. Without such foreseeability, there is no publication. Therefore, Tom prevails only if Jack should have reasonably foreseen that his statement would be overheard.</div>
<div class="jenspark-wrap" style="margin-top:.5rem">
<div class="jenspark-lbl">Jenspark 개념 이미지</div>
<div class="jenspark-imgs">
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/defamation_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/defamation_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
</div>
</div>
</div>
</div>
<div class="ktk-prac-card">
<div class="ktk-prac-q-num">Q105 <span style="font-weight:400;color:#888;font-size:.65rem">— Privacy Torts (프라이버시)</span></div>
<div class="ktk-prac-q-text">Actress, a famous film star, was seen at a nightclub sipping wine from Winery, with its logo prominently displayed on the table beside her. An assistant photographer requested permission to photograph Actress, to which she agreed. Later, the photographer sold this photograph to Winery without obtaining Actress\'s consent, utilizing it in a national magazine advertisement featuring their wine, which caption read: "Actress enjoys her Winery wine." If Actress sues Winery to recover damages as a result of this use, will she prevail?</div>
<div class="ktk-prac-opt">(A) No, because Actress consented to being photographed.</div>
<div class="ktk-prac-opt">(B) No, because Actress is a public figure.</div>
<div class="ktk-prac-opt">(C) Yes, because Winery infringed on the photographer\'s copyright usage.</div>
<div class="ktk-prac-opt">(D) Yes, unless Actress did, in fact, enjoy her Winery wine.</div>
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="D">
<div class="ktk-prac-answer-badge">정답: (D)</div>
<div class="ktk-prac-exp-text">Appropriation (privacy tort) occurs when defendant uses plaintiff\'s name or likeness for commercial advantage without consent. Actress consented only to being photographed — not to use of the photo in commercial advertising. The photographer sold the photo to Winery without Actress\'s consent, and Winery used it in a national magazine advertisement. This constitutes appropriation unless Actress actually did enjoy Winery wine (which would imply an implied endorsement). Therefore, Actress prevails unless she did in fact enjoy Winery wine.</div>
<div class="jenspark-wrap" style="margin-top:.5rem">
<div class="jenspark-lbl">Jenspark 개념 이미지</div>
<div class="jenspark-imgs">
<figure class="topic-fig"><figcaption class="topic-cap">🇰🇷 한글 사례</figcaption><img class="topic-img ko-img" src="images/privacy_ko_prac.png" loading="lazy" alt="🇰🇷 한글 사례"></figure>
<figure class="topic-fig"><figcaption class="topic-cap">🇺🇸 English Case</figcaption><img class="topic-img en-img" src="images/privacy_en_prac.png" loading="lazy" alt="🇺🇸 English Case"></figure>
</div>
</div>
</div>
</div>
</div>
<div class="ktk-prac-block">
<div class="ktk-prac-cl-hd">◆ Other</div>
<div class="ktk-prac-card">
<div class="ktk-prac-q-num">Q32 <span style="font-weight:400;color:#888;font-size:.65rem">— duty_premises</span></div>
<div class="ktk-prac-q-text">(팩트패턴 원문 손상 — 해설 참조)</div>
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="D">
<div class="ktk-prac-answer-badge">정답: (D)</div>
<div class="ktk-prac-exp-text">(D) Liability. An invitee is a person who enters onto defendant\'s land with express or implied invitation for purposes relating to defendant\'s interests or activities (i.e., to conduct business), or where the land is held open to the public at large. Land possessors owe a duty to exercise reasonable care to prevent injuries to invitees and to inspect for hidden dangers on the property. Although Peter initially committed trespass when he walked into the restricted area, once the clerk consented to his presence, his status changed to an invitee. Therefore, the store will be vicariously liable for its failure to exercise reasonable care — including the failure to warn Peter of open dangers that the clerk had reason to believe Peter was unaware of.</div>
</div>
</div>
<div class="ktk-prac-card">
<div class="ktk-prac-q-num">Q63 <span style="font-weight:400;color:#888;font-size:.65rem">— respondeat</span></div>
<div class="ktk-prac-q-text">Miller, a flight attendant employed by Fly Airline, was involved in an altercation with a passenger during a flight. The altercation arose from a dispute over seating. Miller intentionally struck the passenger. The passenger sues both Miller and Fly Airline. Is Fly Airline liable for Miller\'s battery?</div>
<div class="ktk-prac-opt">(A) Yes, because Miller was acting as Fly Airline\'s agent.</div>
<div class="ktk-prac-opt">(B) Yes, because the incident occurred during the course of Miller\'s employment.</div>
<div class="ktk-prac-opt">(C) No, unless Miller\'s use of force was within the scope of employment and for the employer\'s benefit.</div>
<div class="ktk-prac-opt">(D) No, because intentional torts can never be attributed to an employer.</div>
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="C">
<div class="ktk-prac-answer-badge">정답: (C)</div>
<div class="ktk-prac-exp-text">Under respondeat superior, an employer is vicariously liable for an employee\'s tortious acts committed within the scope of employment. An employee\'s intentional tort may fall within the scope of employment if: (1) the employee was authorized to use force, (2) the employer was reckless in employing the individual, or (3) the act was motivated by a purpose to serve the employer. While a flight attendant\'s duties include maintaining order, an unprovoked intentional battery arising from a seating dispute is not authorized conduct and does not serve the employer\'s business purposes. Therefore, Fly Airline is not liable unless Miller\'s use of force was within the scope of employment and for the employer\'s benefit.</div>
</div>
</div>
<div class="ktk-prac-card">
<div class="ktk-prac-q-num">Q104 <span style="font-weight:400;color:#888;font-size:.65rem">— consent</span></div>
<div class="ktk-prac-q-text">Player, a professional soccer athlete, signed written consent with Modic, the team physician, to conduct a knee surgery. Once Player was anesthetized, Medic asked Surgeon, a globally renowned orthopedic surgeon, to carry out the procedure. Surgeon, possessing superior surgical expertise compared to Medic, successfully completed the operation.<br><br>In an action for battery by Player against Surgeon, Player will:</div>
<div class="ktk-prac-opt">(A) Prevail, because Player did not agree to allow Surgeon to perform the operation.</div>
<div class="ktk-prac-opt">(B) Prevail, because the consent was in writing.</div>
<div class="ktk-prac-opt">(C) Not prevail, because Surgeon\'s skill was superior to Medic\'s.</div>
<div class="ktk-prac-opt">(D) Not prevail, because the operation was successful.</div>
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="A">
<div class="ktk-prac-answer-badge">정답: (A)</div>
<div class="ktk-prac-exp-text">Battery requires a harmful or offensive contact that is intentional. Consent is a defense to battery, but consent only covers the scope agreed to. Player consented to Medic performing the surgery, not Surgeon. The scope of Player\'s consent did not extend to Surgeon\'s performance of the operation. Therefore, Player prevails in the battery action against Surgeon because the contact exceeded the scope of Player\'s consent.</div>
</div>
</div>
</div>
</div>
'''

# ── Insert ktk_prac div after the practice cls div ──
# The practice div ends with 4 closing divs then a blank line then <script>
old_practice_end = '</div>\n</div>\n</div>\n</div>\n\n<script>'
count = content.count(old_practice_end)
print(f'ktk_prac insertion anchor: {count}')
if count == 1:
    content = content.replace(old_practice_end, '</div>\n</div>\n</div>\n</div>\n\n' + ktk_prac_html + '\n<script>')
    print('ktk_prac div inserted')
else:
    print(f'ERROR: anchor count={count}, not unique')

with open(r'F:\mbe\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('DONE')
