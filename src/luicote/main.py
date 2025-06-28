#!/usr/bin/env python3

import sys
import os
import subprocess
from pathlib import Path
import argparse
from jinja2 import Environment, FileSystemLoader
import shutil

ROOT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def exit_if_null(value, message):
    if not value:
        print(message)
        sys.exit(1)

#TODO: use it
def parse_args():
    parser = argparse.ArgumentParser(description="Render Haskell project template with Jinja2.")
    parser.add_argument("--output-dir", required=True, help="Directory where the rendered project will be created.")
    parser.add_argument("--folder-name", required=True, help="Project folder name (used in {{ folder_name }}).")
    return parser.parse_args()

def core(project_name:str,output_dir:Path, template_path:Path):

    # Variables Jinja2
    context = {
    "folder_name": project_name,
    "project_description": "A new haskell project",
    "author": "Luis Alberto Díaz Díaz",
    "maintainer_email": "73986926+Luis-omega@users.noreply.github.com",
    }

    print(f"Template dir:{template_path}")
    OUTPUT_DIR = Path(output_dir) / project_name

    env = Environment(
        loader=FileSystemLoader(str(template_path)),
        keep_trailing_newline=True
    )

    if OUTPUT_DIR.exists():
        print("Can't create {output_dir}, it already exists!")
        return -1

    for root, _, files in os.walk(template_path):
        for file_name in files:
            src_path = Path(root) / file_name
            rel_path = src_path.relative_to(template_path)

            # Render (folder_name.cabal → myproject.cabal)
            rendered_rel_path = Path(env.from_string(str(rel_path)).render(context))
            dst_path = OUTPUT_DIR / rendered_rel_path

            dst_path.parent.mkdir(parents=True, exist_ok=True)

            # Render
            template = env.get_template(str(rel_path))
            rendered_content = template.render(context)

            with open(dst_path, "w", encoding="utf-8") as f:
                f.write(rendered_content)

    print(f"Project generated at: {OUTPUT_DIR.resolve()}")
    return 0


def main():
    #args = parse_args()
    if len(sys.argv) < 2:
        print("Usage: luicote <project_name>")
        sys.exit(1)

    name = sys.argv[1]
    exit_if_null(name, "no project name provided")

    home = Path.home()
    dir = home / "projects"
    template_project = dir / "luicote"
    project_path = dir / name

    # Ejecutar main.py usando subprocess

    core(name,dir,ROOT_DIR/"haskell_template")

    # Renombrar folder_name.cabal → <name>.cabal si existe
    old_cabal = project_path / "folder_name.cabal"
    new_cabal = project_path / f"{name}.cabal"
    if old_cabal.exists():
        old_cabal.rename(new_cabal)

    #Initialize git repo
    os.chdir(project_path)
    subprocess.run(["git", "init"])
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"{name} initialization"])

    print(f"Initialized git repo at: {dir}")

if __name__ == "__main__":
    main()
