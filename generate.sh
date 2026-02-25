#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MODULES_DIR="$SCRIPT_DIR/modules"
TEMPLATES_DIR="$SCRIPT_DIR/_templates"

# ── Usage ────────────────────────────────────────────────────────────────────
usage() {
  echo "Usage: $0 <fiche|quiz> <module-slug>"
  echo ""
  echo "Exemples:"
  echo "  $0 fiche sql-advanced"
  echo "  $0 quiz numpy"
  exit 1
}

[[ $# -ne 2 ]] && usage

MODE="$1"
SLUG="$2"

[[ "$MODE" != "fiche" && "$MODE" != "quiz" ]] && usage

# ── Find module ───────────────────────────────────────────────────────────────
MATCH=$(find "$MODULES_DIR" -maxdepth 1 -type d -name "*_${SLUG}" 2>/dev/null | head -1)

if [[ -z "$MATCH" ]]; then
  MATCH=$(find "$MODULES_DIR" -maxdepth 1 -type d -name "*${SLUG}*" 2>/dev/null | head -1)
fi

if [[ -z "$MATCH" ]]; then
  echo "❌ Aucun module trouvé pour le slug : '$SLUG'"
  echo ""
  echo "Modules disponibles :"
  ls "$MODULES_DIR" | sed 's/^/  /'
  exit 1
fi

MODULE_NAME=$(basename "$MATCH")
NOTES_FILE="$MATCH/notes.md"
CONV_FILE="$MATCH/conversation.md"
FICHE_FILE="$MATCH/fiche.md"
TEMPLATE_FILE="$TEMPLATES_DIR/${MODE}-template.md"

echo "✓ Module trouvé : $MODULE_NAME"
echo ""

# ── Check sources ─────────────────────────────────────────────────────────────
has_notes=false
has_conv=false

if [[ -f "$NOTES_FILE" ]] && [[ $(wc -l < "$NOTES_FILE") -gt 2 ]]; then
  has_notes=true
fi

if [[ -f "$CONV_FILE" ]] && [[ $(wc -l < "$CONV_FILE") -gt 3 ]]; then
  has_conv=true
fi

if [[ "$has_notes" == false && "$has_conv" == false ]]; then
  echo "⚠️  Aucune source disponible (notes.md et conversation.md sont vides)."
  echo "   Ajoute des notes ou partage une conversation à Claude Code d'abord."
  echo ""
fi

# ── Show sources summary ──────────────────────────────────────────────────────
if [[ "$has_notes" == true ]]; then
  echo "━━━━━━━━━━━━━━━━━━━━━━━━  notes.md  ━━━━━━━━━━━━━━━━━━━━━━━━━━"
  cat "$NOTES_FILE"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
fi

if [[ "$has_conv" == true ]]; then
  CONV_SESSIONS=$(grep -c "^## Session" "$CONV_FILE" 2>/dev/null || echo "0")
  echo "ℹ️  conversation.md : ${CONV_SESSIONS} session(s) disponible(s)"
  echo ""
fi

# ── Build prompt ──────────────────────────────────────────────────────────────
TEMPLATE_CONTENT=$(cat "$TEMPLATE_FILE")

# Build sources block
build_sources() {
  local notes_block=""
  local conv_block=""

  if [[ "$has_notes" == true ]]; then
    notes_block="### Notes de cours

\`\`\`
$(cat "$NOTES_FILE")
\`\`\`"
  fi

  if [[ "$has_conv" == true ]]; then
    conv_block="### Conversations (extraits triés par module)

\`\`\`
$(cat "$CONV_FILE")
\`\`\`"
  fi

  if [[ -n "$notes_block" && -n "$conv_block" ]]; then
    echo "${notes_block}

${conv_block}"
  elif [[ -n "$notes_block" ]]; then
    echo "$notes_block"
  else
    echo "$conv_block"
  fi
}

if [[ "$MODE" == "fiche" ]]; then
  cat <<PROMPT
━━━━━━━━━━━━━━━━━━━━━━━━  PROMPT À COPIER  ━━━━━━━━━━━━━━━━━━━━━━━━

Voici mes sources sur le module **${SLUG}** :

$(build_sources)

Génère une fiche de révision structurée en suivant exactement ce template
(remplace chaque section par du contenu réel, garde les titres) :

\`\`\`
${TEMPLATE_CONTENT}
\`\`\`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Colle la réponse dans : modules/${MODULE_NAME}/fiche.md
PROMPT

else
  # Pour quiz : on préfère fiche.md si elle existe, sinon on prend les sources brutes
  if [[ -f "$FICHE_FILE" ]] && [[ $(wc -l < "$FICHE_FILE") -gt 2 ]]; then
    SOURCE_LABEL="fiche de révision"
    SOURCE_CONTENT=$(cat "$FICHE_FILE")
    SOURCE_BLOCK="### Fiche de révision

\`\`\`
${SOURCE_CONTENT}
\`\`\`"
  else
    SOURCE_LABEL="sources brutes (fiche.md non encore générée)"
    SOURCE_BLOCK=$(build_sources)
  fi

  cat <<PROMPT
━━━━━━━━━━━━━━━━━━━━━━━━  PROMPT À COPIER  ━━━━━━━━━━━━━━━━━━━━━━━━

Voici ma ${SOURCE_LABEL} sur le module **${SLUG}** :

${SOURCE_BLOCK}

Génère un quiz de 3 questions en suivant exactement ce template
(1 QCM, 1 question ouverte, 1 cas pratique) :

\`\`\`
${TEMPLATE_CONTENT}
\`\`\`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Colle la réponse dans : modules/${MODULE_NAME}/quiz.md
PROMPT
fi
