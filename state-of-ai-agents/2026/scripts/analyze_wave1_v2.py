#!/usr/bin/env python3
"""
Wave 1 Analysis v2: State of AI Coding Agents in Norwegian Public Sector (2026)
Publication-quality analysis addressing peer review issues:
  - Dual-level reporting (respondent N=115, org N=57)
  - Shadow adoption sensitivity analysis (3 metrics × 3 confidence levels)
  - Role recoding into analytical groups
  - Wilson confidence intervals for headline stats
  - "Other" field recoding
  - RQ2 association measures (Cramér's V, governance index)
  - RQ3 Fisher's exact tests by role group
  - Confidence-filtered sensitivity analyses

Python 3.8 or newer (tested 3.8–3.14), standard library only.
"""

import csv
import json
import math
import os
import random
import re
import sys
from collections import Counter, defaultdict

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Usage: analyze_wave1_v2.py [CSV]  (or env AI_AGENTS_CSV). Defaults to the public
# anonymous CSV next to this folder.
DATA_FILE = (sys.argv[1] if len(sys.argv) > 1 else None) or os.environ.get(
    "AI_AGENTS_CSV", os.path.join(SCRIPT_DIR, "..", "ai-agents-2026-anonymous.csv"))
SEED = 20260511  # fixed seed for all permutation tests
N_PERM = 10000

# Column indices (0-based)
COL_TIMESTAMP = 0
COL_ORG = 1
COL_ORG_ORIGINAL = 2
COL_DEVICE = 3
COL_SOURCE = 4
COL_ORG_FREETEXT = 5
COL_ROLE = 6
COL_DEV_SIZE = 7
COL_ADOPTION = 8
COL_ADOPTION_CONF = 9
COL_APPROVED_TOOLS = 10
COL_TOOLS_CONF = 11
COL_INTRO_METHOD = 12
COL_PERSONAL_USE = 13
COL_PERSONAL_TOOLS = 14
COL_USAGE_MODES = 15
COL_INTEGRATIONS = 16
COL_FREQUENCY = 17
COL_BENEFIT = 18
COL_POLICY = 19
COL_POLICY_CONF = 20
COL_SUPPORT = 21
COL_DECISION = 22
COL_VENDOR = 23
COL_MEASUREMENT = 24
COL_CODE_REVIEW = 25
COL_CONCERNS = 26
COL_PUBLIC_CONCERNS = 27
COL_STANCE = 28
COL_GAP = 29
COL_INTERVIEW = 30

# --- Role Recoding ---
ROLE_RECODE = {
    "developer": "practitioner",
    "platform": "practitioner",
    "tech-lead": "technical-leadership",
    "team-lead": "technical-leadership",
    "cto": "organizational-leadership",
    "non-tech-leader": "organizational-leadership",
    "other (Team Lead / Systemutvikler)": "technical-leadership",
    "other (Utviklingsleder)": "technical-leadership",
    "other (Leder + utvikler)": "organizational-leadership",
    "other (ux)": "practitioner",
    "other (KI-Teknolog)": "practitioner",
    "other (Dataforsker)": "practitioner",
    "other (Data Scientist)": "practitioner",
    "other (Svarer som faggruppe for KI)": "organizational-leadership",
    # The public CSV stores the recoded group directly
    "practitioner": "practitioner",
    "technical-leadership": "technical-leadership",
    "organizational-leadership": "organizational-leadership",
}

# --- Tool Recoding ---
# The public CSV already contains recoded tool categories.
TOOL_RECODE = {}

# Adoption maturity ordinal scale
ADOPTION_ORDINAL = {
    "individual": 1,
    "some-teams": 2,
    "officially-approved": 3,
    "most-developers": 4,
}

# Governance "mature" indicators
MATURE_GOVERNANCE = {
    COL_POLICY: {"specific"},
    COL_SUPPORT: {"structured", "training"},
    COL_DECISION: {"central", "approval-process"},
    COL_VENDOR: {"clarified"},
    COL_MEASUREMENT: {"own-metrics", "vendor-data"},
    COL_CODE_REVIEW: {"written", "written-automated"},
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def parse_multiselect(value):
    """Parse semicolon-separated multi-select field."""
    if not value or value.strip() == "":
        return []
    return [v.strip() for v in value.split(";") if v.strip()]


def recode_tools(tools_list):
    """Apply tool recoding to a list of tool values."""
    recoded = []
    for t in tools_list:
        if t in TOOL_RECODE:
            recoded.append(TOOL_RECODE[t])
        else:
            recoded.append(t)
    return recoded


def wilson_ci(n_success, n_total, z=1.96):
    """Wilson score interval for a proportion."""
    if n_total == 0:
        return (0.0, 0.0)
    p = n_success / n_total
    denom = 1 + z**2 / n_total
    center = (p + z**2 / (2 * n_total)) / denom
    margin = z * math.sqrt(p * (1 - p) / n_total + z**2 / (4 * n_total**2)) / denom
    return (max(0.0, center - margin), min(1.0, center + margin))


def pct_ci(n, total):
    """Format percentage with count and Wilson CI."""
    if total == 0:
        return "0% (0/0)"
    p = n / total * 100
    lo, hi = wilson_ci(n, total)
    return f"{p:.0f}% ({n}/{total}, 95% CI: {lo*100:.0f}–{hi*100:.0f}%)"


def pct(n, total):
    """Format percentage with count (no CI)."""
    if total == 0:
        return "0% (0/0)"
    return f"{n/total*100:.0f}% ({n}/{total})"


def fisher_exact_2x2(a, b, c, d):
    """Two-sided Fisher's exact test for 2×2 table [[a,b],[c,d]]."""
    from math import comb
    n = a + b + c + d
    r1, r2, c1, c2 = a + b, c + d, a + c, b + d

    def hypergeom_pmf(k):
        return comb(r1, k) * comb(r2, c1 - k) / comb(n, c1)

    p_observed = hypergeom_pmf(a)
    p_value = sum(
        hypergeom_pmf(k)
        for k in range(max(0, c1 - r2), min(r1, c1) + 1)
        if hypergeom_pmf(k) <= p_observed + 1e-10
    )
    return min(p_value, 1.0)


def chi_square_stat(observed, expected):
    """Compute chi-square statistic from observed and expected count lists."""
    return sum((o - e)**2 / e for o, e in zip(observed, expected) if e > 0)


def cramers_v_2way(table, row_totals, col_totals, grand_total):
    """
    Cramér's V for a contingency table.
    table: dict of (row, col) -> count
    """
    # Compute chi-square
    chi2 = 0.0
    for r_idx, r_total in enumerate(row_totals):
        for c_idx, c_total in enumerate(col_totals):
            expected = r_total * c_total / grand_total if grand_total > 0 else 0
            observed = table.get((r_idx, c_idx), 0)
            if expected > 0:
                chi2 += (observed - expected)**2 / expected
    n_rows = len(row_totals)
    n_cols = len(col_totals)
    k = min(n_rows, n_cols) - 1
    if k <= 0 or grand_total <= 0:
        return 0.0, chi2
    v = math.sqrt(chi2 / (grand_total * k))
    return v, chi2


def spearman_rank_correlation(x, y):
    """Spearman rank correlation for two lists of values."""
    n = len(x)
    if n < 3:
        return 0.0, 1.0

    def rank_data(data):
        sorted_indices = sorted(range(n), key=lambda i: data[i])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j < n - 1 and data[sorted_indices[j + 1]] == data[sorted_indices[j]]:
                j += 1
            avg_rank = (i + j) / 2 + 1
            for k in range(i, j + 1):
                ranks[sorted_indices[k]] = avg_rank
            i = j + 1
        return ranks

    rx = rank_data(x)
    ry = rank_data(y)

    mean_rx = sum(rx) / n
    mean_ry = sum(ry) / n

    num = sum((rx[i] - mean_rx) * (ry[i] - mean_ry) for i in range(n))
    den_x = math.sqrt(sum((rx[i] - mean_rx)**2 for i in range(n)))
    den_y = math.sqrt(sum((ry[i] - mean_ry)**2 for i in range(n)))

    if den_x == 0 or den_y == 0:
        return 0.0, 1.0

    rho = num / (den_x * den_y)

    # Two-sided permutation p-value (shuffle y ranks, fixed seed); valid for small n.
    rng = random.Random(SEED)
    ry_perm = list(ry)
    hits = 0
    for _ in range(N_PERM):
        rng.shuffle(ry_perm)
        num_p = sum((rx[i] - mean_rx) * (ry_perm[i] - mean_ry) for i in range(n))
        if abs(num_p) >= abs(num) - 1e-12:
            hits += 1
    p = (hits + 1) / (N_PERM + 1)
    return rho, p


def majority_vote(values):
    """
    Aggregate org-level response using majority rule.
    Returns (value, method) where method is 'unanimous', 'majority', or 'disagreement'.
    """
    if not values:
        return (None, "empty")
    counter = Counter(values)
    total = len(values)
    if len(counter) == 1:
        return (counter.most_common(1)[0][0], "unanimous")
    top_val, top_count = counter.most_common(1)[0]
    if top_count > total / 2:
        return (top_val, "majority")
    return (None, "disagreement")


def majority_vote_multiselect(respondent_values):
    """
    For multi-select fields at org level, take union of all mentions.
    Returns the set of all unique values mentioned by any respondent.
    """
    all_vals = set()
    for vals in respondent_values:
        all_vals.update(vals)
    return all_vals


# =============================================================================
# LOAD DATA
# =============================================================================



# Raw columns kept in the public CSV (drops organization, timestamp, org original/free text, device,
# source, Q21 free text and interview opt-in).
PUBLIC_COLUMNS = list(range(6, 27)) + [28, 29]
MULTISELECT_COLUMNS = [COL_APPROVED_TOOLS, COL_PERSONAL_TOOLS, COL_USAGE_MODES,
                       COL_INTEGRATIONS, COL_CONCERNS]


def normalize_other(value):
    """In four web-form responses the 'other' free text was attached to the last
    selected option, e.g. 'security; other; privacy (text)'. Move the text back
    to 'other' so the option itself is counted."""
    parts = [p.strip() for p in value.split(";") if p.strip()]
    if "other" in parts:
        for k, part in enumerate(parts):
            m = re.match(r"^([a-z-]+) \((.*)\)$", part, re.S)
            if m and m.group(1) != "other":
                parts[k] = m.group(1)
                parts[parts.index("other")] = f"other ({m.group(2)})"
                break
    return "; ".join(parts) if ";" in value else value



rows = []
with open(DATA_FILE, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    public = True
    assert len(header) == len(PUBLIC_COLUMNS), "expected the public anonymous CSV"
    for row in reader:
        # pad back to the original 31-column layout so COL_* indices hold
        full = [""] * 31
        for idx, v in zip(PUBLIC_COLUMNS, row):
            full[idx] = v
        row = full
        for c in MULTISELECT_COLUMNS:
            row[c] = normalize_other(row[c])
        rows.append(row)

N = len(rows)

# The public CSV has no organization column. Org-level results are published as
# aggregates in org-level-tables.csv.
HAS_ORG = any(r[COL_ORG] for r in rows)
ORG_NA = "not available in public data — see org-level-tables.csv"

# Build org-grouped data
org_groups = defaultdict(list)
for r in rows:
    if r[COL_ORG] not in ("unknown", ""):
        org_groups[r[COL_ORG]].append(r)

N_ORGS = len(org_groups)

# Recode roles
for r in rows:
    r.append(ROLE_RECODE.get(r[COL_ROLE], "unknown"))  # index 31 = recoded role group

COL_ROLE_GROUP = 31

# =============================================================================
# AGGREGATE TO ORG LEVEL
# =============================================================================

# For each org, compute majority-vote values for organizational questions
org_level = {}  # org_name -> dict of aggregated values
ORG_QUESTIONS = [COL_ADOPTION, COL_APPROVED_TOOLS, COL_INTRO_METHOD,
                 COL_POLICY, COL_SUPPORT, COL_DECISION, COL_VENDOR,
                 COL_MEASUREMENT, COL_CODE_REVIEW]

MULTISELECT_ORG_QUESTIONS = {COL_APPROVED_TOOLS}

for org_name, org_rows in org_groups.items():
    org_data = {"n_respondents": len(org_rows)}
    for col in ORG_QUESTIONS:
        if col in MULTISELECT_ORG_QUESTIONS:
            # Union of multi-select
            respondent_values = [parse_multiselect(r[col]) for r in org_rows]
            org_data[col] = majority_vote_multiselect(respondent_values)
            org_data[f"{col}_method"] = "union"
        else:
            values = [r[col] for r in org_rows]
            val, method = majority_vote(values)
            org_data[col] = val
            org_data[f"{col}_method"] = method
    # Also store dev size (take first non-empty or majority)
    sizes = [r[COL_DEV_SIZE] for r in org_rows]
    org_data[COL_DEV_SIZE], org_data[f"{COL_DEV_SIZE}_method"] = majority_vote(sizes)
    org_level[org_name] = org_data


# =============================================================================
# PRINTING
# =============================================================================

print("=" * 80)
print("  STATE OF AI CODING AGENTS IN NORWEGIAN PUBLIC SECTOR")
print("  Wave 1 (2026) — Publication-Quality Analysis (v2)")
print("  Addressing peer review: dual-level, CIs, sensitivity, associations")
print("=" * 80)

# =============================================================================
# SECTION 1: SAMPLE & DEMOGRAPHICS
# =============================================================================
print("\n\n" + "=" * 80)
print("  1. SAMPLE & DEMOGRAPHICS")
print("=" * 80)

print(f"\n  Total respondents: N = {N}")
print(f"  Unique organizations: N_org = {N_ORGS if HAS_ORG else ORG_NA}")
print(f"  Data file: {os.path.basename(DATA_FILE)} ")
print(f"  Columns: {len(header)}")

if HAS_ORG:
    # Org response counts
    org_counts = Counter(r[COL_ORG] for r in rows if r[COL_ORG] != "unknown")
    orgs_multi = {k: v for k, v in org_counts.items() if v > 1}
    orgs_single = {k: v for k, v in org_counts.items() if v == 1}
    print(f"\n  Organizations with single respondent: {len(orgs_single)}")
    print(f"  Organizations with multiple respondents: {len(orgs_multi)}")
    print(f"  Max responses from single org: {max(org_counts.values())} ({org_counts.most_common(1)[0][0]})")
    print(f"  Median responses per org: {sorted(org_counts.values())[len(org_counts)//2]}")

    print("\n  Top 10 organizations by response count:")
    for org, count in org_counts.most_common(10):
        print(f"    {org:40s} {count:3d}")
else:
    print(f"\n  Organization response counts: " + ORG_NA)

# Role distribution — original and recoded
roles = Counter(r[COL_ROLE] for r in rows)
print(f"\n  Role distribution — original (N={N}):")
for role, count in roles.most_common():
    print(f"    {role:45s} {pct(count, N):>18s}")

role_groups = Counter(r[COL_ROLE_GROUP] for r in rows)
print(f"\n  Role distribution — recoded groups (N={N}):")
for rg, count in role_groups.most_common():
    print(f"    {rg:30s} {pct(count, N):>18s}")

# Org size
sizes = Counter(r[COL_DEV_SIZE] for r in rows)
print(f"\n  Organization dev team size (Q3, N={N}):")
for s, count in sizes.most_common():
    print(f"    {s:20s} {pct(count, N):>18s}")

# Confidence overview
print(f"\n  Confidence distribution:")
for label, col in [("Q5b (Adoption)", COL_ADOPTION_CONF),
                   ("Q6b (Tools)", COL_TOOLS_CONF),
                   ("Q14b (Policy)", COL_POLICY_CONF)]:
    conf = Counter(r[col] for r in rows)
    certain = conf.get("certain", 0)
    fairly = conf.get("fairly-sure", 0)
    estimate = conf.get("estimate", 0)
    other = N - certain - fairly - estimate
    print(f"    {label:20s} certain={certain:3d}  fairly-sure={fairly:3d}  estimate={estimate:3d}  other={other}")


# =============================================================================
# SECTION 2: RQ1 — ADOPTION
# =============================================================================
print("\n\n" + "=" * 80)
print("  2. RQ1: ADOPTION")
print("=" * 80)

# --- 2a. Organizational adoption (dual-level) ---
print("\n  --- 2a. Organizational Adoption Level (Q5) — DUAL-LEVEL ---")

# Respondent level
adoption = Counter(r[COL_ADOPTION] for r in rows)
print(f"\n  RESPONDENT-LEVEL (N={N}):")
adoption_order = ["most-developers", "officially-approved", "some-teams", "individual", "not-in-use", "unknown"]
for level in adoption_order:
    count = adoption.get(level, 0)
    if count > 0:
        print(f"    {level:25s} {pct_ci(count, N)}")

if HAS_ORG:
    # Org level (majority vote)
    print(f"\n  ORGANIZATION-LEVEL (N_org={N_ORGS}, majority-vote aggregation):")
    org_adoption = Counter()
    org_adoption_methods = Counter()
    for org_name, od in org_level.items():
        val = od[COL_ADOPTION]
        method = od[f"{COL_ADOPTION}_method"]
        if val is not None:
            org_adoption[val] += 1
        else:
            org_adoption["disagreement"] += 1
        org_adoption_methods[method] += 1

    for level in adoption_order + ["disagreement"]:
        count = org_adoption.get(level, 0)
        if count > 0:
            print(f"    {level:25s} {pct(count, N_ORGS)}")

    print(f"\n  Aggregation method distribution:")
    for method, count in org_adoption_methods.most_common():
        print(f"    {method:15s} {count:3d} orgs")

    # Intra-org disagreement on adoption
    print(f"\n  Intra-org disagreement on adoption (Q5):")
    disagreements_adoption = []
    for org_name, org_rows in org_groups.items():
        if len(org_rows) > 1:
            values = [r[COL_ADOPTION] for r in org_rows]
            if len(set(values)) > 1:
                disagreements_adoption.append((org_name, Counter(values)))
    print(f"    Orgs with disagreement: {len(disagreements_adoption)}/{len(orgs_multi)} multi-respondent orgs")
    for org_name, cnt in disagreements_adoption[:5]:
        print(f"      {org_name}: {dict(cnt)}")
else:
    print(f"\n  ORGANIZATION-LEVEL adoption: " + ORG_NA)

# --- 2b. Tool landscape ---
print("\n\n  --- 2b. Tool Landscape ---")

# Approved tools (Q6) — respondent level with recoding
# Use set() per respondent to avoid double-counting when "other" recodes
# to the same tool as a structured entry (e.g., "other (Claude Code)" + "claude-code")
all_approved_raw = []
all_approved_recoded = []
for r in rows:
    raw = parse_multiselect(r[COL_APPROVED_TOOLS])
    all_approved_raw.extend(raw)
    all_approved_recoded.extend(set(recode_tools(raw)))

print(f"\n  Officially approved tools (Q6, respondent-level, N={N}, multi-select):")
for tool, count in Counter(all_approved_recoded).most_common():
    print(f"    {tool:30s} {pct(count, N):>18s}")

# Personal tools (Q8b) — among users, with recoding
users_yes = [r for r in rows if r[COL_PERSONAL_USE] == "yes"]
N_users = len(users_yes)
print(f"\n  Personal adoption rate: {pct_ci(N_users, N)}")

all_personal_raw = []
all_personal_recoded = []
for r in users_yes:
    raw = parse_multiselect(r[COL_PERSONAL_TOOLS])
    all_personal_raw.extend(raw)
    all_personal_recoded.extend(set(recode_tools(raw)))

print(f"\n  Personal tools used (Q8b, among users N={N_users}, multi-select):")
for tool, count in Counter(all_personal_recoded).most_common():
    print(f"    {tool:30s} {pct(count, N_users):>18s}")

# --- 2c. Shadow Adoption (3 metrics × 3 confidence levels) ---
print("\n\n  --- 2c. Shadow Adoption — Sensitivity Analysis ---")
print("  Three metrics × three confidence filters")

confidence_filters = [
    ("all", lambda r: True),
    ("certain+fairly-sure", lambda r: r[COL_TOOLS_CONF] in ("certain", "fairly-sure")),
    ("certain-only", lambda r: r[COL_TOOLS_CONF] == "certain"),
]

for conf_label, conf_filter in confidence_filters:
    print(f"\n  [{conf_label.upper()}]")
    filtered_users = [r for r in users_yes if conf_filter(r)]
    n_filtered = len(filtered_users)

    # Metric 1: BROAD shadow (all mismatches)
    broad_shadow = 0
    for r in filtered_users:
        approved = set(recode_tools(parse_multiselect(r[COL_APPROVED_TOOLS])))
        personal = set(recode_tools(parse_multiselect(r[COL_PERSONAL_TOOLS])))
        if "none" in approved or "unknown" in approved:
            continue
        unapproved = personal - approved - {"none", "unknown"}
        if unapproved:
            broad_shadow += 1
    # Denominator: users with known approved tools
    users_known_approved = [r for r in filtered_users
                           if "none" not in parse_multiselect(r[COL_APPROVED_TOOLS])
                           and "unknown" not in parse_multiselect(r[COL_APPROVED_TOOLS])]
    n_known = len(users_known_approved)

    # Metric 2: NARROW shadow (exclude browser-llm, open-source)
    narrow_shadow = 0
    for r in users_known_approved:
        if not conf_filter(r):
            continue
        approved = set(recode_tools(parse_multiselect(r[COL_APPROVED_TOOLS])))
        personal = set(recode_tools(parse_multiselect(r[COL_PERSONAL_TOOLS])))
        unapproved = personal - approved - {"none", "unknown", "browser-llm", "open-source"}
        if unapproved:
            narrow_shadow += 1

    # Metric 3: No-approval use (users in orgs with "none" approved who use tools)
    no_approval_users = [r for r in filtered_users
                         if "none" in parse_multiselect(r[COL_APPROVED_TOOLS])]
    n_no_approval = len(no_approval_users)

    print(f"    Filtered users: {n_filtered}, with known approved tools: {n_known}")
    print(f"    1. BROAD shadow (any mismatch):      {pct_ci(broad_shadow, n_known) if n_known > 0 else 'N/A'}")
    print(f"    2. NARROW shadow (excl. browser/OSS): {pct_ci(narrow_shadow, n_known) if n_known > 0 else 'N/A'}")
    print(f"    3. No-approval use:                   {n_no_approval} users in orgs with no approved tools")

# Detail for "all" filter: what tools are shadow
print(f"\n  Shadow tool breakdown (broad, all confidence):")
shadow_tool_detail = Counter()
for r in users_yes:
    approved = set(recode_tools(parse_multiselect(r[COL_APPROVED_TOOLS])))
    personal = set(recode_tools(parse_multiselect(r[COL_PERSONAL_TOOLS])))
    if "none" in approved or "unknown" in approved:
        continue
    unapproved = personal - approved - {"none", "unknown"}
    for t in unapproved:
        shadow_tool_detail[t] += 1
for tool, count in shadow_tool_detail.most_common():
    print(f"    {tool:25s} {count:3d} users")

# --- 2d. Personal Usage Patterns ---
print("\n\n  --- 2d. Personal Usage Patterns (individual-level) ---")

# Usage modes (Q9)
all_modes = []
for r in users_yes:
    all_modes.extend(parse_multiselect(r[COL_USAGE_MODES]))
print(f"\n  Usage modes (Q9, among users N={N_users}, multi-select):")
for mode, count in Counter(all_modes).most_common():
    print(f"    {mode:25s} {pct(count, N_users):>18s}")

# Agentic usage
uses_agent = sum(1 for r in users_yes
                 if {"local-agent", "cloud-agent"} & set(parse_multiselect(r[COL_USAGE_MODES])))
print(f"\n  Agentic users (local-agent or cloud-agent): {pct_ci(uses_agent, N_users)}")

autocomplete_only = sum(1 for r in users_yes
                        if set(parse_multiselect(r[COL_USAGE_MODES])) == {"autocomplete"})
print(f"  Autocomplete-only users: {pct(autocomplete_only, N_users)}")

# Frequency (Q11)
freq = Counter(r[COL_FREQUENCY] for r in users_yes)
print(f"\n  Usage frequency (Q11, among users N={N_users}):")
freq_order = ["daily", "several-weekly", "weekly", "monthly", "rarely"]
for f in freq_order:
    count = freq.get(f, 0)
    if count > 0:
        print(f"    {f:20s} {pct(count, N_users):>18s}")

# Integrations (Q10)
users_with_integrations = sum(1 for r in users_yes
                              if set(parse_multiselect(r[COL_INTEGRATIONS])) - {"none", "dont-understand"})
print(f"\n  Users with integrations (Q10): {pct_ci(users_with_integrations, N_users)}")

# Benefit (Q11b)
benefits = Counter(r[COL_BENEFIT] for r in users_yes)
print(f"\n  Primary benefit (Q11b, among users N={N_users}):")
for b, count in benefits.most_common():
    print(f"    {b:30s} {pct(count, N_users):>18s}")


# =============================================================================
# SECTION 3: RQ2 — GOVERNANCE
# =============================================================================
print("\n\n" + "=" * 80)
print("  3. RQ2: GOVERNANCE")
print("=" * 80)

# --- 3a. Governance Indicators (dual-level) ---
print("\n  --- 3a. Governance Indicators — DUAL-LEVEL ---")

governance_cols = [
    ("Policy (Q14)", COL_POLICY),
    ("Support (Q15)", COL_SUPPORT),
    ("Decision (Q16)", COL_DECISION),
    ("Vendor clarity (Q17)", COL_VENDOR),
    ("Measurement (Q18)", COL_MEASUREMENT),
    ("Code review (Q19)", COL_CODE_REVIEW),
]

for label, col in governance_cols:
    print(f"\n  {label}:")

    # Respondent level
    resp_counter = Counter(r[col] for r in rows)
    print(f"    Respondent-level (N={N}):")
    for val, count in resp_counter.most_common():
        print(f"      {val:25s} {pct(count, N):>18s}")

    if HAS_ORG:
        # Org level
        org_counter = Counter()
        org_methods = Counter()
        for org_name, od in org_level.items():
            val = od[col]
            method = od[f"{col}_method"]
            if val is not None:
                org_counter[val] += 1
            else:
                org_counter["disagreement"] += 1
            org_methods[method] += 1
        print(f"    Organization-level (N_org={N_ORGS}, majority-vote):")
        for val, count in org_counter.most_common():
            print(f"      {val:25s} {pct(count, N_ORGS):>18s}")
        print(f"    Aggregation: {dict(org_methods)}")
    else:
        print(f"\n      Organization-level: " + ORG_NA)

# Policy coverage headline with CI
has_policy_resp = sum(1 for r in rows if r[COL_POLICY] in ("specific", "general"))
print(f"\n  HEADLINE: Policy coverage (specific+general): {pct_ci(has_policy_resp, N)}")

if HAS_ORG:
    # --- 3b. Intra-org Disagreement ---
    print("\n\n  --- 3b. Intra-Organization Disagreement ---")
    print("  (Multi-respondent orgs only, N_multi={})".format(len(orgs_multi)))

    for label, col in governance_cols:
        disagree_count = 0
        for org_name, org_rows in org_groups.items():
            if len(org_rows) <= 1:
                continue
            values = [r[col] for r in org_rows]
            if len(set(values)) > 1:
                disagree_count += 1
        print(f"    {label:25s} disagreement in {pct(disagree_count, len(orgs_multi))}")

    # Permutation null: shuffle each answer across all N respondents (preserves the
    # marginal distribution and every org's size) and recount any-disagreement.
    print(f"\n  Disagreement vs permutation null ({N_PERM} draws, seed {SEED}):")
    print(f"    {'Indicator':25s} {'observed':>10s} {'null mean':>10s} {'null 95% range':>15s} {'P(null>=obs)':>13s} {'P(null<=obs)':>13s}")
    multi_idx = [[i for i, r in enumerate(rows) if r[COL_ORG] == o] for o in orgs_multi]
    n_multi = len(multi_idx)
    for label, col in [("Adoption (Q5)", COL_ADOPTION)] + governance_cols:
        vals = [r[col] for r in rows]
        obs = sum(len({vals[i] for i in g}) > 1 for g in multi_idx)
        rng = random.Random(SEED)
        perm = list(vals)
        null = []
        for _ in range(N_PERM):
            rng.shuffle(perm)
            null.append(sum(len({perm[i] for i in g}) > 1 for g in multi_idx))
        null.sort()
        ge = sum(1 for x in null if x >= obs) / N_PERM
        le = sum(1 for x in null if x <= obs) / N_PERM
        lo, hi = null[int(0.025 * N_PERM)], null[int(0.975 * N_PERM) - 1]
        print(f"    {label:25s} {obs/n_multi*100:9.0f}% {sum(null)/N_PERM/n_multi*100:9.0f}% "
              f"{lo/n_multi*100:6.0f}–{hi/n_multi*100:.0f}% {ge:13.3f} {le:13.3f}")

    # Detailed disagreement for policy
    print(f"\n  Detailed policy (Q14) disagreement:")
    for org_name, org_rows in org_groups.items():
        if len(org_rows) <= 1:
            continue
        values = [r[COL_POLICY] for r in org_rows]
        if len(set(values)) > 1:
            print(f"    {org_name:35s} {dict(Counter(values))}")
else:
    print(f"\n  3b. Intra-organization disagreement: " + ORG_NA)

# --- 3c. Governance × Adoption Maturity ---
print("\n\n  --- 3c. Governance × Adoption Maturity (Association Analysis) ---")

# Compute governance index per respondent
print("\n  Governance Index (count of 'mature' indicators per respondent, 0-6):")
gov_indices = []
for r in rows:
    score = 0
    for col, mature_vals in MATURE_GOVERNANCE.items():
        if r[col] in mature_vals:
            score += 1
    gov_indices.append(score)

gov_index_dist = Counter(gov_indices)
print(f"    Distribution (N={N}):")
for score in range(7):
    count = gov_index_dist.get(score, 0)
    if count > 0:
        print(f"      Score {score}: {pct(count, N)}")
print(f"    Mean: {sum(gov_indices)/N:.2f}, Median: {sorted(gov_indices)[N//2]}")

# Spearman: adoption maturity vs governance index (respondent-level)
adoption_scores = []
gov_scores_for_corr = []
for i, r in enumerate(rows):
    if r[COL_ADOPTION] in ADOPTION_ORDINAL:
        adoption_scores.append(ADOPTION_ORDINAL[r[COL_ADOPTION]])
        gov_scores_for_corr.append(gov_indices[i])

rho, p_val = spearman_rank_correlation(adoption_scores, gov_scores_for_corr)
print(f"\n  Spearman correlation: adoption maturity vs governance index")
print(f"    Respondent-level (n={len(adoption_scores)}):")
print(f"    ρ = {rho:.3f}", end="")
if p_val is not None:
    print(f", permutation p ≈ {p_val:.4f}" if p_val >= 0.001 else f", permutation p < 0.001")
else:
    print(" (p-value requires larger n for approximation)")

if HAS_ORG:
    # Org-level Spearman
    org_adoption_scores = []
    org_gov_scores = []
    for org_name, od in org_level.items():
        adoption_val = od[COL_ADOPTION]
        if adoption_val in ADOPTION_ORDINAL:
            # Compute org-level governance index via majority of each indicator
            org_score = 0
            for col, mature_vals in MATURE_GOVERNANCE.items():
                org_val = od[col]
                if org_val in mature_vals:
                    org_score += 1
            org_adoption_scores.append(ADOPTION_ORDINAL[adoption_val])
            org_gov_scores.append(org_score)

    rho_org, p_org = spearman_rank_correlation(org_adoption_scores, org_gov_scores)
    print(f"\n    Organization-level (n_org={len(org_adoption_scores)}):")
    print(f"    ρ = {rho_org:.3f}", end="")
    if p_org is not None:
        print(f", permutation p ≈ {p_org:.4f}" if p_org >= 0.001 else f", permutation p < 0.001")
    else:
        print(" (p-value requires larger n for approximation)")
else:
    print(f"\n  Organization-level Spearman: " + ORG_NA)

# Cramér's V for each governance indicator × adoption level
print(f"\n  Cramér's V: governance indicators × adoption level (respondent-level):")
adoption_levels_ordered = ["individual", "some-teams", "officially-approved", "most-developers"]
for label, col in governance_cols:
    # Build contingency table
    gov_values = sorted(set(r[col] for r in rows))
    table = {}
    row_totals = []
    for a_idx, a_level in enumerate(adoption_levels_ordered):
        a_rows = [r for r in rows if r[COL_ADOPTION] == a_level]
        row_totals.append(len(a_rows))
        for g_idx, g_val in enumerate(gov_values):
            table[(a_idx, g_idx)] = sum(1 for r in a_rows if r[col] == g_val)
    col_totals = []
    for g_idx in range(len(gov_values)):
        col_totals.append(sum(table.get((a_idx, g_idx), 0) for a_idx in range(len(adoption_levels_ordered))))
    grand_total = sum(row_totals)
    v, chi2 = cramers_v_2way(table, row_totals, col_totals, grand_total)
    df = (len(adoption_levels_ordered) - 1) * (len(gov_values) - 1)
    print(f"    {label:25s} V = {v:.3f} (χ² = {chi2:.2f}, df = {df})")


# Sensitivity: count any policy (specific or general) as mature.
print(f"\n  Governance index sensitivity: policy = specific OR general")
MATURE_ANY_POLICY = {**MATURE_GOVERNANCE, COL_POLICY: {"specific", "general"}}
alt_idx = [sum(r[c] in v for c, v in MATURE_ANY_POLICY.items()) for r in rows]
print(f"    Mean: {sum(alt_idx)/N:.2f}, Median: {sorted(alt_idx)[N//2]}")
pairs = [(ADOPTION_ORDINAL[r[COL_ADOPTION]], alt_idx[i]) for i, r in enumerate(rows) if r[COL_ADOPTION] in ADOPTION_ORDINAL]
rho_a, p_a = spearman_rank_correlation([a for a, _ in pairs], [g for _, g in pairs])
print(f"    Respondent-level (n={len(pairs)}): ρ = {rho_a:.3f}, permutation p ≈ {p_a:.4f}")
if HAS_ORG:
    pairs = [(ADOPTION_ORDINAL[od[COL_ADOPTION]], sum(od[c] in v for c, v in MATURE_ANY_POLICY.items()))
             for od in org_level.values() if od[COL_ADOPTION] in ADOPTION_ORDINAL]
    rho_a, p_a = spearman_rank_correlation([a for a, _ in pairs], [g for _, g in pairs])
    print(f"    Organization-level (n_org={len(pairs)}): ρ = {rho_a:.3f}, permutation p ≈ {p_a:.4f}")
else:
    print("    Organization-level: " + ORG_NA)

# Sensitivity: only formal approval process (not central decisions) and only own
# metrics (not vendor data) count as mature.
print(f"\n  Governance index sensitivity: decision = approval-process only, measurement = own-metrics only")
MATURE_STRICT = {**MATURE_GOVERNANCE, COL_DECISION: {"approval-process"}, COL_MEASUREMENT: {"own-metrics"}}
strict_idx = [sum(r[c] in v for c, v in MATURE_STRICT.items()) for r in rows]
print(f"    Mean: {sum(strict_idx)/N:.2f}, Median: {sorted(strict_idx)[N//2]}")
pairs = [(ADOPTION_ORDINAL[r[COL_ADOPTION]], strict_idx[i]) for i, r in enumerate(rows) if r[COL_ADOPTION] in ADOPTION_ORDINAL]
rho_a, p_a = spearman_rank_correlation([a for a, _ in pairs], [g for _, g in pairs])
print(f"    Respondent-level (n={len(pairs)}): ρ = {rho_a:.3f}, permutation p ≈ {p_a:.4f}")
if HAS_ORG:
    pairs = [(ADOPTION_ORDINAL[od[COL_ADOPTION]], sum(od[c] in v for c, v in MATURE_STRICT.items()))
             for od in org_level.values() if od[COL_ADOPTION] in ADOPTION_ORDINAL]
    rho_a, p_a = spearman_rank_correlation([a for a, _ in pairs], [g for _, g in pairs])
    print(f"    Organization-level (n_org={len(pairs)}): ρ = {rho_a:.3f}, permutation p ≈ {p_a:.4f}")
else:
    print("    Organization-level: " + ORG_NA)


# =============================================================================
# SECTION 4: RQ3 — BARRIERS & CONCERNS
# =============================================================================
print("\n\n" + "=" * 80)
print("  4. RQ3: BARRIERS & CONCERNS")
print("=" * 80)

# --- 4a. Concern Prevalence with CIs ---
print("\n  --- 4a. Concern Prevalence (N={}) ---".format(N))

concern_types = ["skill-loss", "code-quality", "hallucinations", "security",
                 "privacy", "cost", "ip", "workflow", "vendor-lock-in", "no-concerns"]

print(f"\n  {'Concern':<20s} {'Count':>6s}  {'Rate':>35s}")
print(f"  {'-'*20} {'-'*6}  {'-'*35}")
for concern in concern_types:
    count = sum(1 for r in rows if concern in parse_multiselect(r[COL_CONCERNS]))
    print(f"  {concern:<20s} {count:>6d}  {pct_ci(count, N)}")

# Also count "other" mentions
other_concerns = sum(1 for r in rows
                     if any(v.startswith("other") for v in parse_multiselect(r[COL_CONCERNS])))
print(f"  {'other (various)':<20s} {other_concerns:>6d}  {pct(other_concerns, N)}")

# Mean concerns
concern_counts = [len([v for v in parse_multiselect(r[COL_CONCERNS])
                       if not v.startswith("no-concerns")]) for r in rows]
print(f"\n  Mean concerns per respondent: {sum(concern_counts)/N:.2f}")
n_at_cap = sum(1 for r in rows if len(parse_multiselect(r[COL_CONCERNS])) >= 3)
print(f"  Respondents selecting the maximum of three concerns: {pct(n_at_cap, N)}")

# --- 4b. Role-group Differences (Fisher's exact) ---
print("\n\n  --- 4b. Concern Rates by Role Group ---")

role_group_names = ["practitioner", "technical-leadership", "organizational-leadership"]
rg_rows = {rg: [r for r in rows if r[COL_ROLE_GROUP] == rg] for rg in role_group_names}
rg_ns = {rg: len(rg_rows[rg]) for rg in role_group_names}

print(f"\n  Role groups: " + ", ".join(f"{rg}={rg_ns[rg]}" for rg in role_group_names))
print(f"\n  {'Concern':<18s}", end="")
for rg in role_group_names:
    print(f"  {rg[:12]:>14s}", end="")
print(f"  {'Fisher p':>10s}")
print(f"  {'-'*18}" + "  ".join([f"{'-'*14}"] * 3) + f"  {'-'*10}")

key_concerns_for_test = ["skill-loss", "code-quality", "hallucinations", "security"]

for concern in key_concerns_for_test:
    parts = []
    counts_by_rg = []
    for rg in role_group_names:
        n_with = sum(1 for r in rg_rows[rg] if concern in parse_multiselect(r[COL_CONCERNS]))
        n_total = rg_ns[rg]
        parts.append(f"{n_with/n_total*100:5.0f}% ({n_with:2d}/{n_total:2d})")
        counts_by_rg.append((n_with, n_total - n_with))

    # For 2×3 Fisher's exact — we'd need scipy. Use pairwise 2×2 tests instead.
    # Compare practitioners vs leadership (combined tech+org)
    a, b = counts_by_rg[0]  # practitioner: (with, without)
    c = counts_by_rg[1][0] + counts_by_rg[2][0]  # leadership with
    d = counts_by_rg[1][1] + counts_by_rg[2][1]  # leadership without
    p_fish = fisher_exact_2x2(a, b, c, d)

    print(f"  {concern:<18s}  {'  '.join(parts)}  p={p_fish:.3f}")

# Also show all concerns by role group
print(f"\n  Full concern table (% of role group citing concern):")
print(f"  {'Concern':<18s}", end="")
for rg in role_group_names:
    print(f"  {rg[:14]:>14s}", end="")
print()
for concern in concern_types:
    print(f"  {concern:<18s}", end="")
    for rg in role_group_names:
        n_with = sum(1 for r in rg_rows[rg] if concern in parse_multiselect(r[COL_CONCERNS]))
        n_total = rg_ns[rg]
        print(f"  {n_with/n_total*100:11.0f}%  ", end="")
    print()

# --- 4c. Policy Gap and Stance ---
print("\n\n  --- 4c. Policy Gap and Stance (individual-level) ---")

stance = Counter(r[COL_STANCE] for r in rows)
print(f"\n  Personal stance on AI-generated code (Q22, N={N}):")
for val, count in stance.most_common():
    print(f"    {val:25s} {pct(count, N):>18s}")

gap = Counter(r[COL_GAP] for r in rows)
print(f"\n  Perceived policy gap (Q23, N={N}):")
for val, count in gap.most_common():
    print(f"    {val:25s} {pct(count, N):>18s}")


# =============================================================================
# SECTION 5: SENSITIVITY ANALYSES
# =============================================================================
print("\n\n" + "=" * 80)
print("  5. SENSITIVITY ANALYSES")
print("=" * 80)

# --- 5a. Confidence-Filtered Key Findings ---
print("\n  --- 5a. Confidence-Filtered Key Findings ---")
print("  Reporting headline stats under different confidence exclusions.")

# Q5: Adoption level
print(f"\n  Q5 Adoption (% at officially-approved or most-developers):")
conf_filters_q5 = [
    ("All respondents", lambda r: True),
    ("Excl. estimate (certain+fairly-sure)", lambda r: r[COL_ADOPTION_CONF] in ("certain", "fairly-sure")),
    ("Certain only", lambda r: r[COL_ADOPTION_CONF] == "certain"),
]
for label, filt in conf_filters_q5:
    filtered = [r for r in rows if filt(r)]
    n_filt = len(filtered)
    n_high = sum(1 for r in filtered if r[COL_ADOPTION] in ("officially-approved", "most-developers"))
    print(f"    {label:40s} {pct_ci(n_high, n_filt)}")

# Q14: Policy
print(f"\n  Q14 Policy (% with specific or general policy):")
conf_filters_q14 = [
    ("All respondents", lambda r: True),
    ("Excl. estimate", lambda r: r[COL_POLICY_CONF] in ("certain", "fairly-sure")),
    ("Certain only", lambda r: r[COL_POLICY_CONF] == "certain"),
]
for label, filt in conf_filters_q14:
    filtered = [r for r in rows if filt(r)]
    n_filt = len(filtered)
    n_policy = sum(1 for r in filtered if r[COL_POLICY] in ("specific", "general"))
    print(f"    {label:40s} {pct_ci(n_policy, n_filt)}")

# --- 5b. Shadow Adoption Variants ---
print("\n  --- 5b. Shadow Adoption Summary Table ---")
print(f"\n  {'Metric':<35s} {'All':>20s} {'Cert+Fair':>20s} {'Certain':>20s}")
print(f"  {'-'*35} {'-'*20} {'-'*20} {'-'*20}")

for metric_name, exclude_set in [("Broad (all mismatches)", {"none", "unknown"}),
                                  ("Narrow (excl. browser/OSS)", {"none", "unknown", "browser-llm", "open-source"})]:
    row_vals = []
    for conf_label, conf_filter in confidence_filters:
        filtered_users_cf = [r for r in users_yes if conf_filter(r)]
        users_known = [r for r in filtered_users_cf
                       if "none" not in parse_multiselect(r[COL_APPROVED_TOOLS])
                       and "unknown" not in parse_multiselect(r[COL_APPROVED_TOOLS])]
        n_known = len(users_known)
        shadow_count = 0
        for r in users_known:
            approved = set(recode_tools(parse_multiselect(r[COL_APPROVED_TOOLS])))
            personal = set(recode_tools(parse_multiselect(r[COL_PERSONAL_TOOLS])))
            unapproved = personal - approved - exclude_set
            if unapproved:
                shadow_count += 1
        row_vals.append(pct(shadow_count, n_known) if n_known > 0 else "N/A")
    print(f"  {metric_name:<35s} {row_vals[0]:>20s} {row_vals[1]:>20s} {row_vals[2]:>20s}")

if HAS_ORG:
    # Robustness: compare personal tools with the union of tools any respondent in the
    # same org lists as approved (instead of the respondent's own approved list).
    org_approved_union = defaultdict(set)
    for r in rows:
        org_approved_union[r[COL_ORG]] |= set(recode_tools(parse_multiselect(r[COL_APPROVED_TOOLS])))
    users_known_all = [r for r in users_yes
                       if "none" not in parse_multiselect(r[COL_APPROVED_TOOLS])
                       and "unknown" not in parse_multiselect(r[COL_APPROVED_TOOLS])]
    broad_union = narrow_union = cc_own = cc_union_ok = 0
    for r in users_known_all:
        own = set(recode_tools(parse_multiselect(r[COL_APPROVED_TOOLS])))
        union = org_approved_union[r[COL_ORG]]
        personal = set(recode_tools(parse_multiselect(r[COL_PERSONAL_TOOLS])))
        broad_union += bool(personal - union - {"none", "unknown"})
        narrow_union += bool(personal - union - {"none", "unknown", "browser-llm", "open-source"})
        if "claude-code" in personal and "claude-code" not in own:
            cc_own += 1
            cc_union_ok += "claude-code" in union
    print(f"\n  Org-union robustness (approved = union over org respondents, n={len(users_known_all)}):")
    print(f"    Broad shadow:  {pct(broad_union, len(users_known_all))}")
    print(f"    Narrow shadow: {pct(narrow_union, len(users_known_all))}")
    print(f"    Claude Code shadow users: {cc_own}; of these, approved per another org respondent: {cc_union_ok}")
else:
    print(f"\n  Org-union robustness: " + ORG_NA)

# =============================================================================
# SECTION 6: DATA QUALITY & LIMITATIONS
# =============================================================================
print("\n\n" + "=" * 80)
print("  6. DATA QUALITY & LIMITATIONS")
print("=" * 80)

# Missing values
print("\n  Missing/empty values in key columns:")
key_cols_check = [
    (COL_ROLE, "Role (Q2)"),
    (COL_ADOPTION, "Adoption (Q5)"),
    (COL_ADOPTION_CONF, "Adoption confidence (Q5b)"),
    (COL_PERSONAL_USE, "Personal use (Q8)"),
    (COL_POLICY, "Policy (Q14)"),
]
for col_idx, col_name in key_cols_check:
    empty = sum(1 for r in rows if not r[col_idx].strip())
    print(f"    {col_name:30s} {empty} missing")

# Inconsistencies
inconsistent = sum(1 for r in rows if r[COL_PERSONAL_USE] == "no" and r[COL_PERSONAL_TOOLS].strip())
print(f"\n  Inconsistency: use='no' but tools listed: {inconsistent}")

# Non-users
non_users = [r for r in rows if r[COL_PERSONAL_USE] == "no"]
print(f"  Non-users (Q8='no'): {len(non_users)}")

if HAS_ORG:
    # Org-level aggregation limitations
    print(f"\n  Org-level aggregation notes:")
    print(f"    Total orgs: {N_ORGS}")
    print(f"    Single-respondent orgs: {len(orgs_single)} (no aggregation possible, single response = org value)")
    print(f"    Multi-respondent orgs: {len(orgs_multi)}")
    n_disagree_any = sum(1 for org_name, od in org_level.items()
                         if any(od.get(f"{col}_method") == "disagreement"
                                for _, col in governance_cols))
    print(f"    Orgs with disagreement on ≥1 governance indicator: {n_disagree_any}")
else:
    print(f"\n  Org-level aggregation notes: " + ORG_NA)

# Confidence notes
print(f"\n  Confidence impact:")
n_estimate_q5 = sum(1 for r in rows if r[COL_ADOPTION_CONF] == "estimate")
n_estimate_q6 = sum(1 for r in rows if r[COL_TOOLS_CONF] == "estimate")
n_estimate_q14 = sum(1 for r in rows if r[COL_POLICY_CONF] == "estimate")
print(f"    Q5 'estimate' responses: {n_estimate_q5}")
print(f"    Q6 'estimate' responses: {n_estimate_q6}")
print(f"    Q14 'estimate' responses: {n_estimate_q14}")

# Statistical limitations
print(f"\n  Statistical limitations:")
print(f"    - Fisher's exact tests are pairwise (practitioner vs combined leadership)")
print(f"      Full 2×3 tests require scipy (not used here)")
print(f"    - Spearman p-values are two-sided permutation p ({N_PERM} draws, seed {SEED})")
print(f"    - Multiple comparisons: {len(key_concerns_for_test)} Fisher tests performed")
print(f"      Bonferroni threshold: p < {0.05/len(key_concerns_for_test):.4f}")
print(f"    - Cramér's V thresholds: small ≈ 0.1, medium ≈ 0.3, large ≈ 0.5")
print(f"    - Wilson CIs provide better coverage than Wald for small-sample proportions")

# Interview opt-in
print("\n  Interview opt-in (Q24): not in the public CSV (column dropped)")

print("\n" + "=" * 80)
print("  END OF REPORT")
print("=" * 80)
