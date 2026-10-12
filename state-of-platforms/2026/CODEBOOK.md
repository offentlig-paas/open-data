# Codebook: State of Platforms 2026

File: `state-of-platforms-2026-aggregate.csv` (UTF-8, comma-separated, header row). Aggregate frequency tables, not individual responses. Wave 2, collected Q4 2025 – Q1 2026, 48 platform entries from 45 organizations (duplicates merged; three organizations reported two platforms).

## Columns

- `column`: position of the question in the original response file (column 1, organization, is not published). Map to question numbers via `instrument.md`.
- `question`: question text as shown in the form (Norwegian).
- `answer`: answer option. `(no answer)` means not shown or left blank. `other` means text that is not one of the listed options; the text itself is not published.
- `n`: number of responses giving this answer. Counts below 3 are shown as `<3`. If a question would then have only one hidden cell, or hidden cells totalling under 3, the next-smallest cells are also hidden and shown as `suppressed`, so no hidden count can be worked out from the totals.

The first data row (`responses`) gives the total number of responses.

Multi-select questions: each response counts once per option it selected, so counts within a question can add up to more than the number of responses.

## Why aggregates only

The consent text used in both waves said aggregated results would be published. It did not cover publication of respondent-level data, so only frequency tables are released. Organization names, pseudonyms, free text, timestamps, platform names and e-mail addresses are not included.

## Questions

- 2: Type
- 3: Type organisasjon
- 4: Ansatte
- 5: Budsjett (MNOK)
- 6: Hva er din primærrolle?
- 7: Har dere en applikasjonsplattform?
- 8: Hvorfor lager dere plattform?
- 9: Hvilke selvbetjente tjenester består plattformen deres av?
- 10: Ca. hvor mange applikasjonsteam benytter seg av plattformen deres i dag?
- 11: Topp tre programmeringsspråk for applikasjoner?
- 12: Hvordan allokeres ansatte og midler til plattformfunksjoner
- 13: Hvordan oppdager brukere interne plattformer og plattformfunksjonalitet?
- 14: Hvordan benytter brukere plattformfunksjonalitet?
- 15: Hvordan planlegges, prioriteres, utvikles og vedlikeholdes plattformer og deres funksjonalitet?
- 16: Hva er prosessen for å samle inn og lære av tilbakemeldinger?
- 17: Bruker dere Kubernetes?
- 18: Hvilke Kubernetes distribusjoner bruker dere?
- 19: Hvor mange år har dere kjørt Kubernetes i produksjon?
- 20: Hvor mange Kubernetes clustere har dere?
- 21: Hvor mange applikasjoner i produksjon har dere på Kubernetes?
- 22: Utvikler dere egne Kubernetes operators?
- 23: Kjører dere databaser i Kubernetes?
- 24: Bruker dere sky for plattformen deres?
- 25: Hva er deres primære sky for applikasjoner?
- 26: Brukere dere flere sky-leverandører?
- 27: Hvor mange år har dere kjørt applikasjoner i sky?
- 28: Benytter dere serverless funksjoner?
- 29: Hva bruker dere for overvåking av applikasjoner?
- 30: Hva bruker dere for pakking av applikasjoner?
- 31: Hva bruker dere for deploy av applikasjoner?
- 32: Hva bruker dere for nettverksikkerhet?
- 33: Hva bruker dere for applikasjonsikkerhet?
- 34: Hva bruker dere for infrastruktur-automatisering?
