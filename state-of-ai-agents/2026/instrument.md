# Survey Instrument: State of AI Coding Agents — Wave 1

## Instrument Metadata

- **Study:** State of AI Coding Agents in the Norwegian Public Sector
- **Wave:** 1 (Q2 2026, April–May)
- **Target population:** Developers and technical leaders in Norwegian public sector organizations
- **Distribution method:** Online survey (Google Forms) via Offentlig PAAS community + broader Norwegian public sector IT networks
- **Language:** Norwegian (bokmål)
- **Estimated completion time:** 10–12 minutes
- **Core questions carried from previous wave:** 0 (Wave 1 — new study)
- **New questions this wave:** 20 substantive + 4 demographics + intro/consent + interview opt-in
- **Retired questions:** N/A
- **Platform:** Google Forms

---


## Question Numbering: Instrument vs. Google Form

The paper (<https://nye.offentlig-paas.no/forskning>) and the analysis script (`scripts/analyze_wave1_v2.py`) use the Google Form numbering. Q1–Q11b are identical; from the policy question onward the form numbers are two higher. The instrument has 27 items in total, including the three confidence follow-ups, the interview opt-in and the contact field.

| Instrument | Google Form / paper | Topic |
| ---------- | ------------------- | ----- |
| Q1–Q11b    | Q1–Q11b             | Organization, role, size, adoption, tools, personal use |
| Q12        | Q14                 | Policy |
| Q12b       | Q14b                | Policy confidence |
| Q13        | Q15                 | Organizational support |
| Q14        | Q16                 | Decision-making |
| Q15        | Q17                 | Vendor/DPA clarity |
| Q16        | Q18                 | Effect measurement |
| Q17        | Q19                 | Code review |
| Q18        | Q20                 | Concerns |
| Q19        | Q21                 | Public-sector concerns |
| Q20        | Q22                 | Personal stance on AI-generated code |
| Q21        | Q23                 | Perceived policy gap |
| Q23        | Q24                 | Follow-up interview opt-in |

## Google Forms Structure

The survey is organized into **10 sections** in Google Forms. Three branch points provide routing.

```
Section 1: Introduksjon og samtykke
Section 2: Om deg og din organisasjon (demographics + screening)
  → Q3 "Ingen" → Section 10
Section 3: Adopsjon av KI-kodeverktøy (RQ1 — organizational)
Section 4: Din personlige bruk — screening (RQ1 — individual)
  → Q8 "Nei" → Section 6
Section 5: Bruksmønster og fordeler (RQ1 — individual, users only)
Section 6: Styring og organisatorisk støtte (RQ2)
Section 7: Bekymringer og barrierer (RQ3)
Section 8: Oppfølging (Q23)
  → Q23 "Ja" → Section 9; "Nei" → Section 10
Section 9: Kontaktinformasjon for intervju (Q24)
Section 10: Takk for din deltakelse
```

**Branching logic:**

- Section 2 → Q3 "Ingen — vi har ikke utviklere" → skip to Section 10
- Section 4 → Q8 "Nei" → skip to Section 6; "Ja" → go to Section 5
- Section 8 → Q23 "Ja" → go to Section 9; "Nei" → skip to Section 10

---

## Section 1: Introduksjon og samtykke

*Google Forms: Section header with description. No questions — text only.*

**Section title:** KI-kodeverktøy i norsk offentlig sektor

**Section description:**

> **Hva handler undersøkelsen om?**
> Vi kartlegger hvordan norske offentlige virksomheter tar i bruk og styrer KI-kodeverktøy (som GitHub Copilot, Cursor, Claude Code og lignende). Undersøkelsen tar ca. 10 minutter.
>
> Undersøkelsen dekker både din egen bruk av KI-kodeverktøy og hvordan organisasjonen din styrer og legger til rette for slik bruk.
>
> **Hvem er ansvarlig?**
> Undersøkelsen gjennomføres av Offentlig PAAS. Behandlingsansvarlig er Hans Kristian Flaatten (styreleder), kontakt@offentlig-paas.no.
>
> **Hva samler vi inn?**
> Vi samler inn svar om organisasjonens og din bruk av KI-kodeverktøy, styring og bekymringer. Vi spør om organisasjonsnavn for å kunne oppdage og slå sammen duplikater — organisasjonen din vil ikke bli navngitt i publikasjoner. Dersom du ønsker å delta i oppfølgingsintervju, ber vi om e-postadresse — denne lagres separat fra svarene dine.
>
> **Personvern og GDPR**
> Behandlingsgrunnlaget er samtykke (GDPR art. 6 nr. 1 bokstav a). Ingen enkeltpersoner eller organisasjoner vil bli identifisert i publikasjoner. Svarene lagres i Google Forms og slettes senest to år etter at studien er avsluttet.
>
> Du har rett til å be om innsyn, retting eller sletting av dine opplysninger. Du kan også klage til Datatilsynet. Kontakt oss på kontakt@offentlig-paas.no hvis du har spørsmål.
>
> **Frivillig deltakelse**
> Det er helt frivillig å delta, og du kan avslutte når som helst uten å oppgi grunn. Ved å gå videre samtykker du til deltakelse.

---

## Section 2: Om deg og din organisasjon

### Q1: Hvilken organisasjon tilhører du?

- **English translation:** Which organization do you belong to?
- **Type:** Short text (open)
- **Response options:** Free text
- **RQ mapping:** Demographics (linking variable for cross-study analysis with State of Platforms)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** None identified — factual
- **Analysis plan:** Organization-level grouping variable; enables cross-study linking with State of Platforms dataset; enables duplicate detection for multi-respondent orgs
- **Data type:** Nominal (free text, coded to organization list)
- **Skip logic:** None
- **Google Forms notes:** Short answer. Required.

---

### Q2: Hva er din primærrolle?

- **English translation:** What is your primary role?
- **Type:** Single-select
- **Response options:**
  1. Utvikler / ingeniør
  2. Tech lead / arkitekt
  3. Teamleder
  4. Plattformteamleder / plattformutvikler
  5. IT-leder / CTO / IT-direktør
  6. Leder (ikke-teknisk)
  7. Annet (spesifiser)
- **RQ mapping:** Demographics (quality filtering variable per respondent qualification table)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Social desirability — respondents may choose higher-status roles. Mitigated by using descriptive labels.
- **Analysis plan:** Covariate for RQ3 barriers analysis; quality filter for organizational-level questions (RQ1-org, RQ2); frequency table
- **Data type:** Nominal
- **Skip logic:** None
- **Google Forms notes:** Multiple choice. Required. Include "Annet" with short text.

---

### Q3: Omtrent hvor mange utviklere og teknisk personell har organisasjonen din?

*Description text under question:*
> Inkluder både fast ansatte og innleide konsulenter som skriver eller vedlikeholder kode for organisasjonen. Totalantall ansatte i organisasjonen hentes fra offentlige registre.

- **English translation:** Approximately how many developers and technical personnel does your organization have? (Include both permanent employees and contracted consultants who write or maintain code for the organization. Total org headcount is sourced from public registries.)
- **Type:** Single-select
- **Response options:**
  1. Ingen — vi har ikke utviklere
  2. 1–10
  3. 11–50
  4. 51–200
  5. Flere enn 200
  6. Vet ikke
- **RQ mapping:** Demographics (dev team size as grouping variable) + Screening ("Ingen" = no developers)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Estimation error — respondents may not know exact headcount including consultants. Mitigated: wide ranges reduce precision burden; "vet ikke" available. Social desirability — orgs may exclude consultants to appear leaner. Mitigated: description explicitly says to include them.
- **Analysis plan:** Grouping variable; cross-tabulation with adoption level and governance indicators. "Ingen" respondents excluded from analysis (count reported as population coverage). Total org size coded from Q1 using public registries (SSB, annual reports) for cross-study comparison with State of Platforms.
- **Data type:** Ordinal
- **Skip logic:** "Ingen — vi har ikke utviklere" → go to Section 10 (end)
- **Google Forms notes:** Multiple choice. Required. "Ingen" triggers section-level branch to Section 10.

---

## Section 3: Adopsjon av KI-kodeverktøy (RQ1 — organisasjonsnivå)

*Section description:*
> I denne delen spør vi om organisasjonens bruk av KI-kodeverktøy. Svar basert på det du vet om organisasjonen som helhet. Det er helt greit å svare «vet ikke».
>
> Med «KI-kodeverktøy» mener vi verktøy som hjelper utviklere med å skrive, forstå eller endre kode ved hjelp av kunstig intelligens — for eksempel GitHub Copilot, Cursor, Claude Code, Amazon Q, eller lignende.

### Q5: Hva beskriver best organisasjonens bruk av KI-kodeverktøy i dag?

*Description text under question:*
> Velg det alternativet som best beskriver situasjonen i organisasjonen i dag. De tre midterste alternativene skiller mellom uformell bruk (enkeltpersoner på eget initiativ), organisasjonen har tatt en offisiell beslutning men ikke alle bruker verktøyene ennå, og at de fleste utviklere faktisk har tilgang og bruker dem.

- **English translation:** Which best describes your organization's use of AI coding tools today? (Select the option that best describes the current situation. The three middle options distinguish between informal use by individuals, the organization having made an official decision but not everyone using the tools yet, and most developers actually having access and using them.)
- **Type:** Single-select — behavioral anchor scale
- **Response options:**
  1. Ikke i bruk, så vidt jeg vet
  2. Enkeltpersoner bruker KI-verktøy på eget initiativ
  3. Noen team har tatt i bruk KI-verktøy, men det finnes ingen organisasjonsomfattende tilnærming
  4. Organisasjonen har offisielt godkjent eller anskaffet KI-kodeverktøy, men ikke alle team bruker dem ennå
  5. De fleste utviklere har tilgang til og bruker KI-kodeverktøy
  6. Vet ikke
- **RQ mapping:** RQ1 (Adoption — organizational level)
- **Longitudinal status:** New (Wave 1). Designed for exact reuse in future waves.
- **Wording change from previous wave:** N/A
- **Bias risks:** Anchoring (option 1 presented first may depress reported adoption). Social desirability (inflating adoption stage). Mitigated: behavioral anchors describe observable states, not judgments; "vet ikke" option reduces satisficing.
- **Analysis plan:** Frequency distribution; median adoption level; cross-tabulation with org size (Q3) and governance indicators (RQ2). Fisher's exact test for association with org size.
- **Data type:** Ordinal (5-point behavioral anchor + "vet ikke")
- **Skip logic:** None
- **Google Forms notes:** Multiple choice. Required. Option shuffle OFF (anchored scale must preserve order).

---

### Q5b: Hvor sikker er du på svaret over?

- **English translation:** How confident are you in the answer above?
- **Type:** Single-select — confidence indicator
- **Response options:**
  1. Jeg vet dette sikkert (f.eks. er involvert i beslutningen)
  2. Ganske sikker basert på det jeg har sett
  3. Dette er mitt beste estimat
- **RQ mapping:** RQ1 (Data quality weight for Q5)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** None identified — meta-question
- **Analysis plan:** Reported alongside Q5: "X% report adoption level Y (Z% high confidence)." Used as analytical weight for organizational-level claims.
- **Data type:** Ordinal
- **Skip logic:** None
- **Google Forms notes:** Multiple choice. Required.

---

### Q6: Hvilke KI-kodeverktøy er offisielt godkjent eller anskaffet i organisasjonen din?

- **English translation:** Which AI coding tools are officially approved or procured in your organization?
- **Type:** Multi-select (checkboxes)
- **Response options:**
  1. GitHub Copilot
  2. Cursor
  3. Codex
  4. Windsurf / Antigravity
  5. Claude Code
  6. Amazon Q Developer
  7. Gemini Code Assist
  8. JetBrains AI Assistant
  9. Ingen offisielt godkjente verktøy
  10. Vet ikke
  11. Andre (spesifiser)
- **RQ mapping:** RQ1 (Adoption — organizational tools)
- **Longitudinal status:** New (Wave 1). Tool list will need updating in future waves as market evolves.
- **Wording change from previous wave:** N/A
- **Bias risks:** Anchoring — tools listed first may be over-selected. Mitigated: shuffle enabled; "Ingen" and "Vet ikke" participate in shuffle but are visually distinct from tool names. Recognition bias — respondents may select tools they recognize but that aren't actually approved; mitigated by confidence indicator on Q5.
- **Analysis plan:** Mention rates (% of organizations citing each tool, base = responding organizations). Cross-tabulation with organization size. Tool delivery model classification (IDE extension / AI-native IDE / CLI) applied in analysis.
- **Data type:** Nominal (multi-select)
- **Skip logic:** None
- **Google Forms notes:** Checkboxes. Required. Enable "Shuffle option order". Use built-in "Annet" (Other) — stays pinned at bottom. "Ingen offisielt godkjente verktøy" and "Vet ikke" will be shuffled with tool names (no item-level pinning in Google Forms).

---

### Q6b: Hvor sikker er du på svaret over?

- **English translation:** How confident are you in the answer above?
- **Type:** Single-select — confidence indicator
- **Response options:**
  1. Jeg vet dette sikkert (f.eks. er involvert i beslutningen)
  2. Ganske sikker basert på det jeg har sett
  3. Dette er mitt beste estimat
- **RQ mapping:** RQ1 (Data quality weight for Q6; enables shadow adoption gap calculation)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** None identified — meta-question
- **Analysis plan:** Reported alongside Q6. Shadow adoption gap (Q6↔Q8) filtered to respondents with high/medium confidence on Q6 to ensure valid gap measurement.
- **Data type:** Ordinal
- **Skip logic:** None
- **Google Forms notes:** Multiple choice. Required.

---

### Q7: Hva var den viktigste måten KI-kodeverktøy ble innført i organisasjonen din?

- **English translation:** What was the most important way AI coding tools were introduced in your organization?
- **Type:** Single-select
- **Response options:**
  1. Sentral anskaffelse eller IT-avdeling bestemte
  2. Team eller avdeling valgte selv
  3. Enkeltpersoner begynte å bruke verktøy, og det ble etter hvert akseptert
  4. Verktøyet fulgte med en eksisterende avtale (f.eks. Microsoft/GitHub-avtale)
  5. Ikke aktuelt — vi bruker ikke KI-kodeverktøy
  6. Vet ikke
  7. Annet (spesifiser)
- **RQ mapping:** RQ1 (Adoption — primary procurement path; shadow adoption triangulation)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Social desirability — organizations may over-report formal procurement. Mitigated: option 3 normalizes bottom-up adoption ("ble etter hvert akseptert" is non-judgmental). Forced single-choice: respondents whose org has both enterprise procurement AND bottom-up adoption must choose the dominant path.
- **Analysis plan:** Frequency table. Cross-check with Q5 (adoption level) for consistency — "sentral anskaffelse" should correlate with higher adoption levels. Option 3 frequency is a direct shadow adoption indicator.
- **Data type:** Nominal
- **Skip logic:** None
- **Google Forms notes:** Multiple choice. Required. Include "Annet" with short text.

---

## Section 4: Din personlige bruk — screening (RQ1 — individnivå)

*Section description:*
> Nå spør vi om din egen bruk av KI-kodeverktøy — uavhengig av hva organisasjonen offisielt tilbyr.

### Q8: Bruker du KI-kodeverktøy?

- **English translation:** Do you use AI coding tools?
- **Type:** Single-select
- **Response options:**
  1. Ja
  2. Nei
- **RQ mapping:** RQ1 (Adoption — individual level; screening for Section 5)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Minimal — binary screening question.
- **Analysis plan:** User vs. non-user proportion. Cross-tabulation with org adoption level (Q5) — does organizational adoption predict individual use?
- **Data type:** Nominal
- **Skip logic:** "Nei" → skip to Section 6 (Styring og organisatorisk støtte). Non-users skip Q8b–Q11b but still answer RQ2 and RQ3 questions.
- **Google Forms notes:** Multiple choice. Required. Branch: "Nei" → Section 6; "Ja" → Section 5.

---

## Section 5: Bruksmønster og fordeler (RQ1 — individnivå, kun brukere)

*Only shown to respondents who use AI coding tools (Q8 = "Ja").*

### Q8b: Hvilke KI-kodeverktøy bruker du?

- **English translation:** Which AI coding tools do you use?
- **Type:** Multi-select (checkboxes)
- **Response options:**
  1. GitHub Copilot
  2. Cursor
  3. Codex
  4. Windsurf / Antigravity
  5. Claude Code
  6. Amazon Q Developer
  7. Gemini Code Assist / Gemini CLI
  8. JetBrains AI Assistant
  9. ChatGPT, Claude eller lignende via nettleser/API (ikke dedikert kodeverktøy)
  10. Aider, OpenCode eller andre open source-verktøy
  11. Andre (spesifiser)
- **RQ mapping:** RQ1 (Adoption — individual level; shadow adoption via gap with Q6)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Under-reporting of unofficial tool use (fear of consequences). Mitigated: section framing emphasizes "uavhengig av hva organisasjonen offisielt tilbyr" and survey is anonymous. Option 8 captures LLM-via-browser which respondents may not think of as "AI coding tools."
- **Analysis plan:** Mention rates. **Key analysis: gap between Q6 (officially approved) and Q8b (personally used) = shadow adoption index.** Tools appearing in Q8b but not Q6 for the same organization indicate unofficial use. Tool delivery model classification applied in analysis.
- **Data type:** Nominal (multi-select)
- **Skip logic:** None (non-users already branched out at Q8)
- **Google Forms notes:** Checkboxes. Required. Enable "Shuffle option order". Use built-in "Annet" (Other) — stays pinned at bottom.

---

### Q9: Hvilke måter bruker du KI-kodeverktøy på?

- **English translation:** In which ways do you use AI coding tools?
- **Type:** Multi-select (checkboxes)
- **Response options:**
  1. Autofullføring av kode (verktøyet foreslår kode mens jeg skriver)
  2. Chat i editoren (jeg stiller spørsmål og får svar)
  3. Planlegging av oppgaver (KI hjelper meg å bryte ned og planlegge arbeid)
  4. Agentmodus lokalt (verktøyet gjør endringer på tvers av flere filer på min maskin)
  5. Agentmodus i skyen (f.eks. GitHub Copilot coding agent som kjører uten at jeg er til stede)
  6. Kodegjennomgang med KI (f.eks. Copilot code review)
  7. Testgenerering
  8. Feilsøking / debugging
- **RQ mapping:** RQ1 (Adoption — capability modes; distinguishes autocomplete users from agentic users)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Over-reporting of advanced modes (social desirability). Mitigated: each option includes a concrete description in parentheses.
- **Analysis plan:** Mention rates by mode. Cross-tabulation with role (Q2) and org adoption level (Q5). Mode combinations reveal capability profiles (e.g., "autocomplete only" vs. "full agentic").
- **Data type:** Nominal (multi-select)
- **Skip logic:** None (non-users already branched out at Q8)
- **Google Forms notes:** Checkboxes. Required. Enable "Shuffle option order".

---

### Q10: Har du koblet KI-kodeverktøyet ditt til andre systemer?

*Description text under question:*
> Noen KI-verktøy kan kobles til eksterne systemer via integrasjoner (f.eks. MCP-servere eller innebygde integrasjoner). Velg alle som gjelder.

- **English translation:** Have you connected your AI coding tool to other systems? (Some AI tools can connect to external systems via integrations, e.g. MCP servers or built-in integrations. Select all that apply.)
- **Type:** Multi-select (checkboxes)
- **Response options:**
  1. Nei, jeg bruker bare kodegenerering og chat
  2. Kodeadministrasjon (f.eks. GitHub, GitLab)
  3. Oppgavehåndtering (f.eks. Jira, Linear, Azure Boards)
  4. CI/CD (f.eks. GitHub Actions, Jenkins)
  5. Infrastruktur og drift (f.eks. Kubernetes, Terraform)
  6. Overvåking og logger (f.eks. Grafana, Datadog)
  7. Kommunikasjon (f.eks. Slack, Teams)
  8. Vet ikke hva dette betyr
  9. Andre (spesifiser)
- **RQ mapping:** RQ1 (Adoption — agent capability level / MCP; exploratory)
- **Longitudinal status:** New (Wave 1). Exploratory — may be refined or expanded in Wave 2 based on responses.
- **Wording change from previous wave:** N/A
- **Bias risks:** Comprehension risk — many respondents won't understand MCP or integrations. Mitigated: concrete examples per category; "vet ikke hva dette betyr" option. Over-reporting — some may consider standard IDE features as "integrations." Mitigated: categories name external systems, not IDE features.
- **Analysis plan:** Mention rates per category. Integration breadth score (count of categories 2–7 selected). Expected: vast majority at "nei" (code generation only). Cross-tabulation with role (Q2) — tech leads and platform engineers may have higher integration use. Baseline for tracking in future waves.
- **Data type:** Nominal (multi-select)
- **Skip logic:** None (non-users already branched out at Q8)
- **Google Forms notes:** Checkboxes. Required. Enable "Shuffle option order" for categories 2–7. Use built-in "Annet" (Other) — stays pinned at bottom. "Nei" and "Vet ikke" will be shuffled with categories (no item-level pinning).

---

### Q11: Hvor ofte bruker du KI-kodeverktøy i arbeidet ditt?

- **English translation:** How often do you use AI coding tools in your work?
- **Type:** Single-select — frequency scale
- **Response options:**
  1. Daglig
  2. Flere ganger i uken
  3. Ukentlig
  4. Noen ganger i måneden
  5. Sjelden eller aldri
- **RQ mapping:** RQ1 (Adoption — usage intensity; triangulation of adoption claims)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Over-reporting of frequency (social desirability). Mitigated: concrete frequency anchors (daglig/ukentlig etc.) rather than vague labels.
- **Analysis plan:** Frequency distribution. Cross-tabulation with adoption level (Q5) — does organizational adoption correlate with individual intensity? Median frequency by role.
- **Data type:** Ordinal
- **Skip logic:** None (non-users already branched out at Q8)
- **Google Forms notes:** Multiple choice. Required.

---

### Q11b: Hva er den viktigste fordelen du opplever med KI-kodeverktøy?

- **English translation:** What is the most important benefit you experience from AI coding tools?
- **Type:** Single-select — forced-choice (not agree/disagree)
- **Response options:**
  1. Økt hastighet — jeg skriver kode raskere
  2. Bedre kvalitet — KI hjelper meg å skrive bedre kode
  3. Læring — jeg lærer nye teknikker og mønstre
  4. Redusert kjedelig arbeid — KI tar seg av repetitive oppgaver
  5. Jeg opplever ikke vesentlige fordeler
  6. Annet (spesifiser)
- **RQ mapping:** RQ1 (Adoption — benefit perception; triangulation with adoption intensity)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Social desirability — users may feel pressure to report benefits. Mitigated: option 5 ("ingen vesentlige fordeler") is normalized. Forced-single-choice avoids acquiescence.
- **Analysis plan:** Frequency distribution. Cross-tabulation with usage frequency (Q11) — is perceived benefit correlated with intensity? "Ingen vesentlige fordeler" rate is a skepticism indicator.
- **Data type:** Nominal
- **Skip logic:** None (non-users already branched out at Q8)
- **Google Forms notes:** Multiple choice. Required. Include "Annet" with short text.

---

## Section 6: Styring og organisatorisk støtte (RQ2)

*Section description:*
> I denne delen spør vi om hvordan organisasjonen din styrer og støtter bruken av KI-kodeverktøy. Svar basert på det du vet — det er helt greit å svare «vet ikke».

### Q12: Har organisasjonen din retningslinjer eller policy for bruk av KI-kodeverktøy?

- **English translation:** Does your organization have guidelines or a policy for the use of AI coding tools?
- **Type:** Single-select
- **Response options:**
  1. Ja, spesifikt for KI-kodeverktøy
  2. Ja, som del av en generell KI-policy
  3. Nei
  4. Vet ikke
- **RQ mapping:** RQ2 (Governance — policy existence; concrete indicator)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Social desirability — over-reporting policy existence. Mitigated: "vet ikke" option; high "vet ikke" rate is itself a governance invisibility signal. Cross-checked with Q12b confidence.
- **Analysis plan:** Proportions. "Vet ikke" rate reported as governance visibility metric. Cross-tabulation with adoption level (Q5) to test thesis: high adoption + no policy = governance gap.
- **Data type:** Nominal
- **Skip logic:** None
- **Google Forms notes:** Multiple choice. Required.

---

### Q12b: Hvor sikker er du på svaret over?

- **English translation:** How confident are you in the answer above?
- **Type:** Single-select — confidence indicator
- **Response options:**
  1. Jeg vet dette sikkert (f.eks. er involvert i beslutningen)
  2. Ganske sikker basert på det jeg har sett
  3. Dette er mitt beste estimat
- **RQ mapping:** RQ2 (Data quality weight for Q12)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** None identified — meta-question
- **Analysis plan:** Reported alongside Q12. Weight organizational claims by confidence level.
- **Data type:** Ordinal
- **Skip logic:** None
- **Google Forms notes:** Multiple choice. Required.

---

### Q13: Hvordan støtter organisasjonen din utviklere i bruk av KI-kodeverktøy?

- **English translation:** How does your organization support developers in using AI coding tools?
- **Type:** Single-select — behavioral anchor scale
- **Response options:**
  1. Ingen støtte eller opplæring
  2. Uformell kunnskapsdeling mellom utviklere
  3. Delte ressurser eller retningslinjer er tilgjengelige (f.eks. wiki, beste praksis)
  4. Organisert opplæring eller kurs
  5. Strukturert program (f.eks. champions-nettverk, dedikerte ressurspersoner, tilbakemeldingsrutiner)
  6. Vet ikke
- **RQ mapping:** RQ2 (Organizational readiness — support maturity; behavioral anchor)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Over-reporting of support level (social desirability, especially for leaders). Mitigated: behavioral anchors; cross-check with role (leaders may over-report vs. developers).
- **Analysis plan:** Frequency distribution; median support level. Cross-tabulation with adoption level (Q5) for governance-adoption lag analysis. Compare leader vs. developer responses for same org (inconsistency detection).
- **Data type:** Ordinal (5-point behavioral anchor + "vet ikke")
- **Skip logic:** None
- **Google Forms notes:** Multiple choice. Required.

---

### Q14: Hvordan avgjøres det hvilke KI-kodeverktøy utviklere kan bruke?

- **English translation:** How is it decided which AI coding tools developers can use?
- **Type:** Single-select
- **Response options:**
  1. Sentralt besluttet (f.eks. IT-avdelingen eller ledelsen velger for hele organisasjonen)
  2. Via en godkjenningsprosess (f.eks. risikovurdering/ROS, så kan team eller utviklere foreslå verktøy)
  3. Teamet eller tech lead bestemmer
  4. Hver enkelt utvikler bestemmer selv
  5. Ingen har eksplisitt bestemt dette
  6. Vet ikke
- **RQ mapping:** RQ2 (Governance — decision authority; platform team role sub-question)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Attribution bias — respondents may assume more centralization than exists. Mitigated: "ingen har eksplisitt bestemt" and "vet ikke" options normalize lack of governance. Option 2 captures governed-but-decentralized processes (e.g., ROS-based approval).
- **Analysis plan:** Frequency table. Options 1–2 indicate formal governance; options 3–4 indicate decentralized; option 5 indicates governance gap. Cross-tabulation with org size (Q3).
- **Data type:** Nominal
- **Skip logic:** None
- **Google Forms notes:** Multiple choice. Required.

---

### Q15: Har organisasjonen din avklart hvilke KI-leverandører som behandler kildekoden deres?

*Description text under question:*
> Når du bruker KI-kodeverktøy, sendes kildekode til en ekstern modell-leverandør (f.eks. OpenAI, Anthropic, Google) for behandling. Noen organisasjoner har avklart dette gjennom databehandleravtaler eller risikovurderinger.

- **English translation:** Has your organization clarified which AI providers process your source code? (When you use AI coding tools, source code is sent to an external model provider for processing. Some organizations have clarified this through data processing agreements or risk assessments.)
- **Type:** Single-select
- **Response options:**
  1. Ja, det er tydelig avklart
  2. Delvis — noe er avklart, men ikke for alle verktøy
  3. Nei
  4. Vet ikke
- **RQ mapping:** RQ2 (Governance — data sovereignty; concrete indicator)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Comprehension risk — "databehandleravtaler" may be unclear to developers. Mitigated: description text explains the concept in plain language. Over-reporting of clarity (social desirability, especially from leaders).
- **Analysis plan:** Proportions. "Vet ikke" + "nei" = data sovereignty gap metric. Cross-tabulation with adoption level (Q5) — high adoption + unresolved data sovereignty = governance risk signal.
- **Data type:** Ordinal
- **Skip logic:** None
- **Google Forms notes:** Multiple choice. Required.

---

### Q16: Hvordan vurderer organisasjonen din effekten av KI-kodeverktøy?

*Description text under question:*
> Velg det høyeste nivået som passer for organisasjonen din. Hvert nivå inkluderer de under.

- **English translation:** How does your organization assess the impact of AI coding tools? (Select the highest level that applies to your organization. Each level includes those below it.)
- **Type:** Single-select — behavioral anchor scale
- **Response options:**
  1. Vi vurderer ikke effekten
  2. Uformelle tilbakemeldinger og anekdoter
  3. Vi følger med på bruksdata fra verktøyleverandøren (f.eks. antall brukere, akseptrate)
  4. Vi måler effekten med egne metrikker (f.eks. leveransetakt, kvalitet, utvikleropplevelse)
  5. Vet ikke
- **RQ mapping:** RQ2 (Governance — measurement maturity; key cross-study contribution)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Social desirability — orgs may over-report measurement sophistication. Mitigated: behavioral anchors describe concrete activities. "Bruksdata fra verktøyleverandøren" (option 3) is a common but low-maturity measurement — separating it from "egne metrikker" (option 4) captures this distinction.
- **Analysis plan:** Frequency distribution. Cross-study parallel: compare with State of Platforms measurement maturity (49% Ad hoc). Cross-tabulation with adoption level (Q5). **Key metric** — no prior sector-level data exists on measurement maturity for AI coding tools.
- **Data type:** Ordinal (4-point behavioral anchor + "vet ikke")
- **Skip logic:** None
- **Google Forms notes:** Multiple choice. Required.

---

### Q17: Hvordan håndteres KI-generert kode i kodegjennomgang (code review)?

*Description text under question:*
> Med «KI-generert kode» mener vi all kode som er skrevet eller vesentlig endret med hjelp av KI-verktøy — både helt generert kode og kode der KI har foreslått endringer.

- **English translation:** How is AI-generated code handled in code review? (By "AI-generated code" we mean all code written or substantially modified with the help of AI tools — both fully generated code and code where AI has suggested changes.)
- **Type:** Single-select — cumulative behavioral anchor
- **Response options:**
  1. Ingen spesiell håndtering — KI-generert kode gjennomgås som all annen kode
  2. Vi har muntlige retningslinjer om å være ekstra oppmerksom på KI-generert kode
  3. Vi har skriftlige retningslinjer for gjennomgang av KI-generert kode
  4. Vi har skriftlige retningslinjer og bruker automatiserte verktøy for å sjekke KI-generert kode (f.eks. sikkerhetsskanning)
  5. Ikke aktuelt — vi bruker ikke KI-kodeverktøy eller har ikke kodegjennomgang
  6. Vet ikke
- **RQ mapping:** RQ2 (Governance — code review practices; security/quality indicator)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Social desirability — especially from leaders. Mitigated: option 1 is normalized (not framed negatively), behavioral anchors. Options are now cumulative (each level includes the previous) to ensure mutual exclusivity.
- **Analysis plan:** Frequency table. Cross-tabulation with concerns about code quality/security (Q18). Option 1 frequency is a key indicator — most orgs likely have no AI-specific review practices.
- **Data type:** Ordinal (4-point cumulative scale + N/A + don't know)
- **Skip logic:** None
- **Google Forms notes:** Multiple choice. Required.

---

## Section 7: Bekymringer og barrierer (RQ3)

*Section description:*
> Nå spør vi om dine personlige oppfatninger og bekymringer rundt KI-kodeverktøy.

### Q18: Hva er dine viktigste bekymringer knyttet til bruk av KI-kodeverktøy?

*Description text under question:*
> Velg de tre viktigste.

- **English translation:** What are your most important concerns related to the use of AI coding tools? (Select your top three.)
- **Type:** Multi-select (checkboxes) — max 3
- **Response options:**
  1. Sikkerhetssårbarheter i KI-generert kode
  2. Kodekvalitet og teknisk gjeld
  3. Personvern og datahåndtering (kildekode sendes til ekstern leverandør)
  4. Immaterielle rettigheter og lisenser (hvem eier KI-generert kode?)
  5. Tap av kompetanse eller ferdigheter over tid
  6. Kostnad i forhold til nytte
  7. Feil og hallusinasjoner (KI-verktøyet genererer kode som ser riktig ut men er feil)
  8. Arbeidsflyt (verktøyet forstyrrer mer enn det hjelper)
  9. Jeg har ingen vesentlige bekymringer
  10. Andre (spesifiser)
- **RQ mapping:** RQ3 (Barriers — concern identification)
- **Longitudinal status:** New (Wave 1). Concern list derived from literature (Stack Overflow 2025, DORA 2025, GitClear 2025, Aikido 2026).
- **Wording change from previous wave:** N/A
- **Bias risks:** Anchoring — items listed first may be over-selected. Mitigated: shuffle enabled; "Ingen bekymringer" participates in shuffle but is visually distinct from concern items. Priming — listing concerns may create concerns. Mitigated: forced top-3 selection limits indiscriminate checking.
- **Analysis plan:** Mention rates (% of respondents citing each concern, base = all respondents). Top-3 ranking. Cross-tabulation with role (Q2) to test whether concerns vary by role. Fisher's exact test for role-concern associations.
- **Data type:** Nominal (multi-select)
- **Skip logic:** None
- **Google Forms notes:** Checkboxes. Required. Google Forms checkbox validation: "Select at most 3". Enable "Shuffle option order". Use built-in "Annet" (Other) — stays pinned at bottom. "Jeg har ingen vesentlige bekymringer" will be shuffled with concern items (no item-level pinning).

---

### Q19: Har du spesifikke bekymringer knyttet til offentlig sektor?

*Description text under question:*
> For eksempel knyttet til regelverk, innsynskrav, anskaffelsesregler, eller andre forhold som er spesielle for offentlig sektor.

- **English translation:** Do you have specific concerns related to the public sector? (For example related to regulations, freedom of information requirements, procurement rules, or other conditions specific to the public sector.)
- **Type:** Paragraph text (open)
- **Response options:** Free text
- **RQ mapping:** RQ3 (Barriers — public sector-specific concerns; exploratory)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Non-response — open text fields have low response rates; framing with examples helps. Leading — examples may prime specific concerns. Mitigated: examples are broad categories, not specific positions.
- **Analysis plan:** Qualitative coding (thematic analysis). Report themes with representative quotes. Budget ~2 hours for coding. Expected themes: offentlighetsloven (FOIA), anskaffelsesregelverket, Schrems II/data residency.
- **Data type:** Free text
- **Skip logic:** None
- **Google Forms notes:** Paragraph text. Optional (not required — open text should never be required).

---

### Q20: Hvordan forholder du deg til KI-generert kode?

- **English translation:** How do you relate to AI-generated code?
- **Type:** Single-select — behavioral anchor (trust scale)
- **Response options:**
  1. Jeg godtar aldri KI-forslag uten å gjennomgå og forstå koden
  2. Jeg gjennomgår det meste, men godtar enkle forslag uten grundig sjekk
  3. Jeg godtar ofte KI-forslag etter en rask sjekk
  4. Jeg godtar som regel KI-forslag som ser riktige ut
  5. Ikke aktuelt — jeg bruker ikke KI-kodeverktøy
- **RQ mapping:** RQ3 (Barriers — trust; behavioral indicator rather than abstract judgment)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Social desirability — respondents may over-report diligence (options 1–2). Self-report inflation of review thoroughness. Mitigated: behavioral anchors are concrete and incremental; each option is plausible and non-judgmental.
- **Analysis plan:** Frequency distribution. Cross-tabulation with role (Q2) — do more experienced developers accept more readily (METR finding) or less? Cross-tabulation with concerns (Q18) — do people who worry about quality also review more? Median trust level by role.
- **Data type:** Ordinal
- **Skip logic:** None
- **Google Forms notes:** Multiple choice. Required.

---

### Q21: Er det et gap mellom hva organisasjonen din tillater og hva du mener er forsvarlig?

- **English translation:** Is there a gap between what your organization allows and what you consider responsible?
- **Type:** Single-select
- **Response options:**
  1. Organisasjonen er for restriktiv — vi burde bruke KI-verktøy mer
  2. Organisasjonens tilnærming samsvarer med det jeg mener er forsvarlig
  3. Organisasjonen er for liberal — vi burde ha strengere retningslinjer
  4. Organisasjonen har ingen tydelig tilnærming, så det er vanskelig å si
  5. Vet ikke / har ingen mening
- **RQ mapping:** RQ3 (Barriers — perception gap; governance satisfaction indicator)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Framing — "gap" in question text may suggest there should be one. Mitigated: options include "samsvarer" (no gap) and "vet ikke." Question asks for direction of gap, not just existence.
- **Analysis plan:** Frequency distribution. Option 1 vs. 3 reveals tension direction (too restrictive vs. too liberal). Option 4 is a governance invisibility indicator. Cross-tabulation with role (Q2) — do leaders and developers agree?
- **Data type:** Nominal
- **Skip logic:** None
- **Google Forms notes:** Multiple choice. Required.

---

## Section 8: Oppfølging

*Section description:*
> Til slutt — vi planlegger oppfølgingsintervjuer med et lite utvalg deltakere for å utdype funnene. Deltakelse er frivillig og separat fra denne undersøkelsen.

### Q23: Kan vi kontakte deg for et kort oppfølgingsintervju (ca. 30 min, digitalt)?

- **English translation:** May we contact you for a brief follow-up interview (approx. 30 min, digital)?
- **Type:** Single-select
- **Response options:**
  1. Ja
  2. Nei
- **RQ mapping:** Follow-up recruitment (not part of analysis)
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Self-selection — interview volunteers may be more enthusiastic adopters. Documented as a limitation.
- **Analysis plan:** Not analyzed as survey data. Used for purposive selection of interview participants (5 interviews per methodology).
- **Data type:** Nominal
- **Skip logic:** "Ja" → go to Section 9 (kontaktinformasjon); "Nei" → go to Section 10 (takk/slutt)
- **Google Forms notes:** Multiple choice. Required. Branching: "Ja" goes to Section 9, "Nei" goes to Section 10.

---

## Section 9: Kontaktinformasjon for intervju

*Only shown to respondents who answered "Ja" on Q23.*

### Q24: Oppgi e-postadresse for oppfølging

*Description text under question:*
> E-postadressen kobles ikke til dine svar i undersøkelsen. Den brukes kun til å ta kontakt om intervju.

- **English translation:** Provide email address for follow-up. (The email address will not be linked to your survey responses. It is only used to contact you about an interview.)
- **Type:** Short text
- **Response options:** Free text (email)
- **RQ mapping:** Follow-up recruitment
- **Longitudinal status:** New (Wave 1)
- **Wording change from previous wave:** N/A
- **Bias risks:** Privacy concern may deter participation. Mitigated: explicit statement that email is not linked to responses.
- **Analysis plan:** Not analyzed. Contact list stored separately from survey data.
- **Data type:** Free text (email)
- **Skip logic:** None (only reached via Section 8 branch)
- **Google Forms notes:** Short answer with email validation. Optional. This is Section 9 — only shown to respondents who answered "Ja" on Q23.

---

## Section 10: Takk for din deltakelse

*Google Forms: Confirmation page / final section.*

> Takk for at du tok deg tid til å svare! Resultatene vil bli publisert som en del av en forskningsstudie fra Offentlig PAAS.
>
> Har du spørsmål, kontakt oss på [kontakt-e-post].

---

## Question Budget Summary

| Category                        | Questions                          | Count                            |
| ------------------------------- | ---------------------------------- | -------------------------------- |
| Demographics + screening        | Q1–Q3                              | 3                                |
| RQ1 — Adoption (organizational) | Q5, Q5b, Q6, Q6b, Q7               | 5 (3 substantive + 2 confidence) |
| RQ1 — Adoption (individual)     | Q8, Q8b, Q9, Q10, Q11, Q11b        | 6 (5 substantive + Q11b benefit) |
| RQ2 — Governance                | Q12, Q12b, Q13, Q14, Q15, Q16, Q17 | 7 (6 substantive + 1 confidence) |
| RQ3 — Barriers & concerns       | Q18, Q19, Q20, Q21                 | 4                                |
| Follow-up                       | Q23, Q24                           | 2                                |
| **Total substantive**           | Q5–Q21 (excl. Q5b, Q6b, Q12b)      | **18**                           |
| **Total with confidence**       | Q5–Q21                             | **21**                           |
| **Grand total**                 | Q1–Q24                             | **27**                           |

Within the 20-question budget (18 substantive + 3 confidence indicators + Q11b benefit). Estimated completion time: 10–12 minutes.

---

## Respondent Qualification Matrix

This table documents which roles are most qualified for each question type. Used in analysis for quality weighting, not shown to respondents.

| Role                 | RQ1-org (Q5–Q7) | RQ1-individual (Q8–Q11b) | RQ2 (Q12–Q17) | RQ3 (Q18–Q21) |
| -------------------- | :-------------: | :----------------------: | :-----------: | :-----------: |
| CTO / IT-leder       |       ★★★       |            ★★            |      ★★★      |      ★★       |
| Tech lead / arkitekt |       ★★★       |           ★★★            |      ★★★      |      ★★★      |
| Plattformteamleder   |       ★★★       |           ★★★            |      ★★★      |      ★★★      |
| Teamleder            |       ★★        |            ★★            |      ★★       |      ★★       |
| Utvikler / ingeniør  |        ★        |           ★★★            |       ★       |      ★★★      |
| Leder (ikke-teknisk) |       ★★        |            ★             |      ★★       |       ★       |

★★★ = high qualification, ★★ = medium, ★ = low (answers included but lower analytical weight for organizational questions)

---

## Triangulation Map

How multiple questions cross-validate key signals:

| Signal                | Primary question                            | Cross-check questions                                                    |
| --------------------- | ------------------------------------------- | ------------------------------------------------------------------------ |
| Formal adoption level | Q5 (behavioral anchor)                      | Q6 (can they name tools?), Q7 (procurement path), Q11 (usage frequency)  |
| Shadow adoption       | Gap between Q6 (official) and Q8 (personal) | Q7 option 3 ("enkeltpersoner begynte"), Q14 options 4–5 (no one decides) |
| Governance readiness  | Q12 (policy existence)                      | Q14 (who decides), Q15 (data sovereignty), Q13 (support level)           |
| Measurement maturity  | Q16 (assessment approach)                   | Cross-study: State of Platforms measurement maturity                     |
| Trust level           | Q20 (behavioral trust)                      | Q18 (concerns), Q11b (perceived benefits)                                |
| Governance gap        | Q5 vs. Q12/Q16 composite                    | Q21 (perceived gap), Q7 vs. Q14 consistency                              |

---

## CERSE Self-Assessment

Based on Molléri, Petersen & Mendes (2016, 2020) — 26 criteria for survey quality in empirical software engineering.

| #   | Criterion                                | Status | Notes                                                                                                                                                                                                               |
| --- | ---------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Objectives clearly stated                | ✅      | Three RQs with explicit thesis. Research brief documents rationale.                                                                                                                                                 |
| 2   | Target population defined                | ✅      | Developers and technical leaders in Norwegian public sector organizations.                                                                                                                                          |
| 3   | Sampling frame specified                 | ✅      | Offentlig PAAS community (84 member orgs) + broader Norwegian public sector IT networks.                                                                                                                            |
| 4   | Sampling method documented               | ✅      | Convenience sample (community-based). Documented as limitation.                                                                                                                                                     |
| 5   | Sample size justified                    | ⚠️      | Expected n=40–60. Small sample acknowledged — affects statistical power. Fisher's exact test appropriate for 2×2 tables.                                                                                            |
| 6   | Response rate plan                       | ✅      | Previous study achieved ~50–60%. Response tracking protocol included.                                                                                                                                               |
| 7   | Unit of analysis specified               | ✅      | Hybrid: organization (RQ1-org, RQ2) + individual (RQ1-individual, RQ3).                                                                                                                                             |
| 8   | Questions map to objectives              | ✅      | Every question has explicit RQ mapping in metadata. No unmapped questions.                                                                                                                                          |
| 9   | Question types appropriate               | ✅      | Behavioral anchors for ordinal, checkboxes for multi-select, forced-choice over Likert.                                                                                                                             |
| 10  | Response options exhaustive              | ✅      | All closed questions include "Vet ikke" / "Ikke aktuelt" / "Andre (spesifiser)" as appropriate.                                                                                                                     |
| 11  | Response options mutually exclusive      | ✅      | Single-select questions verified for mutual exclusivity. Multi-select questions are intentionally non-exclusive.                                                                                                    |
| 12  | No double-barreled questions             | ✅      | Each question asks exactly one thing. Verified against checklist.                                                                                                                                                   |
| 13  | No leading questions                     | ✅      | Neutral framing throughout. Behavioral anchors describe states, not judgments.                                                                                                                                      |
| 14  | No negations                             | ✅      | All questions phrased positively.                                                                                                                                                                                   |
| 15  | Pilot testing planned                    | ✅      | Cognitive interview protocol with n=5–8 participants. Expert review checklist included.                                                                                                                             |
| 16  | Instrument documented                    | ✅      | Full metadata per question: type, options, RQ mapping, bias risks, analysis plan.                                                                                                                                   |
| 17  | Data collection method specified         | ✅      | Google Forms, online, self-administered.                                                                                                                                                                            |
| 18  | Survey language appropriate              | ✅      | Norwegian (bokmål). Plain language. Technical terms defined in question descriptions.                                                                                                                               |
| 19  | Anonymity/confidentiality addressed      | ✅      | Stated in introduction. Interview opt-in separated from survey responses.                                                                                                                                           |
| 20  | Estimated completion time                | ✅      | 10–12 minutes. Within 15-minute fatigue threshold.                                                                                                                                                                  |
| 21  | Analysis plan specified                  | ✅      | Per-question analysis plans. Fisher's exact test for small samples. Qualitative coding for open text.                                                                                                               |
| 22  | Statistical tests appropriate for sample | ✅      | Fisher's exact test (not chi-square) for small n. Ordinal data analyzed with median/mode, not mean.                                                                                                                 |
| 23  | Validity threats documented              | ✅      | Bias risks per question. Convenience sample limitation. Self-report inflation risk.                                                                                                                                 |
| 24  | Reliability measures                     | ⚠️      | Confidence indicators on Q5, Q6, Q12 provide partial reliability signal (3 of 7 organizational questions). Test-retest not feasible for Wave 1. Cross-respondent agreement within orgs serves as inter-rater check. |
| 25  | Ethics/consent addressed                 | ✅      | Consent in introduction. Voluntary participation. Right to withdraw.                                                                                                                                                |
| 26  | Reporting plan                           | ✅      | Frequencies, cross-tabulations, Fisher's exact. Triangulation map documents cross-validation.                                                                                                                       |

**Score: 24/26 fully met, 2/26 partially met (items 5 and 24).** Both are expected in a small-sample Wave 1 study and documented as limitations.

---

## Pilot Protocol

### Cognitive Interview Guide

- **Participants:** 5–8 individuals from the target population (mix of developers, tech leads, and leaders from different organization sizes). Recruit from community contacts not expected to be in the main survey sample.
- **Method:** Think-aloud protocol (Willis, 2004). Respondent completes the survey while verbalizing their thought process. Interviewer probes specific questions.
- **Format:** Digital (video call), 30–40 minutes per session. Screen sharing while completing the Google Forms draft.
- **Timing:** Record each participant's completion time. If median exceeds 12 minutes, simplify or cut questions.
- **Timeline:** 1–2 weeks before survey launch.

#### Focus questions / probe targets

| Question               | Probe focus                                                                                                                       |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Q5 (adoption level)    | Can respondent distinguish between options 2, 3, and 4? Is the boundary between "noen team" and "offisielt godkjent" clear?       |
| Q6 (official tools)    | Does respondent know which tools are officially approved? Does the tool list feel complete? Are any tools missing?                |
| Q9 (usage modes)       | Does respondent understand "agentmodus"? Is the description in parentheses sufficient?                                            |
| Q10 (integrations/MCP) | Is this question comprehensible to non-expert respondents? Does the description text help? Would developers know if they use MCP? |
| Q12 (policy)           | Can respondent distinguish between "spesifikt for KI-kodeverktøy" and "del av generell KI-policy"?                                |
| Q15 (data sovereignty) | Is the concept clear? Does the description text help? Is "databehandleravtaler" jargon that needs simplification?                 |
| Q16 (measurement)      | Can respondent distinguish between vendor dashboards (option 3) and own metrics (option 4)?                                       |
| Q18 (concerns)         | Is the top-3 constraint workable? Are any concerns missing from the list?                                                         |
| Q21 (perception gap)   | Is the question clear? Do respondents understand "forsvarlig" in this context?                                                    |

#### General probes (all questions)

- "Can you tell me what this question is asking in your own words?"
- "How did you arrive at your answer?"
- "Was there anything confusing about this question?"
- "Did you feel any options were missing?"

#### Post-pilot actions

1. Revise questions where ≥2 participants had comprehension difficulties
2. Add/remove response options based on "missing option" feedback
3. Re-pilot any substantially revised questions with 2–3 participants
4. Document all changes with rationale

### Expert Review Checklist

- [ ] Domain expert 1 (public sector IT leader) reviewed — focus on RQ2 questions, organizational-level validity
- [ ] Domain expert 2 (developer in target population) reviewed — focus on RQ1-individual and RQ3 questions, technical terminology
- [ ] Domain expert 3 (survey methodology expert) reviewed — focus on question design, scale construction, bias risks
- [ ] All feedback incorporated or documented as rejected with rationale
- [ ] Norwegian language review — grammar, spelling, natural phrasing, reading level verification

---

## Sampling Protocol

- **Target population definition:** All developers and technical leaders working in Norwegian public sector organizations (directorates, agencies, municipalities, state enterprises, health trusts) who are involved in or have knowledge of software development practices.
- **Sampling frame:** Offentlig PAAS community mailing list / Slack (84 member organizations as of April 2026). Secondary: broader Norwegian public sector IT networks and contacts from the State of Platforms study.
- **Sampling method:** Convenience sample (non-probabilistic). Consistent with State of Platforms methodology.
- **Known coverage gaps:**
  - Municipalities under-represented (community skews toward large directorates and agencies)
  - Organizations without platform teams may be under-represented (community self-selects for platform-oriented orgs)
  - Non-members of the Offentlig PAAS community are not reachable through primary distribution channel
  - Individual developers without leadership endorsement may not see the survey
- **Expected response rate:** 50–60% based on State of Platforms experience (35/~60 in 2024, 48/84 in 2026). Target: ≥40 responding organizations.
- **Multiple respondents per organization:** Allowed and encouraged — enables RQ2 cross-validation (inconsistency detection). De-duplication rules documented for organizational-level analysis (mode/majority for factual questions; each respondent kept as individual data point for RQ3).
- **Response tracking plan:**
  - Track invitations sent (organizations contacted, individuals if available)
  - Track responses received (total, unique organizations)
  - Track completion rate (started vs. completed, using Google Forms timestamp)
  - Track time-to-complete (Google Forms captures start/end timestamp)
  - Non-response follow-up: one reminder email 7–10 days after initial distribution
  - Report: response rate = completed responses / estimated reachable population

### Linking to State of Platforms

- **Linking variable:** Q1 (organization name) — same as State of Platforms
- **Cross-study analysis:** For organizations appearing in both studies, compare platform maturity with AI adoption and governance. Possible because both studies share the same respondent pool.
- **Privacy note:** Cross-study linking uses organization (not individual) as the join key. No individual-level linking is performed.

---

## Diff from Previous Wave

N/A — this is Wave 1. All questions are new.

| Question     | Change | Justification                          |
| ------------ | ------ | -------------------------------------- |
| All (Q1–Q24) | New    | Wave 1 — no previous instrument exists |

---

## Design Notes for Future Waves

The following design choices were made with longitudinal reuse in mind:

1. **Q5 (adoption level)** — behavioral anchors were designed as a stable ordinal scale. Do not modify wording in Wave 2; if the adoption landscape changes (e.g., agentic becomes default), add new options at the end.
2. **Q6 and Q8 (tool lists)** — tool markets evolve rapidly. In Wave 2, add new tools at the end of the list; do not remove tools that appeared in Wave 1. Retired tools with zero usage can be moved to an "Other" category.
3. **Q9 (usage modes)** — as agentic features become mainstream, consider splitting "agentmodus" into sub-modes in Wave 2 (with a bridging strategy).
4. **Q10 (integrations/MCP)** — explicitly exploratory. Expect to redesign in Wave 2 based on Wave 1 responses and market evolution. Include both old and new formulation in Wave 2 (bridging).
5. **Q16 (measurement)** — cross-study anchor. Keep identical across waves for trend comparison.
6. **Confidence indicators (Q5b, Q12b)** — keep identical. These are structural elements of the measurement approach.
7. **Q18 (concerns list)** — concern list may need updating. Add new concerns at the end; do not remove items from Wave 1.
