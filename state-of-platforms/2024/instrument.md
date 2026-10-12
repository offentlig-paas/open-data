# Survey Instrument: State of Platforms

## Instrument Metadata

- **Study:** State of Platform Maturity in the Norwegian Public Sector
- **Waves:** Wave 1 (Q4 2023), Wave 2 (Q4 2025 – Q1 2026)
- **Target population:** Platform team members and IT leaders in Norwegian public sector organizations
- **Distribution method:** Online survey (Google Forms) via Offentlig PAAS Slack + LinkedIn
- **Language:** Norwegian (bokmål)
- **Estimated completion time:** 10–15 minutes
- **Total questions:** 31 substantive + metadata (timestamp, contact)
- **Instrument changes between waves:** Q19 (own Kubernetes operators) and Q20 (databases in Kubernetes) were added in wave 2 and not asked in wave 1 (2023)
- **Platform:** Google Forms
- **Unit of analysis:** Organization (one response per platform initiative, duplicates merged)

---

## Introduksjon og samtykke

### Faktisk tekst brukt i bølge 1 (2023) og bølge 2 (2025–2026)

_Følgende ingress ble presentert for respondentene i Google Forms:_

> Oppfølging fra undersøkelsen i 2023 om adopsjon av applikasjonsplattformer i Offentlig sektor i regi av Offentlig PaaS. Aggregerte resultater vil bli publisert på Offentlig PaaS Slacken og offentlig-paas.no.
>
> Alle spørsmål besvares i lys av applikasjonsplattformen for din aktuelle organisasjon og tar ca 10 minutter å fullføre.
>
> For mer informasjon om undersøkelsen ta kontakt med kontakt@offentlig-paas.no

_Organisasjonsnavn (Q1) var påkrevd utelukkende for duplikatdeteksjon. E-post var frivillig for oppfølgende kontakt._


## Survey Structure

The survey is organized into **three categories** with questions progressing from general platform engineering to Kubernetes-specific and cloud-specific topics.

```
Category 1: General Platform Engineering (Q1–Q13)
  Demographics, platform existence, motivations, services, scale, languages, CNCF maturity
Category 2: Kubernetes (Q14–Q20)
  Adoption, distributions, tenure, clusters, apps, operators, databases
Category 3: Cloud (Q21–Q31)
  Cloud usage, providers, multi-cloud, tenure, serverless, monitoring, packaging, deploy, security, IaC
```

---

## Category 1: General Platform Engineering

### Q1: Organisasjon

- **English translation:** Organization
- **Type:** Short text (open)
- **RQ mapping:** Demographics (linking variable, duplicate detection)
- **Analysis plan:** Organization-level grouping; duplicate detection and merging

---

### Q2: Type

- **English translation:** Type [of organization]
- **Type:** Single-select
- **Response options:** Statlig (State), Kommunal (Municipal), Akademisk (Academic), Statlig eid (State-owned)
- **RQ mapping:** Demographics

---

### Q3: Type organisasjon

- **English translation:** Type of organization
- **Type:** Single-select
- **RQ mapping:** Demographics (organizational classification)

---

### Q4: Ansatte

- **English translation:** Employees
- **Type:** Numeric / range
- **RQ mapping:** Demographics (organizational scale)

---

### Q5: Budsjett (MNOK)

- **English translation:** Budget (million NOK)
- **Type:** Numeric
- **RQ mapping:** Demographics (organizational scale)

---

### Q6: Hva er din primærrolle?

- **English translation:** What is your primary role?
- **Type:** Single-select
- **RQ mapping:** Demographics (used in duplicate merge: technical roles prioritized)
- **Merge rule:** Technical roles > management > consultants

---

### Q7: Har dere en applikasjonsplattform?

- **English translation:** Do you have an application platform?
- **Type:** Yes/No
- **RQ mapping:** RQ1 (Adoption)
- **Analysis plan:** Adoption rate (% yes); cross-wave comparison

---

### Q8: Har plattformen deres et navn?

- **English translation:** Does your platform have a name?
- **Type:** Short text (open)
- **RQ mapping:** RQ1 (Adoption — platform identity/branding signal)

---

### Q9: Hvorfor lager dere plattform?

- **English translation:** Why are you building a platform?
- **Type:** Multi-select (checkboxes)
- **Response options:**
  - Raskere applikasjonsutvikling (Faster application development)
  - Stabilitet og kvalitet (Stability and quality)
  - Sikkerhet (Security)
  - Ressursoptimalisering (Resource optimization)
  - Kostoptimalisering (Cost optimization)
  - Være attraktiv arbeidsplass (Being an attractive workplace)
  - Støtte flere teknologier (Support multiple technologies)
- **RQ mapping:** RQ2 (Motivations)
- **Analysis plan:** Frequency per option; cross-wave delta; Fisher's exact test per motivation

---

### Q10: Hvilke selvbetjente tjenester består plattformen deres av?

- **English translation:** What self-service capabilities does your platform consist of?
- **Type:** Multi-select (checkboxes)
- **RQ mapping:** RQ1 (Adoption — platform scope)

---

### Q11: Ca. hvor mange applikasjonsteam benytter seg av plattformen deres i dag?

- **English translation:** Approximately how many application teams use your platform today?
- **Type:** Single-select (ranges)
- **Response options:** 0–5, 6–10, 11–50, 51–100, 100+
- **RQ mapping:** RQ1 (Scale)
- **Analysis plan:** Distribution by range; cross-wave shift toward larger platforms

---

### Q12: Topp tre programmeringsspråk for applikasjoner?

- **English translation:** Top three programming languages for applications?
- **Type:** Multi-select (checkboxes)
- **Response options:** Java, Kotlin, Python, TypeScript, JavaScript, .NET, Go, Rust, and others
- **RQ mapping:** RQ4 (Technology)
- **Analysis plan:** Share of total mentions; cross-wave trend

---

### Q13a: Hvordan allokeres ansatte og midler til plattformfunksjoner

- **English translation:** How are staff and funding allocated to platform capabilities?
- **Type:** Single-select (ordinal)
- **CNCF Maturity aspect:** Investment
- **Maturity levels:** L1 (Voluntary) → L2 (Dedicated team) → L3 (Product team) → L4 (Enabled ecosystem)
- **RQ mapping:** RQ3 (Maturity — Investment)

---

### Q13b: Hvordan oppdager brukere interne plattformer og plattformfunksjonalitet?

- **English translation:** How do users discover internal platforms and platform capabilities?
- **Type:** Single-select (ordinal)
- **CNCF Maturity aspect:** Adoption
- **Maturity levels:** L1 (Erratic) → L2 (Extrinsic mandate) → L3 (Intrinsic pull) → L4 (Participatory)
- **RQ mapping:** RQ3 (Maturity — Adoption)

---

### Q13c: Hvordan benytter brukere plattformfunksjonalitet?

- **English translation:** How do users consume platform capabilities?
- **Type:** Single-select (ordinal)
- **CNCF Maturity aspect:** Interfaces
- **Maturity levels:** L1 (Manual/custom) → L2 (Standard paved roads) → L3 (Self-service) → L4 (Integrated workflows)
- **RQ mapping:** RQ3 (Maturity — Interfaces)

---

### Q13d: Hvordan planlegges, prioriteres, utvikles og vedlikeholdes plattformer og deres funksjonalitet?

- **English translation:** How are platforms planned, prioritized, developed, and maintained?
- **Type:** Single-select (ordinal)
- **CNCF Maturity aspect:** Operations
- **Maturity levels:** L1 (By-request) → L2 (Centrally tracked) → L3 (Centrally enabled) → L4 (Fully managed)
- **RQ mapping:** RQ3 (Maturity — Operations)

---

### Q13e: Hva er prosessen for å samle inn og lære av tilbakemeldinger?

- **English translation:** What is the process for gathering and learning from feedback?
- **Type:** Single-select (ordinal)
- **CNCF Maturity aspect:** Measurement
- **Maturity levels:** L1 (Ad hoc) → L2 (Consistent metrics) → L3 (Strategic insights) → L4 (Continuous improvement)
- **RQ mapping:** RQ3 (Maturity — Measurement)

---

## Category 2: Kubernetes

### Q14: Bruker dere Kubernetes?

- **English translation:** Do you use Kubernetes?
- **Type:** Yes/No
- **RQ mapping:** RQ4 (Technology)
- **Analysis plan:** Adoption rate; cross-wave comparison

---

### Q15: Hvilke Kubernetes distribusjoner bruker dere?

- **English translation:** Which Kubernetes distributions do you use?
- **Type:** Multi-select (checkboxes)
- **RQ mapping:** RQ4 (Technology — K8s landscape)
- **Analysis plan:** Managed (AKS/GKE/EKS) vs. self-managed vs. packaged (OpenShift)

---

### Q16: Hvor mange år har dere kjørt Kubernetes i produksjon?

- **English translation:** How many years have you run Kubernetes in production?
- **Type:** Single-select (ranges)
- **RQ mapping:** RQ4 (Technology — tenure)

---

### Q17: Hvor mange Kubernetes clustere har dere?

- **English translation:** How many Kubernetes clusters do you have?
- **Type:** Single-select (ranges)
- **RQ mapping:** RQ1 (Scale)

---

### Q18: Hvor mange applikasjoner i produksjon har dere på Kubernetes?

- **English translation:** How many production applications do you have on Kubernetes?
- **Type:** Single-select (ranges)
- **RQ mapping:** RQ1 (Scale)

---

### Q19: Utvikler dere egne Kubernetes operators?

- **English translation:** Do you develop your own Kubernetes operators?
- **Type:** Yes/No
- **RQ mapping:** RQ4 (Technology — custom extension)

---

### Q20: Kjører dere databaser i Kubernetes?

- **English translation:** Do you run databases in Kubernetes?
- **Type:** Yes/No
- **RQ mapping:** RQ4 (Technology — workload maturity)

---

## Category 3: Cloud

### Q21: Bruker dere sky for plattformen deres?

- **English translation:** Do you use cloud for your platform?
- **Type:** Yes/No
- **RQ mapping:** RQ4 (Technology)

---

### Q22: Hva er deres primære sky for applikasjoner?

- **English translation:** What is your primary cloud for applications?
- **Type:** Single-select
- **RQ mapping:** RQ4 (Technology — cloud provider landscape)

---

### Q23: Brukere dere flere sky-leverandører?

- **English translation:** Do you use multiple cloud providers?
- **Type:** Yes/No
- **RQ mapping:** RQ4 (Technology — multi-cloud)

---

### Q24: Hvor mange år har dere kjørt applikasjoner i sky?

- **English translation:** How many years have you run applications in the cloud?
- **Type:** Single-select (ranges)
- **RQ mapping:** RQ4 (Technology — cloud tenure)

---

### Q25: Benytter dere serverless funksjoner?

- **English translation:** Do you use serverless functions?
- **Type:** Yes/No
- **RQ mapping:** RQ4 (Technology)

---

### Q26: Hva bruker dere for overvåking av applikasjoner?

- **English translation:** What do you use for application monitoring?
- **Type:** Multi-select (checkboxes)
- **RQ mapping:** RQ4 (Technology — observability toolchain)

---

### Q27: Hva bruker dere for pakking av applikasjoner?

- **English translation:** What do you use for packaging applications?
- **Type:** Multi-select (checkboxes)
- **RQ mapping:** RQ4 (Technology — packaging/build)

---

### Q28: Hva bruker dere for deploy av applikasjoner?

- **English translation:** What do you use for deploying applications?
- **Type:** Multi-select (checkboxes)
- **RQ mapping:** RQ4 (Technology — CI/CD)

---

### Q29: Hva bruker dere for nettverksikkerhet?

- **English translation:** What do you use for network security?
- **Type:** Multi-select (checkboxes)
- **RQ mapping:** RQ4 (Technology — security toolchain)

---

### Q30: Hva bruker dere for applikasjonsikkerhet?

- **English translation:** What do you use for application security?
- **Type:** Multi-select (checkboxes)
- **RQ mapping:** RQ4 (Technology — security toolchain)

---

### Q31: Hva bruker dere for infrastruktur-automatisering?

- **English translation:** What do you use for infrastructure automation?
- **Type:** Multi-select (checkboxes)
- **RQ mapping:** RQ4 (Technology — IaC)
- **Analysis plan:** Terraform dominance; cross-wave comparison
