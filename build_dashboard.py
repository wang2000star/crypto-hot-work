#!/usr/bin/env python3
"""Build the self-contained browser dashboard from the collected CSV files."""
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

VENUES = ["ASIACRYPT", "CiC", "CRYPTO", "EUROCRYPT", "JoC", "PKC", "RWC", "TCC", "TCHES", "ToSC"]
JOURNALS = ["CiC", "JoC", "TCHES", "ToSC"]
CONFERENCES = ["ASIACRYPT", "CRYPTO", "EUROCRYPT", "PKC", "TCC"]
COLORS = ["#4f46e5", "#0891b2", "#e11d48", "#ca8a04", "#7c3aed", "#059669", "#ea580c", "#2563eb", "#be123c", "#0f766e"]


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    papers = read_csv("papers_classified.csv")
    ranked = read_csv("topics_ranked.csv")
    outlets = read_csv("iacr_publications.csv")
    years = sorted((key for key in (ranked[0].keys() if ranked else []) if re.fullmatch(r"20\d{2}", key)), key=int)
    total_field = next((key for key in (ranked[0].keys() if ranked else []) if key.startswith("total_")), "total")
    year_range = f"{years[0]}–{years[-1]}" if years else ""
    year_span = f"{len(years)}-year"
    topics = []
    for row in ranked:
        topics.append({
            "name": row["research_direction"],
            "counts": [int(row[y] or 0) for y in years],
            "total": int(row[total_field] or 0),
            "hotYears": [y for y in years if y in row["hot_years_gt_10"].split(", ")],
        })
    topics.sort(key=lambda x: (-x["total"], x["name"]))

    annual_total = Counter(p["year"] for p in papers)
    annual_tagged = Counter(p["year"] for p in papers if p.get("directions", "").strip())
    topic_venue = defaultdict(Counter)
    annual_outlet = defaultdict(Counter)
    outlet_topics = defaultdict(Counter)
    rwc_counts = Counter()
    for row in outlets:
        venue, year = row.get("venue", ""), row.get("year", "")
        if year not in years:
            continue
        if row.get("publication_type", "").startswith("accepted conference talk"):
            rwc_counts[year] += 1
            continue
        if venue in VENUES:
            annual_outlet[venue][year] += 1

    papers_by_topic = defaultdict(list)
    for p in papers:
        year = p.get("year", "")
        direction_names = [x.strip() for x in p.get("directions", "").split(";") if x.strip()]
        outlet_names = {x.strip() for x in p.get("venues", "").split(";") if x.strip()}
        for topic in direction_names:
            for venue in outlet_names:
                if venue in VENUES and venue != "RWC":
                    topic_venue[topic][venue] += 1
                    outlet_topics[venue][topic] += 1
            url = p.get("eprint_url") or p.get("venue_url") or ""
            papers_by_topic[topic].append({
                "title": p.get("title", ""),
                "year": year,
                "url": url,
                "authors": p.get("authors", ""),
                "venues": p.get("venues", ""),
            })

    data = {
        "years": years,
        "yearRange": year_range,
        "yearSpan": year_span,
        "totalField": total_field,
        "generated": date.today().isoformat(),
        "venues": VENUES,
        "journals": JOURNALS,
        "conferences": CONFERENCES,
        "colors": COLORS,
        "topics": topics,
        "paperCount": len(papers),
        "taggedCount": sum(annual_tagged.values()),
        "annualTotal": [annual_total[y] for y in years],
        "annualTagged": [annual_tagged[y] for y in years],
        "annualCoverage": [round(100 * annual_tagged[y] / annual_total[y], 1) if annual_total[y] else 0 for y in years],
        "outletCounts": {v: [annual_outlet[v][y] for y in years] for v in VENUES if v != "RWC"},
        "rwcTalks": [rwc_counts[y] for y in years],
        "topicVenue": {t: {v: topic_venue[t][v] for v in VENUES if v != "RWC"} for t in [x["name"] for x in topics]},
        "outletTopics": {v: dict(outlet_topics[v]) for v in VENUES if v != "RWC"},
        "papersByTopic": dict(papers_by_topic),
    }
    template = Path("dashboard_template.html").read_text(encoding="utf-8")
    # Prevent embedded data from terminating the JSON script element.
    encoded = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    template = template.replace("__DASHBOARD_DATA__", encoded)
    template = template.replace("__YEAR_RANGE__", year_range).replace("__YEAR_SPAN__", year_span)
    template = template.replace("__YEAR_TOTAL_LABEL__", f"{len(years)}-year total")
    template = template.replace("__YEAR_HEADERS__", "".join(f"<th>{y}{'*' if y == years[-1] else ''}</th>" for y in years))
    template = template.replace("__TOTAL_RECORDS__", f"{len(papers):,}")
    template = template.replace("__TAGGED_RECORDS__", f"{sum(annual_tagged.values()):,}")
    template = template.replace("__END_YEAR__", years[-1] if years else "")
    Path("index.html").write_text(template, encoding="utf-8")
    print(f"Built index.html: {len(papers):,} unique records, {len(topics)} directions, {len(outlets):,} venue/program records")


if __name__ == "__main__":
    main()
