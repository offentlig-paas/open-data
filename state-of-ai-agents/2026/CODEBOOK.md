# Codebook: State of AI Coding Agents in the Norwegian Public Sector, Wave 1 (2026)

File: `ai-agents-2026-anonymous.csv` (UTF-8, comma-separated, header row). 115 rows, one per respondent, 40 columns. Collected April–May 2026. This is version 1.1 (see [Changes in v1.1](#changes-in-v11)). `respondent-level-aggregates.csv` is version 1.2.

## Conventions

- Multi-select answers are not published as combinations. They are replaced by derived columns (0/1 flags and counts), see [Derived columns](#derived-columns-v11). The column sections below for Q6, Q8b, Q9, Q10 and Q20 describe the question and its overall code counts only.
- `suppressed`: the value is withheld so that every combination of the quasi-identifiers has at least 3 respondents, or because a small group would otherwise reveal a sensitive answer. See [Removed or changed for privacy](#removed-or-changed-for-privacy).
- Section numbers below give the column order of version 1.0. In v1.1 the single-choice columns keep their order and the derived columns follow after Q23.
- Empty cell: question not shown (respondents who answered `no` to personal use skip the personal-usage questions) or left blank.
- `other`: the respondent chose "Annet" (other). The free text is not released. For the two tool questions, free-text answers are replaced by a tool category instead (`open-source` or an existing tool code); rare categories are merged into `other`, see columns 5 and 9.
- Question numbers follow the Google Form used in the paper. The survey instrument (Norwegian, with English translations) uses its own design numbering; both are given below.
- Codes are listed with their counts. The Norwegian response options from the instrument are given for reference, in instrument order; the codes are short English labels for these options.

## Changes in v1.1

Version 1.0 published multi-select answers as raw combinations. Combined with role and size, the set of approved tools (Q6) could single out an organization: 26 of 34 Q6 combinations were unique, and role, size and Q6 together made 40 of 115 rows unique. Version 1.1:

- Removes the raw Q6, Q8b, Q9, Q10 and Q20 columns.
- Adds per-option flags for Q6, Q8b and Q20 (only options chosen by at least 10 respondents; the rest are folded into `…_other`), top-coded counts (`q6_n_approved`, `q8b_n_used`, `q9_n_modes`, `q10_n_connected`) and `shadow_use`.
- Merges Q5 into `formal` and `informal`, and folds approved tools other than Copilot and Claude Code into `q6_other`.
- Guarantees k ≥ 3 on the quasi-identifier set role + developer team size + Q5 + `q6_copilot` + `q6_claude-code` + `q6_other` + `q6_n_approved`: every combination of these seven columns occurs in at least 3 rows. Unique rows on role + size + Q5 + Q6: 50 in v1.0, 0 in v1.1 (smallest group: 3). To reach this, 151 values in these columns are set to `suppressed` in 40 rows. No rows are removed.
- The guarantee covers only these seven columns. The other single-choice columns (Q7, Q14–Q19 and so on) are not part of it: combined with the seven columns they make many rows unique again. Someone who knows how an organization answered its governance questions can therefore still single out that organization's rows. Do not try to identify respondents or organizations.
- In groups (equal on all seven columns) with fewer than 5 rows, Q23 and `shadow_use` are set to `suppressed` where every respondent in the group gave the same answer. This affects 42 values (Q23: 6, `shadow_use`: 36).
- `shadow_use` follows from the Q6 and Q8b columns, so a suppressed value can often be worked out again (for example, `q8b_browser-llm` = 1 always means `yes`, because browser tools are never approved). In the 15 rows where this was possible, or where `shadow_use` together with the Q8b flags revealed a suppressed Q6 value, 2 more `shadow_use` values and 62 Q8b values (flags and `q8b_n_used`) are set to `suppressed`. In total 38 `shadow_use` values are suppressed, and none of them, nor any suppressed Q6 value, can be derived from the Q6, Q8b and `shadow_use` columns. This was checked by trying every possible Q6 and Q8b answer.

Per-option counts for all codes, including the folded ones, are given in the column sections below and in `respondent-level-aggregates.csv`. The analysis scripts in `scripts/` were written for version 1.0 and do not run on version 1.1.

## Removed or changed for privacy

- The organization column is removed. Responses came from 57 organizations, but the file does not say which responses share an organization. Results that need the organization (majority-vote organization values, intra-organization disagreement, organization-level correlations) are published as aggregates in `org-level-tables.csv`.
- Role is given as three analytical groups only.
- Developer team size bands below 200 are merged, and codes given by fewer than 3 respondents, and categories that could identify an organization (e.g. internal platforms), are merged into `other` (Q6, Q8b, Q11 `rarely`, Q19 `not-applicable`; see the column notes). The one exception is the `other` code in Q8b itself (2 respondents), which cannot be merged further. In version 1.1 the k ≥ 3 guarantee covers the larger quasi-identifier set described in [Changes in v1.1](#changes-in-v11).
- Removed: timestamp, device and collection-channel columns, the original organization text, the free-text question on public-sector concerns (Q21), the interview opt-in (Q24) and contact details, and all free text entered under "other".

- **Figures regenerated from the public CSV differ slightly from the paper.** The respondent who listed `open-source` as approved (Q6, fewer than 3) now has `other`. Figure 2 (`tool-landscape.svg`) therefore has no open-source approved bar, and Figure 3 (`shadow-adoption-flow.svg`) shows 16 open-source shadow users instead of 15. The paper's value (15) is in `respondent-level-aggregates.csv`.

## Columns

### 1. `Hva er din primærrolle?`

- Form question: Q2 *Hva er din primærrolle?* (What is your primary role?)
- Values (recoded from seven form options): `practitioner` (form codes developer, platform, and practitioner roles given as free text) 56; `technical-leadership` (tech-lead, team-lead and leader roles given as free text) 44; `organizational-leadership` (cto, non-tech-leader and leadership roles given as free text) 15.

### 2. `Omtrent hvor mange utviklere og teknisk personell har organisasjonen din?`

- Form question: Q3 (instrument Q3) *Omtrent hvor mange utviklere og teknisk personell har organisasjonen din?*
- English: Approximately how many developers and technical personnel does your organization have? (Include both permanent employees and contracted consultants who write or maintain code for the organization. Total org headcount is sourced from public registries.)
- Type: Single-select
- Instrument options: Ingen — vi har ikke utviklere / 1–10 / 11–50 / 51–200 / Flere enn 200 / Vet ikke
- Codes (count): `1-200` 75, `200+` 36, `unknown` 4 (v1.1: `1-200` 69, `200+` 34, `unknown` 3, `suppressed` 9). The form bands `1-10`, `11-50` and `51-200` are merged into `1-200` so that every role × size combination has at least 3 respondents. Counts for the original bands are in `respondent-level-aggregates.csv`.

### 3. `Hva beskriver best organisasjonens bruk av KI-kodeverktøy i dag?`

- Form question: Q5 (instrument Q5) *Hva beskriver best organisasjonens bruk av KI-kodeverktøy i dag?*
- English: Which best describes your organization's use of AI coding tools today? (Select the option that best describes the current situation. The three middle options distinguish between informal use by individuals, the organization having made an official decision but not everyone using the tools yet, and most developers actually having access and using them.)
- Type: Single-select — behavioral anchor scale
- Instrument options: Ikke i bruk, så vidt jeg vet / Enkeltpersoner bruker KI-verktøy på eget initiativ / Noen team har tatt i bruk KI-verktøy, men det finnes ingen organisasjonsomfattende tilnærming / Organisasjonen har offisielt godkjent eller anskaffet KI-kodeverktøy, men ikke alle team bruker dem ennå / De fleste utviklere har tilgang til og bruker KI-kodeverktøy / Vet ikke
- Codes (count) in v1.0: `officially-approved` 45, `most-developers` 45, `some-teams` 17, `individual` 8
- v1.1 values: `formal` (`officially-approved` and `most-developers`) 86, `informal` (`some-teams` and `individual`) 20, `suppressed` 9

### 4. `Hvor sikker er du på svaret over? (Q5b)`

- Form question: Q5b (instrument Q5b) *Hvor sikker er du på svaret over?*
- English: How confident are you in the answer above?
- Type: Single-select — confidence indicator
- Instrument options: Jeg vet dette sikkert (f.eks. er involvert i beslutningen) / Ganske sikker basert på det jeg har sett / Dette er mitt beste estimat
- Codes (count): `certain` 56, `fairly-sure` 47, `estimate` 11; empty 1

### 5. `Hvilke KI-kodeverktøy er offisielt godkjent eller anskaffet i organisasjonen din?`

- Form question: Q6 (instrument Q6) *Hvilke KI-kodeverktøy er offisielt godkjent eller anskaffet i organisasjonen din?*
- English: Which AI coding tools are officially approved or procured in your organization?
- Type: Multi-select (checkboxes)
- Instrument options: GitHub Copilot / Cursor / Codex / Windsurf / Antigravity / Claude Code / Amazon Q Developer / Gemini Code Assist / JetBrains AI Assistant / Ingen offisielt godkjente verktøy / Vet ikke / Andre (spesifiser)
- Codes (count): `copilot` 94, `claude-code` 40, `codex` 16, `cursor` 13, `none` 9, `jetbrains-ai` 9, `other` 11, `unknown` 4, `gemini` 3. `other` includes the rare categories `internal-platform`, `other-tool`, `code-review-ai`, `amazon-q` and `open-source`; their separate counts are in `respondent-level-aggregates.csv`.

### 6. `Hvor sikker er du på svaret over? (Q6b)`

- Form question: Q6b (instrument Q6b) *Hvor sikker er du på svaret over?*
- English: How confident are you in the answer above?
- Type: Single-select — confidence indicator
- Instrument options: Jeg vet dette sikkert (f.eks. er involvert i beslutningen) / Ganske sikker basert på det jeg har sett / Dette er mitt beste estimat
- Codes (count): `certain` 62, `fairly-sure` 46, `estimate` 7

### 7. `Hva var den viktigste måten KI-kodeverktøy ble innført i organisasjonen din?`

- Form question: Q7 (instrument Q7) *Hva var den viktigste måten KI-kodeverktøy ble innført i organisasjonen din?*
- English: What was the most important way AI coding tools were introduced in your organization?
- Type: Single-select
- Instrument options: Sentral anskaffelse eller IT-avdeling bestemte / Team eller avdeling valgte selv / Enkeltpersoner begynte å bruke verktøy, og det ble etter hvert akseptert / Verktøyet fulgte med en eksisterende avtale (f.eks. Microsoft/GitHub-avtale) / Ikke aktuelt — vi bruker ikke KI-kodeverktøy / Vet ikke / Annet (spesifiser)
- Codes (count): `central` 45, `bundled` 23, `bottom-up` 17, `team` 11, `other` 8, `unknown` 7, `not-applicable` 4

### 8. `Bruker du KI-kodeverktøy?`

- Form question: Q8 (instrument Q8) *Bruker du KI-kodeverktøy?*
- English: Do you use AI coding tools?
- Type: Single-select
- Instrument options: Ja / Nei
- Codes (count): `yes` 106, `no` 9

### 9. `Hvilke KI-kodeverktøy bruker du?`

- Form question: Q8b (instrument Q8b) *Hvilke KI-kodeverktøy bruker du?*
- English: Which AI coding tools do you use?
- Type: Multi-select (checkboxes)
- Instrument options: GitHub Copilot / Cursor / Codex / Windsurf / Antigravity / Claude Code / Amazon Q Developer / Gemini Code Assist / Gemini CLI / JetBrains AI Assistant / ChatGPT, Claude eller lignende via nettleser/API (ikke dedikert kodeverktøy) / Aider, OpenCode eller andre open source-verktøy / Andre (spesifiser)
- Codes (count): `copilot` 78, `claude-code` 48, `browser-llm` 45, `open-source` 18, `codex` 17, `gemini` 11, `cursor` 9, `windsurf` 7, `jetbrains-ai` 3, `other` 2; empty 9. `other` includes `other-tool` and `code-review-ai` (each fewer than 3).

### 10. `Hvilke måter bruker du KI-kodeverktøy på?`

- Form question: Q9 (instrument Q9) *Hvilke måter bruker du KI-kodeverktøy på?*
- English: In which ways do you use AI coding tools?
- Type: Multi-select (checkboxes)
- Instrument options: Autofullføring av kode (verktøyet foreslår kode mens jeg skriver) / Chat i editoren (jeg stiller spørsmål og får svar) / Planlegging av oppgaver (KI hjelper meg å bryte ned og planlegge arbeid) / Agentmodus lokalt (verktøyet gjør endringer på tvers av flere filer på min maskin) / Agentmodus i skyen (f.eks. GitHub Copilot coding agent som kjører uten at jeg er til stede) / Kodegjennomgang med KI (f.eks. Copilot code review) / Testgenerering / Feilsøking / debugging
- Codes (count): `chat` 87, `local-agent` 77, `debugging` 70, `planning` 68, `autocomplete` 58, `code-review` 55, `test-generation` 52, `cloud-agent` 24; empty 9

### 11. `Har du koblet KI-kodeverktøyet ditt til andre systemer?`

- Form question: Q10 (instrument Q10) *Har du koblet KI-kodeverktøyet ditt til andre systemer?*
- English: Have you connected your AI coding tool to other systems? (Some AI tools can connect to external systems via integrations, e.g. MCP servers or built-in integrations. Select all that apply.)
- Type: Multi-select (checkboxes)
- Instrument options: Nei, jeg bruker bare kodegenerering og chat / Kodeadministrasjon (f.eks. GitHub, GitLab) / Oppgavehåndtering (f.eks. Jira, Linear, Azure Boards) / CI/CD (f.eks. GitHub Actions, Jenkins) / Infrastruktur og drift (f.eks. Kubernetes, Terraform) / Overvåking og logger (f.eks. Grafana, Datadog) / Kommunikasjon (f.eks. Slack, Teams) / Vet ikke hva dette betyr / Andre (spesifiser)
- Codes (count): `none` 55, `scm` 40, `cicd` 19, `project-mgmt` 17, `infra` 14, `monitoring` 13, `other` 7, `communication` 6; empty 9

### 12. `Hvor ofte bruker du KI-kodeverktøy i arbeidet ditt?`

- Form question: Q11 (instrument Q11) *Hvor ofte bruker du KI-kodeverktøy i arbeidet ditt?*
- English: How often do you use AI coding tools in your work?
- Type: Single-select — frequency scale
- Instrument options: Daglig / Flere ganger i uken / Ukentlig / Noen ganger i måneden / Sjelden eller aldri
- Codes (count): `daily` 73, `several-weekly` 15, `weekly` 10, `monthly` 7, `other` fewer than 3 (merged from `rarely`); empty 9

### 13. `Hva er den viktigste fordelen du opplever med KI-kodeverktøy?`

- Form question: Q11b (instrument Q11b) *Hva er den viktigste fordelen du opplever med KI-kodeverktøy?*
- English: What is the most important benefit you experience from AI coding tools?
- Type: Single-select — forced-choice (not agree/disagree)
- Instrument options: Økt hastighet — jeg skriver kode raskere / Bedre kvalitet — KI hjelper meg å skrive bedre kode / Læring — jeg lærer nye teknikker og mønstre / Redusert kjedelig arbeid — KI tar seg av repetitive oppgaver / Jeg opplever ikke vesentlige fordeler / Annet (spesifiser)
- Codes (count): `speed` 38, `reduced-toil` 27, `learning` 14, `other` 13, `quality` 8, `no-benefit` 6; empty 9

### 14. `Har organisasjonen din retningslinjer eller policy for bruk av KI-kodeverktøy?`

- Form question: Q14 (instrument Q12) *Har organisasjonen din retningslinjer eller policy for bruk av KI-kodeverktøy?*
- English: Does your organization have guidelines or a policy for the use of AI coding tools?
- Type: Single-select
- Instrument options: Ja, spesifikt for KI-kodeverktøy / Ja, som del av en generell KI-policy / Nei / Vet ikke
- Codes (count): `general` 49, `specific` 47, `unknown` 11, `no` 8

### 15. `Hvor sikker er du på svaret over? (Q14b)`

- Form question: Q14b (instrument Q12b) *Hvor sikker er du på svaret over?*
- English: How confident are you in the answer above?
- Type: Single-select — confidence indicator
- Instrument options: Jeg vet dette sikkert (f.eks. er involvert i beslutningen) / Ganske sikker basert på det jeg har sett / Dette er mitt beste estimat
- Codes (count): `certain` 54, `fairly-sure` 37, `estimate` 24

### 16. `Hvordan støtter organisasjonen din utviklere i bruk av KI-kodeverktøy?`

- Form question: Q15 (instrument Q13) *Hvordan støtter organisasjonen din utviklere i bruk av KI-kodeverktøy?*
- English: How does your organization support developers in using AI coding tools?
- Type: Single-select — behavioral anchor scale
- Instrument options: Ingen støtte eller opplæring / Uformell kunnskapsdeling mellom utviklere / Delte ressurser eller retningslinjer er tilgjengelige (f.eks. wiki, beste praksis) / Organisert opplæring eller kurs / Strukturert program (f.eks. champions-nettverk, dedikerte ressurspersoner, tilbakemeldingsrutiner) / Vet ikke
- Codes (count): `informal` 50, `shared-resources` 26, `training` 22, `structured` 9, `none` 5, `unknown` 3

### 17. `Hvordan avgjøres det hvilke KI-kodeverktøy utviklere kan bruke?`

- Form question: Q16 (instrument Q14) *Hvordan avgjøres det hvilke KI-kodeverktøy utviklere kan bruke?*
- English: How is it decided which AI coding tools developers can use?
- Type: Single-select
- Instrument options: Sentralt besluttet (f.eks. IT-avdelingen eller ledelsen velger for hele organisasjonen) / Via en godkjenningsprosess (f.eks. risikovurdering/ROS, så kan team eller utviklere foreslå verktøy) / Teamet eller tech lead bestemmer / Hver enkelt utvikler bestemmer selv / Ingen har eksplisitt bestemt dette / Vet ikke
- Codes (count): `central` 50, `approval-process` 34, `unknown` 9, `individual` 8, `team` 7, `undecided` 7

### 18. `Har organisasjonen din avklart hvilke KI-leverandører som behandler kildekoden deres?`

- Form question: Q17 (instrument Q15) *Har organisasjonen din avklart hvilke KI-leverandører som behandler kildekoden deres?*
- English: Has your organization clarified which AI providers process your source code? (When you use AI coding tools, source code is sent to an external model provider for processing. Some organizations have clarified this through data processing agreements or risk assessments.)
- Type: Single-select
- Instrument options: Ja, det er tydelig avklart / Delvis — noe er avklart, men ikke for alle verktøy / Nei / Vet ikke
- Codes (count): `clarified` 59, `partial` 34, `unknown` 15, `no` 7

### 19. `Hvordan vurderer organisasjonen din effekten av KI-kodeverktøy?`

- Form question: Q18 (instrument Q16) *Hvordan vurderer organisasjonen din effekten av KI-kodeverktøy?*
- English: How does your organization assess the impact of AI coding tools? (Select the highest level that applies to your organization. Each level includes those below it.)
- Type: Single-select — behavioral anchor scale
- Instrument options: Vi vurderer ikke effekten / Uformelle tilbakemeldinger og anekdoter / Vi følger med på bruksdata fra verktøyleverandøren (f.eks. antall brukere, akseptrate) / Vi måler effekten med egne metrikker (f.eks. leveransetakt, kvalitet, utvikleropplevelse) / Vet ikke
- Codes (count): `informal` 50, `unknown` 30, `vendor-data` 14, `own-metrics` 13, `none` 8

### 20. `Hvordan håndteres KI-generert kode i kodegjennomgang (code review)?`

- Form question: Q19 (instrument Q17) *Hvordan håndteres KI-generert kode i kodegjennomgang (code review)?*
- English: How is AI-generated code handled in code review? (By "AI-generated code" we mean all code written or substantially modified with the help of AI tools — both fully generated code and code where AI has suggested changes.)
- Type: Single-select — cumulative behavioral anchor
- Instrument options: Ingen spesiell håndtering — KI-generert kode gjennomgås som all annen kode / Vi har muntlige retningslinjer om å være ekstra oppmerksom på KI-generert kode / Vi har skriftlige retningslinjer for gjennomgang av KI-generert kode / Vi har skriftlige retningslinjer og bruker automatiserte verktøy for å sjekke KI-generert kode (f.eks. sikkerhetsskanning) / Ikke aktuelt — vi bruker ikke KI-kodeverktøy eller har ikke kodegjennomgang / Vet ikke
- Codes (count): `no-special` 71, `verbal` 14, `unknown` 13, `written` 8, `written-automated` 7, `other` fewer than 3 (merged from `not-applicable`)

### 21. `Hva er dine viktigste bekymringer knyttet til bruk av KI-kodeverktøy?`

- Form question: Q20 (instrument Q18) *Hva er dine viktigste bekymringer knyttet til bruk av KI-kodeverktøy?*
- English: What are your most important concerns related to the use of AI coding tools? (Select your top three.)
- Type: Multi-select (checkboxes) — max 3
- Instrument options: Sikkerhetssårbarheter i KI-generert kode / Kodekvalitet og teknisk gjeld / Personvern og datahåndtering (kildekode sendes til ekstern leverandør) / Immaterielle rettigheter og lisenser (hvem eier KI-generert kode?) / Tap av kompetanse eller ferdigheter over tid / Kostnad i forhold til nytte / Feil og hallusinasjoner (KI-verktøyet genererer kode som ser riktig ut men er feil) / Arbeidsflyt (verktøyet forstyrrer mer enn det hjelper) / Jeg har ingen vesentlige bekymringer / Andre (spesifiser)
- Codes (count): `skill-loss` 82, `code-quality` 65, `hallucinations` 46, `security` 39, `privacy` 31, `cost` 20, `ip` 8, `workflow` 8, `other` 8, `no-concerns` 5

### 22. `Hvordan forholder du deg til KI-generert kode?`

- Form question: Q22 (instrument Q20) *Hvordan forholder du deg til KI-generert kode?*
- English: How do you relate to AI-generated code?
- Type: Single-select — behavioral anchor (trust scale)
- Instrument options: Jeg godtar aldri KI-forslag uten å gjennomgå og forstå koden / Jeg gjennomgår det meste, men godtar enkle forslag uten grundig sjekk / Jeg godtar ofte KI-forslag etter en rask sjekk / Jeg godtar som regel KI-forslag som ser riktige ut / Ikke aktuelt — jeg bruker ikke KI-kodeverktøy
- Codes (count): `mostly-review` 50, `always-review` 28, `quick-check` 18, `not-applicable` 10, `usually-accept` 9

### 23. `Er det et gap mellom hva organisasjonen din tillater og hva du mener er forsvarlig?`

- Form question: Q23 (instrument Q21) *Er det et gap mellom hva organisasjonen din tillater og hva du mener er forsvarlig?*
- English: Is there a gap between what your organization allows and what you consider responsible?
- Type: Single-select
- Instrument options: Organisasjonen er for restriktiv — vi burde bruke KI-verktøy mer / Organisasjonens tilnærming samsvarer med det jeg mener er forsvarlig / Organisasjonen er for liberal — vi burde ha strengere retningslinjer / Organisasjonen har ingen tydelig tilnærming, så det er vanskelig å si / Vet ikke / har ingen mening
- Codes (count): `aligned` 48, `too-liberal` 23, `no-approach` 21, `too-restrictive` 18, `unknown` 5 (v1.1: 6 values `suppressed`, see [Changes in v1.1](#changes-in-v11))

## Derived columns (v1.1)

Flags are `1` (chosen) or `0`. Empty: question not shown. `suppressed`: see [Changes in v1.1](#changes-in-v11). Counts ignore `none` and `unknown`.

| Column | Source | Values |
|---|---|---|
| `q6_copilot`, `q6_claude-code` | Q6 approved tools | `1`/`0`, `suppressed` (includes the respondents who chose only `unknown`) |
| `q6_other` | Q6 | `1` if any other approved tool (codex, cursor, jetbrains-ai, gemini, other) |
| `q6_n_approved` | Q6 | number of approved tools: `0`, `1`, `2`, `3+` |
| `q8b_copilot`, `q8b_claude-code`, `q8b_browser-llm`, `q8b_open-source`, `q8b_codex`, `q8b_gemini` | Q8b tools used | `1`/`0`, `suppressed` |
| `q8b_other` | Q8b | `1` if any other tool used (cursor, windsurf, jetbrains-ai, other) |
| `q8b_n_used` | Q8b | number of tools used: `1`, `2`, `3`, `4+` |
| `shadow_use` | Q8b and Q6 | `yes` if the respondent uses a tool (Q8b, in the merged v1.0 codes) not among the approved tools (Q6); `no`; `suppressed` (includes the respondents who chose only `unknown` in Q6) |
| `q9_n_modes` | Q9 usage modes | number of modes: `1` to `5`, `6+` |
| `q10_n_connected` | Q10 connected systems | number of systems (`none` = 0): `0`, `1`, `2`, `3+` |
| `q20_skill-loss`, `q20_code-quality`, `q20_hallucinations`, `q20_security`, `q20_privacy`, `q20_cost` | Q20 concerns | `1`/`0` |
| `q20_other` | Q20 | `1` if any other concern (ip, workflow, other, no-concerns) |

`shadow_use` uses every tool, including `browser-llm` and `open-source`, so it matches the paper's broad shadow adoption only roughly. Because of suppression, its counts are not comparable with the paper; use `respondent-level-aggregates.csv` and the paper for shadow adoption rates.


## `org-level-tables.csv`

Aggregate organization-level results, computed from the non-public file with the organization column using the same code as the analysis script. Columns: `table`, `measure`, `value`, `n` (denominator), `unit` (`orgs`, `respondents`, `percent` or `p`). Counts below 3 are shown as `<3`. So that a hidden count cannot be worked out from the total, the next-smallest counts in the same table are also hidden, shown as `suppressed`, until at least two cells and at least 3 respondents or organizations are hidden (version 1.1, same rule as State of Platforms). Tables:

- `sample`: number of organizations, and of organizations with one or several respondents.
- `org-level majority vote: …`: the organization's answer by majority vote among its respondents, per question; `disagreement` means no majority.
- `intra-org disagreement vs permutation null: …`: multi-respondent organizations where respondents disagree, compared with a permutation null (10,000 draws, seed 20260511).
- `org-level Spearman: …`: correlation between adoption level and governance index at organization level, with the two sensitivity variants.
- `org-union shadow robustness (respondents)`: shadow adoption when "approved" means approved per any respondent from the same organization.

## `respondent-level-aggregates.csv`

Respondent-level counts per answer option for every closed question (version 1.2). Columns: `table`, `measure` (option code), `value` (count), `n` (denominator), `unit`, `question_id` (the question id in the website survey definition, e.g. `q7-introduction-path`). Version 1.1 had the first five columns only; they are unchanged.

Covered questions (23): `q2-role`, `q3-dev-count`, `q5-adoption-level`, `q5b-confidence`, `q6-approved-tools`, `q6b-confidence`, `q7-introduction-path`, `q8-personal-use`, `q8b-personal-tools`, `q9-usage-modes`, `q10-integrations`, `q11-frequency`, `q11b-benefit`, `q12-policy`, `q12b-confidence`, `q13-support`, `q14-decision-authority`, `q15-data-sovereignty`, `q16-measurement`, `q17-code-review`, `q18-concerns`, `q20-trust`, `q21-perception-gap`. Not covered: the organization (`q1-org`), free text (`q19-public-sector-concerns`), the interview opt-in (`q23-interview`) and the e-mail address (`q24-email`).

- The tables from version 1.1 are kept as they were: team size in the original form bands (`q3-dev-count`), Q6/Q8b tools and Q11/Q17 in the original categories and codes, and the Figure 3 open-source shadow count (15, no `question_id`), which the merged Q6 codes change to 16. They use their own categories (e.g. `internal-platform`, `other-tool`, `code-review-ai`), are not in survey order, and have no zero rows. Only Q11 and Q19 (`q11-frequency`, `q17-code-review`) use `n` 115 with blank answers as `(empty)`; Q8b uses `n` 106 and has no no-answer row.
- The other questions have a table named `<question_id>, survey option values`, using the survey's option values in survey order, with options nobody chose included (count 0). `n` is the number of respondents who answered the question; for multi-select questions the counts add up to more than `n`. A `(no answer)` row (with `n` 115) counts respondents who left the question blank or did not see it; it equals 115 minus `n`.
- Codes are those used in the CSV before merging: role is given as the three analytical groups, and free text under "other" in Q6/Q8b as tool categories.
- Counts below 3 are shown as `<3`. So that a hidden count cannot be worked out from the total, the next-smallest counts in the same table are also hidden, shown as `suppressed`, until at least two cells and at least 3 respondents are hidden. In multi-select tables each `<3` counts as 1. Zero counts are shown. All 11 hidden cells are in the version 1.1 tables; the new tables have no counts below 3.
- Checked against the row file: for the columns with `suppressed` values (team size, Q5, Q23), the tables show the same totals as the column sections above, so they say nothing new about the suppressed values, and none of them can be pinned to a single code. The row file shows the exact counts behind two hidden cells (`q11-frequency` `monthly`, `q17-code-review` `written-automated`), as it already did in version 1.1.
