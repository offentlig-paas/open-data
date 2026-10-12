#!/usr/bin/env python3
"""Analyze State of the Platforms survey responses.

Both CSV files share a common column schema (produced by align_csvs.py).
Detects survey year from filename.

Usage:
    python3 analyze.py <csv-file> ...
    python3 analyze.py *.csv
"""

import csv
import sys
from collections import Counter
from math import comb
from pathlib import Path


# --- Column names (common schema from align_csvs.py) ---
COL_ORG = "Organisasjon"
COL_TYPE = "Type"
COL_TYPE_DETAIL = "Type organisasjon"
COL_EMPLOYEES = "Ansatte"
COL_BUDGET = "Budsjett (MNOK)"
COL_ROLE = "Hva er din primærrolle?"
COL_HAS_PLATFORM = "Har dere en applikasjonsplattform?"
COL_PLATFORM_NAME = "Har plattformen deres et navn?"
COL_MOTIVATION = "Hvorfor lager dere plattform?"
COL_TEAMS = "Ca. hvor mange applikasjonsteam benytter seg av plattformen deres i dag?"
COL_LANGUAGES = "Topp tre programmeringsspråk for applikasjoner?"
COL_K8S = "Bruker dere Kubernetes?"
COL_K8S_DISTRO = "Hvilke Kubernetes distribusjoner bruker dere?"
COL_K8S_YEARS = "Hvor mange år har dere kjørt Kubernetes i produksjon?"
COL_K8S_CLUSTERS = "Hvor mange Kubernetes clustere har dere?"
COL_K8S_APPS = "Hvor mange applikasjoner i produksjon har dere på Kubernetes?"
COL_OPERATORS = "Utvikler dere egne Kubernetes operators?"
COL_DATABASES = "Kjører dere databaser i Kubernetes?"
COL_PRIMARY_CLOUD = "Hva er deres primære sky for applikasjoner?"
COL_CLOUD_YEARS = "Hvor mange år har dere kjørt applikasjoner i sky?"
COL_SERVERLESS = "Benytter dere serverless funksjoner?"

MATURITY_COLS = [
    ("Investment", "Hvordan allokeres ansatte og midler til plattformfunksjoner"),
    ("Adoption", "Hvordan oppdager brukere interne plattformer og plattformfunksjonalitet?"),
    ("Interfaces", "Hvordan benytter brukere plattformfunksjonalitet?"),
    ("Operations", "Hvordan planlegges, prioriteres, utvikles og vedlikeholdes plattformer og deres funksjonalitet?"),
    ("Measurement", "Hva er prosessen for å samle inn og lære av tilbakemeldinger?"),
]

TOOLING_COLS = [
    ("Monitoring", "Hva bruker dere for overvåking av applikasjoner?"),
    ("Packaging", "Hva bruker dere for pakking av applikasjoner?"),
    ("Deployment", "Hva bruker dere for deploy av applikasjoner?"),
    ("Network Security", "Hva bruker dere for nettverksikkerhet?"),
    ("App Security", "Hva bruker dere for applikasjonsikkerhet?"),
    ("IaC", "Hva bruker dere for infrastruktur-automatisering?"),
]

KNOWN_MOTIVATIONS = [
    "Raskere applikasjonsutvikling",
    "Stabilitet og kvalitet",
    "Sikkehet",
    "Resursoptimlaisering",
    "Kostoptimalisering",
    "Være attraktiv arbeidsplass for utviklere",
    "Støtte flere teknolgier",
    "Noen ville ha en plattform",
    "Alle andre har en plattform!",
]

TEAM_ORDER = ["0-5", "6-10", "11-50", "51-100", "Mer enn 100"]
APP_ORDER = ["0-100", "100-500", "500-1000", "1000-2000", "2000+"]
CLUSTER_ORDER = ["1-5", "6-10", "10-19", "20-50", "Mer enn 10"]


# --- Loading ---

def load_csv(path: str) -> tuple[str, list[dict]]:
    """Load aligned CSV, detect year from filename."""
    with open(path, newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r.get(COL_ORG, "").strip()]
    p = path.lower()
    year = "2024" if "2024" in p else "2026" if "2026" in p else "unknown"
    return year, rows


def val(row: dict, col: str) -> str:
    return row.get(col, "").strip()


# --- Analysis functions ---

def flatten(rows: list[dict], col: str) -> Counter:
    counts: Counter = Counter()
    for r in rows:
        v = val(r, col)
        if not v:
            continue
        for item in v.split(","):
            item = item.strip()
            if item and item != "Vet ikke":
                counts[item] += 1
    return counts


def count_single(rows: list[dict], col: str) -> Counter:
    counts: Counter = Counter()
    for r in rows:
        v = val(r, col)
        if v:
            counts[v] += 1
    return counts


def maturity_levels(rows: list[dict], col: str) -> tuple[Counter, int]:
    counts: Counter = Counter()
    for r in rows:
        v = val(r, col)
        if not v or v == "N/A":
            continue
        for lvl in ["1", "2", "3", "4"]:
            if f"Nivå {lvl}" in v:
                counts[f"L{lvl}"] += 1
                break
    return counts, sum(counts.values())


def mcnemar_exact(gained: int, lost: int) -> float:
    """Two-sided exact McNemar test: binomial test on discordant pairs, H0 p=0.5."""
    n = gained + lost
    if n == 0:
        return 1.0
    k = min(gained, lost)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2**n)


def level(row: dict, col: str) -> int | None:
    v = val(row, col)
    for lvl in "1234":
        if f"Nivå {lvl}" in v:
            return int(lvl)
    return None


def panel_pairs(rows24: list[dict], rows26: list[dict]) -> list[tuple[dict, dict]]:
    """Pair each panel org's 2024 row with its first 2026 row (dual-platform orgs: first row)."""
    first24, first26 = {}, {}
    for r in rows24:
        first24.setdefault(r[COL_ORG], r)
    for r in rows26:
        first26.setdefault(r[COL_ORG], r)
    return [(first24[o], first26[o]) for o in sorted(first24.keys() & first26.keys())]


def panel_mcnemar(rows24: list[dict], rows26: list[dict]):
    """Paired panel comparisons (McNemar exact) for the key binary indicators."""
    print_header("Panel paired comparisons (McNemar exact, first-2026-row pairing)")
    pairs = panel_pairs(rows24, rows26)
    plat = [(a, b) for a, b in pairs
            if val(a, COL_HAS_PLATFORM) == "Ja" and val(b, COL_HAS_PLATFORM) == "Ja"]
    ops, meas = MATURITY_COLS[3][1], MATURITY_COLS[4][1]
    tests = [
        ("Security motivation", plat, lambda r: "Sikkerhet" in [m.strip() for m in val(r, COL_MOTIVATION).split(",")]),
        ("Cost motivation", plat, lambda r: "Kostoptimalisering" in [m.strip() for m in val(r, COL_MOTIVATION).split(",")]),
        ("Operations L3+", [(a, b) for a, b in plat if level(a, ops) and level(b, ops)], lambda r: level(r, ops) >= 3),
        ("Measurement L1", [(a, b) for a, b in plat if level(a, meas) and level(b, meas)], lambda r: level(r, meas) == 1),
    ]
    for name, ps, f in tests:
        y24 = sum(f(a) for a, _ in ps)
        y26 = sum(f(b) for _, b in ps)
        gained = sum(not f(a) and f(b) for a, b in ps)
        lost = sum(f(a) and not f(b) for a, b in ps)
        print(f"  {name}: n={len(ps)} pairs, {y24}->{y26}, gained={gained}, lost={lost}, "
              f"McNemar p={mcnemar_exact(gained, lost):.3f}")


# --- Printing helpers ---

def print_header(title: str):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def print_section(title: str):
    print(f"\n--- {title} ---")


def print_counter(counts: Counter, total: int | None = None, ordered: list[str] | None = None):
    """Print counter with percentages."""
    if total is None:
        total = sum(counts.values())
    if total == 0:
        print("  (no data)")
        return
    items = [(k, counts.get(k, 0)) for k in ordered] if ordered else counts.most_common()
    for label, count in items:
        pct = count / total * 100
        print(f"  {label}: {count} ({pct:.0f}%)")


def print_maturity_table(rows: list[dict]):
    """Print all 5 maturity dimensions."""
    print(f"\n  {'Aspect':<14} {'L1':>8} {'L2':>8} {'L3':>8} {'L4':>8}   n")
    print(f"  {'-'*14} {'-'*8} {'-'*8} {'-'*8} {'-'*8}   --")
    for name, col in MATURITY_COLS:
        counts, total = maturity_levels(rows, col)
        if total == 0:
            print(f"  {name:<14}    (no data)")
            continue
        parts = []
        for lvl in ["L1", "L2", "L3", "L4"]:
            c = counts.get(lvl, 0)
            parts.append(f"{c:>3} ({c / total * 100:2.0f}%)")
        print(f"  {name:<14} {parts[0]} {parts[1]} {parts[2]} {parts[3]}   {total}")


# --- Main analysis ---

def analyze(year: str, rows: list[dict]):
    n = len(rows)
    orgs = {r[COL_ORG] for r in rows}

    print_header(f"State of the Platforms {year} — Analysis")

    print(f"\nTotal responses: {n}")
    print(f"Unique organizations: {len(orgs)}")

    print_section("Organization Types")
    print_counter(count_single(rows, COL_TYPE), total=n)

    print_section("Organization Types (detail)")
    print_counter(count_single(rows, COL_TYPE_DETAIL), total=n)

    print_section("Employees & Budget by Type")
    type_groups: dict[str, dict] = {}
    has_any_data = False
    for r in rows:
        t = val(r, COL_TYPE)
        if t not in type_groups:
            type_groups[t] = {"orgs": 0, "employees": 0, "budget": 0, "emp_n": 0, "bud_n": 0}
        type_groups[t]["orgs"] += 1
        emp = val(r, COL_EMPLOYEES)
        bud = val(r, COL_BUDGET)
        if emp:
            try:
                type_groups[t]["employees"] += int(emp)
                type_groups[t]["emp_n"] += 1
                has_any_data = True
            except ValueError:
                pass
        if bud:
            try:
                type_groups[t]["budget"] += int(bud)
                type_groups[t]["bud_n"] += 1
                has_any_data = True
            except ValueError:
                pass

    if has_any_data:
        total_emp = sum(v["employees"] for v in type_groups.values())
        total_bud = sum(v["budget"] for v in type_groups.values())
        total_emp_n = sum(v["emp_n"] for v in type_groups.values())
        total_bud_n = sum(v["bud_n"] for v in type_groups.values())
        for t, v in sorted(type_groups.items(), key=lambda x: -x[1]["orgs"]):
            print(f"  {t}: {v['orgs']} orgs, {v['employees']:,} employees ({v['emp_n']}/{v['orgs']} reported), {v['budget']:,} MNOK ({v['bud_n']}/{v['orgs']} reported)")
        print(f"  TOTAL: {sum(v['orgs'] for v in type_groups.values())} orgs, "
              f"{total_emp:,} employees ({total_emp_n} reported), {total_bud:,} MNOK ({total_bud_n} reported)")
    else:
        print("  (no employee/budget data)")

    # Platform adoption
    print_section("Platform Adoption")
    plat = count_single(rows, COL_HAS_PLATFORM)
    print_counter(plat, total=n)

    # K8s
    print_section("Kubernetes Usage")
    k8s = count_single(rows, COL_K8S)
    print_counter(k8s, total=n)

    # Motivation
    print_section("Motivation (of platform-having orgs)")
    with_plat = [r for r in rows if r.get(COL_HAS_PLATFORM) == "Ja"]
    motivations: Counter = Counter()
    for r in with_plat:
        v = val(r, COL_MOTIVATION)
        if v:
            for m in v.split(","):
                m = m.strip()
                if m:
                    motivations[m] += 1
    known_printed = set()
    for m in KNOWN_MOTIVATIONS:
        if m in motivations:
            c = motivations[m]
            print(f"  {m}: {c} ({c / len(with_plat) * 100:.0f}%)")
            known_printed.add(m)
    extras = {m: c for m, c in motivations.items() if m not in known_printed}
    if extras:
        for m, c in Counter(extras).most_common():
            print(f"  {m}: {c} ({c / len(with_plat) * 100:.0f}%)")

    # Teams
    print_section("Application Teams")
    teams = count_single(rows, COL_TEAMS)
    total_teams = sum(teams.values())
    print_counter(teams, total=total_teams, ordered=TEAM_ORDER)

    # Languages
    print_section("Programming Languages (share of mentions)")
    langs = flatten(rows, COL_LANGUAGES)
    print_counter(langs)

    # K8s distributions
    print_section("Kubernetes Distributions")
    distros = flatten(rows, COL_K8S_DISTRO)
    print_counter(distros)

    # Primary cloud
    print_section("Primary Cloud")
    cloud = count_single(rows, COL_PRIMARY_CLOUD)
    print_counter(cloud)

    # Years K8s in prod
    print_section("Years Kubernetes in Production")
    k8s_yrs = count_single(rows, COL_K8S_YEARS)
    for y, c in sorted(k8s_yrs.items(), key=lambda x: (x[0].isdigit() or x[0][0].isdigit(), int(x[0]) if x[0].isdigit() else 0)):
        print(f"  {y} yr: {c}")

    # Years cloud
    print_section("Years Running Apps in Cloud")
    sky_yrs = count_single(rows, COL_CLOUD_YEARS)
    for y, c in sorted(sky_yrs.items(), key=lambda x: (x[0].isdigit(), int(x[0]) if x[0].isdigit() else 0)):
        print(f"  {y} yr: {c}")

    # K8s clusters
    print_section("Kubernetes Clusters")
    clusters = count_single(rows, COL_K8S_CLUSTERS)
    print_counter(clusters, ordered=[c for c in CLUSTER_ORDER if c in clusters] or None)

    # K8s apps
    print_section("Kubernetes Apps in Production")
    apps = count_single(rows, COL_K8S_APPS)
    print_counter(apps, ordered=[a for a in APP_ORDER if a in apps] or None)

    # Serverless
    print_section("Serverless")
    sl = count_single(rows, COL_SERVERLESS)
    print_counter(sl)

    # Maturity
    print_section("CNCF Platform Maturity Model")
    print_maturity_table(rows)

    # Operators
    print_section("Custom Kubernetes Operators")
    ops = count_single(rows, COL_OPERATORS)
    if ops:
        print_counter(ops)
    else:
        print("  (not asked)")

    # Databases in K8s
    print_section("Databases in Kubernetes")
    db: Counter = Counter()
    has_db_data = False
    for r in rows:
        v = val(r, COL_DATABASES)
        if not v:
            continue
        has_db_data = True
        if v.startswith("Ja"):
            db["Ja"] += 1
        elif v == "Nei":
            db["Nei"] += 1
        elif v == "Vet ikke":
            db["Vet ikke"] += 1
        else:
            db["Other"] += 1
    if has_db_data:
        print_counter(db)
    else:
        print("  (not asked)")

    # Tooling
    print_section("Tooling")
    for tname, col in TOOLING_COLS:
        tools = flatten(rows, col)
        if tools:
            print(f"\n  {tname}:")
            for tool, c in tools.most_common(10):
                print(f"    {tool}: {c}")

    # List organizations
    print_section("Organizations")
    for org in sorted(orgs):
        row = next(r for r in rows if r[COL_ORG] == org)
        parts = [org]
        emp = val(row, COL_EMPLOYEES)
        bud = val(row, COL_BUDGET)
        if emp:
            try:
                parts.append(f"{int(emp):,} emp")
            except ValueError:
                parts.append(f"{emp} emp")
        if bud:
            try:
                parts.append(f"{int(bud):,} MNOK")
            except ValueError:
                parts.append(f"{bud} MNOK")
        parts.append(val(row, COL_TYPE))
        plat_val = val(row, COL_HAS_PLATFORM)
        k = val(row, COL_K8S)
        if plat_val == "Ja":
            pname = val(row, COL_PLATFORM_NAME)
            parts.append(f"platform={pname or 'unnamed'}")
        if k == "Ja":
            parts.append("K8s")
        print(f"  {' | '.join(parts)}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    files = []
    for arg in sys.argv[1:]:
        p = Path(arg)
        if p.is_file():
            files.append(str(p))
        else:
            expanded = list(Path(".").glob(arg))
            files.extend(str(f) for f in expanded if f.is_file())

    if not files:
        print(f"No files found: {sys.argv[1:]}", file=sys.stderr)
        sys.exit(1)

    waves = {}
    for path in files:
        year, rows = load_csv(path)
        waves[year] = rows
        analyze(year, rows)
        print()
    if "2024" in waves and "2026" in waves:
        panel_mcnemar(waves["2024"], waves["2026"])


if __name__ == "__main__" and "--selftest" in sys.argv:
    # Known values: 9 vs 1 discordant -> 0.0215; symmetric -> 1.0
    assert abs(mcnemar_exact(9, 1) - 22 / 1024) < 1e-12
    assert mcnemar_exact(3, 3) == 1.0 and mcnemar_exact(0, 0) == 1.0
    print("selftest ok")
    sys.exit(0)


if __name__ == "__main__":
    main()
