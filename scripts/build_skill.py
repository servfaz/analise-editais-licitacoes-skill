import argparse
import re
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SKILL_DIR = REPO_ROOT / "skills" / "licitacoes-servfaz"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "dist"
REFERENCE_PATTERN = re.compile(r"`?references/([\w-]+\.md)`?")
SHARED_REFERENCES = ["regras-gerais.md", "capacidades.md", "catalogo-de-fontes.md"]
PHASE_BUNDLES = {
    "fase-1-triagem": ["fase-1-triagem.md"],
    "fase-2-analise-edital": ["fase-2-analise-edital.md"],
    "fase-3-impugnacao": ["fase-3-impugnacao.md", "fase-3-temas-e-exemplos.md"],
    "fase-4-pcfp": ["fase-4-pcfp.md", "fase-4-pcfp-regras.md"],
    "fase-5-recurso": ["fase-5-recurso.md"],
}


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return "", text
    end = text.index("\n---\n", 4)
    return text[: end + 5], text[end + 5 :].lstrip("\n")


def reference_title(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError(f"{path.name} não tem título de nível 1")


def find_missing_references(skill_dir):
    references_dir = skill_dir / "references"
    documents = [skill_dir / "SKILL.md", *sorted(references_dir.glob("*.md"))]
    cited = {name for document in documents for name in REFERENCE_PATTERN.findall(document.read_text(encoding="utf-8"))}
    return sorted(name for name in cited if not (references_dir / name).exists())


def bundle_of_reference(reference_name):
    for phase_name, phase_files in PHASE_BUNDLES.items():
        if reference_name in phase_files:
            return phase_name
    return None


def replace_references(text, local_titles, skill_name):
    def to_section_or_skill(match):
        name = match.group(1)
        if name in local_titles:
            return f"a seção «{local_titles[name]}» deste documento"
        phase_name = bundle_of_reference(name)
        if phase_name:
            return f"a skill `{skill_name}-{phase_name}`"
        return match.group(0)

    return REFERENCE_PATTERN.sub(to_section_or_skill, text)


def build_claude_package(skill_dir, output_dir):
    target = output_dir / "claude" / f"{skill_dir.name}.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    package_files = [skill_dir / "SKILL.md", *sorted((skill_dir / "references").glob("*.md"))]
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in package_files:
            archive.write(file_path, Path(skill_dir.name) / file_path.relative_to(skill_dir))
    return target


def compose_single_file(frontmatter, body_parts, local_titles, skill_name):
    sections = [replace_references(part, local_titles, skill_name) for part in body_parts]
    return frontmatter + "\n" + "\n\n---\n\n".join(section.strip() for section in sections) + "\n"


def phase_frontmatter(skill_name, phase_name, phase_title):
    return (
        "---\n"
        f"name: {skill_name}-{phase_name}\n"
        f"description: {phase_title}. Parte do processo de licitações da Servfaz.\n"
        "---\n"
    )


def build_openwebui_package(skill_dir, output_dir):
    references_dir = skill_dir / "references"
    reference_files = sorted(references_dir.glob("*.md"))
    titles = {path.name: reference_title(path) for path in reference_files}
    frontmatter, orchestrator_body = split_frontmatter((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
    target_dir = output_dir / "openwebui"
    target_dir.mkdir(parents=True, exist_ok=True)

    ordered_references = SHARED_REFERENCES + [path.name for path in reference_files if path.name not in SHARED_REFERENCES]
    full_parts = [orchestrator_body] + [(references_dir / name).read_text(encoding="utf-8") for name in ordered_references]
    full_target = target_dir / f"{skill_dir.name}.md"
    full_target.write_text(compose_single_file(frontmatter, full_parts, titles, skill_dir.name), encoding="utf-8")
    written = [full_target]

    for phase_name, phase_files in PHASE_BUNDLES.items():
        bundle_names = SHARED_REFERENCES + phase_files
        bundle_titles = {name: titles[name] for name in bundle_names}
        parts = [(references_dir / name).read_text(encoding="utf-8") for name in bundle_names]
        phase_target = target_dir / f"{skill_dir.name}-{phase_name}.md"
        header = phase_frontmatter(skill_dir.name, phase_name, titles[phase_files[0]])
        phase_target.write_text(compose_single_file(header, parts, bundle_titles, skill_dir.name), encoding="utf-8")
        written.append(phase_target)
    return written


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description="Gera os pacotes da skill para Claude e Open WebUI.")
    parser.add_argument("--target", choices=["claude", "openwebui", "all"], default="all")
    parser.add_argument("--skill-dir", type=Path, default=DEFAULT_SKILL_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv=None):
    arguments = parse_arguments(argv)
    missing = find_missing_references(arguments.skill_dir)
    if missing:
        print(f"Referências inexistentes: {', '.join(missing)}", file=sys.stderr)
        return 1
    written = []
    if arguments.target in ("claude", "all"):
        written.append(build_claude_package(arguments.skill_dir, arguments.output_dir))
    if arguments.target in ("openwebui", "all"):
        written.extend(build_openwebui_package(arguments.skill_dir, arguments.output_dir))
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
