# SWEET.TV: Results and Independent Verification

This lightweight evidence package contains the English business analysis,
exported rankings and targets, case-study tables, the original run manifest,
and one standalone verification script. Training and report-generation modules
are intentionally excluded from Git.

## Run the verification

From the repository root:

```console
python business_analysis/verify_results.py
```

Dependencies: **Python 3.10 or newer, standard library only**. No installation,
GPU, model training, original datasets or Jupyter session is required to verify
the exported results. The script was checked with Python 3.12.14 in `torchenv`
and the bundled Python runtime.

Expected output:

```text
PASS: 11 methods; 4,030 users; 221,650 predictions; 110 case-study recommendations; MAP@5, coverage, candidate validity and notebook hash agree.
Exported-result consistency; no model fitting or raw-history leakage audit was repeated.
```

For machine-readable results, run `python business_analysis/verify_results.py --json`.
Paths are resolved relative to the script. Optional `--outputs PATH` and
`--notebook PATH` arguments select other copies. A failed check exits with a
nonzero status, including when Python is run with `-O`.

## Published files

| File | Purpose |
| --- | --- |
| `verify_results.py` | Independent checks, using only Python's standard library |
| `outputs/business_analysis.md` | English classical-method business analysis, including all Top-5 examples |
| `outputs/method_comparison.csv` | Audited MAP, recorded original-protocol MAP, coverage and stage timings |
| `outputs/validation_predictions.csv` | All 221,650 ranked rows: 11 methods x 4,030 users x 5 ranks |
| `outputs/validation_targets.csv` | Five actual held-out targets for every evaluation user |
| `outputs/candidate_catalog.csv` | The common 1,867-ID eligible catalog |
| `outputs/user_profiles.csv` | Train-history statistics for the two selected users |
| `outputs/user_recommendations.csv` | 110 selected-user recommendations, scores, metadata and hit flags |
| `outputs/user_method_metrics.csv` | Case-study AP@5 and descriptive statistics |
| `outputs/selected_user_history.csv` | Qualified train-history programme counts for the selected users |
| `outputs/selected_user_targets.csv` | Their five actual validation targets |
| `outputs/run_manifest.json` | Unmodified historical provenance: input/source hashes, versions, audit counts and timings |
| `outputs/kaggle_results.png` | Supplied screenshot supporting the separate competition-score discussion |

The original notebook is [`Exam.ipynb`](../Exam.ipynb), and the main English
report is [`final_report.md`](../final_report.md). The standalone
[business analysis](outputs/business_analysis.md) covers the classical methods.

## Checks performed

- The same eleven methods and 4,030 validation users throughout.
- Five distinct eligible IDs, ordered ranks 1-5, for each user and method.
- MAP@5 recomputed from complete exported rankings and targets, agreeing with
  the comparison table within absolute tolerance 1e-12.
- Catalog coverage and comparison-cohort sizes.
- Exact agreement of selected-user examples with the full ranking export.
- Fixed user IDs, profile/history totals, target membership flags and user AP@5.
- Original notebook SHA256, tolerating only Git's LF-to-CRLF conversion.
- Consistency of the recorded original-protocol metrics with printed notebook
  reference values at tolerance 1e-6; this is not a new notebook execution.

## Protocol and fixed settings

Training broadcasts start before **18 May 2020**; validation starts in
**[18 May 2020, 27 July 2020)**. The original analysis matches history and schedule
by channel/time overlap, merges overlapping intervals, and qualifies a viewing
when at least 80% of the complete broadcast duration was watched. Counts are
qualified broadcasts, not seconds. Recommending already watched IDs is allowed.

Each eligible evaluation user has five distinct targets, selected by descending
validation watch count and ascending programme ID. AP@5 divides by **five** even
when a target is outside the catalog. MAP averages all 4,030 users, including
those with no retrieved hits. It does not use the changed metric from the separate
blend sweep that normalises by retrieved positives and omits zero-positive users.

The common catalog contains 1,867 train-known, validation-scheduled IDs. Users A
and B are fixed as `11319785650938584699` and `5911263612844924182`. Original
selection used train-only quantitative criteria: at least 20 qualified views and
five distinct programmes; A maximises stable dominant-category share across the
two train halves, while B maximises category entropy. Success of recommendations
was not a selection criterion.

Recorded parameters: CF has 50 neighbours; ALS uses 64 factors, regularisation
0.1, 30 iterations, confidence input 20 times watch count and seed 42; PPR uses
alpha 0.7, at most 100 iterations, tolerance 1e-8 and batches of 64. The selected
History/CF/ALS/PPR weights are 0.50/0.40/0.05/0.05, with schedule exponent 0.10.
The verifier performs no fitting or new parameter search.

## Verification scope and limits

The original notebook records a four-component result of approximately
**0.367920**; the separately generated boundary-corrected result is **0.367811**.
These are different branches, not inconsistent values for one run. The historical
audit records 411 training records with post-cutoff watching; clipping intervals
and reapplying the same 80% threshold removes 318 records, leaving 316,416.
These historical counts remain in `run_manifest.json`.

**This package independently verifies exported rankings, targets and reported
metrics. It does not reconstruct interactions, retrain models, or independently
certify that no future information entered the generation process.** Reproducing
the boundary correction from raw history requires the separate preparation and
training code plus original datasets, intentionally absent from this reduced
Git package. Manifest audit flags/source hashes are historical provenance, not
independent proof of temporal correctness. Some manifest paths refer to omitted
generation files; this verifier does not require them or validate their current
hashes.

The original notebook expects `dataset11-30.csv`, `export_arh_11-20-final.csv`,
`export_arh_21-30-final.csv`, `export_arh_31-42-final.csv` and `submission.csv`.
Large datasets remain outside Git. That notebook is not the corrected audit
pipeline and has documented state dependencies in its supervised experiments.
This package does not promise that every notebook cell runs sequentially to
produce the corrected table.

## Metadata and interpretation

Narrative documents are in English. CSVs preserve the original source-language
titles, categories and JSON category distributions, keeping the experimental
data unchanged. Keep user IDs as strings to avoid loss of uint64 precision.

`hit_validation_top5` means membership in the five evaluation targets;
`hit_validation` includes any qualified held-out viewing. This package can check
target membership independently, but lacks all held-out interactions needed to
reverify every broader-view flag or original schedule metadata. Scores are
method-specific and are not calibrated probabilities.

Stage timings in the historical comparison are shared local computations, not
production latency or isolated training benchmarks. Missing measurements remain
blank. Kaggle screenshot scores are separate evidence, not a claim of upload-hash
identity or clean local supervised validation. No new model fit, A/B test or
revenue effect is claimed.
