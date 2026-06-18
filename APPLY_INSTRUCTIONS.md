# Applying this bundle

The GitHub integration returned a 403 when attempting to push directly, so this bundle is repository-ready but not pushed.

Recommended application steps from a local clone:

```bash
git checkout -b feature/efgm-v0-2-decision-integrity

# Replace current v0.1 scoring implementation with the patched scoring.py
cp efgm_v0_2_update_bundle/src/efgm/scoring.py src/efgm/scoring.py

# Add v0.2 decision-integrity model
cp efgm_v0_2_update_bundle/src/efgm/schemas_v2.py src/efgm/schemas_v2.py
cp efgm_v0_2_update_bundle/src/efgm/scoring_v2.py src/efgm/scoring_v2.py
cp efgm_v0_2_update_bundle/tests/test_scoring_v2.py tests/test_scoring_v2.py

# Optionally merge the report formula patch manually
cat efgm_v0_2_update_bundle/src/efgm/reports_formula_patch.py

# Add docs
mkdir -p docs
cp efgm_v0_2_update_bundle/docs/EFGM_v0.2_recommendations.md docs/EFGM_v0.2_recommendations.md

pytest

git add src/efgm/scoring.py src/efgm/schemas_v2.py src/efgm/scoring_v2.py tests/test_scoring_v2.py docs/EFGM_v0.2_recommendations.md
git commit -m "Add EFGM v0.2 decision integrity model"
```

Recommended PR title:

```text
Add EFGM v0.2 decision integrity model
```

Recommended PR summary:

```text
This PR updates EFGM scoring to use a geometric mean for positive quality factors and adds a v0.2 decision-integrity model.

The v0.2 model separates input entropy, output entropy, grounding, uncertainty calibration, behavioral entropy, operational entropy, decision quality, outcome confidence, and outcome divergence. This preserves the original lightweight v0.1 model while adding a more testable governance model for AI reasoning, incident review, release readiness, and agentic workflows.
```
