# CryptoScope: IACR research trends

A data collection and analysis project for papers in the IACR Cryptology ePrint Archive and the ten IACR conference/journal venues in scope: ASIACRYPT, CiC, CRYPTO, EUROCRYPT, JoC, PKC, RWC, TCC, TCHES, and ToSC. CHES records map to TCHES; FSE records map to ToSC.

## View the report

Open [`index.html`](index.html) in a browser for an interactive, self-contained dashboard with annual paper counts, direction trends, hot-topic flags, venue breakdowns, and representative papers. It needs no JavaScript libraries or web server. The dashboard is regenerated from the CSV data and can be viewed directly from GitHub Pages when that workflow is enabled for the repository.

## Rebuild the analysis

```bash
python -m pip install -r requirements.txt
python collect_iacr_publications.py
python summarize_topics.py
python build_dashboard.py
```

The collector reads the IACR archive and journal sources, Springer/Crossref proceedings metadata, and the RWC program. To refresh the ePrint corpus, run the existing fetch/merge steps documented in `run_pull.sh`, `fetch_oai_bulk.py`, and `merge_papers.py`; then rerun the analysis commands above.

## Outputs

- `iacr_publications.csv`: collected venue and RWC program records, with source URLs and record type.
- `papers_5y.csv`: ePrint input corpus for 2022–2026 year-to-date.
- `papers_classified.csv`: title-deduplicated records with zero or more research-direction labels.
- `topics_ranked.csv`: yearly direction counts, five-year ranking, and strict `>10` hot-topic years.
- `topic_summary.md`: scope, coverage, ranked summary, and limitations.
- `index.html`: browser-ready report generated from the CSV outputs. Each selected research direction includes an expandable, searchable list of all assigned papers and a CSV download.

The classified corpus is checked in so the static dashboard and report can be rebuilt without rerunning the web collectors. It contains 11,438 title-deduplicated records, of which 2,936 receive at least one direction label; unclassified records do not appear in any direction list.
- `rwc_program.csv`: accepted RWC talks kept apart from proceedings-paper counts.

## Interpreting topic counts

Research directions are assigned using explicit keyword rules in `summarize_topics.py`. The rules are intentionally visible and editable, and one paper can match more than one direction. Counts are machine-assisted candidates; inspect the assigned records before using them as definitive field measurements. A topic is hot in a year only when its count is **greater than 10**. 2026 is a partial year. RWC lists talks rather than proceedings papers, and its talks are excluded from topic counts unless the same title occurs independently as a paper.

The source coverage and known gaps are recorded in `topic_summary.md`. In particular, zero counts can mean that a volume is future, unavailable, or not indexed at collection time.
