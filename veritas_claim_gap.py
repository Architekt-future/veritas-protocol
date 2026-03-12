"""
Veritas Claim Gap Detector v1.0
Philosophy: "The headline promised a mountain. The text delivered a molehill."

Detects asymmetry between the STRONGEST CLAIM in a text (usually headline
or opening sentence) and the ACTUAL EVIDENCE provided in the body.

Classic cases:
  - TSN: "Prophecy about end of war" ← monk said "близько" (soon)
  - Tabloid: "Scientists PROVE X" ← one unnamed researcher speculated
  - Opinion dressed as news: "Experts warn Y will happen" ← one tweet

This is NOT about missing context (that's completeness_checker).
This is about the GAP between what the text promises and what it delivers.

Output:
  gap_score     0.0–1.0  (higher = bigger gap = more suspicious)
  claim_strength 0.0–1.0 (how strong the opening claim is)
  evidence_strength 0.0–1.0 (how well supported the body is)
  verdict       NO_GAP / MINOR_GAP / MODERATE_GAP / MAJOR_GAP
  trigger_phrase  what triggered the strong claim detection
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ClaimGapResult:
    gap_score:        float
    claim_strength:   float
    evidence_strength: float
    verdict:          str
    trigger_phrase:   Optional[str]
    explanation:      str
    is_flagged:       bool


class ClaimGapDetector:

    # ── STRONG CLAIM MARKERS ─────────────────────────────────────────
    # Words that elevate a statement to a STRONG CLAIM requiring evidence

    CLAIM_MARKERS_UK = [
        # Prophecy / prediction framed as fact
        (r'\b(пророцтво|пророцтва|пророкування|передбачення)\b', 0.9),
        (r'\b(прогноз|прогнозують|прогнозує)\b', 0.6),
        (r'\b(провіщає|провістив|провістила)\b', 0.85),

        # Certainty verbs used for uncertain things
        (r'\b(доведено|підтверджено|встановлено|з.ясовано)\b', 0.7),
        (r'\b(точно|напевно|безсумнівно|однозначно)\b', 0.65),
        (r'\b(ніхто не сумнівається|це факт)\b', 0.75),

        # Revelation framing
        (r'\b(розкрив|розкрила|розкрили|викрив|викрили)\b', 0.7),
        (r'\b(таємниця розкрита|правда про|справжня причина)\b', 0.8),

        # Future as certain
        (r'\b(закінчиться|переможе|відбудеться|стане|буде) .{0,30}(точно|напевно|скоро|незабаром|близько)\b', 0.75),
        (r'\b(дав прогноз|дала прогноз|озвучив прогноз)\b', 0.65),

        # War/crisis predictions
        (r'\b(закінчення\s+війни|кінець\s+війни|мир\s+(настане|прийде|буде))\b', 0.8),
        (r'\b(перемога\s+(буде|настане|близько))\b', 0.75),
    ]

    CLAIM_MARKERS_EN = [
        (r'\b(prophecy|prophesied|predicts|predicted)\b', 0.9),
        # Alarm/danger framing
        (r'\b(crossed.{0,20}red line|dangerous red line)\b', 0.80),
        (r'\b(unprecedented|historic|never before seen)\b', 0.65),
        (r'\b(warns?|warning).{0,30}(will|could|might).{0,30}(happen|occur|collapse|destroy)\b', 0.70),
        (r'\b(triggers?|sparks?|ignites?).{0,30}(crisis|war|conflict|chaos)\b', 0.65),
        # Conspiracy/mystery framing
        (r'\b(mystery|suspicious|cannot rule out|foul play)\b', 0.65),
        (r'\b(wiped.{0,20}(clean|out)|deleted.{0,20}(hours?|minutes?).{0,20}after)\b', 0.75),
        (r'\b(no coincidence|suspicious timing|convenient timing)\b', 0.70),
        (r'\b(cover.?up|coverup|silenced|suppressed)\b', 0.75),
        # Escalation framing  
        (r'\b(most (dangerous|serious|significant).{0,30}(ever|in history|in years))\b', 0.70),
        (r'\b(could (start|trigger|spark).{0,30}(war|crisis|collapse))\b', 0.65),
        (r'\b(point of no return|no going back|crossed the line)\b', 0.70),
        # Attribution laundering as strong claim
        (r'\b(some are (saying|claiming)|many believe|people are saying)\b', 0.60),
        (r'\b(sources (say|claim|suggest)|insiders (say|reveal))\b', 0.65),
        (r'\b(forecast|forecasts|foresees)\b', 0.6),
        (r'\b(proven|confirmed|established|revealed)\b', 0.7),
        (r'\b(definitely|certainly|undoubtedly|no doubt)\b', 0.65),
        (r'\b(exposes|uncovers|reveals the truth|real reason)\b', 0.75),
        (r'\b(will end|will win|will happen).{0,30}(soon|shortly|imminently)\b', 0.7),
        (r'\b(end of the war|war will end|peace is coming)\b', 0.8),
        (r'\b(bombshell|explosive|shocking)\b', 0.7),
        (r'\b(scientists (prove|confirm|discover))\b', 0.75),
    ]

    # ── EVIDENCE MARKERS ─────────────────────────────────────────────
    # Words that indicate ACTUAL EVIDENCE is being provided

    STRONG_EVIDENCE = [
        # English strong evidence
        r'\b(according to (the )?(study|research|data|report|survey))\b',
        r'\b(researchers? (at|from) [A-Z][a-z]+)\b',  # "researchers at MIT"
        r'\b(published in [A-Z])\b',  # "published in Nature"
        r'\b(\d+ (people|participants|countries|cases|samples))\b',
        r'\b(peer.reviewed|double.blind|meta.analysis|systematic review)\b',
        r'\b(official (data|statistics|report|statement))\b',
        r'\b(confirmed by (multiple|several|independent))\b',
        r'\b(data (show|shows|suggest|confirm))\b',
        r'\b(census|bureau|ministry|department) (data|report|figures)\b',
        # Verified sources
        r'\b(дослідження\s+(показало|виявило|підтвердило))\b',
        r'\b(за\s+даними\s+[А-ЯІЇЄҐ])',   # "за даними ООН/МОЗ/..."
        r'\b(статистика|офіційні\s+дані|верифіковано)\b',
        r'\b(опубліковано\s+в|журнал|peer-reviewed)\b',
        r'\b(n\s*=\s*\d+|\d+\s*(осіб|учасників|країн|випадків))\b',
        r'\b(according to \w+ study|research (shows|confirms|proves))\b',
        r'\b(official (data|statistics|report)|verified by)\b',
        # Multiple named sources
        r'\b(і\s+[А-ЯІЇЄҐ][а-яіїєґ]+,\s+і\s+[А-ЯІЇЄҐ])',  # "і Петров, і Сидоров"
        r'\b(підтвердили\s+кілька|кілька\s+джерел|множинні\s+джерела)\b',
    ]

    WEAK_EVIDENCE = [
        # English weak evidence
        r'\b(cannot rule out)\b',
        r'\b(suspicious(ly)?|coincidence|no coincidence)\b',
        r'\b(many on social media|social media (users|posts))\b',
        r'\b(pointed to|some pointed|others pointed)\b',
        r'\b(unconfirmed (reports?|sources?))\b',
        r'\b(anonymous (source|official|insider))\b',
        r'\b(it (seems|appears|looks like))\b',
        r'\b(conspiracy theorists?|claim without evidence)\b',
        # Vague/single source
        r'\b(хтось\s+сказав|дехто\s+каже|кажуть|говорять)\b',
        r'\b(можливо|мабуть|здається|схоже|начебто|нібито)\b',
        r'\b(близько|скоро|незабаром)\b(?!\s+\d)',  # "близько" not followed by number
        r'\b(деякі\s+вважають|є\s+думка|поширена\s+думка)\b',
        r'\b(один\s+(монах|священник|експерт|джерело))\b',
        r'\b(maybe|perhaps|apparently|seemingly|reportedly)\b',
        r'\b(some say|sources claim|unconfirmed)\b',
        # Emotional framing instead of data
        r'\b(чудо|дивовижно|неймовірно|сенсаційно)\b',
        r'\b(miracle|amazing|incredible|shocking)\b',
    ]

    def analyze(self, text: str) -> ClaimGapResult:
        if len(text.split()) < 15:
            return ClaimGapResult(
                gap_score=0.0, claim_strength=0.0, evidence_strength=0.5,
                verdict='NO_GAP', trigger_phrase=None,
                explanation='Текст занадто короткий для аналізу.',
                is_flagged=False
            )

        # Split into HEADER (first ~200 chars) and BODY (rest)
        # Header = where claims live; Body = where evidence should live
        header = text[:200]
        body   = text[200:]

        if len(body.split()) < 10:
            # Very short text — treat whole as body
            header = text[:80]
            body   = text

        # ── Measure claim strength in header ─────────────────────────
        claim_strength  = 0.0
        trigger_phrase  = None
        all_markers = self.CLAIM_MARKERS_UK + self.CLAIM_MARKERS_EN

        for pattern, weight in all_markers:
            m = re.search(pattern, header, re.IGNORECASE)
            if m:
                if weight > claim_strength:
                    claim_strength = weight
                    trigger_phrase = m.group(0)

        # Also scan first two sentences of body for claims
        body_sentences = re.split(r'[.!?]', body) if body else []
        first_sentence = ' '.join(body_sentences[:2])
        for pattern, weight in all_markers:
            m = re.search(pattern, first_sentence, re.IGNORECASE)
            if m:
                if weight > claim_strength:
                    claim_strength = min(weight * 0.85, 1.0)  # slightly discounted
                    trigger_phrase = m.group(0)

        # No strong claim found → no gap possible
        if claim_strength < 0.5:
            return ClaimGapResult(
                gap_score=0.0, claim_strength=claim_strength,
                evidence_strength=1.0, verdict='NO_GAP',
                trigger_phrase=None,
                explanation='Текст не містить сильних тверджень що вимагають доказів.',
                is_flagged=False
            )

        # ── Measure evidence strength in body ────────────────────────
        strong_hits = sum(1 for p in self.STRONG_EVIDENCE
                          if re.search(p, body, re.IGNORECASE))
        weak_hits   = sum(1 for p in self.WEAK_EVIDENCE
                          if re.search(p, body, re.IGNORECASE))

        # Evidence score: strong evidence increases it, weak decreases it
        if strong_hits >= 3:
            evidence_strength = 0.9
        elif strong_hits == 2:
            evidence_strength = 0.7
        elif strong_hits == 1:
            evidence_strength = 0.5 - (weak_hits * 0.1)
        else:
            # No strong evidence
            evidence_strength = max(0.05, 0.35 - (weak_hits * 0.08))

        evidence_strength = max(0.0, min(1.0, evidence_strength))

        # ── Calculate gap ─────────────────────────────────────────────
        gap_score = round(claim_strength - evidence_strength, 3)
        gap_score = max(0.0, min(1.0, gap_score))

        # ── Verdict ───────────────────────────────────────────────────
        if gap_score >= 0.65:
            verdict = 'MAJOR_GAP'
        elif gap_score >= 0.45:
            verdict = 'MODERATE_GAP'
        elif gap_score >= 0.25:
            verdict = 'MINOR_GAP'
        else:
            verdict = 'NO_GAP'

        is_flagged = gap_score >= 0.45

        # ── Explanation ───────────────────────────────────────────────
        if verdict == 'MAJOR_GAP':
            explanation = (
                f'Текст заявляє "{trigger_phrase}" — але тіло тексту '
                f'не містить достатніх доказів для такого твердження. '
                f'Це класична техніка: сильний заголовок + слабке підтвердження.'
            )
        elif verdict == 'MODERATE_GAP':
            explanation = (
                f'Твердження "{trigger_phrase}" підкріплено частково. '
                f'Доказова база слабша ніж вимагає заявлена сила висновку.'
            )
        elif verdict == 'MINOR_GAP':
            explanation = (
                f'Незначна невідповідність між силою твердження '
                f'та наведеними доказами.'
            )
        else:
            explanation = 'Сила твердження відповідає наведеним доказам.'

        return ClaimGapResult(
            gap_score=gap_score,
            claim_strength=round(claim_strength, 3),
            evidence_strength=round(evidence_strength, 3),
            verdict=verdict,
            trigger_phrase=trigger_phrase,
            explanation=explanation,
            is_flagged=is_flagged
        )


# ── Smoke tests ──────────────────────────────────────────────────────

if __name__ == '__main__':
    d = ClaimGapDetector()

    tests = [
        ('ТСН Афон',
         'Пророцтво монаха: старець Лука з Афону дав прогноз щодо закінчення війни в Україні. '
         'Ветеранів довго везуть розмитими афонськими дорогами. Монах Лука поспілкувався з паломниками. '
         '«Це велика несправедливість. Ми молимося, аби війна скоріше закінчилася. '
         'Я не знаю коли закінчиться, Бог знає, але це вже близько», — відповідає афонський монах. '
         'Лука не називає точної дати, але він чітко говорить — близько.'),

        ('IronCurtain WIRED',
         'This AI Agent Is Designed to Not Go Rogue. IronCurtain uses a unique method to secure AI agents. '
         'Instead of the agent directly interacting with systems, it runs in an isolated virtual machine. '
         'Niels Provos, a longtime security engineer, is launching the open source project today. '
         'Dino Dai Zovi, a well-known cybersecurity researcher, says the approach aligns with his intuition. '
         'The system maintains an audit log of all policy decisions over time.'),

        ('CNN Іран',
         'Trump crossed a very dangerous red line by killing Iran Supreme Leader Khamenei. '
         'Iran responded with an unprecedented wave of strikes across the Middle East. '
         'Strikes have continued throughout the weekend, killing civilians. '
         'The Iranian deputy foreign minister told CNN we have no option but to respond. '
         'If Trump didn\'t want to see Iran hitting back, he should not have started this war.'),

        ('Daily Mail НЛО',
         'Mystery as UFO vault with 3.8 million files wiped clean hours after Trump demands alien docs. '
         'The Black Vault had its server wiped. Greenewald said he cannot rule out foul play '
         'because of the suspicious timing. The deletion is unexplained. '
         'Many on social media pointed to the Epstein files also being redacted.'),
    ]

    print(f'{"Тест":<20} {"Verdict":<16} {"Claim":>6} {"Evid":>6} {"Gap":>6}  Trigger')
    print('─' * 80)
    for name, text in tests:
        r = d.analyze(text)
        trigger = (r.trigger_phrase or '')[:30]
        print(f'{name:<20} {r.verdict:<16} {r.claim_strength:>6.2f} {r.evidence_strength:>6.2f} {r.gap_score:>6.3f}  {trigger}')
