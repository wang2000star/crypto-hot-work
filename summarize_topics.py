#!/usr/bin/env python3
"""Merge ePrint/IACR venue records and rank specific research directions.

Direction labels are transparent high-precision keyword rules, intended as a
reviewable first-pass taxonomy rather than a substitute for expert screening.
"""
import csv, re, unicodedata
import argparse
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

YEAR_START, YEAR_END = 2017, 2026
RULES = [
    ("BGV/BFV bootstrapping improvements", r"\b(bgv|bfv)\b.{0,70}\bbootstrapp|\bbootstrapp.{0,70}\b(bgv|bfv)\b"),
    ("CKKS bootstrapping improvements", r"\bckks\b.{0,90}\bbootstrapp|\bbootstrapp.{0,90}\bckks\b"),
    ("TFHE bootstrapping improvements", r"\btfhe\b.{0,90}\bbootstrapp|\bbootstrapp.{0,90}\btfhe\b"),
    ("FHE key switching and modulus switching", r"\b(homomorphic encryption|\bfhe\b|\bbgv\b|\bbfv\b|\bckks\b|\btfhe\b).{0,100}\b(key switch|modulus switch|rescal|relineariz)"),
    ("FHE implementation and hardware acceleration", r"\b(fhe|homomorphic encryption|ckks|bgv|bfv|tfhe)\b.{0,100}\b(hardware|gpu|fpga|accelerat|implement|risc-v|riscv)"),
    ("Lattice KEM attacks and security analysis", r"\b(lattice|ml-kem|kyber|saber|hqc|frodo|kem).{0,100}\b(attack|cryptanal|side.channel|fault|security analysis|key recovery)"),
    ("Dilithium/ML-DSA signature construction and optimization", r"\b(dilithium|ml-dsa)\b.{0,100}\b(signature|signing|implementation|optimization|efficient|masking)"),
    ("Falcon signature construction and implementation", r"\bfalcon\b.{0,100}\b(signature|signing|implementation|optimization|efficient|masking)"),
    ("Other lattice signature construction and efficiency", r"\blattice.based signature|\blattice signatures?\b"),
    ("Lattice reduction and PQC security estimation", r"\b(lwe|sieving|lattice reduction|bkz|svp|sieving|cryptographic estimation).{0,100}\b(quantum|cost|complexity|security|reduction|estimat)"),
    ("Zero-knowledge folding and recursive proof systems", r"\b(folding scheme|folding schemes|recursive proof|recursive snark|incrementally verifiable|ivc|accumulation scheme)"),
    ("zkSNARK lookup arguments and arithmetization", r"\b(lookup argument|lookup table|plonk|snark|zk.?snark).{0,100}\b(lookup|arithmetization|constraint system|sumcheck)"),
    ("Zero-knowledge proof aggregation and succinctness", r"\b(snark|zk.?proof|zero.knowledge proof|proof system).{0,100}\b(aggregate|aggregation|succinct|prover time|proof size)"),
    ("MPC preprocessing and communication efficiency", r"\b(multiparty computation|multi.party computation|\bmpc\b).{0,100}\b(preprocess|preprocessing|communication|round|offline phase|online phase)"),
    ("Malicious-secure MPC protocol construction", r"\b(multiparty computation|multi.party computation|\bmpc\b).{0,100}\b(malicious|dishonest majority|active security|abort)"),
    ("Private set intersection protocols", r"\b(private set intersection|\bpsi\b)\b"),
    ("Threshold and distributed signature protocols", r"\b(threshold signature|threshold signatures|distributed signing|threshold signing|multi.signature|multisignature)\b"),
    ("Anonymous credentials and blind signatures", r"\b(anonymous credential|anonymous credentials|blind signature|blind signatures|anonymous token)\b"),
    ("Differential and linear cryptanalysis of block ciphers", r"\b(differential|linear|integral|algebraic) cryptanal|\b(round|key recovery) attack.{0,60}\b(aes|des|cipher|sbox|arx)\b"),
    ("Power and electromagnetic attacks on post-quantum implementations", r"\b(ml-kem|ml-dsa|kyber|dilithium|falcon|hqc|post.quantum)\b.{0,100}\b(power analysis|electromagnetic|side.channel|leakage)\b|\b(power analysis|electromagnetic|side.channel|leakage)\b.{0,100}\b(ml-kem|ml-dsa|kyber|dilithium|falcon|hqc|post.quantum)\b"),
    ("Cache and timing attacks on cryptographic implementations", r"\b(cache|timing) (attack|attacks|leakage|side.channel)\b|\b(cache|timing) side.channel\b"),
    ("Masking and leakage-resistant implementation techniques", r"\b(masking|masked implementation|leakage.resilient)\b.{0,90}\b(side.channel|power|implementation|cryptographic)\b"),
    ("Fault injection against cryptographic implementations", r"\b(fault injection|fault attack|fault attacks|fault analysis)\b"),
    ("Post-quantum cryptography implementation and leakage", r"\b(post.quantum|ml-kem|ml-dsa|kyber|dilithium|falcon|hqc)\b.{0,100}\b(implementation|leakage|constant.time)"),
    ("Universal composability proofs for multiparty protocols", r"\b(mpc|multiparty computation|multi.party computation)\b.{0,100}\b(universally composable|universal composability|uc security|composability)\b"),
    ("Verifiable computation and SNARK-based applications", r"\b(verifiable computation|zk.?snark|snark).{0,100}\b(machine learning|blockchain|rollup|application|outsourc|delegat)"),
]

def norm_title(s):
    s = unicodedata.normalize("NFKD", s or "").casefold()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()

def read_csv(path):
    p = Path(path)
    if not p.exists(): return []
    with p.open(encoding="utf-8-sig", newline="") as f: return list(csv.DictReader(f))

def eprint_year(row):
    m = re.search(r"eprint\.iacr\.org/(\d{4})/", row.get("PDF链接", ""))
    return m.group(1) if m else ""

def write_summary(years, papers, venues, ranked, total_field):
    tagged_count = sum(bool(p["directions"]) for p in papers)
    lines = [
        "# IACR papers: collection and topic ranking", "",
        "## Scope", "",
        f"Period: {years[0]}–{years[-1]} inclusive (collection snapshot {date.today().isoformat()}; {years[-1]} is year-to-date). "
        "The ten IACR venues are ASIACRYPT, CiC, CRYPTO, EUROCRYPT, JoC, PKC, RWC, TCC, TCHES, and ToSC. "
        "CHES is normalized to TCHES; FSE is normalized to ToSC. The ePrint Archive is included as the additional source.", "",
        "## Topic method", "",
        "Titles, abstracts, and keywords are merged by normalized title to reduce obvious ePrint/proceedings duplicates. "
        "Direction labels use explicit keyword rules in `summarize_topics.py`; a paper can receive multiple labels. "
        f"`topics_ranked.csv` sorts directions by the {len(years)}-year total and reports each year. A direction is hot in a year "
        "only when its count is strictly greater than 10.", "",
        "These are machine-assisted candidate counts, not a manually validated final taxonomy. Some venue records lack abstracts, "
        "and false positives or missed matches are possible; expert review is needed before treating rankings as definitive. "
        f"{years[-1]} is year-to-date.", "",
        "## Collection coverage", "",
        f"ePrint input records: {sum(p.get('venues') == 'ePrint' or 'ePrint' in p.get('venues', '').split('; ') for p in papers):,}. "
        f"IACR venue and RWC program source records: {len(venues):,}. Title-deduplicated paper records: {len(papers):,}. "
        f"At least one direction label: {tagged_count:,} ({100 * tagged_count / max(1, len(papers)):.1f}%).", "",
        "| Venue / program | " + " | ".join(map(str, years)) + " |", "|---|" + "|".join(["---:"] * len(years)) + "|",
    ]
    counts = Counter((r.get("venue", ""), str(r.get("year", ""))) for r in venues
                     if not r.get("publication_type", "").startswith("accepted conference talk"))
    for venue in ["ASIACRYPT", "CiC", "CRYPTO", "EUROCRYPT", "JoC", "PKC", "RWC", "TCC", "TCHES", "ToSC"]:
        if venue == "RWC":
            yearly = [sum(1 for r in venues if r.get("venue") == "RWC" and str(r.get("year")) == str(y)
                          and r.get("publication_type", "").startswith("accepted conference talk")) for y in years]
        else:
            yearly = [counts[(venue, str(y))] for y in years]
        lines.append("| " + venue + " | " + " | ".join(map(str, yearly)) + " |")
    lines += ["", "RWC entries are accepted talk titles, not proceedings papers; they are kept in `rwc_program.csv` and excluded "
              "from topic counts unless independently present as papers. The collector found 43 RWC talks for 2025; other RWC years "
              "had no accessible accepted-talk list in this snapshot. Other source indexes may omit older, future, or not-yet-indexed records.", "",
              "## Ranked research directions", "",
              "| Rank | Research direction | " + " | ".join(map(str, years)) + f" | {len(years)}-year total | Hot years (>10) |",
              "|---:|---|" + "|".join(["---:"] * (len(years) + 1)) + "|---|---|"]
    for i, row in enumerate(ranked, 1):
        annual = " | ".join(str(row[str(y)]) for y in years)
        lines.append(f"| {i} | {row['research_direction']} | {annual} | {row[total_field]} | {row['hot_years_gt_10'] or '—'} |")
    lines += ["", f"Counts are computed from the {len(years)}-year, title-deduplicated corpus. Papers can contribute to more than one direction."]
    Path("topic_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def main():
    ap = argparse.ArgumentParser(description="Classify IACR papers over a publication-year range")
    ap.add_argument("--input", default="papers_10y.csv")
    ap.add_argument("--start-year", type=int, default=YEAR_START)
    ap.add_argument("--end-year", type=int, default=YEAR_END)
    args = ap.parse_args()
    years = range(args.start_year, args.end_year + 1)
    total_field = f"total_{args.start_year}_{args.end_year}"
    eprints = read_csv(args.input)
    venue = read_csv("iacr_publications.csv")
    papers, rwc_talks = {}, []
    for r in eprints:
        title = r.get("标题", "").strip()
        y = eprint_year(r)
        if not title or y not in map(str, years): continue
        k = norm_title(title)
        papers[k] = {"title": title, "year": y, "authors": r.get("作者", ""), "abstract": r.get("摘要", ""),
                     "keywords": r.get("关键词", ""), "venues": "ePrint", "eprint_url": r.get("PDF链接", ""), "venue_url": ""}
    for r in venue:
        title = r.get("title", "").strip(); y = r.get("year", "")
        if not title or y not in map(str, years): continue
        k = norm_title(title)
        if "talk" in (r.get("publication_type", "").lower()) and k not in papers:
            rwc_talks.append(r)
            continue
        if k in papers:
            old = papers[k]
            old["venues"] = old["venues"] + "; " + r.get("venue", "")
            old["venue_url"] = r.get("url", "")
            if r.get("abstract") and not old["abstract"]: old["abstract"] = r["abstract"]
        else:
            papers[k] = {"title": title, "year": y, "authors": r.get("authors", ""), "abstract": r.get("abstract", ""),
                         "keywords": "", "venues": r.get("venue", ""), "eprint_url": "", "venue_url": r.get("url", "")}
    counts = Counter(); tagged = []
    for p in papers.values():
        text = " ".join([p["title"], p["abstract"], p["keywords"]]).casefold()
        topics = [name for name, pattern in RULES if re.search(pattern, text, re.I)]
        p["directions"] = "; ".join(topics)
        p["hot_topic_directions"] = ""
        for t in topics: counts[(t, p["year"])] += 1
        tagged.append(p)
    hot = {t for (t, y), n in counts.items() if n > 10}
    ranked = []
    for name, _ in RULES:
        row = {"research_direction": name}
        for y in years: row[str(y)] = counts[(name, str(y))]
        row[total_field] = sum(row[str(y)] for y in years)
        row["hot_years_gt_10"] = ", ".join(str(y) for y in years if row[str(y)] > 10)
        row["hot_topic"] = "yes" if row["hot_years_gt_10"] else "no"
        ranked.append(row)
    ranked.sort(key=lambda r: (-r[total_field], r["research_direction"]))
    for p in tagged:
        p["hot_topic_directions"] = "; ".join(t for t in p["directions"].split("; ") if t in hot)
    with open("papers_classified.csv", "w", newline="", encoding="utf-8-sig") as f:
        cols = ["title", "year", "authors", "venues", "directions", "hot_topic_directions", "abstract", "keywords", "eprint_url", "venue_url"]
        w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n"); w.writeheader(); w.writerows(sorted(tagged,key=lambda p:(p["year"],p["title"].casefold())))
    with open("rwc_program.csv", "w", newline="", encoding="utf-8-sig") as f:
        cols = ["title", "authors", "year", "url", "source"]
        w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n"); w.writeheader()
        for r in sorted(rwc_talks, key=lambda x:(x.get("year", ""), x.get("title", "").casefold())):
            w.writerow({k:r.get(k, "") for k in cols})
    with open("topics_ranked.csv", "w", newline="", encoding="utf-8-sig") as f:
        cols = ["rank", "research_direction", *map(str, years), total_field, "hot_years_gt_10", "hot_topic"]
        w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n"); w.writeheader()
        for i,r in enumerate(ranked,1): w.writerow({"rank":i,**r})
    write_summary(years, tagged, venue, ranked, total_field)
    print(f"Period: {args.start_year}–{args.end_year}")
    print(f"ePrint records: {len(eprints)}; IACR venue records: {len(venue)}; unique title records: {len(tagged)}")
    print(f"Tagged records: {sum(bool(p['directions']) for p in tagged)}; unmatched records remain blank")
    print("Top research directions:")
    for r in ranked[:15]: print(f"{r[total_field]:>4} {r['research_direction']} | hot years: {r['hot_years_gt_10'] or '-'}")

if __name__ == "__main__": main()
