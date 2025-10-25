import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(log_dict: dict) -> set:
    """
    Analyses log data to ID anomalous IPs using an Isolation Forest model

    Args:
        log_dict (dict): Dictionary of log data

    Returns:
        A set containing the IP addresses flagged as anomalies
    """

    if not log_dict:
        return set()

    # 1. Feature Engineering
    records = []  # Convert the dictionary to a list
    for ip, data in log_dict.items():
        error_rate = (data["errors"] / data["total"]) if data["total"] > 0 else 0

        # Get the number of unique paths requested
        # The data must be modified for the parser first
        unique_paths = data.get("paths", set())

        records.append({
            "ip_address": ip,
            "total_requests": data["total"],
            "error_rate": error_rate,
            "unique_path_count": len(unique_paths)
        })

    df = pd.DataFrame(records)

    # Select the features for the model
    features = df[["total_requests", "error_rate", "unique_path_count"]]


    # 2. Model training & prediction
    # Initialise the Isolation Forest model
    # 'contamination' is the expected proportion of outliers in the data
    model = IsolationForest(contamination="auto", random_state=42)

    # Train the model and generate predictions
    df["anomaly_score"] = model.fit_predict(features)   # "-1" = anomaly


    # 3. Return the results
    anomalous_ips = set(df[df["anomaly_score"] == -1]["ip_address"])

    print(f"[*] Anomaly detection complete.\nFound {len(anomalous_ips)} anomalous IP addresses")
    return anomalous_ips


