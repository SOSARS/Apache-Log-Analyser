# Apache Log Analyser Case Study

## Executive summary

PyLog Threat Analyser is a Python portfolio project for initial investigation of Apache access logs. It combines IP-level activity summaries with Isolation Forest anomaly detection. The project documentation also describes AbuseIPDB enrichment, SQLite caching, terminal and CSV reports, Docker packaging and automated tests.

Review of the supplied detector, evaluation scripts and ground-truth labels confirms the feature construction, scoring rule and metric calculations described below. The detector fits and scores the same batch of IP summaries; this is exploratory outlier analysis rather than independent validation of a trained model.

The supplied labels contain **15 distinct IP addresses: three labelled ATTACK and twelve labelled BENIGN**. The historical claims of 100% detection and zero false positives cannot currently be confirmed because the original narrative contains contradictory scores and counts, and the input log and parser have not been supplied for a rerun. Production accuracy, sustained throughput and real-time capability remain unestablished.

## Problem and objective

Apache access logs contain request information that can help an analyst identify unusual client behaviour. High request volume alone does not establish malicious activity: legitimate users, shared IP addresses and internal tools can also generate heavy traffic.

The project's objective is to summarise traffic by IP address, identify unusual combinations of activity and provide information for further investigation. It assists triage; it does not prove an attack or replace contextual analysis by an analyst.

## Evidence reviewed

| File | What was verified |
|---|---|
| `anomaly_detector.py` | Feature construction, model parameters, batch fitting, decision scores and threshold rule |
| `measure_performance.py` | Label loading, metric formulas, fixed evaluation threshold and timer boundaries |
| `tune_threshold.py` | Threshold sweep using one set of scores |
| `ground_truth_labels.csv` | Fifteen unique IP labels: three ATTACK and twelve BENIGN |
| `README.md` | Documented application architecture and usage; implementation outside the supplied scripts was not verified |

The supplied Python files pass syntax parsing. The metric function was checked against known outcomes: three detected attacks and twelve correctly ignored benign IPs produce TP=3, FP=0, TN=12 and FN=0; flagging three of the twelve benign IPs produces an FPR of 25%. These checks validate the formulas, not the detector's historical results.

## Technical approach

### Parsing and aggregation

Both evaluation scripts call `parse_apache_file("test_access.log")` from `file_parser.py`. The detector expects one dictionary entry per IP containing a request count (`total`), error count (`errors`) and a collection of distinct paths (`paths`).

The parser and input log are required to verify the supported Apache format, which status codes count as errors, handling of malformed entries and the actual number of accepted requests. They also determine whether all labelled IPs appear in the analysed data.

### Feature engineering

The detector creates one row per IP with three features:

| Feature | Calculation |
|---|---|
| Request volume | `data["total"]` |
| Error rate | `data["errors"] / data["total"]`, or zero when total is zero |
| Path diversity | Number of distinct paths in `data.get("paths", set())` |

Request timestamps, HTTP methods, credentials and user agents are not model features in the supplied detector. Consequently, the model does not directly measure request rate, distinguish different credential attacks or use timing patterns from the synthetic generator.

### Model fitting and scoring

The implementation fits:

```python
IsolationForest(contamination="auto", random_state=42)
```

It then calls `decision_function` on the **same feature rows used for fitting**. The random seed makes this stage repeatable for the same ordered inputs, dependency versions and model parameters; it does not establish generalisation.

Lower decision scores indicate more unusual activity. At the standard zero boundary, negative scores represent outliers relative to the fitted model. A decision score is not a calibrated probability of maliciousness and does not explain which feature caused the result.

### Threshold rule

An IP is flagged when:

```python
score < threshold
```

The detector's default threshold is `0.0`. The performance script explicitly uses `-0.05`. These are different configurations and should be reported separately.

The tuning script fits the detector once, obtains scores and evaluates nine thresholds from `0.0` to `-0.08` in steps of `-0.01`. Making the threshold more negative flags fewer IPs and can reduce both false positives and true positives.

### Enrichment and reporting

The README describes AbuseIPDB enrichment with SQLite caching and terminal/CSV reporting. Neither enrichment nor API lookup time is included in the supplied performance measurement. These components require their source files and a separate runtime check to verify their behaviour.

## Evaluation design

The labels are used to evaluate and select a threshold; they are not passed into Isolation Forest fitting. Therefore, fitting is unsupervised, but threshold selection is label-informed.

The scripts use the same `test_access.log` and label file for threshold exploration and performance measurement. They do not implement a separate validation or test dataset. Results from this workflow describe performance on the development batch, not performance on unseen traffic.

The original study describes synthetic login-abuse and reconnaissance scenarios alongside legitimate browsing. The specific scenario assignments, request counts, timing distributions and user-profile counts require the generator and input log to verify. Until then, use ATTACK/BENIGN labels rather than claiming verified counts for each attack subtype.

## Metric definitions

The unit of evaluation is a labelled IP address, not an individual request, person or independent incident.

- **True positive (TP):** an ATTACK-labelled IP is flagged.
- **False negative (FN):** an ATTACK-labelled IP is not flagged.
- **False positive (FP):** a BENIGN-labelled IP is flagged.
- **True negative (TN):** a BENIGN-labelled IP is not flagged.

```text
TPR = TP / (TP + FN)
FPR = FP / (FP + TN)
```

The scripts express these rates as percentages. With three attack labels, one missed IP changes TPR by approximately 33.3 percentage points. With twelve benign labels, one false alarm changes FPR by approximately 8.3 percentage points. This small sample provides limited evidence about real-world error rates.

A 25% FPR means that one quarter of the benign labelled IPs were flagged. It does not mean one false alarm for every four genuine threats. That ratio depends on the number of actual attacks and benign cases.

## Status of historical results

The previous narrative reported 100% TPR and 25% FPR at a zero threshold, followed by 100% TPR and 0% FPR at `-0.05`. These results are **unverified historical claims**, not accepted findings of this review.

The narrative needs reconciliation with reproducible output because:

- It states thirteen IPs, while the supplied labels contain fifteen.
- Its profile counts and description of three high-volume false positives are inconsistent.
- It reports a reconnaissance score of `-0.034`, which would not satisfy `score < -0.05`.
- It gives conflicting benign score ranges.
- A reported attacker score of `-0.065` would be missed at thresholds of `-0.07` and `-0.08`, if that score is accurate; more negative thresholds cannot be assumed to preserve detection.

Until the rerun resolves these points, no optimal threshold or perfect detection claim is established.

## Performance measurement scope

`measure_performance.py` parses the log and loads labels **before** starting its timer. The timed call performs feature construction, model fitting, scoring and the detector's completion message. It excludes log parsing, AbuseIPDB enrichment, report generation and evaluation metric calculation.

The script divides the number of aggregated requests by this detector-only duration. This produces a request-normalised rate for the detector stage, not end-to-end log ingestion throughput. The model itself operates on IP summaries, rather than processing each request individually.

The historical narrative reports 2,867 requests, about 0.13 seconds and approximately 22,560 entries per second. The duration is printed to two decimal places, whereas throughput uses the unrounded duration, so those displayed numbers alone do not prove an arithmetic error. However, the missing dataset and measurement output prevent verification, and a single small-batch run does not establish sustained production performance.

A future benchmark should use a monotonic high-resolution timer, separate each stage, record dependency versions and hardware, repeat runs and report dataset sizes in both requests and unique IPs. Cached and uncached enrichment should be measured separately.

## Implementation issues identified

The code review found several issues to address before relying on evaluation output:

1. **Empty input return:** `detect_anomalies` returns only `set()` for empty input, although callers expect `(anomalous_ips, score_dict)`. It should return a consistent pair.
2. **Missing predictions:** the metric function treats missing prediction keys as unflagged. A missing attack can become an FN and a missing benign IP a TN without an explicit coverage warning.
3. **Unlabelled IPs:** predictions outside the ground-truth keys are excluded from the metrics. Log/label coverage should be checked before evaluation.
4. **Label validation:** labels other than `ATTACK` are treated as benign, and duplicate IP rows overwrite earlier labels when loaded. Reject invalid labels and duplicates explicitly.
5. **Missing paths:** absent `paths` becomes an empty set, which can conceal a parser/schema mismatch. Validate the expected input fields.

These findings are based on the supplied code. The Python files have not been modified as part of this document revision.

## Reproducible next evaluation

1. Supply `file_parser.py`, `test_access.log`, the generator and dependency versions.
2. Confirm a one-to-one match between log IPs and ground-truth labels, or explicitly document excluded IPs.
3. Export each IP's feature values, decision score, ground-truth label, threshold and predicted label from one run.
4. Calculate TP, FP, TN and FN directly from that export and retain the raw output.
5. Use a development dataset for choosing the threshold, then evaluate the fixed procedure on independently generated scenarios. Document whether each batch is fitted separately or scored using a previously fitted model.
6. Include benign high-error traffic, legitimate scanners, low-volume attacks and varied traffic mixes to test less obvious cases.

## Lessons and next priorities

The verified work demonstrates modular Python development, interpretable activity summaries, unsupervised batch scoring and a basic labelled evaluation workflow. The immediate improvement is stronger evidence: consistent datasets, complete label coverage and metrics generated from a single traceable run.

Future work can explore temporal features, additional log formats and SIEM-compatible exports. Automated blocking should wait until detections have been validated and reviewed; unusual activity alone is insufficient justification for mitigation.

## Conclusion

PyLog Threat Analyser is an exploratory security triage project with a working feature and scoring design visible in the supplied code. Its current evaluation is small, synthetic and performed on the batch used for fitting and threshold exploration. A reproducible rerun is needed before reporting detection rates or throughput as established results. Clearly separating implementation, observed results and limitations makes the project easier to assess and defend in a technical interview.
