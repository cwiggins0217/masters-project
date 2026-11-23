#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: $0 {pre|post|followup}" >&2
    exit 2
}

[[ $# -eq 1 ]] || usage

PHASE="$1"

case "$PHASE" in
    pre|post|followup) ;;
    *) usage ;;
esac

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DEMO="$(cd "$SCRIPT_DIR/.." && pwd)"

INPUTS="$DEMO/staging/inputs"
RENDERER="$DEMO/staging/renderer"
XSL="$RENDERER/xsl/xccdf-report.xsl"
MAP="$INPUTS/ubuntu2404-context.xml"
JSON="$INPUTS/comparison.json"
WRAPPER="$RENDERER/render-assessed.pl"
RESULTS="$INPUTS/$PHASE/results.xml"

for file in "$XSL" "$MAP" "$JSON" "$WRAPPER" "$RESULTS"; do
    if [[ ! -f "$file" ]]; then
        echo "Missing required input: $file" >&2
        exit 1
    fi
done

for program in perl xsltproc; do
    command -v "$program" >/dev/null || {
        echo "Missing program: $program" >&2
        exit 1
    }
done

mkdir -p "$DEMO/generated"

# Create a distinct output directory for each invocation.
# This avoids overwriting evidence or previous reports.
RUN_DIR="$(mktemp -d "$DEMO/generated/${PHASE}-XXXXXXXX")"
OUTPUT="$RUN_DIR/report.html"

echo "Phase: $PHASE"
echo "XCCDF input: $RESULTS"
echo "Output: $OUTPUT"

perl "$WRAPPER" \
    "$JSON" \
    "$PHASE" \
    "$XSL" \
    "$RESULTS" \
    "$OUTPUT" \
    --stringparam enrichment-file "$MAP"

if [[ ! -s "$OUTPUT" ]]; then
    echo "Renderer did not produce a nonempty report." >&2
    exit 1
fi

echo
echo "Report generated successfully."
sha256sum "$OUTPUT"

echo
echo "Expected sections:"
for heading in \
    'Assessment' \
    'Summary' \
    'Supporting Evidence/Documentation' \
    'Explanation and sources'
do
    if grep -Fq "$heading" "$OUTPUT"; then
        echo "  FOUND: $heading"
    else
        echo "  MISSING: $heading"
        exit 1
    fi
done

echo
echo "Report: $OUTPUT"
