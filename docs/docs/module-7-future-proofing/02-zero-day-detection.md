---
id: 02-zero-day-detection
title: Chapter 2
sidebar_position: 2
---

# Chapter 2: Zero-Day Detection & Behavioral Analysis

## 2.1 The Zero-Day Problem

**Zero-Days**: Vulnerabilities unknown to vendors, with NO existing signatures

### Traditional Approach (Fails Against Zero-Days)
```
Signature-Based Detection:
├─ Need known malware hash
├─ Need known network pattern
├─ Need known C2 domain
└─ Result: Zero-days are invisible for 6-18 months (average 437 days)
```

### AI SOC Approach (Behavioral Analysis)
```
Behavioral Detection:
├─ Watch HOW threat behaves, not WHAT it is
├─ Baseline normal behavior for each host/user
├─ Detect deviation from baseline (anomaly)
├─ No signatures needed
└─ Result: Zero-days detected in hours/days (not months)
```

---

## 2.2 Behavioral Baseline Learning

### Building User/Host Baselines

```python
class BehavioralBaseline:
    """
    Builds statistical baselines for normal behavior
    to detect anomalies (potential zero-days)
    """

    def __init__(self, user_id, host_id, baseline_days=30):
        self.user_id = user_id
        self.host_id = host_id
        self.baseline_days = baseline_days
        self.baseline_data = self.compute_baseline()

    def compute_baseline(self):
        """
        Compute statistical profile of normal behavior
        """
        baseline = {
            'user_activity': {
                'login_hours': self.get_normal_login_hours(),      # 8 AM - 6 PM
                'login_days': self.get_normal_login_days(),        # Mon-Fri
                'typical_locations': self.get_typical_login_ips(),  # 3-5 IP ranges
                'location_deviation_threshold': 0.15              # Alert if >15% deviation
            },

            'process_behavior': {
                'typical_processes': self.get_typical_processes(),  # Explorer, Outlook, Chrome
                'process_chain_patterns': self.get_process_chains(),
                'spawning_parent_processes': {
                    'explorer.exe': ['cmd.exe', 'notepad.exe'],    # Normal spawns
                    'outlook.exe': ['iexplore.exe'],
                    'chrome.exe': ['cmd.exe']  # Unusual but possible
                },
                'suspicious_parent_combinations': {
                    'winword.exe': ['powershell.exe'],  # Alert level: HIGH
                    'excel.exe': ['cmd.exe', 'wscript.exe'],  # Alert level: HIGH
                }
            },

            'network_behavior': {
                'typical_destinations': self.get_typical_network_destinations(),
                'typical_ports': [80, 443, 25, 53],
                'typical_protocols': ['HTTP', 'HTTPS', 'DNS', 'SMTP'],
                'typical_data_volume_mb_per_day': 150,
                'data_volume_deviation_threshold': 0.50  # Alert if 2x normal
            },

            'file_access': {
                'typical_directories': [
                    'C:\\Users\\john\\Documents\\',
                    'C:\\Users\\john\\Desktop\\',
                    'C:\\Users\\john\\Downloads\\',
                    'G:\\Shared Drives\\',  # Network share
                ],
                'typical_file_types': ['.docx', '.xlsx', '.pdf', '.txt'],
                'file_operations_per_hour': 45,
                'file_operations_deviation_threshold': 0.80  # Alert if 5x normal
            },

            'registry_access': {
                'typical_registry_paths': [
                    'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\',
                    'HKEY_LOCAL_MACHINE\\Software\\Microsoft\\',
                ],
                'modifications_per_day': 3,
                'suspicious_modification_threshold': 0.10  # Alert on few mods to suspicious paths
            }
        }

        return baseline

    def score_anomaly(self, event):
        """
        Score how anomalous an event is
        Returns 0-100 (0=normal, 100=highly suspicious)
        """
        anomaly_score = 0

        # Check user activity
        if not self.is_normal_login_time(event['timestamp']):
            anomaly_score += 15  # Off-hours login

        if not self.is_normal_login_location(event['source_ip']):
            anomaly_score += 20  # Unusual location

        # Check process behavior
        if self.is_suspicious_process_spawn(event['process'], event['parent_process']):
            anomaly_score += 30  # Suspicious parent-child relationship

        # Check network behavior
        if self.is_unusual_network_destination(event['destination']):
            anomaly_score += 25  # Suspicious network connection

        # Check file access
        if event['file_operation_rate'] > self.baseline_data['file_access']['file_operations_per_hour'] * 5:
            anomaly_score += 40  # Bulk file operations (ransomware indicator)

        # Check registry access
        if self.is_suspicious_registry_path(event['registry_path']):
            anomaly_score += 25  # Persistence mechanism

        return min(anomaly_score, 100)

    def get_normal_login_hours(self):
        """
        Analyze last 30 days to find typical login hours
        """
        login_times = self.query_historical_logins(days=30)
        hours = [lt.hour for lt in login_times]

        # Find hour range where 95% of logins occur
        sorted_hours = sorted(hours)
        lower_bound = sorted_hours[int(len(sorted_hours) * 0.05)]
        upper_bound = sorted_hours[int(len(sorted_hours) * 0.95)]

        return (lower_bound, upper_bound)  # e.g., (7, 20) = 7 AM - 8 PM
```

---

## 2.3 Real-World Zero-Day Detection Example

### Case Study: Detecting Novel Ransomware (No Known Signatures)

```
Timeline:
─────────
Day 0:  New ransomware deployed (NOT in any threat feed)
        • No YARA signature exists
        • No antivirus definitions
        • No Sigma rule
        • No IOCs in threat intelligence

Day 0, Hour 1: AI SOC Behavioral Detection
        Event 1: Process spawned from Office macro
        Event 2: Registry modification
        Event 3: Network connection to unknown IP
        Event 4: Bulk file creation with unusual extension

        Anomaly Scores:
        ├─ Event 1: +15 (Office macro = slightly unusual)
        ├─ Event 2: +25 (Registry persistence = suspicious)
        ├─ Event 3: +25 (Network to unknown dest = suspicious)
        └─ Event 4: +40 (Bulk file ops = high risk)

        Total: 105 (exceeds threshold of 50)
        Result: ALERT GENERATED ✓

        No signatures needed. Detected by deviation from baseline.

Day 0, Hour 2: Threat Intelligence Correlation
        • Correlate novel patterns with known ATT&CK techniques
        • Match against threat actor playbooks
        • Confidence: 87% likely ransomware

Day 0, Hour 4: Automated Response
        • Generate Sigma/YARA rules from observed behaviors
        • Deploy rules across all hosts
        • Block C2 communication
        • Isolate infected host

Day 1: Rule Updates
        • New rule added to detection engine
        • If this variant appears again, detected immediately

Traditional SOC Same Scenario:
├─ Signatures released: ~437 days after zero-day disclosure
├─ Time to detect in their environment: 6-18 months
├─ Estimated damage: $1-3M
└─ Result: Customer data already exfiltrated
```

---

## 2.4 Behavioral Analysis Techniques

### Technique 1: Statistical Anomaly Detection

```python
from scipy import stats
import numpy as np

class StatisticalAnomalyDetector:
    """
    Detect deviations using statistical methods
    """

    def detect_using_zscore(self, event_value, baseline_values):
        """
        Z-score: How many standard deviations from mean?
        Values > 3 are statistical anomalies
        """
        mean = np.mean(baseline_values)
        std_dev = np.std(baseline_values)

        z_score = (event_value - mean) / std_dev

        if abs(z_score) > 3:
            return True  # Anomaly detected
        return False

    def detect_using_iqr(self, event_value, baseline_values):
        """
        Interquartile Range: Outlier detection
        """
        q1 = np.percentile(baseline_values, 25)
        q3 = np.percentile(baseline_values, 75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        if event_value < lower_bound or event_value > upper_bound:
            return True  # Outlier detected
        return False

    def detect_using_isolation_forest(self, event_features, baseline_samples):
        """
        Isolation Forest: ML-based anomaly detection
        """
        from sklearn.ensemble import IsolationForest

        # Train on normal baseline
        iso_forest = IsolationForest(contamination=0.1)
        iso_forest.fit(baseline_samples)

        # Score new event
        anomaly_score = iso_forest.score_samples([event_features])[0]

        if anomaly_score < -0.5:  # Anomalous (more negative = more anomalous)
            return True
        return False
```

---