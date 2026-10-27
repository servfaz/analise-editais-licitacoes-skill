import argparse
import re
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SKILL_DIR = REPO_ROOT / "skills" / "licitacoes-servfaz"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "dist"
REFERENCE_PATTERN = re.compile(r"references/[\w./-]*\w\.(?:md|json)")
PACKAGED_ROOT_FILES = ["SKILL.md"]
PACKAGED_DIRECTORIES = ["references"]
READ_LIMIT_CHARACTERS = 20000


def packaged_files(skill_dir):
    files = [skill_dir / name for name in PACKAGED_ROOT_FILES]
    for directory in PACKAGED_DIRECTORIES:
        files.extend(sorted(path for path in (skill_dir / directory).rglob("*") if path.is_file()))
    return files


def markdown_documents(skill_dir):
    return [path for path in packaged_files(skill_dir) if path.suffix == ".md"]


def find_missing_references(skill_dir):
    cited = {
        reference
        for document in markdown_documents(skill_dir)
        for reference in REFERENCE_PATTERN.findall(document.read_text(encoding="utf-8"))
    }
    return sorted(reference for reference in cited if not (skill_dir / reference).is_file())


def find_oversized_documents(skill_dir, limit=READ_LIMIT_CHARACTERS):
    sizes = {path: len(path.read_text(encoding="utf-8")) for path in markdown_documents(skill_dir)}
    return sorted((path.relative_to(skill_dir).as_posix(), size) for path, size in sizes.items() if size > limit)


def build_package(skill_dir, output_dir):
    target = output_dir / f"{skill_dir.name}.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in packaged_files(skill_dir):
            archive.write(file_path, Path(skill_dir.name) / file_path.relative_to(skill_dir))
    return target


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description="Valida a skill e gera o pacote .zip para Claude e Open WebUI.")
    parser.add_argument("--skill-dir", type=Path, default=DEFAULT_SKILL_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv=None):
    arguments = parse_arguments(argv)
    missing = find_missing_references(arguments.skill_dir)
    if missing:
        print(f"Referências inexistentes: {', '.join(missing)}", file=sys.stderr)
        return 1
    for relative_path, size in find_oversized_documents(arguments.skill_dir):
        print(f"Aviso: {relative_path} tem {size} caracteres (limite de leitura padrão do Open WebUI: {READ_LIMIT_CHARACTERS})", file=sys.stderr)
    print(build_package(arguments.skill_dir, arguments.output_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
