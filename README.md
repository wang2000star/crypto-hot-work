# CryptoScope: IACR research trends

A data collection and analysis project for papers in the IACR Cryptology ePrint Archive and the ten IACR conference/journal venues in scope: ASIACRYPT, CiC, CRYPTO, EUROCRYPT, JoC, PKC, RWC, TCC, TCHES, and ToSC. CHES records map to TCHES; FSE records map to ToSC.

## View the report

Open [`index.html`](index.html) in a browser for an interactive, self-contained dashboard with annual paper counts, direction trends, hot-topic flags, venue breakdowns, and representative papers. It needs no JavaScript libraries or web server. The dashboard is regenerated from the CSV data and can be viewed directly from GitHub Pages when that workflow is enabled for the repository.

## Rebuild the analysis

```bash
python summarize_topics.py --input papers_10y.csv --start-year 2017 --end-year 2026
python build_dashboard.py
```

`paper-pull` owns paper discovery and metadata collection. It exports `papers_10y.csv` and `iacr_publications.csv`; this project consumes those files for classification, ranking, and the HTML report. The ten-year publication window is 2017–2026 inclusive, with 2026 year-to-date. Keep collection credentials, checkpoints, and fetch logic in `paper-pull`.

## Outputs

- `iacr_publications.csv`: collected venue and RWC program records, with source URLs and record type.
- `papers_10y.csv`: fetched ePrint input corpus for 2017–2026 year-to-date.
- `papers_classified.csv`: title-deduplicated decade records with zero or more research-direction labels.
- `topics_ranked.csv`: yearly direction counts, ten-year ranking, and strict `>10` hot-topic years.
- `topic_summary.md`: scope, coverage, ranked summary, and limitations.
- `index.html`: browser-ready report generated from the CSV outputs. Each selected research direction includes an expandable, searchable list of all assigned papers and a CSV download.

The classified corpus and fetched input snapshots are checked in so the static dashboard and report can be rebuilt without rerunning the collectors. Unclassified records remain available in the dataset but do not appear in any direction list.
- `rwc_program.csv`: accepted RWC talks kept apart from proceedings-paper counts.

## Interpreting topic counts

Research directions are assigned using explicit keyword rules in `summarize_topics.py`. The rules are intentionally visible and editable, and one paper can match more than one direction. Counts are machine-assisted candidates; inspect the assigned records before using them as definitive field measurements. A topic is hot in a year only when its count is **greater than 10**. 2026 is a partial year. RWC lists talks rather than proceedings papers, and its talks are excluded from topic counts unless the same title occurs independently as a paper.

The source coverage and known gaps are recorded in `topic_summary.md`. In particular, zero counts can mean that a volume is future, unavailable, or not indexed at collection time.
