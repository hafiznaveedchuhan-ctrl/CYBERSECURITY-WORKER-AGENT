---
id: chapter-4
title: Chapter 4
sidebar_position: 4
---

# Chapter 4: Enterprise Security & Compliance Architecture

## 4.1 Encryption: Protecting Data at Rest and in Transit

### Data Encryption Strategy

**At Rest** (Data stored on disk):
```
┌─────────────────┐
│ Raw Alert Data  │
└────────┬────────┘
         │
         ▼
┌──────────────────────────┐
│ AES-256 Encryption       │
│ (FIPS 140-2 certified)   │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Encrypted Data on Disk   │
│ (At rest: AES-256-GCM)   │
└──────────────────────────┘
```

**Implementation**:
```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64
import os

class DataEncryption:
    def __init__(self, master_key):
        self.master_key = master_key

    def encrypt_alert_data(self, alert_data: dict) -> bytes:
        """
        Encrypt alert data before storage
        """
        # Derive key from master key
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=os.urandom(16),
            iterations=100000,
        )

        # Use Fernet for authenticated encryption
        key = base64.urlsafe_b64encode(
            kdf.derive(self.master_key)
        )
        f = Fernet(key)

        # Encrypt
        encrypted = f.encrypt(json.dumps(alert_data).encode())
        return encrypted

    def decrypt_alert_data(self, encrypted_data: bytes) -> dict:
        """
        Decrypt alert data on retrieval
        """
        f = Fernet(self.master_key)
        decrypted = f.decrypt(encrypted_data)
        return json.loads(decrypted.decode())
```

**In Transit** (Data traveling over network):
```
┌────────────────┐
│  Alert Data    │
└────────┬───────┘
         │
         ▼
    ┌─────────────────────┐
    │ TLS 1.3 Encryption  │
    │ 256-bit ciphers     │
    └──────────┬──────────┘
               │
               ▼
         ┌──────────────┐
         │ HTTPS/QUIC   │
         │ (Encrypted)  │
         └──────────────┘
```

**Compliance Benefit**:
- ✓ SOC 2 Trust Service Criterion 7.1 (Encryption)
- ✓ GDPR Article 32 (Security of processing)
- ✓ HIPAA Technical Safeguards (§164.312(a)(2)(i))

---

## 4.2 Audit Logs: Complete Activity Trail

### Audit Log Architecture

Every action in the AI SOC system is logged:

```python
class AuditLogger:
    def __init__(self, log_sink):
        self.log_sink = log_sink

    def log_action(self, action_type: str, actor: str,
                   resource: str, result: str, details: dict):
        """
        Log all system actions for compliance
        """
        audit_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'action_type': action_type,  # create, read, update, delete, execute
            'actor': actor,  # User ID or service account
            'resource': resource,  # Alert ID, Incident ID, etc.
            'result': result,  # success, failure, denied
            'details': details,
            'source_ip': get_client_ip(),
            'user_agent': get_user_agent(),
            'correlation_id': get_correlation_id(),
        }

        # Write to immutable audit log
        self.log_sink.write_immutable(audit_entry)

        # Also send to SIEM for monitoring
        self.send_to_siem(audit_entry)

# Example audit log entries
auditlog.log_action(
    action_type='read',
    actor='analyst@company.com',
    resource='ALERT-2024-001842',
    result='success',
    details={'reason': 'Incident investigation'}
)

auditlog.log_action(
    action_type='delete',
    actor='admin@company.com',
    resource='ALERT-2024-001843',
    result='success',
    details={'reason': 'False positive cleanup', 'count': 42}
)
```

**Audit Log Sample**:
```json
{
  "timestamp": "2024-01-15T14:32:15.843Z",
  "action_type": "read",
  "actor": "john.smith@company.com",
  "actor_role": "security_analyst",
  "resource_type": "incident",
  "resource_id": "INC-2024-0001842",
  "result": "success",
  "details": {
    "purpose": "Ransomware incident investigation",
    "data_accessed": [
      "alert_details",
      "enrichment_data",
      "threat_intelligence",
      "forensic_artifacts"
    ]
  },
  "source_ip": "192.168.1.50",
  "session_id": "sess_abc123def456",
  "correlation_id": "corr_xyz789",
  "retention_period": "7_years"  # SOC 2 requirement
}
```

**Log Retention Policy**:
- ✓ Immutable storage (WORM - Write Once Read Many)
- ✓ Encrypted audit logs (AES-256)
- ✓ Tamper-evident hashing (SHA-256)
- ✓ 7-year retention (SOC 2 requirement)
- ✓ Geographic redundancy (multiple data centers)

---

## 4.3 Role-Based Access Control (RBAC)

### RBAC Model

```
┌─────────────────────────────────────────────────┐
│              Roles Definition                   │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Role: SOC Analyst (L1)                   │  │
│  ├──────────────────────────────────────────┤  │
│  │ Permissions:                              │  │
│  │ • READ alerts (all)                       │  │
│  │ • CREATE incident tickets                 │  │
│  │ • UPDATE incident status                  │  │
│  │ • Cannot: DELETE, EXPORT, MODIFY rules   │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Role: Security Engineer                  │  │
│  ├──────────────────────────────────────────┤  │
│  │ Permissions:                              │  │
│  │ • READ/WRITE rules (Sigma, YARA)         │  │
│  │ • CREATE/TEST detection rules             │  │
│  │ • DEPLOY rules to production              │  │
│  │ • Cannot: DELETE incidents, EXPORT data  │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Role: Incident Response Lead             │  │
│  ├──────────────────────────────────────────┤  │
│  │ Permissions:                              │  │
│  │ • All analyst permissions                 │  │
│  │ • DELETE false positive incidents         │  │
│  │ • EXPORT incident reports                 │  │
│  │ • TRIGGER automated response actions      │  │
│  │ • Cannot: DELETE audit logs, MODIFY RBAC │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Role: SOC Manager / CISO                 │  │
│  ├──────────────────────────────────────────┤  │
│  │ Permissions:                              │  │
│  │ • ALL permissions                         │  │
│  │ • Modify RBAC roles and assignments       │  │
│  │ • Review audit logs                       │  │
│  │ • Generate compliance reports             │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Role: Integration Service Account        │  │
│  ├──────────────────────────────────────────┤  │
│  │ Permissions:                              │  │
│  │ • API READ (alerts)                       │  │
│  │ • API WRITE (update status)               │  │
│  │ • Cannot: UI access, DELETE, MODIFY      │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
└─────────────────────────────────────────────────┘
```

**RBAC Implementation**:

```python
class RoleBasedAccessControl:
    def __init__(self, user_id, roles):
        self.user_id = user_id
        self.roles = roles  # List of role names
        self.permissions = self._compute_permissions()

    def _compute_permissions(self) -> set:
        """
        Compute effective permissions from all assigned roles
        """
        permissions = set()

        role_permissions = {
            'analyst_l1': {
                'read_alerts',
                'create_incidents',
                'update_incidents'
            },
            'security_engineer': {
                'read_alerts',
                'write_detection_rules',
                'deploy_rules',
                'test_rules'
            },
            'incident_lead': {
                'read_alerts',
                'create_incidents',
                'update_incidents',
                'delete_false_positives',
                'export_reports',
                'trigger_response'
            },
            'ciso': {
                '*'  # All permissions
            }
        }

        for role in self.roles:
            permissions.update(role_permissions.get(role, set()))

        return permissions

    def has_permission(self, action: str) -> bool:
        """
        Check if user has permission for action
        """
        if '*' in self.permissions:
            return True
        return action in self.permissions

    def enforce_access(self, action: str, resource: str):
        """
        Enforce access control
        """
        if not self.has_permission(action):
            raise AccessDeniedException(
                f"User {self.user_id} does not have {action} permission"
            )

        # Log access attempt
        auditlog.log_action(
            action_type=action,
            actor=self.user_id,
            resource=resource,
            result='success'
        )
```

---

## 4.4 Compliance Alignment

### SOC 2 Type II Mapping

| SOC 2 Trust Service Criterion | Implementation | Evidence |
|------|-----|------|
| **CC6.1** User Access Provisioning | RBAC enforces least privilege | RBAC matrix, audit logs |
| **CC6.2** User Access Rights | Role definitions reviewed quarterly | Role review meetings |
| **CC7.1** Data Encryption | AES-256 at rest, TLS 1.3 in transit | Encryption key management |
| **CC7.2** Change Management | All rule changes logged, reviewed | Git commits, code review |
| **CC7.3** Logging & Monitoring | Immutable audit logs (7-year retention) | Audit log samples |
| **CC8.1** Incident Response | Automated detection + manual escalation | Incident response playbooks |
| **CC9.1** Vulnerability Mgmt | Pen testing + code scanning | Pentest reports, CVE tracking |
| **CC9.2** Configuration Mgmt | IaC, config drift detection | Terraform files, compliance scans |
| **CC9.3** Secure Development | Secure coding practices, SAST/DAST | Code review process, test results |

### GDPR Alignment

| GDPR Article | Requirement | Implementation |
|------|-----|------|
| **Article 32** | Security of processing | AES-256 encryption, access controls |
| **Article 33** | Breach notification | Automated detection + 72-hour notification |
| **Article 34** | Notifying data subjects | Breach notification workflow |
| **Article 5(1)(e)** | Data minimization | Log retention policies, anonymization |
| **Article 17** | Right to be forgotten | Automated data deletion on request |
| **Article 25** | Privacy by design | Encryption first, minimize collection |

---