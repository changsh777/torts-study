import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'F:\mbe\_extracted\quiz_data.json', encoding='utf-8') as f:
    data = json.load(f)
pq = data['practice']
fixes = []

# P-Q1: B->C  (deadly force to protect property not allowed; warning doesn't excuse it)
pq[0]['correct_answer'] = 'C'
pq[0]['explanation'] = (
    "A person may not use deadly force (such as a spring gun, trap, or explosive device) "
    "merely to protect property. Under Katko v. Briney, the use of a deadly trap to protect "
    "unoccupied property is unlawful. A warning sign does not excuse the use of deadly force "
    "against a trespasser. Here, Tom planted an explosive charge in his driveway. Rocker will "
    "prevail if Tom was responsible for planting the charge, regardless of the warning sign, "
    "under both battery and strict liability theories."
)
fixes.append('P-Q1: B->C')

# P-Q2: D->B  (explanation says D is wrong; Jones has valid consent/mutual combat defense)
pq[1]['correct_answer'] = 'B'
pq[1]['explanation'] = (
    "In general, a defendant has no duty to rescue. Owens had no duty to rescue Vick (A is wrong). "
    "D is incorrect because Owens could be liable if he had undertaken a rescue and then abandoned "
    "it, or if he actively prevented others from rescuing. The absolute 'never' in D is wrong. "
    "Jones and Vick mutually agreed to fight, which may constitute consent -- a valid defense to "
    "battery. Therefore B (Jones has a valid defense) is the best available answer."
)
fixes.append('P-Q2: D->B')

# P-Q3: C->B  (explanation explicitly says B is the only answer that establishes causation)
pq[2]['correct_answer'] = 'B'
pq[2]['explanation'] = (
    "To prevail on lack of informed consent, the plaintiff must establish causation: would a "
    "reasonable person in the patient's position have refused the surgery if informed of the risk? "
    "Breach of duty alone (C) is insufficient. B correctly captures the causation element: "
    "Patient prevails only if a reasonable person would not have consented after full disclosure. "
    "Without this causation link, the non-disclosure does not give rise to liability."
)
fixes.append('P-Q3: C->B')

# P-Q4: C->A  (Zilch is a professional; explanation applies professional standard)
pq[3]['correct_answer'] = 'A'
pq[3]['explanation'] = (
    "In a contributory negligence jurisdiction, a plaintiff is barred from any recovery if her "
    "negligence contributed to the injury. Zilch was a professional worker safety inspector -- "
    "held to the standard of a reasonable person with his specialized training and experience. "
    "A reasonable worker safety inspector would know to wear a hard hat and avoid standing under "
    "overhead tracks in an active plant. Because Zilch's professional knowledge means he should "
    "have been aware of the danger, his failure to take precautions is contributory negligence, "
    "and Whizbang prevails."
)
fixes.append('P-Q4: C->A')

# P-Q5: A->C  (contributory negligence for roller blading with known balance problems)
pq[4]['correct_answer'] = 'C'
pq[4]['explanation'] = (
    "Mario is clearly liable for the head injury. For the hip injury: under eggshell plaintiff, "
    "Mario takes Shirley as he finds her (osteoporosis). The inner ear damage causing balance "
    "problems is a foreseeable consequence of a head injury, so the chain of causation is not "
    "broken by the fall. However, this is a contributory negligence jurisdiction. If Shirley "
    "acted unreasonably by going roller blading despite knowing she had balance problems caused "
    "by the accident, her contributory negligence bars recovery for the hip injury. She can "
    "recover for the head injury, but for the hip only if roller blading was not unreasonable."
)
fixes.append('P-Q5: A->C')

# P-Q6: C->B  (alternative causation doctrine applies; burden shifts to each defendant)
pq[5]['correct_answer'] = 'B'
pq[5]['explanation'] = (
    "Under the alternative-cause doctrine (Summers v. Tice), when (i) multiple defendants "
    "acted negligently, (ii) at least one caused the plaintiff's harm, and (iii) plaintiff "
    "cannot identify which defendant caused the harm, the burden shifts to each defendant to "
    "prove they did not cause the injury. Here, both Elway and Favre threw identical footballs "
    "at the roller coaster (negligent). One ball hit Rocky's eye, but since the balls were "
    "identical, Rocky cannot prove which defendant threw it. The burden shifts to each defendant. "
    "Rocky will prevail against both unless one can prove he did not throw the ball that hit the eye."
)
fixes.append('P-Q6: C->B')

# P-Q8: A->D  (no actual harm from numbing agent = no damages = no recovery)
pq[7]['correct_answer'] = 'D'
pq[7]['explanation'] = (
    "Negligence requires proof of all four elements: duty, breach, causation, and damages. "
    "Even assuming Dr. Doolittle breached her duty of informed consent by not disclosing the "
    "1% risk, Ricky suffered no harm -- the surgery succeeded and no sensation was lost. "
    "Without actual damages, the negligence claim fails. The existence of an undisclosed risk "
    "that never materialized is not sufficient for recovery."
)
fixes.append('P-Q8: A->D')

# P-Q9: B->A  (Patience did not apprehend danger = assault fails = Dimitri wins)
pq[8]['correct_answer'] = 'A'
pq[8]['explanation'] = (
    "Assault requires the plaintiff to actually experience imminent apprehension of harmful or "
    "offensive contact. Patience was wearing headphones at full volume and was completely unaware "
    "of Dimitri's car. Since Patience never subjectively apprehended any imminent contact, the "
    "essential element of assault is missing. Dimitri wins the assault claim."
)
fixes.append('P-Q9: B->A')

# P-Q11: C->D  (transferred intent; intent to contact Mike transfers to Susan)
pq[10]['correct_answer'] = 'D'
pq[10]['explanation'] = (
    "Under transferred intent, a defendant's intent to commit an intentional tort against one "
    "person transfers to another person actually harmed. Sam intended to throw coffee at Mike "
    "(intent to cause offensive contact with Mike). When the coffee hit Susan instead, Sam's "
    "intent transfers to the contact with Susan. The contact with Susan's dress satisfies the "
    "contact element of battery. C is incorrect because transferred intent does not require "
    "Sam to have been aware of the risk to Susan."
)
fixes.append('P-Q11: C->D')

# P-Q16: C->A  (high utility helps defendant win design defect; C helps plaintiff)
pq[15]['correct_answer'] = 'A'
pq[15]['explanation'] = (
    "In a design defect risk-utility analysis, the defendant wins by showing benefits outweigh "
    "risks. High usefulness and desirability of the product (A) is the factor most likely to "
    "help the defendant -- it shows the product's utility to users and the public justifies "
    "the risk. By contrast: (B) high likelihood of serious injury helps plaintiff; (C) ability "
    "to spread loss via insurance helps plaintiff by showing defendant can bear the cost; "
    "(D) availability of a safer substitute helps plaintiff by establishing reasonable "
    "alternative design."
)
fixes.append('P-Q16: C->A')

# P-Q17: C->B  (which is FALSE: Tina CAN sue retailer under strict products liability)
pq[16]['correct_answer'] = 'B'
pq[16]['explanation'] = (
    "The question asks which statement is FALSE. Under strict products liability (Restatement "
    "Second s.402A), any commercial seller in the distribution chain -- including retailers -- "
    "may be strictly liable. Therefore, Tina CAN sue Cars for You (the retailer), making B "
    "false. A is true (Sammy can sue manufacturer and retailer); C is true (Tina can sue "
    "Sammy in negligence for failing to get required inspections); D is true (consumers have "
    "no duty to discover latent defects but must exercise due care)."
)
fixes.append('P-Q17: C->B')

with open(r'F:\mbe\_extracted\quiz_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Practice {len(fixes)}개 수정:')
for fix in fixes:
    print(f'  - {fix}')
