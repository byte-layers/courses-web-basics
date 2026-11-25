#!/usr/bin/env bash
# Produit la vidéo d'un scénario : narration (say), enregistrement (navigateur + DevTools,
# Playwright), assemblage (ffmpeg).
#
#   bash make-video.sh html-css-basics-01-onglet-reseau            # tout
#   bash make-video.sh html-css-basics-01-onglet-reseau revoice    # nouvelle voix ou nouveau texte,
#                                                 # sans réenregistrer la scène
#   bash make-video.sh html-css-basics-01-onglet-reseau tts|record|assemble   # une seule étape
set -euo pipefail
cd "$(dirname "$0")"
name="${1:?nom du scénario, ex. html-css-basics-01-onglet-reseau}"
mode="${2:-all}"
scenario="$name/scenario.cjs"
out="out/$name"
mkdir -p "$out"
t0=$(date +%s)
case "$mode" in
  all)      steps="tts record assemble" ;;
  revoice)  steps="tts assemble" ;;
  tts|record|assemble) steps="$mode" ;;
  *) echo "mode inconnu : $mode (all, revoice, tts, record, assemble)"; exit 2 ;;
esac
for step in $steps; do
  t=$(date +%s)
  echo "── $step"
  script="$step.cjs"
  # Un scénario « VS Code puis navigateur » a son propre enregistreur.
  if [ "$step" = record ] && grep -q "recorder: 'vscode'" "$scenario"; then script=record-vscode.cjs; fi
  node "$script" "$scenario" "$out"
  echo "   ($(( $(date +%s) - t )) s)"
done
echo "total : $(( $(date +%s) - t0 )) s"
