"""Independently verify published CSV evidence using only Python's standard library.

Run: python business_analysis/verify_results.py
This checks exported results, not model fitting or the raw-history boundary audit.
"""
import argparse
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path

EXPECTED_USERS = ('11319785650938584699', '5911263612844924182')
EXPECTED_METHODS = {
    'Global Popularity', 'User History', 'History + Schedule', 'History + Time',
    'History + Schedule + Time', 'Item-based CF', 'Implicit ALS',
    'Personalized PageRank', 'History + CF + Schedule',
    'History + CF + ALS + Schedule', 'History + CF + ALS + PPR + Schedule',
}


def require(condition, message):
    # Explicit checks remain active under python -O.
    if not condition:
        raise ValueError(message)


def rows(path):
    with path.open(newline='', encoding='utf-8-sig') as stream:
        yield from csv.DictReader(stream)


def flag(value):
    require(value in ('True', 'False'), f'Invalid boolean: {value!r}')
    return value == 'True'


def ap_at_five(predicted, actual):
    hits = 0
    precision_sum = 0.0
    for rank, show in enumerate(predicted, 1):
        if show in actual:
            hits += 1
            precision_sum += hits / rank
    return precision_sum / 5


def verify(output_dir, notebook):
    required = ('business_analysis.md', 'method_comparison.csv', 'user_profiles.csv',
                'user_recommendations.csv', 'user_method_metrics.csv',
                'selected_user_history.csv', 'selected_user_targets.csv',
                'validation_predictions.csv', 'validation_targets.csv',
                'candidate_catalog.csv', 'run_manifest.json', 'kaggle_results.png')
    for filename in required:
        path = output_dir / filename
        require(path.is_file() and path.stat().st_size > 0, f'Missing evidence: {path}')
    catalog_rows = [int(r['tv_show_id']) for r in rows(output_dir / 'candidate_catalog.csv')]
    catalog = set(catalog_rows)
    require(len(catalog_rows) == len(catalog) == 1867 and all(s > 0 for s in catalog),
            'Expected 1,867 unique positive candidate IDs')
    truth = {}
    for r in rows(output_dir / 'validation_targets.csv'):
        truth.setdefault(r['user_id'], []).append(int(r['tv_show_id']))
    require(len(truth) == 4030, 'Expected 4,030 validation users')
    require(all(len(v) == len(set(v)) == 5 for v in truth.values()), 'Invalid five-item targets')
    truth = {u: set(v) for u, v in truth.items()}
    comparison = list(rows(output_dir / 'method_comparison.csv'))
    require(len(comparison) == 11 and {r['method'] for r in comparison} == EXPECTED_METHODS,
            'Comparison methods differ from the eleven reported methods')

    # Stream contiguous (method, user) groups to avoid loading the 11 MB ranking table.
    seen_groups = set()
    method_aps = {m: [] for m in EXPECTED_METHODS}
    recommended = {m: set() for m in EXPECTED_METHODS}
    selected_predictions = {}
    predictions_count = 0
    grouped = itertools.groupby(rows(output_dir / 'validation_predictions.csv'),
                                key=lambda r: (r['method'], r['user_id']))
    for (method, user), group in grouped:
        require(method in EXPECTED_METHODS and user in truth, 'Unknown method or user in predictions')
        require((method, user) not in seen_groups, 'Repeated prediction group')
        seen_groups.add((method, user))
        records = list(group)
        require([int(r['rank']) for r in records] == [1, 2, 3, 4, 5],
                f'Invalid ranks for {method}, {user}')
        prediction = [int(r['tv_show_id']) for r in records]
        require(len(set(prediction)) == 5 and set(prediction) <= catalog,
                f'Duplicate or ineligible predictions for {method}, {user}')
        method_aps[method].append(ap_at_five(prediction, truth[user]))
        recommended[method].update(prediction)
        predictions_count += 5
        if user in EXPECTED_USERS:
            selected_predictions[(method, user)] = prediction
    require(predictions_count == 221650, 'Expected 221,650 validation predictions')
    require(len(seen_groups) == len(truth) * len(EXPECTED_METHODS), 'Methods use different user cohorts')
    recalculated = {}
    for r in comparison:
        method = r['method']
        require(len(method_aps[method]) == len(truth), f'Incomplete cohort for {method}')
        actual = math.fsum(method_aps[method]) / len(truth)
        require(math.isclose(actual, float(r['map_at_5']), rel_tol=0, abs_tol=1e-12),
                f'MAP@5 mismatch for {method}: recomputed={actual}, exported={r["map_at_5"]}')
        require(int(r['validation_users']) == len(truth) and int(r['common_candidates']) == len(catalog),
                f'Protocol counts differ for {method}')
        require(int(r['recommended_unique_shows']) == len(recommended[method]), 'Coverage count mismatch')
        require(math.isclose(float(r['catalog_coverage']), len(recommended[method])/len(catalog),
                             rel_tol=0, abs_tol=1e-12), 'Catalog coverage mismatch')
        # This only checks consistency of the recorded reproduction, not a new notebook run.
        require(abs(float(r['notebook_protocol_map_at_5']) - float(r['notebook_saved_map_at_5'])) < 1e-6,
                f'Recorded original-protocol mismatch for {method}')
        recalculated[method] = actual

    profiles = list(rows(output_dir / 'user_profiles.csv'))
    require(len(profiles) == 2 and {r['user_id'] for r in profiles} == set(EXPECTED_USERS),
            'Selected profile users differ')
    for r in profiles:
        require(r['last_view'] < '2020-05-18', 'Profile timestamp is beyond the training period')
        category_counts = json.loads(r['category_counts'])
        require(sum(category_counts.values()) == int(r['interactions']), 'Profile category totals differ')
    histories = {}
    for r in rows(output_dir / 'selected_user_history.csv'):
        key = (r['user_id'], int(r['tv_show_id']))
        require(key not in histories, 'Duplicate selected-user history ID')
        histories[key] = int(r['watch_count'])
    for r in profiles:
        counts = [v for (u, _), v in histories.items() if u == r['user_id']]
        require(sum(counts) == int(r['interactions']) and len(counts) == int(r['unique_shows']),
                'Profile differs from exported history')
    chosen_targets = {}
    for r in rows(output_dir / 'selected_user_targets.csv'):
        chosen_targets.setdefault(r['user_id'], []).append(int(r['tv_show_id']))
    require(set(chosen_targets) == set(EXPECTED_USERS), 'Selected target users differ')
    require(all(len(v) == 5 and set(v) == truth[u] for u, v in chosen_targets.items()),
            'Selected targets differ from full validation targets')
    chosen = list(rows(output_dir / 'user_recommendations.csv'))
    require(len(chosen) == 110, 'Expected 110 case-study recommendations')
    chosen_keys = set()
    for r in chosen:
        method, user, rank, show = r['method'], r['user_id'], int(r['rank']), int(r['tv_show_id'])
        key = (method, user, rank)
        require(key not in chosen_keys and (method, user) in selected_predictions, 'Invalid case-study key')
        chosen_keys.add(key)
        require(1 <= rank <= 5 and selected_predictions[(method, user)][rank-1] == show,
                'Case-study row differs from the full validation ranking')
        require(flag(r['hit_validation_top5']) == (show in truth[user]), 'Incorrect target-hit flag')
        require(not flag(r['hit_validation_top5']) or flag(r['hit_validation']), 'Target hit lacks validation hit')
        require(int(r['historical_watch_count']) == histories.get((user, show), 0), 'History-count mismatch')
        require(math.isfinite(float(r['score'])), 'Nonfinite recommendation score')
        require(r['title'] and r['category'] and not flag(r['metadata_missing']), 'Missing case-study metadata')
    user_metrics = list(rows(output_dir / 'user_method_metrics.csv'))
    require(len(user_metrics) == 22, 'Expected 22 user-method metric rows')
    metric_keys = set()
    for r in user_metrics:
        key = (r['method'], r['user_id'])
        require(key not in metric_keys and key in selected_predictions, 'Invalid user-method metric key')
        metric_keys.add(key)
        prediction = selected_predictions[key]
        require(math.isclose(float(r['ap_at_5']), ap_at_five(prediction, truth[key[1]]),
                             rel_tol=0, abs_tol=1e-12), 'Case-study AP@5 mismatch')
        require(int(r['hits_top5']) == len(set(prediction) & truth[key[1]]), 'Case-study hit count mismatch')

    manifest = json.loads((output_dir / 'run_manifest.json').read_text(encoding='utf-8'))
    require(set(manifest['selected_users']) == set(EXPECTED_USERS), 'Manifest selected users differ')
    require(manifest['checks']['recommendation_rows'] == len(chosen), 'Manifest row count differs')
    require(notebook.is_file(), f'Missing original notebook: {notebook}')
    data = notebook.read_bytes()
    expected = manifest['notebook_sha256']
    # Git may check LF text out as CRLF; allow this transport-only conversion.
    notebook_match = hashlib.sha256(data).hexdigest() == expected
    newline_match = hashlib.sha256(data.replace(b'\r\n', b'\n')).hexdigest() == expected
    require(notebook_match or newline_match, 'Notebook content differs from the recorded original')
    return dict(status='PASS', methods=11, validation_users=len(truth),
                validation_prediction_rows=predictions_count, selected_recommendation_rows=len(chosen),
                candidates=len(catalog), recomputed_map_at_5=recalculated,
                notebook_matches_recorded_hash=True,
                scope='Exported-result consistency; no model fitting or raw-history leakage audit was repeated.')


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--outputs', type=Path, default=Path(__file__).resolve().parent / 'outputs')
    parser.add_argument('--notebook', type=Path, default=root / 'Exam.ipynb')
    parser.add_argument('--json', action='store_true', help='Print machine-readable verification results')
    args = parser.parse_args()
    try:
        result = verify(args.outputs, args.notebook)
    except (ValueError, KeyError, OSError, csv.Error, TypeError) as error:
        parser.exit(1, f'FAIL: {error}\n')
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print('PASS: 11 methods; 4,030 users; 221,650 predictions; 110 case-study recommendations; '
              'MAP@5, coverage, candidate validity and notebook hash agree.')
        print(result['scope'])


if __name__ == '__main__':
    main()
