# IACR papers: collection and topic ranking

## Scope

Period: 2017–2026 inclusive (collection snapshot 2026-09-27; 2026 is year-to-date). The ten IACR venues are ASIACRYPT, CiC, CRYPTO, EUROCRYPT, JoC, PKC, RWC, TCC, TCHES, and ToSC. CHES is normalized to TCHES; FSE is normalized to ToSC. The ePrint Archive is included as the additional source.

## Topic method

Titles, abstracts, and keywords are merged by normalized title to reduce obvious ePrint/proceedings duplicates. Direction labels use explicit keyword rules in `summarize_topics.py`; a paper can receive multiple labels. `topics_ranked.csv` sorts directions by the 10-year total and reports each year. A direction is hot in a year only when its count is strictly greater than 10.

These are machine-assisted candidate counts, not a manually validated final taxonomy. Some venue records lack abstracts, and false positives or missed matches are possible; expert review is needed before treating rankings as definitive. 2026 is year-to-date.

## Collection coverage

ePrint input records: 17,557. IACR venue and RWC program source records: 5,943. Title-deduplicated paper records: 19,082. At least one direction label: 4,199 (22.0%).

| Venue / program | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ASIACRYPT | 67 | 65 | 70 | 84 | 96 | 97 | 105 | 127 | 143 | 0 |
| CiC | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 103 | 142 | 113 |
| CRYPTO | 72 | 78 | 81 | 85 | 102 | 96 | 125 | 165 | 156 | 189 |
| EUROCRYPT | 67 | 67 | 73 | 83 | 78 | 85 | 110 | 117 | 123 | 142 |
| JoC | 33 | 32 | 36 | 46 | 45 | 28 | 41 | 39 | 36 | 30 |
| PKC | 36 | 49 | 42 | 42 | 53 | 39 | 50 | 59 | 60 | 65 |
| RWC | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 43 | 0 |
| TCC | 0 | 50 | 41 | 65 | 65 | 60 | 68 | 68 | 70 | 0 |
| TCHES | 33 | 48 | 42 | 60 | 80 | 83 | 78 | 101 | 111 | 149 |
| ToSC | 58 | 39 | 46 | 54 | 41 | 48 | 44 | 44 | 58 | 29 |

RWC entries are accepted talk titles, not proceedings papers; they are kept in `rwc_program.csv` and excluded from topic counts unless independently present as papers. The collector found 43 RWC talks for 2025; other RWC years had no accessible accepted-talk list in this snapshot. Other source indexes may omit older, future, or not-yet-indexed records.

## Ranked research directions

| Rank | Research direction | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | 10-year total | Hot years (>10) |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | Lattice KEM attacks and security analysis | 17 | 23 | 22 | 24 | 45 | 55 | 62 | 63 | 72 | 66 | 449 | 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 |
| 2 | Lattice reduction and PQC security estimation | 22 | 36 | 27 | 40 | 22 | 36 | 49 | 54 | 71 | 72 | 429 | 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 |
| 3 | Differential and linear cryptanalysis of block ciphers | 28 | 25 | 29 | 31 | 37 | 42 | 45 | 49 | 55 | 63 | 404 | 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 |
| 4 | Post-quantum cryptography implementation and leakage | 5 | 6 | 22 | 13 | 31 | 37 | 41 | 50 | 75 | 59 | 339 | 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 |
| 5 | Fault injection against cryptographic implementations | 25 | 25 | 31 | 36 | 25 | 34 | 43 | 40 | 42 | 37 | 338 | 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 |
| 6 | Anonymous credentials and blind signatures | 12 | 12 | 18 | 16 | 15 | 29 | 42 | 38 | 68 | 65 | 315 | 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 |
| 7 | Threshold and distributed signature protocols | 4 | 8 | 14 | 24 | 21 | 30 | 40 | 47 | 58 | 69 | 315 | 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 |
| 8 | MPC preprocessing and communication efficiency | 21 | 21 | 22 | 31 | 31 | 31 | 29 | 33 | 50 | 43 | 312 | 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 |
| 9 | Power and electromagnetic attacks on post-quantum implementations | 4 | 4 | 7 | 10 | 17 | 42 | 36 | 39 | 58 | 54 | 271 | 2021, 2022, 2023, 2024, 2025, 2026 |
| 10 | Masking and leakage-resistant implementation techniques | 22 | 17 | 11 | 16 | 30 | 38 | 32 | 25 | 27 | 33 | 251 | 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 |
| 11 | Private set intersection protocols | 9 | 9 | 10 | 18 | 22 | 25 | 27 | 47 | 42 | 35 | 244 | 2020, 2021, 2022, 2023, 2024, 2025, 2026 |
| 12 | FHE implementation and hardware acceleration | 8 | 10 | 9 | 11 | 22 | 19 | 36 | 34 | 29 | 26 | 204 | 2020, 2021, 2022, 2023, 2024, 2025, 2026 |
| 13 | Zero-knowledge proof aggregation and succinctness | 6 | 2 | 11 | 12 | 15 | 20 | 16 | 43 | 33 | 35 | 193 | 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 |
| 14 | Malicious-secure MPC protocol construction | 11 | 16 | 14 | 17 | 13 | 20 | 21 | 19 | 25 | 17 | 173 | 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026 |
| 15 | Dilithium/ML-DSA signature construction and optimization | 2 | 5 | 5 | 5 | 8 | 20 | 22 | 23 | 37 | 40 | 167 | 2022, 2023, 2024, 2025, 2026 |
| 16 | Zero-knowledge folding and recursive proof systems | 0 | 1 | 4 | 6 | 4 | 9 | 17 | 39 | 33 | 28 | 141 | 2023, 2024, 2025, 2026 |
| 17 | Other lattice signature construction and efficiency | 11 | 9 | 10 | 5 | 6 | 14 | 18 | 15 | 24 | 20 | 132 | 2017, 2022, 2023, 2024, 2025, 2026 |
| 18 | Cache and timing attacks on cryptographic implementations | 10 | 12 | 21 | 9 | 15 | 12 | 13 | 13 | 12 | 14 | 131 | 2018, 2019, 2021, 2022, 2023, 2024, 2025, 2026 |
| 19 | Verifiable computation and SNARK-based applications | 2 | 1 | 6 | 11 | 5 | 6 | 11 | 26 | 27 | 10 | 105 | 2020, 2023, 2024, 2025 |
| 20 | Falcon signature construction and implementation | 0 | 0 | 6 | 0 | 5 | 12 | 15 | 15 | 24 | 27 | 104 | 2022, 2023, 2024, 2025, 2026 |
| 21 | zkSNARK lookup arguments and arithmetization | 1 | 0 | 0 | 2 | 3 | 14 | 20 | 18 | 20 | 24 | 102 | 2022, 2023, 2024, 2025, 2026 |
| 22 | TFHE bootstrapping improvements | 4 | 0 | 0 | 1 | 5 | 12 | 13 | 16 | 33 | 13 | 97 | 2022, 2023, 2024, 2025, 2026 |
| 23 | CKKS bootstrapping improvements | 0 | 0 | 1 | 4 | 5 | 4 | 4 | 10 | 17 | 24 | 69 | 2025, 2026 |
| 24 | BGV/BFV bootstrapping improvements | 0 | 1 | 2 | 1 | 2 | 4 | 5 | 14 | 10 | 6 | 45 | 2024 |
| 25 | FHE key switching and modulus switching | 0 | 1 | 1 | 0 | 2 | 2 | 5 | 4 | 6 | 6 | 27 | — |
| 26 | Universal composability proofs for multiparty protocols | 2 | 0 | 0 | 1 | 1 | 2 | 0 | 1 | 6 | 3 | 16 | — |

Counts are computed from the 10-year, title-deduplicated corpus. Papers can contribute to more than one direction.
