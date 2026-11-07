"""System Design native Hermes registration; Python standard library only."""
from pathlib import Path
import re


def register(ctx):
    here = Path(__file__).resolve().parent
    root = next((p for p in (here.parent, here) if (p / "skills/system-design-enter/SKILL.md").is_file()), None)
    if root is None:
        raise RuntimeError("System Design skills are missing; reinstall the complete package")
    refs = root / "skills/system-design-enter/references"
    bootstrap = ("[system-design bootstrap v1]\nUse System Design only for architecture requests. "
                 "Load the requested skill or system-design-enter; do not restart routing.\n"
                 f"Installed skills root: {root / 'skills'}\n\n" +
                 (refs / "policies.md").read_text(encoding="utf-8") + "\n\n" +
                 (refs / "host-tools.md").read_text(encoding="utf-8"))
    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        text = skill.read_text(encoding="utf-8")
        description = re.search(r"^description: (.+)$", text, re.M).group(1)
        ctx.register_skill(skill.parent.name, skill, description=description)

    def pre_llm_call(is_first_turn=None, platform=None, **kwargs):
        if is_first_turn and platform != "subagent":
            return {"context": bootstrap}
        return None

    ctx.register_hook("pre_llm_call", pre_llm_call)
