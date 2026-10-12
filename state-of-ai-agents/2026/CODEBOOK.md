# Codebook: State of AI Coding Agents in the Norwegian Public Sector, Wave 1 (2026)

File: `ai-agents-2026-anonymous.csv` (UTF-8, comma-separated, header row). 115 rows, one per respondent, 23 columns. Collected April–May 2026.

## Conventions

- Multi-select answers are semicolon-separated codes (e.g. `copilot;claude-code`).
- Empty cell: question not shown (respondents who answered `no` to personal use skip the personal-usage questions) or left blank.
- `other`: the respondent chose "Annet" (other). The free text is not released. For the two tool questions, free-text answers are replaced by a tool category instead (`open-source` or an existing tool code); rare categories are merged into `other`, see columns 5 and 9.
- Question numbers follow the Google Form used in the paper. The survey instrument (Norwegian, with English translations) uses its own design numbering; both are given below.
- Codes are listed with their counts. The Norwegian response options from the instrument are given for reference, in instrument order; the codes are short English labels for these options.

## Removed or changed for privacy

- The organization column is removed. Responses came from 57 organizations, but the file does not say which responses share an organization. Results that need the organization (majority-vote organization values, intra-organization disagreement, organization-level correlations) are published as aggregates in `org-level-tables.csv`.
- Role is given as three analytical groups only.
- Developer team size bands below 200 are merged, and codes given by fewer than 3 respondents, and categories that could identify an organization (e.g. internal platforms), are merged into `other` (Q6, Q8b, Q11 `rarely`, Q19 `not-applicable`; see the column notes). The one exception is the `other` code in Q8b itself (2 respondents), which cannot be merged further. The result: every role × size combination has at least 3 respondents (smallest group: 4).
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
- Codes (count): `1-200` 75, `200+` 36, `unknown` 4. The form bands `1-10`, `11-50` and `51-200` are merged into `1-200` so that every role × size combination has at least 3 respondents. Counts for the original bands are in `respondent-level-aggregates.csv`.

### 3. `Hva beskriver best organisasjonens bruk av KI-kodeverktøy i dag?`

- Form question: Q5 (instrument Q5) *Hva beskriver best organisasjonens bruk av KI-kodeverktøy i dag?*
- English: Which best describes your organization's use of AI coding tools today? (Select the option that best describes the current situation. The three middle options distinguish between informal use by individuals, the organization having made an official decision but not everyone using the tools yet, and most developers actually having access and using them.)
- Type: Single-select — behavioral anchor scale
- Instrument options: Ikke i bruk, så vidt jeg vet / Enkeltpersoner bruker KI-verktøy på eget initiativ / Noen team har tatt i bruk KI-verktøy, men det finnes ingen organisasjonsomfattende tilnærming / Organisasjonen har offisielt godkjent eller anskaffet KI-kodeverktøy, men ikke alle team bruker dem ennå / De fleste utviklere har tilgang til og bruker KI-kodeverktøy / Vet ikke
- Codes (count): `officially-approved` 45, `most-developers` 45, `some-teams` 17, `individual` 8

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
- Codes (count): `aligned` 48, `too-liberal` 23, `no-approach` 21, `too-restrictive` 18, `unknown` 5


## `org-level-tables.csv`

Aggregate organization-level results, computed from the non-public file with the organization column using the same code as the analysis script. Columns: `table`, `measure`, `value`, `n` (denominator), `unit` (`orgs`, `respondents`, `percent` or `p`). Counts below 3 are shown as `<3`. For single-choice questions the totals allow these to be recovered; we consider univariate counts non-disclosive. Tables:

- `sample`: number of organizations, and of organizations with one or several respondents.
- `org-level majority vote: …`: the organization's answer by majority vote among its respondents, per question; `disagreement` means no majority.
- `intra-org disagreement vs permutation null: …`: multi-respondent organizations where respondents disagree, compared with a permutation null (10,000 draws, seed 20260511).
- `org-level Spearman: …`: correlation between adoption level and governance index at organization level, with the two sensitivity variants.
- `org-union shadow robustness (respondents)`: shadow adoption when "approved" means approved per any respondent from the same organization.

## `respondent-level-aggregates.csv`

Respondent-level counts that the merged codes in the CSV no longer show: developer team size in the original form bands, and Q6/Q8b tools in the original categories, Q11 and Q19 in the original codes, and the Figure 3 open-source shadow count (15), which the merged Q6 codes change to 16. Same columns as `org-level-tables.csv`; Counts below 3 are shown as `<3`. For single-choice questions the totals allow these to be recovered; we consider univariate counts non-disclosive.
