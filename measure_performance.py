import csv
from file_parser import parse_apache_file
from anomaly_detector import detect_anomalies
import time


def load_ground_truth(filepath):
    """Load the ground truth csv file."""
    ground_truth = {}

    with open(filepath, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ip = row["IP Address"]
            label = row["Label"]
            ground_truth[ip] = label

        return ground_truth


def calculate_metrics(predictions, ground_truth):
    """
    Calculate True Positive Rate and False Positive Rate.
    :param predictions: dict of {ip: True/False} where True = flagged as anomaly
    :param ground_truth: dict of {ip: "ATTACK"/"BENIGN"}
    """

    # Initialise counters
    true_positives = 0   # Correctly flagged attacks
    false_positives = 0  # Incorrectly flagged benign users
    true_negatives = 0   # Correctly ignored benign users
    false_negatives = 0  # Missed attacks

    for ip, true_label in ground_truth.items():
        predicted_anomaly = predictions.get(ip, False)

        if true_label == "ATTACK":
            if predicted_anomaly:
                true_positives += 1
            else:
                false_negatives += 1
        else:  # BENIGN
            if predicted_anomaly:
                false_positives += 1
            else:
                true_negatives += 1

    total_attacks = true_positives + false_negatives
    total_benign = false_positives + true_negatives

    tpr = (true_positives / total_attacks * 100) if total_attacks > 0 else 0
    fpr = (false_positives / total_benign * 100) if total_benign > 0 else 0

    return {
        "true_positives": true_positives,
        "false_positives": false_positives,
        "true_negatives": true_negatives,
        "false_negatives": false_negatives,
        "true_positive_rate": tpr,
        "false_positive_rate": fpr,
        "total_attacks": total_attacks,
        "total_benign": total_benign
    }



def main():
    print(f"[*] Loading test dataset...")
    log_dict = parse_apache_file("test_access.log")

    print(f"[*] Loading ground truth labels...")
    ground_truth = load_ground_truth("ground_truth_labels.csv")

    print(f"[*] Running anomaly detection...")
    start_time = time.time()  # Timer for processing
    anomalous_ips, score_dict = detect_anomalies(log_dict, threshold=-0.05)
    end_time = time.time()  # End of the timer

    processing_time = end_time - start_time
    num_entries = sum(data["total"] for data in log_dict.values())

    # Convert anomalous_ips set to predictions dict
    predictions = {ip: (ip in anomalous_ips) for ip in ground_truth.keys()}

    print(f"[*] Calculating performance metrics...\n")
    metrics = calculate_metrics(predictions, ground_truth)

    # Return the results
    print("PROCESSING PERFORMANCE")
    print("=" * 50)
    print(f"Total log entries analysed: {num_entries}")
    print(f"Processing time: {processing_time:.2f} seconds")
    print(f"Throughput: {num_entries/processing_time:.2f} entries/second")
    print("=" * 50)
    print("PERFORMANCE METRICS")
    print("=" * 50)
    print(f"True Positives: {metrics['true_positives']}/{metrics['total_attacks']} attacks detected.")
    print(f"False Negatives: {metrics['false_negatives']}/{metrics['total_attacks']} attacks missed.")
    print(f"False Positives: {metrics['false_positives']}/{metrics['total_benign']} benign users flagged.")
    print(f"True Negatives: {metrics['true_negatives']}/{metrics['total_benign']} benign users ignored.")
    print()
    print(f"True Positive Rate (TPR): {metrics['true_positive_rate']:.1f}%")
    print(f"False Positive Rate (FPR): {metrics['false_positive_rate']:.1f}%")

    # Reveal misclassified IPs
    print("\nMISSED ATTACKS (False Negatives):")
    for ip in ground_truth:
        if ground_truth[ip] == "ATTACK" and ip not in anomalous_ips:
            score = score_dict.get(ip, 0.0)
            print(f"\t{ip} (score: {score:.3f})")

    print(f"\nFALSE ALARMS (False Positives):")
    for ip in ground_truth:
        if ground_truth[ip] == "BENIGN" and ip in anomalous_ips:
            score = score_dict.get(ip, 0.0)
            print(f"\t{ip} (score: {score:.3f})")


if __name__ == "__main__":
    main()