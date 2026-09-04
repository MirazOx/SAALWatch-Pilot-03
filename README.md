# SAALWatch Pilot 03 — News-headline affect snapshot

**An exploratory pilot, not an audit — and an honest null result.** It tests
whether international news headlines lean on high-arousal language, using a simple
lexical (bag-of-words) score. In this snapshot, the hypothesis was **not
supported**.

## Question
Drawing on Oxford Internet Institute computational-propaganda research and Jose
van Dijck's *The Platform Society*: do newsrooms optimise headlines for affective
intensity (anger, fear, outrage) to compete for algorithmic visibility?

## Data & method
- **Sample:** 97 headlines from three outlets' live RSS feeds (BBC Asia, Al
  Jazeera, NYT World), one snapshot.
- **Score:** an Affective Intensity Score (AIS) = share of a headline's tokens
  that appear in a curated 30-word high-arousal lexicon. A headline is counted
  "high-arousal" only above a 15%-of-tokens threshold.

## Result
Across all three outlets, **0.0% of headlines crossed the high-arousal
threshold**, and average AIS was very low (BBC 1.4%, NYT 0.9%, Al Jazeera 0.3%).
The small gaps between outlets are noise at this scale, not a ranking. **On this
sample, these outlets show no sign of optimising headlines for affective intensity.**

## Why the null is not proof of "calm" newsrooms
The measure is deliberately crude and its limits partly produce the result:
- **Bag-of-words** has no semantics — it can't tell a legitimate state "crisis"
  from a sensational "chaos", and it misses framing entirely.
- **The lexicon is arbitrary and English-centric.** It contains `deadly` but not
  `death`, so "sentenced to **death**" scores 0. Applying this to South Asian
  media would need a Bengali corpus and a semantic model.
- **The 15% threshold** is near-unreachable for normal-length headlines, so "0%
  high-arousal" reflects the method as much as the text.

This pilot demonstrates the data pipeline; it does not yet measure affect validly.

## Reproduce
```bash
python3 nlp_audit.py        # fetches live RSS, scores, writes the CSV, prints metrics
```
No third-party dependencies (Python standard library only). Because it reads live
feeds, rerunning returns current headlines, not the 97 captured here;
`nlp_affective_polarization_dataset.csv` is the archived snapshot. The script does
not generate `index.html` (that write-up is hand-maintained).

## Files
- `nlp_affective_polarization_dataset.csv` — scored headlines
- `nlp_audit.py` — fetch + score + metrics (dependency-free)
- `index.html` — the write-up (hand-maintained)
- `LICENSE` — MIT (code)

Code is released under the MIT License. Headlines are third-party news content
(BBC / Al Jazeera / NYT) included for research inspection, not relicensed.

Part of the South Asia Algorithm Watch (SAALWatch) initiative.
