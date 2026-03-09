"""
AXIOM Configuration Module
Configuration settings for the AXIOM ethics auditing agent.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class AXIOMConfig:
    """Configuration for AXIOM ethics auditing system."""
    
    # Model Configuration
    model_name: str = "MultiverseComputingCAI/HyperNova-60B-2602"
    max_tokens: int = 4096
    temperature: float = 0.3
    
    # Risk Scoring Thresholds
    risk_thresholds: Dict[str, float] = field(default_factory=lambda: {
        "LOW": 0.0,
        "MEDIUM": 0.3,
        "HIGH": 0.6,
        "CRITICAL": 0.8
    })
    
    # Carbon Footprint Baseline (kg CO2/kWh)
    carbon_baseline: float = 0.233
    
    # Output Paths
    output_dir: str = "./output"
    legal_docs_dir: str = "./legal_docs"
    alternatives_dir: str = "./alternatives"
    temp_repo_dir: str = "./temp_repos"
    
    # Semantic Analysis Settings
    semantic_analysis_enabled: bool = True
    llm_analysis_enabled: bool = True
    min_code_lines_for_analysis: int = 3
    
    # Detection Sensitivity
    detect_low_risk: bool = True
    detect_data_retention: bool = True
    detect_consent_flows: bool = True
    detect_documentation_gaps: bool = True
    
    # LOW Risk Patterns (Documentation and Minor Concerns)
    low_risk_patterns: Dict[str, Dict] = field(default_factory=lambda: {
        "missing_data_retention_doc": {
            "description": "Missing documentation for data retention policies",
            "keywords": ["retention", "retain", "store", "storage", "keep data", "save data"],
            "risk_score": 0.15,
            "category": "DOCUMENTATION"
        },
        "indirect_user_profiling": {
            "description": "Potential indirect user profiling through behavior analysis",
            "keywords": ["behavior", "pattern", "profile", "user preference", "usage pattern"],
            "risk_score": 0.2,
            "category": "PRIVACY"
        },
        "insufficient_logging": {
            "description": "Insufficient audit logging for data access",
            "keywords": ["log", "audit", "access log"],
            "risk_score": 0.18,
            "category": "SECURITY"
        },
        "missing_consent_mechanism": {
            "description": "No explicit consent mechanism for data collection",
            "keywords": ["collect", "gather", "input", "form"],
            "risk_score": 0.22,
            "category": "CONSENT"
        },
        "implicit_data_sharing": {
            "description": "Implicit data sharing through third-party integrations",
            "keywords": ["api", "external", "service", "integration", "webhook"],
            "risk_score": 0.25,
            "category": "SHARING"
        },
        "insecure_data_handling": {
            "description": "Potential insecure data handling practices",
            "keywords": ["password", "token", "key", "secret", "credential"],
            "risk_score": 0.28,
            "category": "SECURITY"
        },
        "missing_error_handling": {
            "description": "Missing error handling for sensitive operations",
            "keywords": ["try:", "except", "error", "exception", "catch"],
            "risk_score": 0.15,
            "category": "RELIABILITY"
        },
        "verbose_logging": {
            "description": "Verbose logging that may expose sensitive information",
            "keywords": ["print(", "log.", "debug", "console.log"],
            "risk_score": 0.2,
            "category": "PRIVACY"
        },
        "hardcoded_values": {
            "description": "Hardcoded configuration values that should be externalized",
            "keywords": ["config", "setting", "constant"],
            "risk_score": 0.12,
            "category": "MAINTAINABILITY"
        },
        "missing_input_validation": {
            "description": "Missing input validation on user-facing functions",
            "keywords": ["input", "request", "params", "args"],
            "risk_score": 0.25,
            "category": "SECURITY"
        }
    })
    
    # MEDIUM+ Risk Patterns
    tracking_patterns: List[str] = field(default_factory=lambda: [
        r"cookie.*track",
        r"fingerprint",
        r"user.*track",
        r"analytics.*collect",
        r"third.party.*share",
        r"location.*track",
        r"behavior.*monitor",
        r"session.*track",
        r"event.*track",
        r"click.*track",
        r"scroll.*track",
        r"heatmap"
    ])
    
    bias_patterns: List[str] = field(default_factory=lambda: [
        r"demographic",
        r"race|ethnicity|gender",
        r"protected.*class",
        r"discriminat",
        r"stereotyp",
        r"proxy.*variable",
        r"age|religion|nationality",
        r"income.*bracket",
        r"zip.*code.*bias",
        r"redlining"
    ])
    
    surveillance_patterns: List[str] = field(default_factory=lambda: [
        r"monitor.*employee",
        r"keystroke.*log",
        r"screen.*record",
        r"camera.*access",
        r"audio.*record",
        r"continuous.*track",
        r"activity.*log",
        r"productivity.*track",
        r"time.*track",
        r"screenshot"
    ])
    
    dark_pattern_indicators: List[str] = field(default_factory=lambda: [
        r"confirm.*shaming",
        r"roach.*motel",
        r"forced.*continuity",
        r"hidden.*cost",
        r"bait.*switch",
        r"misdirection",
        r"urgency.*pressure",
        r"dark.*pattern",
        r"trick.*question",
        r"privacy.*zuckering",
        r"roachmotel"
    ])
    
    # Semantic Analysis Prompts
    semantic_detection_prompt: str = """You are an expert AI ethics auditor analyzing code for ethical implications.

Analyze the following code for ethical issues related to:
1. DATA PRIVACY - Insecure handling, lack of encryption, excessive collection
2. USER CONSENT - Missing consent flows, implicit data collection
3. ALGORITHMIC BIAS - Discriminatory logic, unfair treatment
4. SURVEILLANCE - Excessive monitoring, tracking
5. TRANSPARENCY - Missing documentation, opaque operations
6. DATA RETENTION - Unclear retention policies
7. THIRD-PARTY SHARING - Uncontrolled data sharing

For each issue found, provide:
- Issue type (one of: PRIVACY, CONSENT, BIAS, SURVEILLANCE, TRANSPARENCY, RETENTION, SHARING)
- Risk level (LOW, MEDIUM, HIGH, CRITICAL)
- Description of the issue
- Specific code evidence
- Recommendation for fix

Code to analyze:
```{language}
{code}
```

Respond in JSON format:
{{
  "issues": [
    {{
      "type": "PRIVACY",
      "risk_level": "MEDIUM",
      "description": "...",
      "evidence": "...",
      "recommendation": "...",
      "line_numbers": [1, 2]
    }}
  ],
  "summary": "..."
}}"""


# GDPR Article References
GDPR_ARTICLES = {
    "Article_5": "Principles relating to processing of personal data",
    "Article_6": "Lawfulness of processing",
    "Article_7": "Conditions for consent",
    "Article_17": "Right to erasure ('right to be forgotten')",
    "Article_22": "Automated individual decision-making, including profiling",
    "Article_25": "Data protection by design and by default",
    "Article_32": "Security of processing"
}

# CCPA Section References
CCPA_SECTIONS = {
    "Section_1798.100": "Right to know what personal information is collected",
    "Section_1798.105": "Right to deletion of personal information",
    "Section_1798.110": "Right to know personal information sold/disclosed",
    "Section_1798.115": "Right to opt-out of sale of personal information",
    "Section_1798.125": "Non-discrimination for exercising rights"
}

# Issue Categories and Descriptions
ISSUE_CATEGORIES = {
    "PRIVACY": "Data privacy and protection concerns",
    "CONSENT": "User consent and permission issues",
    "BIAS": "Algorithmic bias and fairness concerns",
    "SURVEILLANCE": "Excessive monitoring or tracking",
    "TRANSPARENCY": "Lack of transparency or documentation",
    "RETENTION": "Data retention policy concerns",
    "SHARING": "Third-party data sharing issues",
    "SECURITY": "Security and access control concerns",
    "DOCUMENTATION": "Missing or inadequate documentation",
    "RELIABILITY": "Code reliability and error handling"
}

# Risk Level Descriptions
RISK_DESCRIPTIONS = {
    "LOW": "Minor concern that should be documented and monitored",
    "MEDIUM": "Moderate risk that requires review and potential mitigation",
    "HIGH": "Significant risk that requires immediate attention",
    "CRITICAL": "Severe risk that must be addressed before deployment"
}
