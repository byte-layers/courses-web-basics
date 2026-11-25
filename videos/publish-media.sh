#!/usr/bin/env bash
# Publie une vidéo sur https://media.byte-layers.com (R2), nommée par son
# sha256, et affiche son adresse à citer dans l'étape. Voir publish-media.cjs.
#
#   bash publish-media.sh out/html-css-basics-01-onglet-reseau/html-css-basics-01-onglet-reseau.mp4
set -euo pipefail
file="$(cd "$(dirname "${1:?fichier .mp4 ou .webm}")" && pwd)/$(basename "$1")"
cd "$(dirname "$0")"
exec node publish-media.cjs "$file"
