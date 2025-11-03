from file_parser import parse_apache_file
from anomaly_detector import detect_anomalies
from measure_performance import load_ground_truth, calculate_metrics


def main():
    print("[*] Loading test dataset...")
    log_dict = parse_apache_file("test_access.log")
    ground_truth = load_ground_truth("ground_truth_labels.csv")

    # Get scores once
    _, score_dict = detect_anomalies(log_dict, threshold=-999)  # Get all scores

    # Test different thresholds
    thresholds = [0.0, -0.01, -0.02, -0.03, -0.04, -0.05, -0.06, -0.07, -0.08]

    print("\n" + "=" * 70)
    print("THRESHOLD TUNING RESULTS")
    print("=" * 70)
    print(f"{'Threshold':<12} {'TPR':<8} {'FPR':<8} {'Attacks Caught':<15} {'False Alarms'}")
    print("-" * 70)

    for threshold in thresholds:
        # Manually calculate which IPs would be flagged at this threshold
        anomalous_ips = {ip for ip, score in score_dict.items() if score < threshold}
        predictions = {ip: (ip in anomalous_ips) for ip in ground_truth.keys()}

        metrics = calculate_metrics(predictions, ground_truth)

        print(f"{threshold:<12.2f} {metrics['true_positive_rate']:<8.1f} "
              f"{metrics['false_positive_rate']:<8.1f} "
              f"{metrics['true_positives']}/{metrics['total_attacks']:<13} "
              f"{metrics['false_positives']}/{metrics['total_benign']}")

    print("=" * 70)
    print("\nRecommendation: Choose threshold where TPR is high and FPR is acceptable")


if __name__ == "__main__":
    main()