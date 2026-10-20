# State of Platforms 2024

Survey of application platforms, Kubernetes and cloud use in Norwegian public sector organizations (Wave 1, collected Q4 2023, 35 organizations).

- `state-of-platforms-2024-aggregate.csv`: frequency table per question (aggregates only, counts below 3 suppressed)
- `CODEBOOK.md`: file format and why only aggregates are published
- `instrument.md`: the survey instrument (Norwegian, with English notes)

The table is produced by `../scripts/aggregate.py` from the non-public response file. Columns 22 and 23 (own Kubernetes operators, databases in Kubernetes) were not asked in 2024; all responses are `(no answer)`. Questions and answers are in Norwegian. Results are published at <https://nye.offentlig-paas.no>.

## How to cite

> Flaatten, H. K. (2024). *State of Platforms in the Norwegian Public Sector, 2024* [Data set]. Offentlig PAAS. https://github.com/offentlig-paas/open-data/tree/main/state-of-platforms/2024

License: data and documentation CC BY 4.0 (`LICENSE` in the repository root); script MIT (`../scripts/LICENSE`).

## Changes

- 2026-10-20 (v1.1): secondary suppression. Cells that could be recovered from question totals are now hidden as `suppressed`.
