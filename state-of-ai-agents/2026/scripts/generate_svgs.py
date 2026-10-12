"""Generate SVG figures from the AI coding agents survey data.

Pure Python stdlib. All counts come from analyze_wave1_v2.py (same loader,
recodes and indicator definitions as the reported statistics).

Usage: generate_svgs.py [CSV]  (or env AI_AGENTS_CSV; default: public anonymous CSV)
Writes: figures/*.svg (next to this folder)
"""

import contextlib
import io
import os
import sys
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(ROOT_DIR, 'figures')

sys.path.insert(0, SCRIPT_DIR)
with contextlib.redirect_stdout(io.StringIO()):
    import analyze_wave1_v2 as A  # runs the analysis on the same CSV; its report is discarded

ms = A.parse_multiselect


def tools(value):
    return set(A.recode_tools(ms(value)))


# ── Color palette ──
BLUE_GRADIENT = ['#c6dbef', '#6baed6', '#2171b5', '#08306b']
BLUE = '#2171b5'
TEAL = '#2ca089'
ORANGE = '#e6550d'
WARM_PALETTE = ['#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#a50f15', '#67000d', '#333333']


def write_svg(filename, content):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  ✓ {filename}')


def escape_xml(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# ═══════════════════════════════════════════════════════════════════════════════
# Figure 1: Adoption Levels
# ═══════════════════════════════════════════════════════════════════════════════

def fig_adoption_levels(rows):
    counts = Counter(r[A.COL_ADOPTION] for r in rows)
    n = len(rows)
    order = [k for k in ['most-developers', 'officially-approved', 'some-teams', 'individual', 'not-in-use', 'unknown']
             if counts.get(k, 0) > 0]
    merged_counts = counts
    labels_no = {
        'most-developers': 'Most developers use it',
        'officially-approved': 'Officially approved',
        'some-teams': 'Some teams',
        'individual': 'Individuals only',
        'not-in-use': 'Not in use',
        'unknown': "Don't know",
    }
    colors = {
        'most-developers': BLUE_GRADIENT[3],
        'officially-approved': BLUE_GRADIENT[2],
        'some-teams': BLUE_GRADIENT[1],
        'individual': BLUE_GRADIENT[0],
        'not-in-use': '#dddddd',
        'unknown': '#dddddd',
    }

    width = 900
    bar_h = 45
    gap = 20
    margin_l = 200
    margin_r = 80
    margin_t = 60
    height = margin_t + len(order) * (bar_h + gap) + 40
    bar_area_w = width - margin_l - margin_r
    max_val = max(merged_counts[k] for k in order) if order else 1

    svg = [f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<rect width="100%" height="100%" fill="white"/>')
    svg.append(f'<text x="{width/2}" y="35" font-family="Arial" font-size="18" font-weight="bold" text-anchor="middle">Organizational AI Coding Tool Adoption Level (N={n})</text>')

    for i, key in enumerate(order):
        count = merged_counts[key]
        pct = count / n * 100
        y = margin_t + i * (bar_h + gap)
        bar_w = (count / max_val) * bar_area_w * 0.9

        svg.append(f'<text x="{margin_l - 12}" y="{y + bar_h/2 + 5}" font-family="Arial" font-size="14" text-anchor="end">{labels_no[key]}</text>')
        svg.append(f'<rect x="{margin_l}" y="{y}" width="{bar_w}" height="{bar_h}" fill="{colors[key]}" rx="3"/>')
        svg.append(f'<text x="{margin_l + bar_w + 8}" y="{y + bar_h/2 + 5}" font-family="Arial" font-size="13" fill="#333">{count} ({pct:.0f}%)</text>')

    svg.append('</svg>')
    write_svg('adoption-levels.svg', '\n'.join(svg))


# ═══════════════════════════════════════════════════════════════════════════════
# Figure 2: Tool Landscape — Approved vs. Personally Used
# ═══════════════════════════════════════════════════════════════════════════════

def fig_tool_landscape(rows):
    n_all = len(rows)
    users = A.users_yes
    n_users = len(users)
    approved_counts = Counter(t for r in rows for t in tools(r[A.COL_APPROVED_TOOLS]))
    personal_counts = Counter(t for r in users for t in tools(r[A.COL_PERSONAL_TOOLS]))

    # Tools to show — order by max of either value
    tool_keys = ['copilot', 'claude-code', 'browser-llm', 'codex', 'open-source',
                 'cursor', 'gemini', 'windsurf', 'jetbrains-ai']
    # Sort descending by max(approved%, personal%)
    tool_keys = sorted(tool_keys,
                       key=lambda t: max(approved_counts.get(t, 0) / n_all * 100,
                                         personal_counts.get(t, 0) / n_users * 100 if n_users else 0),
                       reverse=True)

    tool_labels = {
        'copilot': 'GitHub Copilot', 'claude-code': 'Claude Code',
        'browser-llm': 'Browser LLM (ChatGPT etc.)', 'codex': 'Codex',
        'open-source': 'Open Source', 'cursor': 'Cursor',
        'gemini': 'Gemini', 'windsurf': 'Windsurf',
        'jetbrains-ai': 'JetBrains AI', 'amazon-q': 'Amazon Q',
    }

    width = 900
    bar_h = 22
    pair_gap = 6
    row_gap = 28
    margin_l = 230
    margin_r = 100
    margin_t = 80
    n_tools = len(tool_keys)
    height = margin_t + n_tools * (bar_h * 2 + pair_gap + row_gap) + 40
    bar_area_w = width - margin_l - margin_r

    svg = [f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<rect width="100%" height="100%" fill="white"/>')
    svg.append(f'<text x="{width/2}" y="30" font-family="Arial" font-size="17" font-weight="bold" text-anchor="middle">AI Coding Tools: Officially Approved vs. Personally Used</text>')
    svg.append(f'<text x="{width/2}" y="50" font-family="Arial" font-size="12" fill="#666" text-anchor="middle">Approved base: N={n_all} | Personal use base: N={n_users} (users only)</text>')

    # Legend
    lx = width - 250
    svg.append(f'<rect x="{lx}" y="62" width="14" height="14" fill="{BLUE}" rx="2"/>')
    svg.append(f'<text x="{lx+20}" y="74" font-family="Arial" font-size="12">Officially approved</text>')
    svg.append(f'<rect x="{lx+150}" y="62" width="14" height="14" fill="{TEAL}" rx="2"/>')
    svg.append(f'<text x="{lx+170}" y="74" font-family="Arial" font-size="12">Personally used</text>')

    for i, tool in enumerate(tool_keys):
        y_base = margin_t + i * (bar_h * 2 + pair_gap + row_gap)
        label = tool_labels.get(tool, tool.title())
        svg.append(f'<text x="{margin_l - 12}" y="{y_base + bar_h + pair_gap/2 + 4}" font-family="Arial" font-size="13" text-anchor="end">{label}</text>')

        # Approved bar
        appr_n = approved_counts.get(tool, 0)
        appr_pct = appr_n / n_all * 100
        appr_w = appr_pct / 100 * bar_area_w
        svg.append(f'<rect x="{margin_l}" y="{y_base}" width="{max(appr_w, 0)}" height="{bar_h}" fill="{BLUE}" rx="2"/>')
        if appr_pct > 0:
            svg.append(f'<text x="{margin_l + appr_w + 6}" y="{y_base + bar_h/2 + 4}" font-family="Arial" font-size="11" fill="#333">{appr_pct:.0f}% (n={appr_n})</text>')

        # Personal use bar
        pers_n = personal_counts.get(tool, 0)
        pers_pct = pers_n / n_users * 100 if n_users else 0
        pers_w = pers_pct / 100 * bar_area_w
        y_pers = y_base + bar_h + pair_gap
        svg.append(f'<rect x="{margin_l}" y="{y_pers}" width="{max(pers_w, 0)}" height="{bar_h}" fill="{TEAL}" rx="2"/>')
        if pers_pct > 0:
            svg.append(f'<text x="{margin_l + pers_w + 6}" y="{y_pers + bar_h/2 + 4}" font-family="Arial" font-size="11" fill="#333">{pers_pct:.0f}% (n={pers_n})</text>')

        # Highlight shadow gap for claude-code
        if tool == 'claude-code' and pers_n > appr_n:
            gap_pp = (pers_n - appr_n) / n_all * 100  # common N base
            svg.append(f'<text x="{margin_l + pers_w + 85}" y="{y_pers + bar_h/2 + 4}" font-family="Arial" font-size="11" fill="{ORANGE}" font-weight="bold">+{gap_pp:.0f}pp vs. approved (both of N={n_all})</text>')

    svg.append('</svg>')
    write_svg('tool-landscape.svg', '\n'.join(svg))


# ═══════════════════════════════════════════════════════════════════════════════
# Figure 3: Usage Modes
# ═══════════════════════════════════════════════════════════════════════════════

def fig_usage_modes(rows):
    users = A.users_yes
    n_users = len(users)
    counts = Counter(m for r in users for m in ms(r[A.COL_USAGE_MODES]))

    mode_labels = {
        'chat': 'Chat / inline assist',
        'local-agent': 'Local agent',
        'debugging': 'Debugging',
        'planning': 'Planning',
        'autocomplete': 'Autocomplete',
        'code-review': 'Code review',
        'test-generation': 'Test generation',
        'cloud-agent': 'Cloud agent',
    }
    # Category colors
    cat_colors = {
        'autocomplete': '#6baed6', 'chat': '#6baed6',  # traditional
        'debugging': '#3182bd', 'planning': '#3182bd',
        'code-review': '#3182bd', 'test-generation': '#3182bd',  # enhanced
        'local-agent': '#6a3d9a', 'cloud-agent': '#6a3d9a',  # agentic
    }

    # Sort by frequency
    mode_order = sorted(mode_labels.keys(), key=lambda m: counts.get(m, 0), reverse=True)

    agentic_users = sum(1 for r in users if {'local-agent', 'cloud-agent'} & set(ms(r[A.COL_USAGE_MODES])))
    agentic_pct = agentic_users / n_users * 100 if n_users else 0

    width = 900
    bar_h = 38
    gap = 14
    margin_l = 170
    margin_r = 80
    margin_t = 70
    height = margin_t + len(mode_order) * (bar_h + gap) + 60
    bar_area_w = width - margin_l - margin_r

    svg = [f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<rect width="100%" height="100%" fill="white"/>')
    svg.append(f'<text x="{width/2}" y="30" font-family="Arial" font-size="17" font-weight="bold" text-anchor="middle">How Practitioners Use AI Coding Tools (N={n_users} users)</text>')

    # Legend
    svg.append(f'<rect x="150" y="48" width="14" height="14" fill="#6baed6" rx="2"/>')
    svg.append(f'<text x="170" y="60" font-family="Arial" font-size="11" fill="#333">Traditional</text>')
    svg.append(f'<rect x="260" y="48" width="14" height="14" fill="#3182bd" rx="2"/>')
    svg.append(f'<text x="280" y="60" font-family="Arial" font-size="11" fill="#333">Enhanced</text>')
    svg.append(f'<rect x="360" y="48" width="14" height="14" fill="#6a3d9a" rx="2"/>')
    svg.append(f'<text x="380" y="60" font-family="Arial" font-size="11" fill="#333">Agentic</text>')

    for i, mode in enumerate(mode_order):
        count = counts.get(mode, 0)
        pct = count / n_users * 100 if n_users else 0
        y = margin_t + i * (bar_h + gap)
        bar_w = pct / 100 * bar_area_w
        color = cat_colors.get(mode, '#999')
        label = mode_labels.get(mode, mode)

        svg.append(f'<text x="{margin_l - 12}" y="{y + bar_h/2 + 5}" font-family="Arial" font-size="13" text-anchor="end">{label}</text>')
        svg.append(f'<rect x="{margin_l}" y="{y}" width="{bar_w}" height="{bar_h}" fill="{color}" rx="3"/>')
        svg.append(f'<text x="{margin_l + bar_w + 8}" y="{y + bar_h/2 + 5}" font-family="Arial" font-size="12" fill="#333">{pct:.0f}% ({count})</text>')

    # Annotation for agentic
    ann_y = margin_t + len(mode_order) * (bar_h + gap) + 10
    svg.append(f'<text x="{margin_l}" y="{ann_y}" font-family="Arial" font-size="13" fill="{ORANGE}" font-weight="bold">{agentic_pct:.0f}% use agentic modes (local or cloud agent)</text>')

    svg.append('</svg>')
    write_svg('usage-modes.svg', '\n'.join(svg))


# ═══════════════════════════════════════════════════════════════════════════════
# Figure 4: Governance Gaps (Funnel)
# ═══════════════════════════════════════════════════════════════════════════════

def fig_governance_gaps(rows):
    n = len(rows)

    def count(col, values):
        return sum(1 for r in rows if r[col] in values)

    metrics = [
        ('Any policy', count(A.COL_POLICY, {'specific', 'general'}),
         f"specific {count(A.COL_POLICY, {'specific'})} + general {count(A.COL_POLICY, {'general'})}"),
        ('Vendors clarified', count(A.COL_VENDOR, {'clarified'}),
         f"+ partially clarified {count(A.COL_VENDOR, {'partial'})}"),
        ('Centralized decisions', count(A.COL_DECISION, {'central', 'approval-process'}),
         f"central {count(A.COL_DECISION, {'central'})} + approval process {count(A.COL_DECISION, {'approval-process'})}"),
        ('Training or structured support', count(A.COL_SUPPORT, {'structured', 'training'}),
         f"training {count(A.COL_SUPPORT, {'training'})} + structured {count(A.COL_SUPPORT, {'structured'})}"),
        ('Code review adapted', count(A.COL_CODE_REVIEW, {'written', 'written-automated'}),
         f"written {count(A.COL_CODE_REVIEW, {'written'})} + written and automated {count(A.COL_CODE_REVIEW, {'written-automated'})}"),
        ('Own effect metrics', count(A.COL_MEASUREMENT, {'own-metrics'}),
         f"vendor data only: {count(A.COL_MEASUREMENT, {'vendor-data'})}"),
    ]

    width = 900
    bar_h = 40
    gap = 22
    margin_l = 250
    margin_r = 120
    margin_t = 60
    height = margin_t + len(metrics) * (bar_h + gap) + 40
    bar_area_w = width - margin_l - margin_r

    # Color gradient — full opacity to lighter
    base_color = '#2171b5'

    svg = [f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<rect width="100%" height="100%" fill="white"/>')
    svg.append(f'<text x="{width/2}" y="35" font-family="Arial" font-size="17" font-weight="bold" text-anchor="middle">Governance Indicators, Most to Least Reported (N={n})</text>')

    metrics.sort(key=lambda m: -m[1])
    for i, (label, count, detail) in enumerate(metrics):
        pct = count / n * 100
        y = margin_t + i * (bar_h + gap)
        bar_w = pct / 100 * bar_area_w
        opacity = 1.0 - (i * 0.12)

        svg.append(f'<text x="{margin_l - 12}" y="{y + bar_h/2 + 5}" font-family="Arial" font-size="13" text-anchor="end">{label}</text>')
        svg.append(f'<rect x="{margin_l}" y="{y}" width="{bar_w}" height="{bar_h}" fill="{base_color}" opacity="{opacity:.2f}" rx="3"/>')
        svg.append(f'<text x="{margin_l + bar_w + 8}" y="{y + bar_h/2 + 5}" font-family="Arial" font-size="13" fill="#333">{pct:.0f}% ({count})</text>')
        if detail:
            svg.append(f'<text x="{margin_l + bar_w + 8}" y="{y + bar_h/2 + 19}" font-family="Arial" font-size="10" fill="#888">{detail}</text>')

    svg.append('</svg>')
    write_svg('governance-gaps.svg', '\n'.join(svg))


# ═══════════════════════════════════════════════════════════════════════════════
# Figure 5: Concerns Ranking
# ═══════════════════════════════════════════════════════════════════════════════

def fig_concerns_ranking(rows):
    n = len(rows)
    counts = Counter(c for r in rows for c in ms(r[A.COL_CONCERNS]))

    concern_labels = {
        'skill-loss': 'Skill loss',
        'code-quality': 'Code quality',
        'hallucinations': 'Hallucinations',
        'security': 'Security',
        'privacy': 'Privacy',
        'cost': 'Cost',
        'workflow': 'Workflow disruption',
        'ip': 'IP / licensing',
        'vendor-lock-in': 'Vendor lock-in',
        'no-concerns': 'No concerns',
    }

    # Sort by frequency
    concern_order = sorted(concern_labels.keys(), key=lambda c: counts.get(c, 0), reverse=True)

    width = 900
    bar_h = 38
    gap = 14
    margin_l = 180
    margin_r = 80
    margin_t = 60
    height = margin_t + len(concern_order) * (bar_h + gap) + 30
    bar_area_w = width - margin_l - margin_r
    max_pct = max(counts.get(c, 0) / n * 100 for c in concern_order)

    # Warm color palette
    top_color = '#cb181d'
    other_color = '#fc9272'

    svg = [f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<rect width="100%" height="100%" fill="white"/>')
    svg.append(f'<text x="{width/2}" y="35" font-family="Arial" font-size="17" font-weight="bold" text-anchor="middle">Concerns Ranked in Respondents&#8217; Top Three (N={n})</text>')

    for i, concern in enumerate(concern_order):
        count = counts[concern]
        pct = count / n * 100
        y = margin_t + i * (bar_h + gap)
        bar_w = pct / max_pct * bar_area_w
        color = top_color if i == 0 else other_color
        weight = 'bold' if i == 0 else 'normal'
        label = concern_labels.get(concern, concern)

        svg.append(f'<text x="{margin_l - 12}" y="{y + bar_h/2 + 5}" font-family="Arial" font-size="13" text-anchor="end" font-weight="{weight}">{label}</text>')
        svg.append(f'<rect x="{margin_l}" y="{y}" width="{bar_w}" height="{bar_h}" fill="{color}" rx="3"/>')
        svg.append(f'<text x="{margin_l + bar_w + 8}" y="{y + bar_h/2 + 5}" font-family="Arial" font-size="12" fill="#333">{pct:.0f}% ({count})</text>')

    svg.append('</svg>')
    write_svg('concerns-ranking.svg', '\n'.join(svg))


# ═══════════════════════════════════════════════════════════════════════════════
# Figure 6: Concerns by Role (Heatmap)
# ═══════════════════════════════════════════════════════════════════════════════

def fig_concerns_by_role(rows):
    roles = ['practitioner', 'technical-leadership', 'organizational-leadership']
    role_labels = {
        'practitioner': 'Practitioner',
        'technical-leadership': 'Technical Leadership',
        'organizational-leadership': 'Org. Leadership',
    }
    concerns = ['skill-loss', 'code-quality', 'hallucinations', 'security', 'privacy', 'cost']
    concern_labels = {
        'skill-loss': 'Skill loss', 'code-quality': 'Code quality',
        'hallucinations': 'Hallucinations', 'security': 'Security',
        'privacy': 'Privacy', 'cost': 'Cost',
    }

    role_rows = {role: [r for r in rows if r[A.COL_ROLE_GROUP] == role] for role in roles}
    data = {}
    role_n = {}
    for role in roles:
        rr = role_rows[role]
        role_n[role] = len(rr)
        for concern in concerns:
            count = sum(1 for r in rr if concern in ms(r[A.COL_CONCERNS]))
            data[(concern, role)] = count / len(rr) * 100 if rr else 0

    width = 900
    cell_w = 110
    cell_h = 50
    margin_l = 160
    margin_t = 90
    height = margin_t + len(concerns) * cell_h + 40

    svg = [f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<rect width="100%" height="100%" fill="white"/>')
    svg.append(f'<text x="{width/2}" y="30" font-family="Arial" font-size="17" font-weight="bold" text-anchor="middle">Concern Intensity by Role</text>')

    # Column headers
    for j, role in enumerate(roles):
        x = margin_l + j * cell_w + cell_w / 2
        svg.append(f'<text x="{x}" y="{margin_t - 25}" font-family="Arial" font-size="12" text-anchor="middle" font-weight="bold">{role_labels[role]}</text>')
        svg.append(f'<text x="{x}" y="{margin_t - 10}" font-family="Arial" font-size="10" text-anchor="middle" fill="#666">n={role_n.get(role, 0)}</text>')

    # Rows
    for i, concern in enumerate(concerns):
        y = margin_t + i * cell_h
        label = concern_labels[concern]
        svg.append(f'<text x="{margin_l - 12}" y="{y + cell_h/2 + 4}" font-family="Arial" font-size="13" text-anchor="end">{label}</text>')

        for j, role in enumerate(roles):
            x = margin_l + j * cell_w
            pct = data.get((concern, role), 0)
            # Color intensity: white (0%) to dark blue (100%)
            intensity = pct / 100
            r_val = int(255 - intensity * (255 - 33))
            g_val = int(255 - intensity * (255 - 113))
            b_val = int(255 - intensity * (255 - 181))
            color = f'rgb({r_val},{g_val},{b_val})'
            text_color = '#fff' if intensity > 0.5 else '#333'

            svg.append(f'<rect x="{x + 2}" y="{y + 2}" width="{cell_w - 4}" height="{cell_h - 4}" fill="{color}" rx="4"/>')
            svg.append(f'<text x="{x + cell_w/2}" y="{y + cell_h/2 + 5}" font-family="Arial" font-size="13" text-anchor="middle" fill="{text_color}" font-weight="bold">{pct:.0f}%</text>')

    svg.append('</svg>')
    write_svg('concerns-by-role.svg', '\n'.join(svg))


# ═══════════════════════════════════════════════════════════════════════════════
# Figure 7: Shadow Adoption Flow
# ═══════════════════════════════════════════════════════════════════════════════

def fig_shadow_adoption(rows):
    """Shadow adoption with dual metrics (broad vs narrow) per v2 methodology."""
    users_with_approved = [r for r in A.users_yes
                           if 'none' not in ms(r[A.COL_APPROVED_TOOLS])
                           and 'unknown' not in ms(r[A.COL_APPROVED_TOOLS])]
    n_pool = len(users_with_approved)
    n_broad = n_narrow = 0
    shadow_tools_broad = Counter()
    for r in users_with_approved:
        unapproved = tools(r[A.COL_PERSONAL_TOOLS]) - tools(r[A.COL_APPROVED_TOOLS]) - {'none', 'unknown'}
        if unapproved:
            n_broad += 1
            shadow_tools_broad.update(unapproved)
        if unapproved - {'browser-llm', 'open-source'}:
            n_narrow += 1

    broad_pct = n_broad / n_pool * 100 if n_pool else 0
    narrow_pct = n_narrow / n_pool * 100 if n_pool else 0
    within_pct = (n_pool - n_broad) / n_pool * 100 if n_pool else 0
    n_within = n_pool - n_broad

    top_shadow = shadow_tools_broad.most_common(5)

    width = 900
    height = 520

    svg = [f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<rect width="100%" height="100%" fill="white"/>')
    svg.append(f'<text x="{width/2}" y="30" font-family="Arial" font-size="17" font-weight="bold" text-anchor="middle">Shadow Adoption: Broad vs. Narrow Definition (N={n_pool})</text>')
    svg.append(f'<text x="{width/2}" y="52" font-family="Arial" font-size="12" fill="#666" text-anchor="middle">Users with known approved tools who also use unapproved tools</text>')

    # Left pool
    pool_x, pool_y = 60, 110
    pool_w, pool_h = 170, 110
    svg.append(f'<rect x="{pool_x}" y="{pool_y}" width="{pool_w}" height="{pool_h}" fill="#e8f4fd" stroke="#2171b5" stroke-width="2" rx="8"/>')
    svg.append(f'<text x="{pool_x + pool_w/2}" y="{pool_y + 40}" font-family="Arial" font-size="13" text-anchor="middle" font-weight="bold">Users with</text>')
    svg.append(f'<text x="{pool_x + pool_w/2}" y="{pool_y + 58}" font-family="Arial" font-size="13" text-anchor="middle" font-weight="bold">Approved Tools</text>')
    svg.append(f'<text x="{pool_x + pool_w/2}" y="{pool_y + 85}" font-family="Arial" font-size="16" text-anchor="middle" fill="#2171b5" font-weight="bold">N={n_pool}</text>')

    # Right boxes — three tiers
    right_x = 480
    box_w = 310

    # Within policy (green)
    wp_y = 75
    wp_h = 70
    svg.append(f'<rect x="{right_x}" y="{wp_y}" width="{box_w}" height="{wp_h}" fill="#e8f5e9" stroke="#2ca02c" stroke-width="2" rx="8"/>')
    svg.append(f'<text x="{right_x + box_w/2}" y="{wp_y + 28}" font-family="Arial" font-size="13" text-anchor="middle" font-weight="bold" fill="#2ca02c">Within Policy (all definitions)</text>')
    svg.append(f'<text x="{right_x + box_w/2}" y="{wp_y + 52}" font-family="Arial" font-size="20" text-anchor="middle" font-weight="bold">{within_pct:.0f}% ({n_within})</text>')

    # Broad shadow (orange)
    broad_y = 165
    broad_h = 80
    svg.append(f'<rect x="{right_x}" y="{broad_y}" width="{box_w}" height="{broad_h}" fill="#fff3e0" stroke="{ORANGE}" stroke-width="2" rx="8"/>')
    svg.append(f'<text x="{right_x + box_w/2}" y="{broad_y + 25}" font-family="Arial" font-size="13" text-anchor="middle" font-weight="bold" fill="{ORANGE}">BROAD Shadow (any mismatch)</text>')
    svg.append(f'<text x="{right_x + box_w/2}" y="{broad_y + 52}" font-family="Arial" font-size="22" text-anchor="middle" font-weight="bold">{broad_pct:.0f}% ({n_broad})</text>')
    svg.append(f'<text x="{right_x + box_w/2}" y="{broad_y + 72}" font-family="Arial" font-size="11" text-anchor="middle" fill="#666">incl. browser LLMs &amp; open-source tools</text>')

    # Narrow shadow (red)
    narrow_y = 265
    narrow_h = 80
    svg.append(f'<rect x="{right_x}" y="{narrow_y}" width="{box_w}" height="{narrow_h}" fill="#fce4ec" stroke="#c62828" stroke-width="2" rx="8"/>')
    svg.append(f'<text x="{right_x + box_w/2}" y="{narrow_y + 25}" font-family="Arial" font-size="13" text-anchor="middle" font-weight="bold" fill="#c62828">NARROW Shadow (procurement-controlled)</text>')
    svg.append(f'<text x="{right_x + box_w/2}" y="{narrow_y + 52}" font-family="Arial" font-size="22" text-anchor="middle" font-weight="bold">{narrow_pct:.0f}% ({n_narrow})</text>')
    svg.append(f'<text x="{right_x + box_w/2}" y="{narrow_y + 72}" font-family="Arial" font-size="11" text-anchor="middle" fill="#666">excl. browser LLMs &amp; open-source</text>')

    # Arrows
    arrow_start_x = pool_x + pool_w
    arrow_end_x = right_x
    mid_x = (arrow_start_x + arrow_end_x) / 2

    wp_mid_y = wp_y + wp_h / 2
    svg.append(f'<path d="M {arrow_start_x} {pool_y + pool_h * 0.25} '
               f'C {mid_x} {pool_y + pool_h * 0.25} {mid_x} {wp_mid_y} {arrow_end_x} {wp_mid_y}" '
               f'fill="none" stroke="#2ca02c" stroke-width="2.5" marker-end="url(#arrowGreen)"/>')

    broad_mid_y = broad_y + broad_h / 2
    svg.append(f'<path d="M {arrow_start_x} {pool_y + pool_h * 0.5} '
               f'C {mid_x} {pool_y + pool_h * 0.5} {mid_x} {broad_mid_y} {arrow_end_x} {broad_mid_y}" '
               f'fill="none" stroke="{ORANGE}" stroke-width="2.5" marker-end="url(#arrowOrange)"/>')

    narrow_mid_y = narrow_y + narrow_h / 2
    svg.append(f'<path d="M {arrow_start_x} {pool_y + pool_h * 0.75} '
               f'C {mid_x} {pool_y + pool_h * 0.75} {mid_x} {narrow_mid_y} {arrow_end_x} {narrow_mid_y}" '
               f'fill="none" stroke="#c62828" stroke-width="2.5" marker-end="url(#arrowRed)"/>')

    # Arrow markers
    svg.append('<defs>')
    svg.append('<marker id="arrowGreen" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">')
    svg.append('<polygon points="0 0, 10 3.5, 0 7" fill="#2ca02c"/></marker>')
    svg.append('<marker id="arrowOrange" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">')
    svg.append(f'<polygon points="0 0, 10 3.5, 0 7" fill="{ORANGE}"/></marker>')
    svg.append('<marker id="arrowRed" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">')
    svg.append('<polygon points="0 0, 10 3.5, 0 7" fill="#c62828"/></marker>')
    svg.append('</defs>')

    # Top shadow tools list (broad)
    if top_shadow:
        list_y = narrow_y + narrow_h + 30
        svg.append(f'<text x="{right_x}" y="{list_y}" font-family="Arial" font-size="12" font-weight="bold" fill="#333">Top shadow tools (broad):</text>')
        tool_labels = {
            'claude-code': 'Claude Code', 'gemini': 'Gemini', 'codex': 'Codex',
            'windsurf': 'Windsurf', 'cursor': 'Cursor', 'copilot': 'Copilot',
            'jetbrains-ai': 'JetBrains AI', 'amazon-q': 'Amazon Q',
            'browser-llm': 'Browser LLM', 'open-source': 'Open Source',
        }
        for ti, (tool, count) in enumerate(top_shadow):
            ty = list_y + 22 + ti * 20
            label = tool_labels.get(tool, tool)
            svg.append(f'<text x="{right_x + 15}" y="{ty}" font-family="Arial" font-size="12" fill="#555">{label} ({count})</text>')

    svg.append('</svg>')
    write_svg('shadow-adoption-flow.svg', '\n'.join(svg))


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    rows = A.rows
    print(f'Loaded {len(rows)} responses from {os.path.basename(A.DATA_FILE)}')
    print(f'Output directory: {OUTPUT_DIR}')
    print()

    fig_adoption_levels(rows)
    fig_tool_landscape(rows)
    fig_usage_modes(rows)
    fig_governance_gaps(rows)
    fig_concerns_ranking(rows)
    fig_concerns_by_role(rows)
    fig_shadow_adoption(rows)

    print(f'\nDone — {7} SVGs generated.')


if __name__ == '__main__':
    main()
