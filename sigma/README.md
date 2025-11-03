# Sigma Detection Rules

This directory contains Sigma rules for detecting attack patterns identified by the PyLog Threat Analyser.

## What is Sigma?

Sigma is a generic signature format for SIEM systems, allowing security teams to write detection rules once and deploy them across multiple platforms (Splunk, ELK, QRadar, etc.). Think of it as "YARA for log events."

## Rules Included

### 1. Credential Stuffing (`credential_stuffing.yml`)
**Detects:** Rapid failed login attempts (100+ in 5 minutes)  
**Severity:** High  
**MITRE ATT&CK:** T1110.003 (Password Spraying), T1110.004 (Credential Stuffing)

Identifies automated credential stuffing attacks where attackers test stolen username/password pairs against authentication endpoints.

### 2. Web Vulnerability Scanning (`web_vulnerability_scan.yml`)
**Detects:** Automated probing of common vulnerability paths (50+ in 10 minutes)  
**Severity:** High  
**MITRE ATT&CK:** T1595.002 (Vulnerability Scanning), T1190 (Exploit Public-Facing Application)

Flags reconnaissance activity where attackers scan for exposed configuration files, admin panels, and backup files.

### 3. Excessive HTTP Errors (`excessive_http_errors.yml`)
**Detects:** Abnormal error rates from single IP (80+ errors in 5 minutes, >85% error rate)  
**Severity:** Medium  
**MITRE ATT&CK:** T1595 (Active Scanning)

Identifies suspicious activity patterns that may indicate attack probing, broken automated tools, or misconfigured bots.

## How to Use These Rules

### Convert to Your SIEM Platform

Use the [sigmac](https://github.com/SigmaHQ/sigma) converter tool:
```bash
# For Splunk
sigmac -t splunk credential_stuffing.yml

# For Elasticsearch
sigmac -t es-qs web_vulnerability_scan.yml

# For QRadar
sigmac -t qradar excessive_http_errors.yml
```

### Integration with PyLog Threat Analyser

These Sigma rules complement the ML-based anomaly detection:

- **Sigma Rules:** Fast, reliable detection of KNOWN attack patterns
- **ML Anomaly Detection:** Catches UNKNOWN or novel attacks that evade signatures

**Recommended Workflow:**
1. Deploy Sigma rules for immediate alerting on common attacks
2. Use PyLog Threat Analyser for deeper analysis and zero-day threat detection
3. When ML model flags new attack patterns, create Sigma rules for faster detection next time

## Customisation

Adjust thresholds based on your environment:

- **High-traffic sites:** Increase count thresholds to reduce false positives
- **Low-traffic sites:** Decrease timeframes for faster detection
- **Development environments:** Add specific IP ranges to `falsepositives`

## References

- [Sigma Specification](https://github.com/SigmaHQ/sigma-specification)
- [Sigma Rule Repository](https://github.com/SigmaHQ/sigma)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)