#!/usr/bin/env python3
"""
Deploy Module 6 and 7 to Docusaurus docs structure and prepare for GitHub push
"""

import re
import os
from pathlib import Path

# Base paths
PROJECT_ROOT = Path("D:\\hafiz naveed chuhan\\Agentic-AI-CYBERSECURITY")
MODULE_6_SOURCE = PROJECT_ROOT / "Module_6_Advanced_Implementation_Operational_Excellence.md"
MODULE_7_SOURCE = PROJECT_ROOT / "Module_7_Future_Proofing_Continuous_Learning.md"
DOCS_DIR = PROJECT_ROOT / "docs" / "docs"

# Create module directories
MODULE_6_DIR = DOCS_DIR / "module-6-advanced-implementation"
MODULE_7_DIR = DOCS_DIR / "module-7-future-proofing"

MODULE_6_DIR.mkdir(parents=True, exist_ok=True)
MODULE_7_DIR.mkdir(parents=True, exist_ok=True)

print("[OK] Created directory structure")

def read_file(path):
    """Read markdown file"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    """Write markdown file"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] Created: {path.name}")

# Read source files
module6_content = read_file(MODULE_6_SOURCE)
module7_content = read_file(MODULE_7_SOURCE)

# Module 6: Index
module6_index = """---
id: index
title: Module 6 - Advanced Implementation & Operational Excellence
sidebar_position: 6
---

# Module 6: Advanced Implementation and Operational Excellence

## Overview

This module transforms theoretical AI SOC architecture into production-grade operational systems. Learn how **7 specialized AI Employs** orchestrate to detect, investigate, and remediate complex threats in real-time with **95% accuracy** and **10x faster response times** than traditional SOCs.

## Learning Outcomes

By the end of this module, you will understand:

- How coordinated AIs respond to ransomware attacks in <2 seconds
- Technical basis for 95% detection accuracy across 4 metrics
- Production-grade Sigma and YARA detection rule creation
- SOC 2 compliant infrastructure design
- Alert fatigue reduction through intelligent reporting

## Module Structure

| Chapter | Topics |
|---------|--------|
| **1. Ransomware Simulation** | Attack workflow, 7 AI Employs in action, MITRE ATT&CK mapping |
| **2. Accuracy Deep Dive** | Metrics breakdown, ML ensemble, speed optimization |
| **3. Detection Rules** | Sigma/YARA rules, tuning methodology, conversions |
| **4. Compliance** | Encryption, audit logs, RBAC, SOC 2 & GDPR |
| **5. Reporting** | Alert fatigue, report templates, KPIs |

## Key Metrics

- **Detection Speed**: 1.2 seconds (vs 45 min average SOC)
- **Accuracy**: 95% (TPR: 96%, FPR: 2%, Precision: 97%, F1: 0.965)
- **False Positive Reduction**: 80% fewer alerts
- **Compliance**: SOC 2 Type II certified, GDPR compliant
"""

write_file(MODULE_6_DIR / "index.md", module6_index)

# Module 7: Index
module7_index = """---
id: index
title: Module 7 - Future-Proofing & Continuous Learning
sidebar_position: 7
---

# Module 7: Future-Proofing Your AI SOC

## Overview

Strategic guidance for evolving threats, continuous improvement, and global operations. Learn how to future-proof your AI SOC against emerging threats, zero-day attacks, and adversarial adaptation.

## Learning Outcomes

By the end of this module, you will understand:

- Continuous learning mechanisms for automated model improvement
- Zero-day detection using behavioral analysis
- Threat actor evolution prediction and adaptation
- Global SOC architecture with GDPR compliance

## Module Structure

| Chapter | Topics |
|---------|--------|
| **1. Continuous Learning** | Feedback loops, weekly retraining, model versioning |
| **2. Zero-Day Detection** | Behavioral baselines, anomaly scoring, statistical methods |
| **3. Threat Actor Evolution** | TTP tracking, evolution timeline, prediction models |
| **4. Global/Multi-Region SOCs** | Distributed architecture, GDPR compliance, federated intel |

## Strategic Focus

- **Adaptation**: Stay ahead of evolving threats
- **Scale**: Operate globally with regional compliance
- **Intelligence**: Federated threat sharing across regions
- **Improvement**: 3.2% weekly accuracy gains
"""

write_file(MODULE_7_DIR / "index.md", module7_index)

# Extract and create Module 6 chapters
def extract_chapter_6(chapter_num, start_marker, end_marker):
    """Extract chapter from Module 6"""
    start_idx = module6_content.find(start_marker)
    if end_marker:
        end_idx = module6_content.find(end_marker, start_idx)
        if end_idx == -1:
            end_idx = len(module6_content)
    else:
        end_idx = len(module6_content)

    return module6_content[start_idx:end_idx].strip()

chapters_6 = [
    (1, "# Chapter 1:", "# Chapter 2:"),
    (2, "# Chapter 2:", "# Chapter 3:"),
    (3, "# Chapter 3:", "# Chapter 4:"),
    (4, "# Chapter 4:", "# Chapter 5:"),
    (5, "# Chapter 5:", "---"),  # Last chapter
]

chapter_files_6 = [
    "01-ransomware-simulation.md",
    "02-accuracy-deep-dive.md",
    "03-detection-rules.md",
    "04-compliance.md",
    "05-reporting.md",
]

for (num, start, end), filename in zip(chapters_6, chapter_files_6):
    content = extract_chapter_6(num, start, end)
    # Add frontmatter
    frontmatter = f"""---
id: chapter-{num}
title: Chapter {num}
sidebar_position: {num}
---

"""
    write_file(MODULE_6_DIR / filename, frontmatter + content)

# Extract and create Module 7 chapters
chapters_7 = [
    (1, "# Chapter 1:", "# Chapter 2:"),
    (2, "# Chapter 2:", "# Chapter 3:"),
    (3, "# Chapter 3:", "# Chapter 4:"),
    (4, "# Chapter 4:", "---"),  # Last chapter
]

chapter_files_7 = [
    "01-continuous-learning.md",
    "02-zero-day-detection.md",
    "03-threat-actor-evolution.md",
    "04-global-soc.md",
]

def extract_chapter_7(chapter_num, start_marker, end_marker):
    """Extract chapter from Module 7"""
    start_idx = module7_content.find(start_marker)
    if end_marker:
        end_idx = module7_content.find(end_marker, start_idx)
        if end_idx == -1:
            end_idx = len(module7_content)
    else:
        end_idx = len(module7_content)

    return module7_content[start_idx:end_idx].strip()

for (num, start, end), filename in zip(chapters_7, chapter_files_7):
    content = extract_chapter_7(num, start, end)
    # Add frontmatter
    frontmatter = f"""---
id: chapter-{num}
title: Chapter {num}
sidebar_position: {num}
---

"""
    write_file(MODULE_7_DIR / filename, frontmatter + content)

print("\n[SUCCESS] All Docusaurus files created successfully!")
print(f"\nModule 6: {len(list(MODULE_6_DIR.glob('*.md')))} files")
print(f"Module 7: {len(list(MODULE_7_DIR.glob('*.md')))} files")
