#!/usr/bin/env python3
"""build_contracts_ktk.py — contracts/index.html (KTK-first build) 생성"""
import os, html

OUT = os.path.join(os.path.dirname(__file__), '..', 'torts-deploy', 'contracts', 'index.html')

# ── 문제 데이터 ──────────────────────────────────────────────────────────────
# imgs: [ko_prac_img, en_prac_img]  (contracts/images/ 기준, 확장자 없이)
BLOCKS = [

  ("📌 Applicable Law & Formation", [
    dict(
      num="Q3", label="Applicable Law — UCC Output Contract",
      text="Bestbake, Co., a bakery product manufacturer, entered into a written agreement with Today's Pastry Inc., a pastry retailer. Under the agreement, Today's Pastry agreed to purchase all of Bestbake's one-year output of baked buns. The agreement specified no fixed quantity. When Bestbake tendered its output, Today's Pastry refused to accept any baked buns. In a breach of contract action by Bestbake, which of the following best explains why Today's Pastry is liable?",
      opts=["(A) Nothing can be recovered, because the contract lacks a specific quantity term and is unenforceable under the UCC.",
            "(B) Nothing can be recovered, because the contract lacked mutuality of obligation — Bestbake was not bound to produce any specific amount.",
            "(C) Bestbake can recover, because UCC output contracts impose a best efforts obligation on both buyer and seller.",
            "(D) Bestbake can recover only production costs, because the contract did not specify a purchase price."],
      correct="C",
      exp="Because the contract involves the sale of goods, the UCC controls. Under the UCC, output contracts are agreements in which the buyer agrees to purchase all of a seller's output. Such contracts impose an implied obligation of good faith — sellers must use best efforts to supply, and buyers must use best efforts to purchase. The absence of a fixed quantity term does not render the contract unenforceable under the UCC; output contracts satisfy the UCC Statute of Frauds because the output itself constitutes a sufficient quantity term.",
      imgs=["applicable_law_ko_prac","applicable_law_en_prac"]
    ),
    dict(
      num="Q56", label="UCC §2-207 — Accommodation / Counter-Offer",
      text='Zoe, a widget manufacturer, received a purchase order from Books for 1,000 conforming widgets. Zoe did not have conforming widgets in stock. Zoe sent Books a shipment of non-conforming (defective) widgets along with a note stating: "We are sending defective widgets in case you can use them." Books received the shipment. Which of the following best describes the legal effect of Zoe\'s response?',
      opts=["(A) Zoe's shipment constitutes an acceptance of Books's offer, creating a binding contract for 1,000 conforming widgets.",
            "(B) Zoe's shipment of non-conforming goods with an explanatory note constitutes a counter-offer, which Books may accept or reject.",
            "(C) Zoe's shipment constitutes a breach of the original contract, and Books may sue for the difference in value.",
            "(D) There is no contract because Zoe failed to ship conforming goods in response to the purchase order."],
      correct="B",
      exp="Under the UCC, when a seller responds to a purchase order by shipping non-conforming goods as an 'accommodation' — accompanied by a notice that the goods are sent as a substitute — the shipment constitutes a counter-offer rather than an acceptance. Books may freely accept the counter-offer (and thereby be bound to pay the listed price for the defective widgets) or reject it (in which case no contract exists and Books simply returns the goods). If Zoe had shipped the non-conforming goods without the explanatory note, it would constitute both an acceptance and a breach.",
      imgs=["ucc_battle_forms_ko_prac","ucc_battle_forms_en_prac"]
    ),
  ]),

  ("📌 Offer, Acceptance & Firm Offer", [
    dict(
      num="Q57", label="Firm Offer — Non-Merchant Revocation",
      text="On November 1, Debby, a retired accountant, entered into a contract to sell law books to Solicitor for $10,000, payable on December 1 delivery. On November 10, Debby sent Solicitor a written note: 'I've decided to include the book stacks. I'll deliver them along with the books on December 1 at no extra charge. Please notify me by November 15 if you want them — I won't offer them to anyone else until then.' On November 14, Solicitor faxed acceptance. On November 1, Debby told Solicitor she had decided not to include the stacks. Debby was not a merchant with respect to law books or bookshelves. Will Debby's communication operate as a legally effective revocation of her offer to include the stacks?",
      opts=["(A) Yes, because Solicitor had a pre-existing obligation to pay $10,000 for the law books.",
            "(B) Yes, because Debby was not a merchant with respect to book stacks, so the UCC Firm Offer rule does not apply.",
            "(C) No, because Debby gave written assurance that the offer would remain open until November 15.",
            "(D) No, because Solicitor detrimentally relied on the promise to include the stacks."],
      correct="B",
      exp="The UCC Firm Offer rule (§2-205) provides that a signed, written offer by a merchant assuring it will be held open is irrevocable for the stated period (up to 3 months) without consideration. However, this rule applies only to merchants. Debby was not a merchant with respect to law books or bookshelves. Under Common Law, which governs here, a promise to hold an offer open is not binding without consideration. The $10,000 book sale did not constitute consideration for the promise to hold the stack offer open. Therefore, without consideration, Debby's promise to keep the offer open was not binding, and the offer was freely revocable.",
      imgs=["firm_offer_option_ko_prac","firm_offer_option_en_prac"]
    ),
    dict(
      num="Q77", label="Consideration — Pre-Existing Duty Rule",
      text="Collector, the owner of an impressionist painting valued at $400,000, was victimized when a burglar stole it. Having insured the painting with Assisi Insurance Co. for $300,000, Collector offered Checker, a full-time investigator employed by Assisi, a reward of $25,000 if he successfully retrieved the painting undamaged. Assisi's policy allows its investigators to keep rewards from clients. Checker located and returned the painting in undamaged condition. If Collector refuses to pay Checker, and Checker sues for $25,000, what is the probable result under the prevailing modern rule?",
      opts=["(A) Collector wins, because Checker owed Assisi a pre-existing duty to recover the painting if possible.",
            "(B) Collector wins, because Assisi, Checker's employer, had a pre-existing duty to ensure the painting was returned to Collector.",
            "(C) Checker wins, because Collector would be unjustly enriched by receiving the $400,000 painting while paying only $300,000 in insurance proceeds.",
            "(D) Checker wins, because the pre-existing duty rule does not apply when the duty was owed to a third party rather than to the promisor."],
      correct="D",
      exp="Under the traditional pre-existing duty rule, performing a duty one is already legally obligated to perform is not valid consideration. However, under the modern rule, the pre-existing duty rule does not apply when the duty was owed to a third party (Assisi) rather than to the promisor (Collector). Checker's duty ran to Assisi, his employer — not to Collector, who made the reward offer. Since Checker owed no pre-existing duty to Collector, Checker's performance constitutes valid consideration for Collector's reward promise.",
      imgs=["consideration_ko_prac","consideration_en_prac"]
    ),
  ]),

  ("📌 Capacity & Ratification", [
    dict(
      num="Q78", label="Capacity — Minor's Ratification",
      text="Suzy White, a minor both in fact and appearance, purchased a telescope on credit from Patrick Smith, age 30, for an agreed sum of $100. Shortly after reaching the age of majority, White met Smith, apologized for the overdue payment of $100 for the telescope, but stated she discovered the telescope's actual value was only $70 and promised to pay that reduced amount. White later retracted her promise and decided against paying Smith anything. In a breach of contract action by Smith against White, Smith's most likely recovery is:",
      opts=["(A) $0, because White disaffirmed the contract before the age of majority.",
            "(B) $100, because White ratified the full original contract upon reaching majority.",
            "(C) $70, because White's promise upon reaching majority was an effective ratification at that reduced amount.",
            "(D) The reasonable market value of the telescope, because necessaries doctrine applies."],
      correct="C",
      exp="When a minor reaches the age of majority, the minor may ratify contracts entered into during minority. Ratification can be express or implied by conduct. Here, White expressly ratified by promising to pay $70 after reaching majority. Although the original contract price was $100, White's post-majority promise to pay $70 constitutes an effective ratification at the reduced amount. Once ratified, the contract becomes fully binding and White cannot disaffirm. White's subsequent retraction is therefore ineffective — she is bound to pay $70.",
      imgs=["capacity_minors_ko_prac","capacity_minors_en_prac"]
    ),
    dict(
      num="Q91", label="Capacity — Illusory Promise ('as soon as possible')",
      text="Suzy White purchased a telescope from Patrick Smith after reaching the age of majority and promised to pay $100 'as soon as possible.' White later refused to pay anything. Smith sues for breach of contract. White argues that the phrase 'as soon as possible' renders her promise illusory and therefore unenforceable. What effect does this quoted language have on the enforceability of the promise?",
      opts=["(A) None — the promise remains enforceable because 'as soon as possible' merely postpones the time of payment, not the obligation itself.",
            "(B) It renders the promise illusory because White could always claim she lacks the ability to pay.",
            "(C) It requires White to prove her ability to pay before the promise becomes binding.",
            "(D) It requires Smith to prove White's ability to pay at the time the promise was made."],
      correct="A",
      exp="An illusory promise is one that appears to be a commitment but actually imposes no obligation on the promisor — for example, 'I'll pay if I feel like it.' The phrase 'as soon as possible' is not illusory because it still imposes a real obligation to pay — it merely makes the payment time contingent on White's financial ability. Courts interpret 'as soon as possible' as an objective standard, not a subjective escape hatch. The promise creates a binding obligation to pay within a reasonable time when payment becomes feasible, and White's absolute refusal to pay anything constitutes a breach.",
      imgs=["capacity_minors_ko_prac","capacity_minors_en_prac"]
    ),
  ]),

  ("📌 Parol Evidence & Course of Performance", [
    dict(
      num="Q21", label="Parol Evidence Rule — Course of Performance",
      text="Wavelaster Inc., a radio manufacturer, and Wetailers Co., a retailer, finalized a written agreement under which Wavelaster would sell and Wetailers would purchase all radio equipment, estimated at 20 units per month, from January 1999 to December 2001, at $50 per unit. In late December 2001, Wetailers returned 25 non-defective radios. The written agreement explicitly allowed buyers to return defective radios for a refund but was silent on returning non-defective radios. In a suit by Wavelaster against Wetailers, Wetailers seeks to introduce evidence that over the 3-year contract period, it had returned 125 non-defective radios which Wavelaster accepted. Wavelaster opposes admission of this evidence. The trial court is likely to rule the evidence:",
      opts=["(A) Inadmissible, because the evidence is barred by the parol evidence rule.",
            "(B) Inadmissible, because the express terms of the agreement contradict the course of performance evidenced.",
            "(C) Admissible, because the evidence supports an agreement not within the relevant statute of frauds.",
            "(D) Admissible, because course-of-performance evidence, when available, is considered the best indication of what the parties intended the writing to mean."],
      correct="D",
      exp="Under the UCC, course of performance — how the parties actually conducted themselves under the contract — is the best evidence of what the parties intended their contract to mean. The parol evidence rule bars evidence that contradicts an integrated written agreement, but it does not bar course-of-performance evidence used to interpret or explain ambiguous terms. The written contract was silent (not contradictory) on non-defective returns, so the course-of-performance evidence (125 returns accepted over 3 years) is admissible to interpret what the parties meant. Under UCC hierarchy: Course of Performance > Course of Dealing > Trade Usage.",
      imgs=["parol_evidence_ko_prac","parol_evidence_en_prac"]
    ),
  ]),

  ("📌 Conditions & Waiver", [
    dict(
      num="Q53a", label="Conditions — Waiver of Express Condition",
      text="Kevin and Steve entered into a contract providing that Kevin would supply Steve with an engine, but only if Kevin notified Steve in writing no later than February 1. On January 1, Steve verbally told Kevin, 'Just send the engine without the written notice — that's fine with me.' Kevin shipped the engine without providing any written notice. Steve now refuses to accept the engine and pay, claiming the written notice condition was not satisfied. Will Steve prevail?",
      opts=["(A) Yes, because express conditions require strict compliance, and Kevin failed to provide written notice as required.",
            "(B) No, because Kevin substantially performed by shipping the engine on time.",
            "(C) No, because Steve verbally waived the written notice condition before Kevin performed.",
            "(D) Yes, because an oral statement cannot waive a written condition in a contract."],
      correct="C",
      exp="A condition is an event that must occur before a party's performance obligation becomes due, unless the condition is waived or excused. A party may waive a condition — including a written-notice condition — orally. Here, Steve's verbal statement on January 1 constituted an express oral waiver of the written-notice condition. Once Steve waived the condition and Kevin performed in reliance on that waiver, Steve is estopped from retracting the waiver. Steve's attempt to enforce the written-notice condition after waiving it is ineffective.",
      imgs=["conditions_waiver_ko_prac","conditions_waiver_en_prac"]
    ),
    dict(
      num="Q51", label="UCC Perfect Tender — Right to Cure",
      text="Nathan ordered specialized industrial equipment from Carlillenes, with delivery required by July 1. On June 30, Nathan inspected the delivered equipment and discovered that one spare part was missing. Nathan immediately notified Carlillenes of the defect. Carlillenes offered to install the missing spare part by Monday, July 1. Which of the following best describes the parties' rights?",
      opts=["(A) Nathan may reject the equipment, but Carlillenes is also entitled to an opportunity to cure by July 1.",
            "(B) Nathan must accept the equipment because the missing spare part is immaterial and does not impair the equipment's value.",
            "(C) Nathan may reject the equipment, and Carlillenes has no right to cure once the buyer has rightfully rejected.",
            "(D) Nathan must give Carlillenes a reasonable additional time beyond July 1 to install the spare part."],
      correct="A",
      exp="Under the UCC's Perfect Tender Rule, a buyer may reject goods that fail to conform to the contract in any respect, even if the non-conformity is trivial. Therefore, Nathan can reject the equipment because of the missing spare part. However, when a defect is discovered before the contract deadline and time for performance has not yet expired, the seller has a right to cure the defective delivery before the deadline. Here, the defect was discovered on June 30, one day before the July 1 deadline, giving Carlillenes the right to cure by installing the spare part by July 1. Nathan may reject, but must allow Carlillenes the opportunity to cure within the contract period.",
      imgs=["material_breach_cure_ko_prac","material_breach_cure_en_prac"]
    ),
  ]),

  ("📌 Impracticability & Mistake", [
    dict(
      num="Q34", label="Impracticability / Risk Allocation",
      text="Const Inc. contracted with Newtech to design and construct a 15-story office building on Newtech's land for $20 million. During excavation, workers encountered an unexpectedly thick granite layer, requiring excavation 1 foot deeper than designed. This increased construction costs by $3 million and is projected to result in a $2 million loss for Const Inc. Const Inc. notified Newtech that it would not continue without additional compensation. If Newtech refuses and sues Const Inc. for breach, how will the court most likely rule?",
      opts=["(A) Const Inc. is excused under the modern doctrine of commercial impracticability due to the severe practical difficulty posed by the granite.",
            "(B) Const Inc. is excused because the contract is void for mutual mistake — both parties assumed there was no subsurface granite.",
            "(C) Newtech prevails, because Const Inc. assumed the risk that subsurface conditions might increase excavation costs.",
            "(D) Newtech prevails, because Const Inc. should have known about the subsurface granite based on the site's geological history."],
      correct="C",
      exp="A contract may be rescinded for mutual mistake only if both parties acted under a common erroneous assumption about a material fact and the party seeking rescission did not bear the risk of the mistake. Impracticability excuses performance only when an unanticipated event makes performance commercially impracticable and the risk of that event was not allocated to the performing party. Here, Const Inc. is engaged in the business of excavation and had the opportunity to investigate the foundation before contracting. As an excavation professional, Const Inc. assumed the risk that subsurface conditions — including granite — might increase costs. Neither impracticability nor mutual mistake provides relief when the party asserting it bore the risk.",
      imgs=["impossibility_frustration_ko_prac","impossibility_frustration_en_prac"]
    ),
  ]),

  ("📌 Breach & Remedies", [
    dict(
      num="Q53b", label="Liquidated Damages — Penalty Analysis",
      text="Melanie owns a fishing boat which she charters for $500 per day. On July 1, Paul booked the boat for July 15 for himself and his family, paying a $200 deposit. The contract allowed Melanie to retain the deposit if Paul canceled or failed to appear. Melanie told Paul to arrive at the dock by 5 a.m. on July 15. Paul did not arrive until noon because he had been attempting to charter a cheaper boat. By 10 a.m., Melanie had taken Tyra's family on a trip for $400. Which of the following accurately describes the rights of the parties?",
      opts=["(A) Melanie may retain the full $200 deposit, because it was difficult to estimate Melanie's actual damages and the amount was a reasonable forecast of anticipated loss.",
            "(B) Melanie is entitled to retain only $50 (10% of the contract price) and must return $150 to Paul.",
            "(C) Melanie must return $100 to Paul to avoid unjust enrichment.",
            "(D) Melanie must return $100 to Paul, because the liquidated damages clause operates as a penalty under the circumstances."],
      correct="D",
      exp="A liquidated damages clause is enforceable only if (1) damages were difficult to estimate at the time of contracting, and (2) the stipulated amount was a reasonable forecast of compensatory damages. A clause that results in a recovery grossly disproportionate to actual damages constitutes an unenforceable penalty. Here, Melanie's actual damages were limited: she earned $400 from Tyra's trip, so her actual loss from Paul's breach was approximately $100 ($500 - $400). Retaining the full $200 deposit — double her actual damages — would result in a windfall and constitutes a penalty. Melanie may retain $100 to compensate her actual loss but must return the remaining $100.",
      imgs=["liquidated_damages_ko_prac","liquidated_damages_en_prac"]
    ),
    dict(
      num="Q69", label="Breach — Expectation Damages + Duty to Mitigate",
      text="Jay, a building contractor, entered into a contract with Gyson to perform construction work on Gyson's warehouse for a projected profit of $3,000. Before Jay began any work, Gyson expressly and unequivocally repudiated the contract. Despite receiving clear notice of Gyson's repudiation, Jay proceeded to purchase $5,000 worth of materials and began preliminary work before stopping. Jay then filed suit seeking $8,000 in damages ($5,000 in materials + $3,000 expected profit). What is Jay's most likely recovery?",
      opts=["(A) $0, because Jay's failure to mitigate bars any recovery.",
            "(B) $3,000 — the expected profit only, because the $5,000 post-breach expenditure was avoidable.",
            "(C) $5,000 — the value of the benefit Jay conferred on Gyson.",
            "(D) $8,000 — full expectation damages including all costs and profits."],
      correct="B",
      exp="By default, aggrieved parties are entitled to expectation damages — the amount that would put the non-breaching party in the position they would have been had the contract been performed. However, the aggrieved party has a duty to mitigate damages: they cannot recover losses they could have reasonably avoided after breach. Here, Jay can recover the $3,000 profit he would have earned had the contract been performed. However, Jay cannot recover the $5,000 spent on materials after being notified of Gyson's express repudiation, because those expenses were reasonably avoidable. Jay's failure to mitigate after receiving clear notice of repudiation bars recovery of the post-breach expenditure.",
      imgs=["breach_remedies_ko_prac","breach_remedies_en_prac"]
    ),
    dict(
      num="Q74", label="Anticipatory Repudiation — Dealer's Best Defense",
      text="On February 1, Dealer obtained a rare coin from Hellenes for $1,000 and in exchange gave Hellenes a signed written promise to deliver a similar coin 'not later than December 31' at no cost. The coin market fell sharply from October 11. On October 15, Hellenes asked Dealer about performance. On October 17, Dealer responded that 'it would be unfair to fulfill his obligation within the upcoming weeks due to the market's surprising shift.' On November 15, Hellenes sued. The trial commenced December 1. If Dealer moves to dismiss Hellenes' complaint, what is Dealer's best argument?",
      opts=["(A) Dealer did not repudiate the contract on October 17 and may still perform by the contract deadline of December 31.",
            "(B) Even if Dealer repudiated, Hellenes' only remedy is specific performance because the coin is a unique chattel.",
            "(C) Under the doctrine of impossibility and commercial impracticability, the market decline excuses Dealer's performance.",
            "(D) Even if Dealer repudiated, Hellenes has no remedy without first demanding in writing that Dealer retract the repudiation."],
      correct="A",
      exp="Anticipatory repudiation requires an unequivocal and definitive statement of intent not to perform before the performance deadline. Dealer's statement on October 17 — that it 'would be unfair' to perform 'within the upcoming weeks' — is arguably ambiguous rather than an unequivocal refusal to perform by December 31. Dealer's best argument for dismissal is that this ambiguous statement does not constitute an anticipatory repudiation, and Dealer still has until December 31 to perform. An ambiguous statement about performance difficulty is not the same as a clear repudiation. (Note: (B) is incorrect — UCC doesn't restrict aggrieved party to specific performance. (C) is weak — market decline alone is not impracticability. (D) is incorrect — no written demand is required under UCC.)",
      imgs=["anticipatory_repudiation_ko_prac","anticipatory_repudiation_en_prac"]
    ),
  ]),

  ("📌 Accord & Satisfaction", [
    dict(
      num="Q22", label="Accord & Satisfaction — 'Payment in Full' Check",
      text="Wavelaster Inc. and Wetailers Co. had a written radio supply agreement from January 1999 to December 2001 at $50/unit. In late December 2001, Wetailers returned 25 non-defective radios. Along with the returned radios, Wetailers included a check payable to Wavelaster for the balance due on all other goods delivered, conspicuously marked: 'Payment in full for all goods sold to Wetailers Co. to date.' Wavelaster's clerk, reading this notation and knowing that Wetailers had also returned the 25 non-defective radios for credit, deposited the check without protest. The canceled check was later returned to Wetailers. Which ground would best serve Wetailers in defense?",
      opts=["(A) Wavelaster's deposit of the check and its return to Wetailers estopped Wavelaster from claiming any additional amount.",
            "(B) By depositing the check without protest and with knowledge of its wording, Wavelaster discharged any claim against Wetailers through accord and satisfaction.",
            "(C) The deposit of the check constituted a novation, replacing Wavelaster's original claim with the check amount.",
            "(D) Wetailers' notation on the check constituted a unilateral modification of the contract, which Wavelaster accepted by depositing the check."],
      correct="B",
      exp="An accord is a contract under which the obligee (creditor) agrees to accept a different performance in satisfaction of the obligor's (debtor's) existing duty. Satisfaction occurs when the accord is performed, thereby discharging the original obligation. A 'Payment in Full' check, when deposited by the creditor with knowledge of its notation, constitutes an accord and satisfaction. Wavelaster's clerk read the 'Payment in Full' notation and deposited the check anyway without protest — this constitutes Wavelaster's acceptance of the accord. Once deposited, Wavelaster cannot later claim the balance for the 25 returned radios. Answer (A) is close but estoppel is a weaker and less precise ground than accord and satisfaction.",
      imgs=["accord_satisfaction_ko_prac","accord_satisfaction_en_prac"]
    ),
    dict(
      num="Q55", label="Accord & Satisfaction — Good Faith Dispute",
      text="Attorney represented Client in a real estate transaction and sent a bill for $8,000 in legal fees. Client disputed the amount, believing that due to an unexpected title problem that arose, the work was worth only $5,000. The parties exchanged several letters expressing their disagreement. Client then sent Attorney a check for $5,000 marked 'Payment in full and final satisfaction of all legal fees owed.' Attorney read the notation and deposited the check without protest or reservation of rights. Attorney now sues for the remaining $3,000. What is the most likely outcome?",
      opts=["(A) Attorney prevails, because the original $8,000 fee agreement controls and a unilateral check notation cannot modify it.",
            "(B) Client prevails, because Attorney's deposit of the check without protest constituted an accord and satisfaction discharging the remaining balance.",
            "(C) Attorney prevails, because the check notation was not signed by Attorney as required to modify the fee agreement.",
            "(D) Client prevails, because the fee agreement lacked consideration since the title problem was not anticipated."],
      correct="B",
      exp="An accord and satisfaction requires (1) a good-faith dispute about the amount owed and (2) an unambiguous tender of a check as full payment, followed by the creditor's deposit. A good-faith dispute about the amount owed provides sufficient consideration for the accord, even with a partial payment. Here, there was a legitimate, bona fide dispute about the amount of legal fees (the parties exchanged letters). Client unambiguously tendered the check as 'full and final satisfaction.' Attorney read the notation and deposited the check without protest, thereby accepting the accord. The accord is satisfied, discharging the remaining $3,000 obligation.",
      imgs=["accord_satisfaction_ko_prac","accord_satisfaction_en_prac"]
    ),
  ]),

  ("📌 Third-Party Beneficiary", [
    dict(
      num="Q57c", label="Third-Party Beneficiary — Vesting of Rights",
      text="Kailyn, owner of a taxi fleet, contracted with Phil, a petroleum dealer, for the purchase of Kailyn's total gasoline requirements for one year. As part of the agreement, Phil agreed to exclusively engage Sally's advertising agency for a year. When Sally learned of the Kailyn-Phil contract, she declined another advertising account to ensure she could serve both Phil and Kailyn. Sally was an intended beneficiary of the Kailyn-Phil contract. Kailyn performed his contract with Phil for six months, during which Phil engaged Sally's advertising services. Kailyn and Sally then divorced, and Kailyn informed Phil he no longer needed to use Sally's services. Phil told Sally he would stop using her services. In a lawsuit by Sally against Phil to enforce the contract, Sally would likely:",
      opts=["(A) Succeed, because Phil and Kailyn could not, without Sally's consent, modify the contract to discharge Phil's duties to Sally once her rights vested.",
            "(B) Succeed, because Kailyn acted in bad faith in releasing Phil from his duties to Sally.",
            "(C) Not succeed, because the promisor and promisee of a third-party beneficiary contract retain the right to modify or terminate absent a contrary provision.",
            "(D) Not succeed, because any agency relationship between Kailyn and Sally was terminated by their divorce."],
      correct="A",
      exp="A third-party beneficiary's rights vest when the beneficiary (1) manifests assent to the contract, (2) changes position in justifiable reliance, or (3) brings suit to enforce it. Once rights vest, the promisor and promisee cannot modify or rescind the contract without the beneficiary's consent. Here, Sally was an intended beneficiary whose rights vested when she declined another advertising account in reliance on the Kailyn-Phil contract and began performing advertising services for six months. After Sally's rights vested, Kailyn and Phil could not discharge Phil's duties to Sally without Sally's consent. Sally may enforce the contract against Phil.",
      imgs=["third_party_ko_prac","third_party_en_prac"]
    ),
    dict(
      num="Q33", label="Third-Party Beneficiary — Incidental Beneficiary",
      text="On February 1, Beth contracted with Carlson to sell a specific rare coin for $12,000, with delivery and payment on May 1. Unknown to Carlson, Beth also contracted on March 1 with Harald to sell the same coin for $10,000, delivery April 1. The coin's value fell to $8,000 by April 1, and Beth delivered the coin to Harald. The market recovered to $12,000 by May 1, but Beth failed to deliver to Carlson. Harald later told Carlson that Carlson should take legal action against Beth. Carlson now seeks to enforce the Beth-Harald contract as a third-party beneficiary. Will Carlson prevail in enforcing the Beth-Harald contract?",
      opts=["(A) No, because Carlson is only an incidental beneficiary of the Beth-Harald contract and has no standing to enforce it.",
            "(B) No, because the Beth-Harald contract was already fully performed by the time Carlson sought to enforce it.",
            "(C) Yes, because Carlson was an intended creditor beneficiary of the Beth-Harald contract.",
            "(D) Yes, because Harald's disclosure to Carlson constituted an effective assignment of rights."],
      correct="A",
      exp="A third party may enforce a contract only if they are an intended beneficiary — one the contracting parties intended to benefit. An incidental beneficiary — one who merely happens to benefit as a side effect — has no enforceable rights. Under the intent-to-benefit test, a party is an intended beneficiary only if the contract was made for the purpose of benefiting that party. Here, the Beth-Harald contract was made for Beth and Harald's benefit. Harald was unaware of the Beth-Carlson contract; he did not intend the Beth-Harald deal to benefit Carlson. Carlson is merely an incidental beneficiary with no standing to enforce the Beth-Harald contract. Carlson's remedy, if any, lies against Beth for breach of the Beth-Carlson contract.",
      imgs=["third_party_ko_prac","third_party_en_prac"]
    ),
    dict(
      num="Q95", label="Third-Party Beneficiary — Incidental Beneficiary (Neighbor)",
      text="Landowner contracted with Contractor to construct a large office building on Landowner's lot. Neighbor, whose property adjoins Landowner's, hoped the building would block the prevailing wind from his property and reduce his heating bills. Contractor failed to complete the building as contracted. Neighbor sues Contractor as a third-party beneficiary of the Landowner-Contractor contract. Which of the following best states why Neighbor cannot recover?",
      opts=["(A) Neighbor is only an incidental beneficiary of the Landowner-Contractor contract and has no enforceable rights under it.",
            "(B) Neighbor lacks privity of contract with Contractor and therefore has no tort or contract claim.",
            "(C) Neighbor cannot enforce the contract because there is no showing that Contractor breached a duty owed to Neighbor personally.",
            "(D) Neighbor's interest — reduced heating bills — is too speculative to constitute a legally cognizable harm."],
      correct="A",
      exp="Incidental beneficiaries are third parties who receive a practical benefit from a contract's performance, but the contracting parties did not intend to confer a legal benefit on them. Under the intent-to-benefit test, a party is an incidental beneficiary — with no enforceable rights — when the contract was not made for the purpose of benefiting that party. Here, the Landowner-Contractor contract was made to construct a building for Landowner's benefit. Any benefit to Neighbor (reduced wind, lower heating costs) is incidental and unintended by the contracting parties. Incidental beneficiaries have no standing to sue to enforce the contract.",
      imgs=["third_party_ko_prac","third_party_en_prac"]
    ),
  ]),

  ("📌 Assignment & Delegation", [
    dict(
      num="Q63", label="Assignment — Executory Contract / Rights vs. Duties",
      text="Jay, a flour supplier, contracted with Smith, a bakery, to supply all of Smith's flour requirements for one year starting November 1. Before performance began, Jay sold his entire business to Brooks Inc. and assigned all his contracts — including the Smith contract — to Brooks Inc. Jay notified Smith of the assignment. Brooks Inc. performed the contract and delivered flour to Smith. Smith seeks to argue that the assignment was invalid. Which of the following statements best supports Smith's claim that she need not pay Brooks Inc.?",
      opts=["(A) Smith never consented to dealing with Brooks Inc. as her flour supplier.",
            "(B) The assignment language transferred rights only; the performance obligations remained with Jay.",
            "(C) Both I (executory contracts are non-assignable) and III (assignment language transfers rights only, not duties) are accurate statements supporting Smith's obligation to pay Jay.",
            "(D) Both I and III are accurate: executory contracts and rights transfers support why Smith's payment should go to Brooks Inc."],
      correct="D",
      exp="Generally, contractual rights can be assigned freely. When Jay assigned the contract to Brooks Inc. and notified Smith, Brooks Inc. acquired the right to receive payment from Smith. The assignment language 'transfer of all contracts' transferred Jay's right to payment — not a discharge of Jay's obligations. Executory contracts (those not yet performed) are generally assignable unless they materially change the obligor's duties. Here, the flour-supply contract was assignable because supplying flour to Smith did not become materially different just because Brooks Inc. would supply it. Once Smith was notified of the assignment, she was obligated to pay Brooks Inc., not Jay. Statements I and III together support why Smith's payment obligation runs to Brooks Inc.",
      imgs=["assignment_delegation_ko_prac","assignment_delegation_en_prac"]
    ),
    dict(
      num="Q64", label="Assignment — Obligor's Payment to Assignor After Notice",
      text="Jay contracted with Smith to supply flour for one year. Before performance, Jay sold his business and assigned the Smith contract to Brooks Inc. Jay notified Smith of the assignment. Brooks Inc. performed the contract and delivered flour per the contract terms. Smith paid Jay directly (instead of Brooks Inc.), believing her obligation was still owed to Jay. Brooks Inc. now sues Smith for the contract price. Which of the following defenses is available to Smith?",
      opts=["(A) Smith was not required to pay Brooks Inc. because she never expressly consented to the assignment.",
            "(B) Smith's payment to Jay discharged her obligation because Jay remained liable to Brooks Inc. as the delegator.",
            "(C) Smith's payment to Jay discharges her obligation because she was not notified of the assignment.",
            "(D) Smith has no valid defense — payment to Jay after receiving notice of the assignment does not discharge her obligation to Brooks Inc."],
      correct="D",
      exp="Once an obligor (Smith) receives notice of an assignment, the obligor must pay the assignee (Brooks Inc.). Payment to the assignor (Jay) after receiving notice of the assignment does NOT discharge the obligor's duty to the assignee. Smith received notice that Jay had assigned the contract to Brooks Inc. By paying Jay after that notice, Smith's payment was ineffective as to Brooks Inc. Smith remains obligated to pay Brooks Inc. and her only recourse is to seek reimbursement from Jay for the duplicative payment. Therefore, Smith has no valid defense against Brooks Inc.'s suit.",
      imgs=["assignment_delegation_ko_prac","assignment_delegation_en_prac"]
    ),
  ]),

  ("📌 Implied-in-Fact Contract", [
    dict(
      num="Q70", label="Implied-in-Fact Contract — vs. Quasi-Contract",
      text="In which of the following situations is an implied-in-fact contract most likely formed?",
      opts=["(A) A taxpayer mistakenly overpays taxes, and the government retains the overpayment without taking any action.",
            "(B) Doctor treats Ryder, an unconscious accident victim at the scene of a crash, and Ryder fully recovers.",
            "(C) Doctor fixes Neighbor's driveway while Neighbor watches and does not object to the work being done.",
            "(D) Contractor performs landscaping on the wrong house while the owner is away on vacation and unaware."],
      correct="C",
      exp="An implied-in-fact contract arises from conduct rather than words — courts infer an agreement from the parties' behavior and surrounding circumstances. The key element is that both parties manifested mutual assent through conduct. In (C), Neighbor observed Doctor fixing the driveway and did not object — this creates a reasonable inference that Neighbor agreed to pay for the benefit received, forming an implied-in-fact contract. Contrast (B): because Ryder was unconscious, he could not manifest assent, so no implied-in-fact contract is formed (though quasi-contract/unjust enrichment may apply). In (A), a mistaken tax overpayment cannot create an implied obligation on the government. In (D), the absent owner had no opportunity to accept or reject.",
      imgs=["implied_contract_ko_prac","implied_contract_en_prac"]
    ),
  ]),

]

# ── HTML 생성 ──────────────────────────────────────────────────────────────────

CSS = """
:root{--acc:#3d1880;--brd:#e0d0f0;--mut:#888;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Malgun Gothic',Arial,sans-serif;background:#f8f6ff;font-size:14px;}
.top-bar{position:sticky;top:0;z-index:400;background:#2d2060;color:#fff;padding:.45rem 1rem;display:flex;align-items:center;gap:.8rem;font-size:.78rem;}
.top-bar a{color:#c9b8f8;text-decoration:none;font-weight:700;}
.top-bar a:hover{color:#fff;}
.top-title{font-weight:700;font-size:.85rem;}
.ctabs{position:sticky;top:36px;z-index:299;background:#fff;border-bottom:2px solid var(--brd);display:flex;overflow-x:auto;}
.ctab{padding:.55rem 1.2rem;font-size:.78rem;font-weight:700;color:var(--mut);cursor:pointer;border-bottom:3px solid transparent;white-space:nowrap;transition:.15s;}
.ctab:hover{color:var(--acc);background:#f4f0ff;}
.ctab.on{color:var(--acc);border-bottom-color:var(--acc);}
.cls{display:none;padding:.8rem .9rem 4rem;max-width:1060px;margin:0 auto;}
.cls.on{display:block;}
/* KTK prac */
.ktk-prac-block{border:1.5px solid #c9b8e8;border-radius:8px;overflow:hidden;margin-bottom:1rem;}
.ktk-prac-cl-hd{background:#2d2060;color:#fff;font-size:.78rem;font-weight:700;padding:.45rem 1rem;}
.ktk-prac-card{border-top:1px solid #e0d0f0;padding:.7rem 1rem .8rem;}
.ktk-prac-q-num{font-size:.7rem;font-weight:700;color:#4a2d7a;margin-bottom:.3rem;}
.ktk-prac-q-text{font-size:.83rem;line-height:1.78;color:#222;margin-bottom:.55rem;}
.ktk-prac-opt{font-size:.8rem;padding:.2rem .5rem;margin:.15rem 0;border-radius:3px;line-height:1.5;color:#333;}
.ktk-prac-btn{width:100%;background:#4a2d7a;color:#fff;border:none;border-radius:4px;padding:.45rem;font-size:.78rem;font-weight:700;cursor:pointer;margin-top:.5rem;}
.ktk-prac-btn:hover{background:#3a1d6a;}
.ktk-prac-explain{display:none;margin-top:.6rem;border-top:1.5px dashed #d0b8f0;padding-top:.6rem;}
.ktk-prac-explain.kp-open{display:block;}
.ktk-prac-answer-badge{display:inline-block;background:#1a6a1a;color:#fff;font-size:.7rem;font-weight:700;padding:.2rem .7rem;border-radius:12px;margin-bottom:.4rem;}
.ktk-prac-exp-text{font-size:.8rem;line-height:1.75;color:#222;margin-bottom:.6rem;}
/* jenspark */
.jenspark-wrap{margin-top:.5rem;}
.jenspark-lbl{font-size:.65rem;font-weight:700;color:#7a5c00;background:#fdf6e3;padding:.2rem .6rem;border-radius:3px;display:inline-block;margin-bottom:.35rem;}
.jenspark-imgs{display:flex;gap:.5rem;flex-wrap:wrap;}
.topic-fig{flex:1;min-width:140px;max-width:320px;margin:0;}
.topic-cap{font-size:.65rem;font-weight:700;color:#555;display:block;margin-bottom:.2rem;}
.topic-img{width:100%;border-radius:4px;border:1px solid #ddd;display:block;}
.placeholder-img{width:100%;height:110px;border-radius:4px;border:1.5px dashed #c9b8e8;background:#f8f4ff;display:flex;align-items:center;justify-content:center;color:#b0a0cc;font-size:.7rem;font-weight:700;}
"""

JS = """
function showCls(id){
  document.querySelectorAll('.ctab').forEach(t=>t.classList.remove('on'));
  document.querySelectorAll('.cls').forEach(c=>c.classList.remove('on'));
  var el=document.getElementById(id);
  if(el) el.classList.add('on');
  var tabs=document.querySelectorAll('.ctab');
  tabs.forEach(t=>{ if(t.getAttribute('onclick') && t.getAttribute('onclick').includes("'"+id+"'")) t.classList.add('on'); });
}
function toggleKtkExp(btn){
  var exp=btn.nextElementSibling;
  if(!exp) return;
  exp.classList.toggle('kp-open');
  btn.textContent=exp.classList.contains('kp-open')?'답·해설 닫기':'답·해설 보기';
}
"""

def esc(s):
    return html.escape(s)

def make_img(src):
    return f'''<figure class="topic-fig">
<img class="topic-img" src="images/{src}.png" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'" alt="{src}">
<div class="placeholder-img" style="display:none">🖼 {src}.png</div>
</figure>'''

def make_card(p):
    opts_html = '\n'.join(f'<div class="ktk-prac-opt">{esc(o)}</div>' for o in p['opts'])
    imgs_html = '\n'.join(make_img(i) for i in p['imgs'])
    return f'''<div class="ktk-prac-card">
<div class="ktk-prac-q-num">{esc(p["num"])} <span style="font-weight:400;color:#888;font-size:.65rem">— {esc(p["label"])}</span></div>
<div class="ktk-prac-q-text">{esc(p["text"])}</div>
{opts_html}
<button class="ktk-prac-btn" onclick="toggleKtkExp(this)">답·해설 보기</button>
<div class="ktk-prac-explain" data-correct="{esc(p["correct"])}">
<div class="ktk-prac-answer-badge">정답: ({esc(p["correct"])})</div>
<div class="ktk-prac-exp-text">{esc(p["exp"])}</div>
<div class="jenspark-wrap">
<div class="jenspark-lbl">Jenspark 개념 이미지</div>
<div class="jenspark-imgs">{imgs_html}</div>
</div>
</div>
</div>'''

def make_block(title, problems):
    cards = '\n'.join(make_card(p) for p in problems)
    return f'''<div class="ktk-prac-block">
<div class="ktk-prac-cl-hd">{esc(title)}</div>
{cards}
</div>'''

blocks_html = '\n'.join(make_block(t, ps) for t, ps in BLOCKS)
total = sum(len(ps) for _, ps in BLOCKS)

html_out = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Contracts — MBE Study</title>
<style>{CSS}</style>
</head>
<body>
<div class="top-bar">
<a href="../index.html">← 과목 목록</a>
<span class="top-title">📝 Contracts</span>
<span style="margin-left:auto;font-size:.7rem;color:#b0a0e8">KTK {total}문제</span>
</div>
<div class="ctabs">
  <div class="ctab on" onclick="showCls('ktk_prac')">📋 KTK 문제풀이</div>
  <div class="ctab" onclick="showCls('placeholder_fc')" style="opacity:.4;cursor:default">🃏 플래시카드 (준비 중)</div>
  <div class="ctab" onclick="showCls('placeholder_vocab')" style="opacity:.4;cursor:default">📖 어휘 (준비 중)</div>
  <div class="ctab" onclick="showCls('placeholder_irac')" style="opacity:.4;cursor:default">✍ IRAC (준비 중)</div>
</div>
<div class="cls on" id="ktk_prac">
<div style="padding:.6rem 1rem .2rem;font-size:.75rem;color:#666">KTK 문제풀이 ({total}문제) — 팩트패턴 분석 후 ▼ 버튼으로 정답·해설 확인</div>
{blocks_html}
</div>
<script>{JS}</script>
</body>
</html>"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html_out)

lines = html_out.count('\n')
print("Done: " + OUT)
print("Problems: " + str(total) + " / Lines: " + str(lines))
