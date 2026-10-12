# State of AI Coding Agents 2026 (wave 1)

Survey of AI coding tool adoption, governance and concerns among developers and technical leaders in the Norwegian public sector. Collected April–May 2026, 115 respondents from 57 organizations.

- `ai-agents-2026-anonymous.csv`: anonymized responses, one row per respondent, without organization
- `org-level-tables.csv`: organization-level results as aggregates
- `respondent-level-aggregates.csv`: counts for size bands and tool categories that are merged in the CSV
- `CODEBOOK.md`: columns and codes
- `instrument.md`: the survey instrument (Norwegian, with English translations)
- `scripts/`: analysis and figure scripts

## Reproduce the analysis

Python 3.8 or newer (tested 3.8–3.14), standard library only.

```sh
python3 scripts/analyze_wave1_v2.py            # prints the full report
python3 scripts/generate_svgs.py               # writes figures/*.svg
```

Both read `ai-agents-2026-anonymous.csv` by default. Pass another path as the first argument or set `AI_AGENTS_CSV`.

Expected headline numbers: personal use 92% (106/115), broad shadow adoption 62% (60/96), narrow shadow adoption 30% (29/96).

The public CSV has no organization column, so the script prints organization-level sections as "not available in public data"; those results are in `org-level-tables.csv`. Developer team size and rare tool categories are coarsened in the CSV, so the script prints the merged values; original counts are in `respondent-level-aggregates.csv`.

Regenerated figures differ slightly from the paper: Figure 2 has no open-source approved bar (fewer than 3 respondents, merged into `other`), and for the same reason Figure 3 shows 16 open-source shadow users instead of 15.

License: data and documentation CC BY 4.0; scripts MIT (see `scripts/LICENSE`).

## How to cite

> Flaatten, H. K., & Sandvik, A. O. (2026). *State of AI Coding Agents in the Norwegian Public Sector, wave 1 (2026)* [Data set]. Offentlig PAAS. https://github.com/offentlig-paas/open-data/tree/main/state-of-ai-agents/2026
