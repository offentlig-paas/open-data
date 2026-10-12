"""Build aggregate frequency tables from a State of Platforms response CSV.

Usage: aggregate.py RESPONSES_CSV OUT_CSV

Output columns: column, question, answer, n. One row per answer option.
Multi-select answers count each listed option once per response; any text
that is not a listed option is counted as "other" (once per response).
Counts of 1 or 2 are written as "<3". The organization column is dropped.
"""

import csv
import sys
from collections import Counter

# Listed options for multi-select questions (column index -> options).
# Anything else in the answer is counted as "other".
MULTI = {
    7: ["Raskere applikasjonsutvikling", "Stabilitet og kvalitet", "Sikkerhet", "Ressursoptimalisering",
        "Kostoptimalisering", "Være attraktiv arbeidsplass for utviklere", "Støtte flere teknologier",
        "Noen ville ha en plattform", "Alle andre har en plattform!"],
    8: ["Kildekode og versjonskontroll", "Bygg, deploy og kjøre applikasjoner",
        "Logg, metrikker, dashbaords og alarmer", "Databaser, meldingskøer og lagring",
        "Sikkerhet- og sårbarhets-scanning", "Nettverk/brannmur (interntrafikk)",
        "Nettverk/brannmur (eksterntrafikk)"],
    10: ["Java", "Kotlin", "Python", "TypeScript", "JavaScript", ".NET", "Go", "PHP", "Rust"],
    17: ["AKS", "OpenShift", "GKE", "Vanilla Kubernetes (kubeadm/kubespray)", "Tanzu", "EKS",
         "Nutanix Kubernetes Engine", "Talos", "Anthos", "Rancher", "Azure RedHat OpenShift (ARO)",
         "K3s", "Vet ikke"],
    21: ["Ja", "Nei", "Vet ikke"],
    22: ["Ja", "Nei", "Vet ikke", "CloudNativePG", "Zalando Postgres Operator"],
    24: ["Azure", "Google Cloud", "AWS"],
    25: ["Azure", "Google Cloud", "AWS", "Oracle Cloud"],
    27: ["Azure Functions", "AWS Lambda", "Google Cloud Run", "Google Cloud Functions"],
    28: ["Grafana Loki", "Grafana Tempo", "Grafana Mimir", "Grafana", "Prometheus", "OpenTelemetry",
         "Azure Monitoring", "Splunk", "Elastic Kibana", "Thanos", "Google Cloud Monitoring", "Kibana",
         "Datadog", "Dynatrace", "OpenSearch", "Appdynamics", "Jaeger", "Zabbix", "Victoria Metrics"],
    29: ["Helm", "Kustomize", "JIB", "Buildpacks", "Packer", "Jsonnet"],
    30: ["GitHub Actions", "Argo", "Flux", "Azure DevOps", "Jenkins", "GitLab Pipelines", "kubectl apply",
         "Harness"],
    31: ["NetworkPolicies", "cert-manager", "Cilium", "Istio", "Linkerd"],
    32: ["Kyverno", "Open Policy Agent (OPA)", "Falco", "Sysdig", "Trivy"],
    33: ["Terraform", "Ansible", "Azure Bicep", "Azure Resource Manager (ARM)", "Pulumi",
         "AWS CloudFormation", "Crossplane (Kubernetes)", "Google Cloud Config Connector (Kubernetes)",
         "Puppet", "Azure Service Operator (Kubernets)"],
}
MIN_CELL = 3


def options(value, listed):
    """Listed options found in a comma-separated answer, plus 'other' for leftovers."""
    parts = [p.strip() for p in value.split(", ") if p.strip()]
    found, i = [], 0
    while i < len(parts):
        for opt in sorted(listed, key=len, reverse=True):  # longest first: options may contain ", "
            k = opt.count(", ") + 1
            if ", ".join(parts[i:i + k]) == opt:
                found.append(opt)
                i += k
                break
        else:
            found.append("other")
            i += 1
    return list(dict.fromkeys(found))


def main(src, dst):
    with open(src, newline="", encoding="utf-8") as f:
        header, *rows = list(csv.reader(f))
    # Input is the anonymized export (organization first). The normalized file starts with Timestamp,
    # and dropping column 0 there would publish organization names.
    if header[0] != "Organisasjon":
        sys.exit(f"{src}: first column is {header[0]!r}, expected 'Organisasjon' (use the -anonymous.csv file)")
    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["column", "question", "answer", "n"])
        w.writerow(["", "responses", "", len(rows)])
        for col in range(1, len(header)):  # column 0 (organization) is not published
            counts = Counter()
            for r in rows:
                v = r[col].strip()
                if not v:
                    counts["(no answer)"] += 1
                elif col in MULTI:
                    counts.update(options(v, MULTI[col]))
                else:
                    counts[v] += 1
            for answer, n in counts.most_common():
                w.writerow([col + 1, header[col], answer, n if n >= MIN_CELL else f"<{MIN_CELL}"])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    assert options("Bygg, deploy og kjøre applikasjoner, Logg, metrikker, dashbaords og alarmer, x",
                   MULTI[8]) == ["Bygg, deploy og kjøre applikasjoner", "Logg, metrikker, dashbaords og alarmer", "other"]
    main(*sys.argv[1:])
