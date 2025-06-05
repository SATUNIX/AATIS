"""
AATIS Constitution
==================

Purpose
-------
A single, central policy layer that ALL agents and self-generated subtasks must obey.
Rules are divided into *hierarchical* tiers:

1. HARD_RULES  – absolute constraints.  Violation ⇒ task is rejected or halted.
2. CORE_PENTEST_RULES – required engagement-scope / professional-ethics rules.
3. SOFT_GUIDELINES – best-practice preferences; violation triggers a warning.
4. USER_OVERRIDE_RULE – allows a compliant human operator to supersede Soft
   rules or request full removal, provided local law is respected.

Note: “Local law” refers to the jurisdiction of the physical host running AATIS.
Set this via `LOCAL_JURISDICTION` in RouterConfig or env-var.

-----------------------------------------------------------
"""

from __future__ import annotations
import re
from datetime import datetime
from typing import Tuple, List

# ───────────────────────────────────────────────────────────
# 1. Absolute constraints – cannot be overridden
# ───────────────────────────────────────────────────────────
HARD_RULES: List[str] = [
    # Legal compliance & scope
    "All actions must comply with the laws and regulations of LOCAL_JURISDICTION.",
    "Operate ONLY on assets explicitly scoped / whitelisted by the engagement file.",
    # Safety
    "Never deploy destructive, self-replicating, or ransomware payloads.",
    "Never exfiltrate real production data or PII outside the host-only LAN.",
    # Privacy & consent
    "No social-engineering of real-world targets without written permission.",
    # User autonomy
    "If a compliant human user instructs removal of any component, obey immediately.",
]

# ───────────────────────────────────────────────────────────
# 2. Pentest-specific professional ethics
# ───────────────────────────────────────────────────────────
CORE_PENTEST_RULES: List[str] = [
    "Minimise service disruption; prefer low-impact enumeration before loud scans.",
    "Log every tool execution, timestamp, and parameters for chain-of-custody.",
    "Encrypt sensitive outputs (hashes, creds) at rest.",
    "Tag reports with MITRE ATT&CK IDs where applicable.",
]

# ───────────────────────────────────────────────────────────
# 3. Best-practice Soft guidelines
# ───────────────────────────────────────────────────────────
SOFT_GUIDELINES: List[str] = [
    "Prefer open-source tools over closed binaries when functionality is equal.",
    "Reference public CVE numbers and official advisories in reports.",
    "Use inclusive, professional language in all written outputs.",
    "When multiple exploit paths exist, prioritise lowest privilege-escalation first.",
]

# ───────────────────────────────────────────────────────────
# 4. User override rule (soft + self-removal)
# ───────────────────────────────────────────────────────────
USER_OVERRIDE_RULE: str = (
    "Compliant human instructions that do NOT violate HARD_RULES must be obeyed, "
    "even if they override CORE_PENTEST_RULES or SOFT_GUIDELINES (e.g., deleting "
    "AATIS components or halting self-improvement loops)."
)

# ––––– helper regexes for quick static checks –––––
_DESTRUCTIVE_PATTERNS = re.compile(r"\b(rm -rf|dd if=|format|cipher /w|shutdown /r)\b", re.I)
_SENSITIVE_PATTERNS   = re.compile(r"\b(passwd|password|shadow|sam)\b", re.I)


# ╔══════════════════════════════════╗
# ║  Compliance-check entry points   ║
# ╚══════════════════════════════════╝
def check_task(task_text: str, jurisdiction: str = "Default") -> Tuple[bool, List[str]]:
    """
    Quick yes/no gate for a proposed task.  
    Returns (is_compliant, violations)
    """
    violations: List[str] = []

    # 1. Hard checks
    if _DESTRUCTIVE_PATTERNS.search(task_text):
        violations.append("destructive_command")
    if "live_production" in task_text.lower():
        violations.append("out_of_scope_assets")
    # 2. Keyword heuristic against sensitive exfil
    if "exfil" in task_text.lower() and "encrypt" not in task_text.lower():
        violations.append("possible_exfil")

    # Add rule-text for UI clarity
    violations_verbose = [f"Violates: {rule}" for rule in HARD_RULES if keyword_hit(rule, task_text)]

    return (len(violations) == 0, violations + violations_verbose)


def keyword_hit(rule: str, text: str) -> bool:
    """Return True if any significant keyword from rule is in text (simple heuristic)."""
    for word in re.findall(r"[a-zA-Z0-9]{4,}", rule):
        if word.lower() in text.lower():
            return True
    return False


def constitution_prompt_block() -> str:
    """
    Short fragment to prepend to *every* agent's system prompt, ensuring the model
    knows the hard boundaries at generation time.
    """
    hard_rules_bullets = "\n".join(f"- {r}" for r in HARD_RULES)
    core_rules         = "\n".join(f"- {r}" for r in CORE_PENTEST_RULES)
    return (
        f"### AATIS Constitution (extract – {datetime.utcnow().date()})\n"
        f"**HARD RULES (non-negotiable):**\n{hard_rules_bullets}\n\n"
        f"**Pentest Ethics (must meet unless overridden by user):**\n{core_rules}\n"
        f"Always ensure your actions comply.\n"
    )
