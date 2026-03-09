"""
AXIOM Detection Module (Phase 1) - ROBUST VERSION
Scans code for tracking, bias, surveillance, dark patterns, and security issues.
Assigns risk scores from LOW to CRITICAL using semantic analysis.
"""

import re
import ast
import json
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk levels for ethical issues."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class EthicalIssue:
    """Represents an identified ethical issue."""
    issue_type: str
    risk_level: RiskLevel
    risk_score: float
    line_number: int
    code_snippet: str
    description: str
    evidence: List[str] = field(default_factory=list)
    recommendation: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "id": f"{self.issue_type}_{self.line_number}",
            "issue_type": self.issue_type,
            "category": self.issue_type,
            "risk_level": self.risk_level.value,
            "risk_score": self.risk_score,
            "line_number": self.line_number,
            "code_snippet": self.code_snippet,
            "description": self.description,
            "evidence": self.evidence,
            "recommendation": self.recommendation
        }


class AXIOMDetector:
    """
    Phase 1: Detection Module - ROBUST VERSION
    Scans code for ethical issues using pattern matching and semantic analysis.
    """
    
    def __init__(self, config=None):
        self.config = config
        self.issues: List[EthicalIssue] = []
        self.risk_thresholds = {
            "LOW": 0.0,
            "MEDIUM": 0.3,
            "HIGH": 0.6,
            "CRITICAL": 0.8
        }
        
        # Expanded detection patterns for ROBUST detection
        self.patterns = {
            # CRITICAL: Security vulnerabilities
            "HARDCODED_SECRET": {
                "pattern": r'(password|secret|key|token)\s*=\s*["\'][^"\']+["\']',
                "description": "Hardcoded credentials or secrets detected",
                "risk_score": 0.9,
                "category": "SECURITY"
            },
            "CORS_WILDCARD": {
                "pattern": r'allow_origins\s*=\s*\[\s*["\']\*["\']\s*\]',
                "description": "CORS configured with wildcard origin - allows any domain",
                "risk_score": 0.85,
                "category": "SECURITY"
            },
            "INSECURE_CORS": {
                "pattern": r'allow_credentials\s*=\s*True.*allow_origins.*\*',
                "description": "Insecure CORS: credentials allowed with wildcard origin",
                "risk_score": 0.9,
                "category": "SECURITY"
            },
            
            # HIGH: Data handling issues
            "CONSOLE_LOG_CREDENTIALS": {
                "pattern": r'console\.log.*\b(password|secret|token|key)\b',
                "description": "Sensitive credentials logged to console",
                "risk_score": 0.75,
                "category": "PRIVACY"
            },
            "PRINT_CREDENTIALS": {
                "pattern": r'print\s*\(.*\b(password|secret|token|key)\b',
                "description": "Sensitive credentials printed to output",
                "risk_score": 0.75,
                "category": "PRIVACY"
            },
            "NO_INPUT_VALIDATION": {
                "pattern": r'@app\.(post|get|put|delete).*\n.*(?!.*validate)(?!.*schema).*(?:request|req|input)',
                "description": "API endpoint without input validation",
                "risk_score": 0.65,
                "category": "SECURITY"
            },
            "UNVALIDATED_FILE_UPLOAD": {
                "pattern": r'UploadFile|upload.*file.*(?!.*validate)(?!.*check)',
                "description": "File upload without validation checks",
                "risk_score": 0.7,
                "category": "SECURITY"
            },
            
            # MEDIUM: Privacy and consent issues
            "USER_DATA_COLLECTION": {
                "pattern": r'(email|name|password|user).*create|User\.create|insert.*user',
                "description": "User data collection without explicit consent mechanism",
                "risk_score": 0.55,
                "category": "CONSENT"
            },
            "THIRD_PARTY_API": {
                "pattern": r'(openai|anthropic|google|azure|aws)\s*=|api_key.*=|apikey',
                "description": "Third-party API integration - data may be shared externally",
                "risk_score": 0.5,
                "category": "SHARING"
            },
            "COOKIE_SETTING": {
                "pattern": r'cookies\.set|setCookie|cookie.*=',
                "description": "Cookie being set - may require consent",
                "risk_score": 0.45,
                "category": "TRACKING"
            },
            "SESSION_MANAGEMENT": {
                "pattern": r'session|jwt|token.*sign|expiresIn',
                "description": "Session/token management - consider data retention implications",
                "risk_score": 0.4,
                "category": "RETENTION"
            },
            "DATABASE_STORAGE": {
                "pattern": r'\.save\(\)|\.create\(|insert.*into|mongoose.*model',
                "description": "Data persistence - retention policy should be documented",
                "risk_score": 0.35,
                "category": "RETENTION"
            },
            
            # LOW: Documentation and transparency
            "MISSING_DOCSTRING": {
                "pattern": r'^def\s+\w+\s*\([^)]*\)\s*->\s*\w+\s*:\s*\n\s+[^"\']',
                "description": "Function lacks documentation/docstring",
                "risk_score": 0.15,
                "category": "DOCUMENTATION"
            },
            "ENV_FALLBACK": {
                "pattern": r'os\.environ\.get\([^)]+\)\s*or\s*["\']',
                "description": "Environment variable with hardcoded fallback",
                "risk_score": 0.25,
                "category": "SECURITY"
            },
            "VERBOSE_LOGGING": {
                "pattern": r'console\.log|print\s*\(|logger\.debug',
                "description": "Verbose logging may expose sensitive information",
                "risk_score": 0.2,
                "category": "PRIVACY"
            },
            "EXTERNAL_REQUEST": {
                "pattern": r'requests\.(get|post)|axios|fetch\(|http\.(request|get)',
                "description": "External API call - data leaves the system",
                "risk_score": 0.3,
                "category": "SHARING"
            },
            "PASSWORD_HASHING": {
                "pattern": r'bcrypt|hash.*password|hashpw',
                "description": "Password hashing detected - verify strong algorithm used",
                "risk_score": 0.2,
                "category": "SECURITY"
            },
            "ERROR_EXPOSURE": {
                "pattern": r'return.*error\.message|return.*error\[|catch.*error.*=>.*res\.json',
                "description": "Error details may be exposed to client",
                "risk_score": 0.4,
                "category": "SECURITY"
            },
            "TRACKING_PATTERNS": {
                "pattern": r'analytics|track|monitor|event.*log|user.*behavior',
                "description": "Potential user tracking or analytics",
                "risk_score": 0.35,
                "category": "TRACKING"
            },
            "AI_ML_PROCESSING": {
                "pattern": r'ChatOpenAI|gpt-|llm|model.*predict|embedding',
                "description": "AI/ML processing - consider data usage transparency",
                "risk_score": 0.45,
                "category": "TRANSPARENCY"
            },
            "FILE_OPERATIONS": {
                "pattern": r'open\(|aiofiles|tempfile|upload.*dir',
                "description": "File operations - ensure secure handling and cleanup",
                "risk_score": 0.3,
                "category": "SECURITY"
            },
            "CROSS_ORIGIN": {
                "pattern": r'CORS|cross.?origin|Access-Control',
                "description": "Cross-origin configuration - verify security settings",
                "risk_score": 0.35,
                "category": "SECURITY"
            }
        }
        
        # Semantic analysis keywords for contextual detection
        self.semantic_indicators = {
            "data_collection": ["collect", "gather", "store", "save", "persist"],
            "user_tracking": ["track", "monitor", "analytics", "behavior", "session"],
            "third_party": ["api", "external", "service", "integration", "webhook"],
            "sensitive_data": ["password", "email", "name", "phone", "address", "ssn"],
            "consent": ["consent", "agree", "opt", "permission", "authorize"],
            "retention": ["retain", "keep", "store", "duration", "expire", "ttl"],
            "security": ["encrypt", "hash", "secure", "protect", "sanitize"]
        }
    
    def _score_to_level(self, score: float) -> RiskLevel:
        """Convert risk score to risk level."""
        if score >= self.risk_thresholds["CRITICAL"]:
            return RiskLevel.CRITICAL
        elif score >= self.risk_thresholds["HIGH"]:
            return RiskLevel.HIGH
        elif score >= self.risk_thresholds["MEDIUM"]:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _analyze_code_semantics(self, code: str, filename: str) -> List[EthicalIssue]:
        """Perform semantic analysis to detect contextual issues."""
        issues = []
        lines = code.split('\n')
        
        # Check for missing consent in data collection
        has_data_collection = any(kw in code.lower() for kw in self.semantic_indicators["data_collection"])
        has_consent = any(kw in code.lower() for kw in self.semantic_indicators["consent"])
        has_user_creation = "user" in code.lower() and ("create" in code.lower() or "signup" in code.lower() or "register" in code.lower())
        
        if has_user_creation and not has_consent:
            # Find the line with user creation
            for line_num, line in enumerate(lines, 1):
                if re.search(r'User\.create|create\s*\(|insert|\.save\(', line, re.IGNORECASE):
                    issues.append(EthicalIssue(
                        issue_type="CONSENT",
                        risk_level=RiskLevel.MEDIUM,
                        risk_score=0.5,
                        line_number=line_num,
                        code_snippet=line.strip(),
                        description="User data collection without explicit consent mechanism",
                        evidence=["No consent validation found", "User data persisted without consent flow"],
                        recommendation="Implement explicit consent collection before storing user data"
                    ))
                    break
        
        # Check for missing data retention documentation
        has_storage = any(kw in code.lower() for kw in ["save", "create", "insert", "store"])
        has_retention = any(kw in code.lower() for kw in self.semantic_indicators["retention"])
        
        if has_storage and not has_retention:
            for line_num, line in enumerate(lines, 1):
                if re.search(r'\.save\(|\.create\(|insert\s+into', line, re.IGNORECASE):
                    issues.append(EthicalIssue(
                        issue_type="RETENTION",
                        risk_level=RiskLevel.LOW,
                        risk_score=0.25,
                        line_number=line_num,
                        code_snippet=line.strip(),
                        description="Missing data retention policy documentation",
                        evidence=["Data stored without documented retention period"],
                        recommendation="Document data retention policies and implement automatic cleanup"
                    ))
                    break
        
        # Check for indirect profiling through behavior analysis
        has_behavior = any(kw in code.lower() for kw in ["behavior", "pattern", "preference", "usage"])
        if has_behavior:
            for line_num, line in enumerate(lines, 1):
                if re.search(r'behavior|pattern|preference', line, re.IGNORECASE):
                    issues.append(EthicalIssue(
                        issue_type="PRIVACY",
                        risk_level=RiskLevel.LOW,
                        risk_score=0.2,
                        line_number=line_num,
                        code_snippet=line.strip(),
                        description="Potential indirect user profiling through behavior analysis",
                        evidence=["Behavioral pattern analysis detected"],
                        recommendation="Disclose profiling practices and provide opt-out mechanism"
                    ))
                    break
        
        return issues
    
    def scan_code(self, code: str, filename: str) -> Dict:
        """
        Main entry point for Phase 1: Detection
        Scans code for all ethical issue types using pattern matching and semantic analysis.
        """
        logger.info(f"Starting robust detection scan for {filename}")
        
        all_issues = []
        lines = code.split('\n')
        
        # Pattern-based detection
        for pattern_name, pattern_config in self.patterns.items():
            try:
                for line_num, line in enumerate(lines, 1):
                    if re.search(pattern_config["pattern"], line, re.IGNORECASE):
                        # Check for duplicates
                        snippet = line.strip()
                        is_duplicate = any(i.code_snippet == snippet and i.issue_type == pattern_config["category"] 
                                           for i in all_issues)
                        if is_duplicate:
                            continue
                        
                        issue = EthicalIssue(
                            issue_type=pattern_config["category"],
                            risk_level=self._score_to_level(pattern_config["risk_score"]),
                            risk_score=pattern_config["risk_score"],
                            line_number=line_num,
                            code_snippet=snippet,
                            description=pattern_config["description"],
                            evidence=[f"Pattern match: {pattern_name}"],
                            recommendation=self._get_recommendation(pattern_name)
                        )
                        all_issues.append(issue)
            except re.error as e:
                logger.warning(f"Regex error in pattern {pattern_name}: {e}")
        
        # Semantic analysis
        semantic_issues = self._analyze_code_semantics(code, filename)
        
        # Add semantic issues that aren't duplicates
        for si in semantic_issues:
            is_dup = any(i.code_snippet == si.code_snippet and i.issue_type == si.issue_type 
                        for i in all_issues)
            if not is_dup:
                all_issues.append(si)
        
        # Sort by risk score (highest first)
        all_issues.sort(key=lambda x: x.risk_score, reverse=True)
        
        # Calculate summary statistics
        risk_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
        for issue in all_issues:
            risk_counts[issue.risk_level.value] += 1
        
        result = {
            "filename": filename,
            "total_issues": len(all_issues),
            "risk_distribution": risk_counts,
            "issues": [issue.to_dict() for issue in all_issues],
            "requires_debate": any(issue.risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL] for issue in all_issues)
        }
        
        logger.info(f"Robust detection complete: Found {len(all_issues)} issues")
        logger.info(f"Risk distribution: {risk_counts}")
        return result
    
    def _get_recommendation(self, pattern_name: str) -> str:
        """Get recommendation for a specific pattern."""
        recommendations = {
            "HARDCODED_SECRET": "Move secrets to environment variables or secure vault",
            "CORS_WILDCARD": "Restrict CORS origins to specific trusted domains",
            "INSECURE_CORS": "Disable credentials when using wildcard origins or specify exact origins",
            "CONSOLE_LOG_CREDENTIALS": "Remove logging of sensitive data immediately",
            "PRINT_CREDENTIALS": "Remove console output of sensitive information",
            "NO_INPUT_VALIDATION": "Implement input validation using schemas or validation libraries",
            "UNVALIDATED_FILE_UPLOAD": "Add file type, size, and content validation",
            "USER_DATA_COLLECTION": "Implement explicit consent collection flow",
            "THIRD_PARTY_API": "Document third-party data sharing and implement data processing agreements",
            "COOKIE_SETTING": "Implement cookie consent banner and respect user preferences",
            "SESSION_MANAGEMENT": "Document session duration and implement secure session handling",
            "DATABASE_STORAGE": "Document data retention policies and implement automatic cleanup",
            "MISSING_DOCSTRING": "Add docstrings to all functions for maintainability",
            "ENV_FALLBACK": "Remove hardcoded fallbacks for security-sensitive configuration",
            "VERBOSE_LOGGING": "Review logging to ensure no sensitive data is logged",
            "EXTERNAL_REQUEST": "Document external data sharing and implement proper error handling",
            "PASSWORD_HASHING": "Ensure bcrypt with sufficient rounds (10+) is used",
            "ERROR_EXPOSURE": "Return generic error messages to clients, log details server-side",
            "TRACKING_PATTERNS": "Document tracking practices and provide opt-out mechanism",
            "AI_ML_PROCESSING": "Disclose AI processing to users and document data usage",
            "FILE_OPERATIONS": "Implement secure file handling with validation and cleanup",
            "CROSS_ORIGIN": "Review and restrict CORS settings to necessary origins only"
        }
        return recommendations.get(pattern_name, "Review code for ethical implications")
