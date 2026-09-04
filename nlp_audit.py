import urllib.request
import xml.etree.ElementTree as ET
import csv
import re
from datetime import datetime
import ssl

# Bypass SSL for local fetching
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# SAALWatch Pilot 03: The Platformization of News & Affective Polarization
# Methodology: Natural Language Processing (NLP) of News Headlines
# Theoretical Framework: Jose van Dijck's "Platform Society" & Algorithmic News Logic

FEEDS = {
    "BBC Asia": "http://feeds.bbci.co.uk/news/world/asia/rss.xml",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "NYT World": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
}

# A localized lexical dictionary of "Affective / High-Arousal" words 
# typically optimized for algorithmic engagement (click-through rates).
AFFECTIVE_LEXICON = {
    'clash', 'crisis', 'attack', 'dead', 'deadly', 'violence', 'protest', 'outrage', 
    'fury', 'slams', 'fears', 'threat', 'panic', 'chaos', 'corruption', 'scandal',
    'murder', 'critical', 'intense', 'conspiracy', 'regime', 'crackdown', 'warns',
    'explosive', 'brutal', 'shocking', 'massive', 'escalates', 'bloodshed', 'riots'
}

all_headlines = []

print("[*] Initiating NLP Headline Extraction Pipeline...")

for outlet, url in FEEDS.items():
    try:
        print(f"  -> Fetching RSS feed for {outlet}...")
        req = urllib.request.Request(url, headers={'User-Agent': 'SAALWatch-Academic/1.0'})
        response = urllib.request.urlopen(req, context=ctx).read()
        
        root = ET.fromstring(response)
        
        # Parse standard RSS 2.0 structure
        for item in root.findall('.//item'):
            title = item.find('title').text if item.find('title') is not None else ""
            date = item.find('pubDate').text if item.find('pubDate') is not None else datetime.now().isoformat()
            
            # NLP Pre-processing
            clean_title = re.sub(r'[^\w\s]', '', title.lower())
            tokens = clean_title.split()
            
            # Affective Intensity Scoring (AIS)
            affective_hits = [word for word in tokens if word in AFFECTIVE_LEXICON]
            ais_score = (len(affective_hits) / len(tokens) * 100) if tokens else 0
            
            all_headlines.append({
                'outlet': outlet,
                'date': date,
                'title': title,
                'word_count': len(tokens),
                'affective_hits': len(affective_hits),
                'ais_score': ais_score,
                'hit_words': ", ".join(affective_hits)
            })
    except Exception as e:
        print(f"[!] Error processing {outlet}: {e}")

if not all_headlines:
    print("[!] No data extracted. Exiting.")
    exit(1)

# Statistical Aggregation
outlet_stats = {}
for h in all_headlines:
    out = h['outlet']
    if out not in outlet_stats:
        outlet_stats[out] = {'total_articles': 0, 'total_ais': 0, 'highly_affective': 0}
    
    outlet_stats[out]['total_articles'] += 1
    outlet_stats[out]['total_ais'] += h['ais_score']
    if h['ais_score'] > 15.0: # Arbitrary threshold for highly sensational
        outlet_stats[out]['highly_affective'] += 1

for out in outlet_stats:
    outlet_stats[out]['avg_ais'] = outlet_stats[out]['total_ais'] / outlet_stats[out]['total_articles']
    outlet_stats[out]['affective_ratio'] = (outlet_stats[out]['highly_affective'] / outlet_stats[out]['total_articles']) * 100

# Save Dataset
csv_filename = "nlp_affective_polarization_dataset.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['outlet', 'date', 'title', 'word_count', 'affective_hits', 'ais_score', 'hit_words'])
    writer.writeheader()
    writer.writerows(all_headlines)

print(f"[+] Processed {len(all_headlines)} headlines. Dataset saved to {csv_filename}")

# --- Report metrics to stdout ----------------------------------------------
# NOTE: this script intentionally does NOT write index.html. The public
# dashboard (index.html) is maintained by hand; regenerating it here would
# overwrite that curated page, which reports this pilot's result honestly:
# in the captured snapshot, ~0% of headlines crossed the high-arousal
# threshold -- i.e. the hypothesis was not supported. Treat the figures below
# as an exploratory, English-lexicon, bag-of-words probe, not an audit.
print("[=] Average affective intensity by outlet:")
for outlet, stats in outlet_stats.items():
    print(f"      {outlet}: avg AIS {stats['avg_ais']:.1f}% | "
          f"{stats['affective_ratio']:.1f}% above high-arousal threshold "
          f"({stats['total_articles']} headlines)")

top = sorted(all_headlines, key=lambda x: x['ais_score'], reverse=True)[:5]
print("[=] Highest-scoring headlines (flagged on ordinary hard-news words):")
for h in top:
    print(f"      {h['ais_score']:.1f}%  [{h['outlet']}]  {h['title']}  "
          f"(hits: {h['hit_words'] or 'none'})")
