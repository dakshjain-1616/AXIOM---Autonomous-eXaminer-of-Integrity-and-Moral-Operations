"""
AXIOM Legalize Module
Phase 5: Generate mock legal documentation including GDPR compliance notes,
CCPA disclosures, Terms of Service clauses, and timestamped audit trail.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

from axiom_config import GDPR_ARTICLES, CCPA_SECTIONS


@dataclass
class LegalDocument:
    """Represents a generated legal document."""
    document_type: str
    title: str
    content: str
    timestamp: str
    related_issues: List[str]
    compliance_framework: str
    file_path: Optional[str] = None


@dataclass
class AuditTrailEntry:
    """Single entry in the audit trail."""
    timestamp: str
    phase: str
    action: str
    details: Dict
    risk_level: Optional[str] = None


class LegalDocumentGenerator:
    """
    Generates mock legal documentation for ethical compliance.
    Includes GDPR, CCPA, and Terms of Service documentation.
    """
    
    def __init__(self, output_dir: str = "./legal_docs"):
        """
        Initialize legal document generator.
        
        Args:
            output_dir: Directory to save legal documents
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.audit_trail: List[AuditTrailEntry] = []
    
    def generate_gdpr_compliance_doc(self, issues: List[Dict]) -> LegalDocument:
        """
        Generate GDPR compliance documentation.
        
        Args:
            issues: List of detected ethical issues
            
        Returns:
            LegalDocument with GDPR compliance notes
        """
        timestamp = datetime.now().isoformat()
        
        content = []
        content.append("# GDPR Compliance Assessment")
        content.append(f"**Generated**: {timestamp}")
        content.append("")
        content.append("## Executive Summary")
        content.append("This document assesses compliance with the General Data Protection Regulation (GDPR) "
                      "based on detected ethical issues in the codebase.")
        content.append("")
        
        # Article 5: Principles
        content.append(f"### {GDPR_ARTICLES['Article_5']}")
        content.append("**Assessment**: Data processing must be lawful, fair, and transparent.")
        content.append("")
        
        article5_issues = [i for i in issues if i.get("category", "").upper() in
                          ["TRACKING", "SURVEILLANCE", "DARK_PATTERNS"]]
        if article5_issues:
            content.append("**Potential Violations**:")
            for issue in article5_issues:
                content.append(f"- {issue.get('description', 'Unknown issue')}")
        else:
            content.append("**Status**: ✅ No apparent violations detected")
        content.append("")
        
        # Article 6: Lawfulness
        content.append(f"### {GDPR_ARTICLES['Article_6']}")
        content.append("**Assessment**: Processing must have a legal basis (consent, contract, legal obligation, etc.)")
        content.append("")
        
        article6_issues = [i for i in issues if i.get("category", "").upper() == "TRACKING"]
        if article6_issues:
            content.append("**Potential Violations**:")
            for issue in article6_issues:
                content.append(f"- {issue.get('description', 'Unknown issue')}: May lack legal basis")
        else:
            content.append("**Status**: ✅ No apparent violations detected")
        content.append("")
        
        # Article 7: Consent
        content.append(f"### {GDPR_ARTICLES['Article_7']}")
        content.append("**Assessment**: Consent must be freely given, specific, informed, and unambiguous.")
        content.append("")
        
        article7_issues = [i for i in issues if i.get("category", "").upper() == "DARK_PATTERNS"]
        if article7_issues:
            content.append("**Potential Violations**:")
            for issue in article7_issues:
                content.append(f"- {issue.get('description', 'Unknown issue')}: May invalidate consent")
        else:
            content.append("**Status**: ✅ No apparent violations detected")
        content.append("")
        
        # Article 17: Right to Erasure
        content.append(f"### {GDPR_ARTICLES['Article_17']}")
        content.append("**Assessment**: Data subjects have the right to have their data erased.")
        content.append("")
        
        article17_issues = [i for i in issues if i.get("category", "").upper() in ["TRACKING", "SURVEILLANCE"]]
        if article17_issues:
            content.append("**Considerations**:")
            content.append("- Ensure data deletion mechanisms are implemented")
            content.append("- Verify data is not retained longer than necessary")
        else:
            content.append("**Status**: ✅ No specific concerns")
        content.append("")
        
        # Article 22: Automated Decision-Making
        content.append(f"### {GDPR_ARTICLES['Article_22']}")
        content.append("**Assessment**: Data subjects have rights regarding automated decision-making.")
        content.append("")
        
        article22_issues = [i for i in issues if i.get("category", "").upper() == "BIAS"]
        if article22_issues:
            content.append("**Potential Violations**:")
            for issue in article22_issues:
                content.append(f"- {issue.get('description', 'Unknown issue')}: May violate Article 22")
            content.append("- Ensure human oversight for consequential decisions")
            content.append("- Provide right to contest automated decisions")
        else:
            content.append("**Status**: ✅ No apparent violations detected")
        content.append("")
        
        # Compliance Summary
        content.append("## Compliance Summary")
        high_risk_issues = [i for i in issues if i.get("risk_level") in ["HIGH", "CRITICAL"]]
        if high_risk_issues:
            content.append(f"**Status**: ⚠️ {len(high_risk_issues)} high-risk issues require attention")
        else:
            content.append("**Status**: ✅ No high-risk compliance issues detected")
        content.append("")
        content.append("## Recommendations")
        content.append("1. Conduct regular privacy impact assessments")
        content.append("2. Implement privacy-by-design principles")
        content.append("3. Ensure transparent data processing practices")
        content.append("4. Provide clear mechanisms for data subject rights")
        
        content_str = "\n".join(content)
        
        return LegalDocument(
            document_type="GDPR_Compliance",
            title="GDPR Compliance Assessment",
            content=content_str,
            timestamp=timestamp,
            related_issues=[i.get("id") for i in issues],
            compliance_framework="GDPR"
        )
    
    def generate_ccpa_disclosure(self, issues: List[Dict]) -> LegalDocument:
        """
        Generate CCPA disclosure documentation.
        
        Args:
            issues: List of detected ethical issues
            
        Returns:
            LegalDocument with CCPA disclosures
        """
        timestamp = datetime.now().isoformat()
        
        content = []
        content.append("# CCPA Privacy Disclosure")
        content.append(f"**Generated**: {timestamp}")
        content.append("")
        content.append("## Your Privacy Rights Under CCPA")
        content.append("")
        
        # Section 1798.100
        content.append(f"### {CCPA_SECTIONS['Section_1798.100']}")
        content.append("We collect the following categories of personal information:")
        content.append("")
        
        tracking_issues = [i for i in issues if i.get("category", "").upper() == "TRACKING"]
        if tracking_issues:
            content.append("**Data Collection Practices**:")
            for issue in tracking_issues:
                content.append(f"- {issue.get('description', 'Unknown tracking')}")
        else:
            content.append("- No specific tracking mechanisms identified")
        content.append("")
        
        # Section 1798.105
        content.append(f"### {CCPA_SECTIONS['Section_1798.105']}")
        content.append("You have the right to request deletion of your personal information.")
        content.append("")
        content.append("**Deletion Process**:")
        content.append("1. Submit a deletion request through our privacy portal")
        content.append("2. We will verify your identity")
        content.append("3. Information will be deleted within 45 days")
        content.append("")
        
        # Section 1798.110
        content.append(f"### {CCPA_SECTIONS['Section_1798.110']}")
        content.append("You have the right to know if your information is sold or disclosed.")
        content.append("")
        
        sharing_issues = [i for i in issues if "share" in i.get("description", "").lower()]
        if sharing_issues:
            content.append("**Third-Party Sharing**:")
            for issue in sharing_issues:
                content.append(f"- {issue.get('description', 'Unknown sharing')}")
        else:
            content.append("- No third-party sharing identified")
        content.append("")
        
        # Section 1798.115
        content.append(f"### {CCPA_SECTIONS['Section_1798.115']}")
        content.append("You have the right to opt-out of the sale of your personal information.")
        content.append("")
        content.append("**Opt-Out Process**:")
        content.append("1. Click 'Do Not Sell My Personal Information' link")
        content.append("2. Complete the opt-out form")
        content.append("3. Your preference will be honored within 15 days")
        content.append("")
        
        # Section 1798.125
        content.append(f"### {CCPA_SECTIONS['Section_1798.125']}")
        content.append("We will not discriminate against you for exercising your CCPA rights.")
        content.append("")
        content.append("**Non-Discrimination Policy**:")
        content.append("- No denial of goods or services")
        content.append("- No different pricing or quality")
        content.append("- No suggestion of different rates or quality")
        content.append("")
        
        # Contact Information
        content.append("## Contact Information")
        content.append("For privacy-related inquiries:")
        content.append("- Email: privacy@example.com")
        content.append("- Phone: 1-800-PRIVACY")
        content.append("- Address: 123 Privacy Lane, Compliance City, CA 90210")
        content.append("")
        
        # Last Updated
        content.append(f"**Last Updated**: {timestamp}")
        
        content_str = "\n".join(content)
        
        return LegalDocument(
            document_type="CCPA_Disclosure",
            title="CCPA Privacy Disclosure",
            content=content_str,
            timestamp=timestamp,
            related_issues=[i.get("id") for i in issues],
            compliance_framework="CCPA"
        )
    
    def generate_terms_of_service(self, issues: List[Dict]) -> LegalDocument:
        """
        Generate Terms of Service clauses.
        
        Args:
            issues: List of detected ethical issues
            
        Returns:
            LegalDocument with ToS clauses
        """
        timestamp = datetime.now().isoformat()
        
        content = []
        content.append("# Terms of Service")
        content.append(f"**Last Updated**: {timestamp}")
        content.append("")
        content.append("## 1. Acceptance of Terms")
        content.append("By accessing or using our services, you agree to be bound by these Terms of Service.")
        content.append("")
        
        content.append("## 2. Data Collection and Use")
        content.append("### 2.1 Information We Collect")
        
        tracking_issues = [i for i in issues if i.get("category", "").upper() == "TRACKING"]
        if tracking_issues:
            content.append("We collect the following information:")
            for issue in tracking_issues:
                content.append(f"- {issue.get('description', 'Data collection')}")
        else:
            content.append("We collect information necessary to provide our services.")
        
        content.append("")
        content.append("### 2.2 How We Use Your Information")
        content.append("- To provide and maintain our services")
        content.append("- To improve user experience")
        content.append("- To comply with legal obligations")
        content.append("")
        
        content.append("### 2.3 Data Sharing")
        sharing_issues = [i for i in issues if "share" in i.get("description", "").lower()]
        if sharing_issues:
            content.append("We may share your information with:")
            for issue in sharing_issues:
                content.append(f"- {issue.get('description', 'Third parties')}")
        else:
            content.append("We do not sell your personal information to third parties.")
        content.append("")
        
        content.append("## 3. User Rights")
        content.append("### 3.1 Your Privacy Rights")
        content.append("You have the right to:")
        content.append("- Access your personal information")
        content.append("- Request correction of inaccurate data")
        content.append("- Request deletion of your data")
        content.append("- Object to certain processing activities")
        content.append("- Withdraw consent at any time")
        content.append("")
        
        content.append("### 3.2 Exercising Your Rights")
        content.append("To exercise your rights, contact us at privacy@example.com.")
        content.append("")
        
        content.append("## 4. Automated Decision-Making")
        bias_issues = [i for i in issues if i.get("category", "").upper() == "BIAS"]
        if bias_issues:
            content.append("### 4.1 Profiling and Automated Decisions")
            content.append("We use automated systems that may affect your rights:")
            for issue in bias_issues:
                content.append(f"- {issue.get('description', 'Automated processing')}")
            content.append("")
            content.append("### 4.2 Your Rights Regarding Automated Decisions")
            content.append("You have the right to:")
            content.append("- Obtain human intervention")
            content.append("- Express your point of view")
            content.append("- Contest the decision")
        else:
            content.append("We do not engage in automated decision-making that produces legal or similarly significant effects.")
        content.append("")
        
        content.append("## 5. Limitation of Liability")
        content.append("To the extent permitted by law, we shall not be liable for any indirect, incidental, "
                      "special, consequential, or punitive damages arising from your use of our services.")
        content.append("")
        
        content.append("## 6. Changes to Terms")
        content.append("We may update these Terms of Service from time to time. We will notify you of any "
                      "material changes by posting the new terms on this page.")
        content.append("")
        
        content.append("## 7. Contact Information")
        content.append("For questions about these Terms of Service, contact us at:")
        content.append("- Email: legal@example.com")
        content.append("- Address: 123 Legal Street, Compliance City, CA 90210")
        content.append("")
        
        content.append(f"**Last Updated**: {timestamp}")
        
        content_str = "\n".join(content)
        
        return LegalDocument(
            document_type="Terms_of_Service",
            title="Terms of Service",
            content=content_str,
            timestamp=timestamp,
            related_issues=[i.get("id") for i in issues],
            compliance_framework="General"
        )
    
    def add_audit_entry(self, phase: str, action: str, details: Dict, 
                        risk_level: Optional[str] = None):
        """
        Add entry to audit trail.
        
        Args:
            phase: Pipeline phase
            action: Action performed
            details: Additional details
            risk_level: Risk level if applicable
        """
        entry = AuditTrailEntry(
            timestamp=datetime.now().isoformat(),
            phase=phase,
            action=action,
            details=details,
            risk_level=risk_level
        )
        self.audit_trail.append(entry)
    
    def generate_audit_trail(self) -> LegalDocument:
        """
        Generate timestamped audit trail document.
        
        Returns:
            LegalDocument with complete audit trail
        """
        timestamp = datetime.now().isoformat()
        
        content = []
        content.append("# AXIOM Ethics Audit Trail")
        content.append(f"**Generated**: {timestamp}")
        content.append("")
        content.append("## Audit Log")
        content.append("")
        
        for i, entry in enumerate(self.audit_trail, 1):
            content.append(f"### Entry {i}")
            content.append(f"- **Timestamp**: {entry.timestamp}")
            content.append(f"- **Phase**: {entry.phase}")
            content.append(f"- **Action**: {entry.action}")
            if entry.risk_level:
                content.append(f"- **Risk Level**: {entry.risk_level}")
            content.append("- **Details**:")
            for key, value in entry.details.items():
                content.append(f"  - {key}: {value}")
            content.append("")
        
        content.append("## Audit Summary")
        content.append(f"- **Total Entries**: {len(self.audit_trail)}")
        
        phase_counts = {}
        risk_counts = {}
        for entry in self.audit_trail:
            phase_counts[entry.phase] = phase_counts.get(entry.phase, 0) + 1
            if entry.risk_level:
                risk_counts[entry.risk_level] = risk_counts.get(entry.risk_level, 0) + 1
        
        content.append("- **Phase Distribution**:")
        for phase, count in phase_counts.items():
            content.append(f"  - {phase}: {count} entries")
        
        if risk_counts:
            content.append("- **Risk Distribution**:")
            for risk, count in risk_counts.items():
                content.append(f"  - {risk}: {count} entries")
        
        content.append("")
        content.append(f"**Audit Completed**: {timestamp}")
        content.append("**Auditor**: AXIOM Autonomous Ethics Agent")
        content.append("**Framework Version**: 1.0.0")
        
        content_str = "\n".join(content)
        
        return LegalDocument(
            document_type="Audit_Trail",
            title="AXIOM Ethics Audit Trail",
            content=content_str,
            timestamp=timestamp,
            related_issues=[],
            compliance_framework="AXIOM"
        )
    
    def save_document(self, document: LegalDocument, filename: Optional[str] = None) -> str:
        """
        Save legal document to file.
        
        Args:
            document: Document to save
            filename: Optional filename override
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{document.document_type}_{timestamp}.md"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(document.content)
        
        document.file_path = filepath
        
        return filepath
    
    def save_audit_trail_json(self, filepath: Optional[str] = None) -> str:
        """
        Save audit trail as JSON for programmatic access.
        
        Args:
            filepath: Optional filepath override
            
        Returns:
            Path to saved file
        """
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(self.output_dir, f"audit_trail_{timestamp}.json")
        
        audit_data = {
            "generated_at": datetime.now().isoformat(),
            "total_entries": len(self.audit_trail),
            "entries": [
                {
                    "timestamp": entry.timestamp,
                    "phase": entry.phase,
                    "action": entry.action,
                    "details": entry.details,
                    "risk_level": entry.risk_level
                }
                for entry in self.audit_trail
            ]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(audit_data, f, indent=2)
        
        return filepath
