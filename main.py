import os
import shutil
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def parse_args():
    parser = argparse.ArgumentParser(description="Render Haskell project template with Jinja2.")
    parser.add_argument("--output-dir", required=True, help="Directory where the rendered project will be created.")
    parser.add_argument("--folder-name", required=True, help="Project folder name (used in {{ folder_name }}).")
    return parser.parse_args()


def main():
    args = parse_args()

    # Variables Jinja2
    context = {
        "folder_name": args.folder_name,
    "project_description": "A new haskell project",
    "author": "Luis Alberto Díaz Díaz",
    "maintainer_email": "73986926+Luis-omega@users.noreply.github.com",
    }

    TEMPLATE_DIR = Path("template")
    OUTPUT_DIR = Path(args.output_dir) / args.folder_name

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        keep_trailing_newline=True
    )

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    for root, _, files in os.walk(TEMPLATE_DIR):
        for file_name in files:
            src_path = Path(root) / file_name
            rel_path = src_path.relative_to(TEMPLATE_DIR)

            # Render del nombre del archivo (por ejemplo, folder_name.cabal → myproject.cabal)
            rendered_rel_path = Path(env.from_string(str(rel_path)).render(context))
            dst_path = OUTPUT_DIR / rendered_rel_path

            dst_path.parent.mkdir(parents=True, exist_ok=True)

            # Render del contenido del archivo
            template = env.get_template(str(rel_path))
            rendered_content = template.render(context)

            with open(dst_path, "w", encoding="utf-8") as f:
                f.write(rendered_content)

    print(f"Proyecto generado en: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
