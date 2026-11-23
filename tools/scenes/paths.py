"""Où un script de scène écrit son JSON.

Toujours dans `.layers/assets/<asset>` du contenu (le dossier parent de `scenes/`). Si la variable
`BL_SCENES` donne le chemin de `packages/scenes` d'un worktree du monorepo, aussi dans
`lessons/zz-<id>/lesson.json` de ce worktree, pour la valider et la capturer :

    BL_SCENES=…/packages/scenes python3 program-architectures/scenes/archi.py
    cd …/packages/scenes && pnpm exec tsx scripts/validate.ts lessons/zz-archi/lesson.json
    pnpm capture zz-archi --beats --only=desktop-light
"""
import os
from pathlib import Path


def outputs(here, asset, lesson_id):
    out = [Path(here).parent / ".layers" / "assets" / asset]
    scenes = os.environ.get("BL_SCENES")
    if scenes:
        out.append(Path(scenes) / "lessons" / f"zz-{lesson_id}" / "lesson.json")
    return [str(p) for p in out]
