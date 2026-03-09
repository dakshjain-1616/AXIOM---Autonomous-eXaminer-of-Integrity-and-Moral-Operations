"""
AXIOM Pipeline Orchestrator
Main orchestration module for the 5-phase autonomous ethics auditing pipeline.
"""

import os
import re
import json
import subprocess
import tempfile
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from axiom_config import AXIOMConfig, GDPR_ARTICLES, CCPA_SECTIONS
from axiom_detection import AXIOMDetector, EthicalIssue
from axiom_debate import AXIOMDebateEngine, DebateArgument, DebateRound
from axiom_resolve import AXIOMResolver, CodeAlternative
from axiom_impact import ImpactAnalyzer, CarbonEstimate, ComplexityLevel
from axiom_legalize import LegalDocumentGenerator, LegalDocument, AuditTrailEntry


class AXIOMPipeline:
    """
    Main orchestrator for the AXIOM 5-phase ethics auditing pipeline.
    
    Phases:
    1. Detect: Scan code for ethical risks
    2. Debate: Adversarial reasoning for MEDIUM+ risks
    3. Resolve: Generate privacy-compliant alternatives
    4. Impact: Estimate carbon footprint delta
    5. Legalize: Generate legal documentation
    """
    
    def __init__(self, config: Optional[AXIOMConfig] = None):
        """
        Initialize AXIOM pipeline.
        
        Args:
            config: Configuration object (uses defaults if None)
        """
        self.config = config or AXIOMConfig()
        self.timestamp = datetime.now().isoformat()
        
        # Initialize phase modules
        self.detector = AXIOMDetector(self.config)
        self.debater = AXIOMDebateEngine(self.config)
        self.resolver = AXIOMResolver(self.config)
        self.impact_analyzer = ImpactAnalyzer(self.config.carbon_baseline)
        self.legal_generator = LegalDocumentGenerator(self.config.legal_docs_dir)
        
        # Results storage
        self.detection_results: Optional[Dict] = None
        self.debate_results: List[Dict] = []
        self.resolution_results: List[Dict] = []
        self.impact_results: List[CarbonEstimate] = []
        self.legal_documents: List[LegalDocument] = []
        
        # Create output directories
        os.makedirs(self.config.output_dir, exist_ok=True)
        os.makedirs(self.config.legal_docs_dir, exist_ok=True)
        os.makedirs(self.config.alternatives_dir, exist_ok=True)
    
    def _clone_repository(self, repo_url: str, github_token: Optional[str] = None) -> str:
        """
        Clone a GitHub repository to a temporary directory.
        
        Args:
            repo_url: GitHub repository URL
            github_token: Optional token for private repositories
            
        Returns:
            Path to cloned repository
        """
        # Create temp directory for repos
        temp_dir = os.path.join(self.config.temp_repo_dir, 
                                f"repo_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(temp_dir, exist_ok=True)
        
        # Modify URL for private repos if token provided
        if github_token and "github.com" in repo_url:
            # Convert https://github.com/user/repo to https://token@github.com/user/repo
            if repo_url.startswith("https://"):
                repo_url = repo_url.replace("https://", f"https://{github_token}@")
        
        print(f"  → Cloning repository: {repo_url}")
        
        try:
            # Clone with depth 1 for efficiency
            result = subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, temp_dir],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"  ✓ Repository cloned successfully to: {temp_dir}")
            return temp_dir
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Failed to clone repository: {e.stderr}")
            raise RuntimeError(f"Failed to clone repository: {e.stderr}")
    
    def _get_code_files(self, repo_path: str) -> List[Tuple[str, str]]:
        """
        Recursively get all supported code files from repository.
        
        Args:
            repo_path: Path to cloned repository
            
        Returns:
            List of (filepath, content) tuples
        """
        supported_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs'}
        code_files = []
        
        for root, dirs, files in os.walk(repo_path):
            # Skip hidden directories and common non-source directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in 
                      {'node_modules', '__pycache__', 'venv', '.git', 'dist', 'build'}]
            
            for file in files:
                if any(file.endswith(ext) for ext in supported_extensions):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if content.strip():  # Skip empty files
                                # Get relative path from repo root
                                rel_path = os.path.relpath(filepath, repo_path)
                                code_files.append((rel_path, content))
                    except Exception as e:
                        print(f"    Warning: Could not read {filepath}: {e}")
        
        return code_files
    
    def run_on_repo(self, repo_url: str, github_token: Optional[str] = None) -> Dict:
        """
        Execute the complete 5-phase pipeline on a GitHub repository.
        
        Args:
            repo_url: GitHub repository URL
            github_token: Optional token for private repositories
            
        Returns:
            Dictionary with all results and file paths
        """
        print(f"\n{'='*60}")
        print(f"AXIOM Ethics Audit Pipeline - Repository Mode")
        print(f"Repository: {repo_url}")
        print(f"Started: {self.timestamp}")
        print(f"{'='*60}\n")
        
        # Clone repository
        repo_path = self._clone_repository(repo_url, github_token)
        
        try:
            # Get all code files
            print("\n[PHASE 0] SCAN: Discovering code files...")
            code_files = self._get_code_files(repo_path)
            print(f"  ✓ Found {len(code_files)} code files to audit")
            
            # Aggregate results from all files
            all_issues = []
            all_debates = []
            all_resolutions = []
            all_impacts = []
            annotated_files = []
            
            # Process each file
            for idx, (rel_path, code) in enumerate(code_files, 1):
                print(f"\n[FILE {idx}/{len(code_files)}] Auditing: {rel_path}")
                
                # Phase 1: Detect
                detection_result = self.detector.scan_code(code, rel_path)
                file_issues = detection_result.get('issues', [])
                
                if file_issues:
                    print(f"  ✓ Detected {len(file_issues)} issues")
                    for issue in file_issues:
                        issue['file_path'] = rel_path  # Add file context
                    all_issues.extend(file_issues)
                    
                    # Phase 2: Debate (for MEDIUM+ risks)
                    medium_plus = [i for i in file_issues 
                                   if i.get('risk_level') in ["MEDIUM", "HIGH", "CRITICAL"]]
                    for issue in medium_plus:
                        debate = self.debater.debate_issue(
                            issue.get('description', 'Unknown'),
                            issue.get('risk_level', 'MEDIUM'),
                            issue.get('category', 'Unknown')
                        )
                        if debate:
                            all_debates.append(debate)
                            issue['debate_synthesis'] = debate.synthesis
                    
                    # Phase 3: Resolve
                    if file_issues:
                        resolution = self.resolver.resolve({'issues': file_issues})
                        resolutions = resolution.get('alternatives', [])
                        for r in resolutions:
                            r['file_path'] = rel_path
                        all_resolutions.extend(resolutions)
                        
                        # Add inline annotations
                        annotated_code = self._add_inline_annotations(code, file_issues)
                        annotated_path = os.path.join(
                            self.config.output_dir, 
                            "annotated", 
                            rel_path
                        )
                        os.makedirs(os.path.dirname(annotated_path), exist_ok=True)
                        with open(annotated_path, 'w', encoding='utf-8') as f:
                            f.write(annotated_code)
                        annotated_files.append(annotated_path)
                        print(f"  ✓ Annotations saved: {annotated_path}")
                        
                        # Phase 4: Impact
                        for r in resolutions:
                            orig = r.get('original_snippet', '')
                            alt = r.get('alternative_snippet', '')
                            if orig and alt:
                                impact = self.impact_analyzer.analyze_code(orig, alt)
                                all_impacts.append(impact)
            
            # Calculate overall risk
            risk_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
            for issue in all_issues:
                risk_counts[issue.get('risk_level', 'LOW')] += 1
            
            overall_risk = "LOW"
            if risk_counts["CRITICAL"] > 0:
                overall_risk = "CRITICAL"
            elif risk_counts["HIGH"] > 0:
                overall_risk = "HIGH"
            elif risk_counts["MEDIUM"] > 0:
                overall_risk = "MEDIUM"
            
            # Phase 5: Legalize (generate consolidated docs)
            print("\n[PHASE 5] LEGALIZE: Generating legal documentation...")
            
            gdpr_doc = self.legal_generator.generate_gdpr_compliance_doc(all_issues)
            self.legal_documents.append(gdpr_doc)
            gdpr_path = self.legal_generator.save_document(gdpr_doc, "GDPR_Compliance.md")
            print(f"  ✓ GDPR compliance document: {gdpr_path}")
            
            ccpa_doc = self.legal_generator.generate_ccpa_disclosure(all_issues)
            self.legal_documents.append(ccpa_doc)
            ccpa_path = self.legal_generator.save_document(ccpa_doc, "CCPA_Disclosure.md")
            print(f"  ✓ CCPA disclosure document: {ccpa_path}")
            
            tos_doc = self.legal_generator.generate_terms_of_service(all_issues)
            self.legal_documents.append(tos_doc)
            tos_path = self.legal_generator.save_document(tos_doc, "Terms_of_Service.md")
            print(f"  ✓ Terms of Service document: {tos_path}")
            
            audit_doc = self.legal_generator.generate_audit_trail()
            self.legal_documents.append(audit_doc)
            audit_path = self.legal_generator.save_document(audit_doc, "Audit_Trail.md")
            audit_json_path = self.legal_generator.save_audit_trail_json()
            print(f"  ✓ Audit trail document: {audit_path}")
            print(f"  ✓ Audit trail JSON: {audit_json_path}")
            
            print(f"\n{'='*60}")
            print(f"AXIOM Repository Audit Complete")
            print(f"{'='*60}\n")
            
            # Return comprehensive results
            return {
                "repository_url": repo_url,
                "repository_path": repo_path,
                "timestamp": self.timestamp,
                "files_audited": len(code_files),
                "detection": {
                    "issues_count": len(all_issues),
                    "overall_risk": overall_risk,
                    "risk_distribution": risk_counts,
                    "issues": all_issues
                },
                "debate": {
                    "debates_count": len(all_debates),
                    "debates": [
                        {
                            "issue": d.issue,
                            "devil_argument": d.devil_argument.argument[:200] if hasattr(d, 'devil_argument') else "",
                            "angel_argument": d.angel_argument.argument[:200] if hasattr(d, 'angel_argument') else "",
                            "synthesis": d.synthesis[:200] if hasattr(d, 'synthesis') else ""
                        }
                        for d in all_debates
                    ]
                },
                "resolution": {
                    "alternatives_count": len(all_resolutions),
                    "alternatives": all_resolutions,
                    "annotated_files": annotated_files
                },
                "impact": {
                    "analyses_count": len(all_impacts),
                    "total_delta_co2e": sum(i.delta_co2e for i in all_impacts) if all_impacts else 0,
                    "analyses": [{
                        "original_co2e": i.original_co2e,
                        "alternative_co2e": i.alternative_co2e,
                        "delta_co2e": i.delta_co2e,
                        "percentage_change": i.percentage_change
                    } for i in all_impacts]
                },
                "legal": {
                    "documents_count": len(self.legal_documents),
                    "documents": [
                        {
                            "type": d.document_type,
                            "title": d.title,
                            "timestamp": d.timestamp,
                            "file_path": d.file_path
                        }
                        for d in self.legal_documents
                    ]
                }
            }
            
        finally:
            # Cleanup: Remove temporary repository
            if os.path.exists(repo_path):
                print(f"\n  → Cleaning up temporary repository...")
                shutil.rmtree(repo_path)
                print(f"  ✓ Cleanup complete")
    
    def run(self, code: str, filename: str = "audited_code.py") -> Dict:
        """
        Execute the complete 5-phase pipeline.
        
        Args:
            code: Source code to audit
            filename: Name of the file being audited
            
        Returns:
            Dictionary with all results and file paths
        """
        print(f"\n{'='*60}")
        print(f"AXIOM Ethics Audit Pipeline")
        print(f"Target: {filename}")
        print(f"Started: {self.timestamp}")
        print(f"{'='*60}\n")
        
        # Phase 1: Detect
        print("\n[PHASE 1/5] DETECT: Scanning for ethical risks...")
        self.detection_results = self.detector.scan_code(code, filename)
        issues = self.detection_results.get('issues', [])
        risk_dist = self.detection_results.get('risk_distribution', {})
        overall_risk = 'LOW'
        if risk_dist.get('CRITICAL', 0) > 0:
            overall_risk = 'CRITICAL'
        elif risk_dist.get('HIGH', 0) > 0:
            overall_risk = 'HIGH'
        elif risk_dist.get('MEDIUM', 0) > 0:
            overall_risk = 'MEDIUM'
        print(f"  ✓ Detected {len(issues)} issues")
        print(f"  ✓ Overall risk level: {overall_risk}")
        
        self.legal_generator.add_audit_entry(
            "DETECT", 
            "Code scan completed",
            {"issues_found": len(issues),
             "risk_level": overall_risk},
            overall_risk
        )
        
        # Phase 2: Debate (for MEDIUM+ risks)
        print("\n[PHASE 2/5] DEBATE: Conducting adversarial reasoning...")
        medium_plus_issues = [
            i for i in issues 
            if i.get('risk_level') in ["MEDIUM", "HIGH", "CRITICAL"]
        ]
        
        if medium_plus_issues:
            print(f"  → Debating {len(medium_plus_issues)} MEDIUM+ risk issues...")
            for issue in medium_plus_issues:
                debate_result = self.debater.debate_issue(
                    issue.get('description', 'Unknown'),
                    issue.get('risk_level', 'MEDIUM'),
                    issue.get('category', 'Unknown')
                )
                self.debate_results.append(debate_result)
                print(f"    ✓ Debate completed for: {issue.get('description', 'Unknown')[:50]}...")
                
                consensus = getattr(debate_result, 'consensus_reached', False)
                self.legal_generator.add_audit_entry(
                    "DEBATE",
                    f"Adversarial debate for issue",
                    {"issue_description": issue.get('description', 'Unknown'),
                     "consensus": consensus},
                    issue.get('risk_level')
                )
        else:
            print("  → No MEDIUM+ risk issues to debate")
        
        # Phase 3: Resolve
        print("\n[PHASE 3/5] RESOLVE: Generating privacy-compliant alternatives...")
        if issues:
            resolution_results = self.resolver.resolve(self.detection_results)
            self.resolution_results = resolution_results.get('alternatives', [])
            print(f"  ✓ Generated {len(self.resolution_results)} alternatives")
            
            # Add inline annotations to code
            annotated_code = self._add_inline_annotations(code, issues)
            annotated_path = os.path.join(self.config.output_dir, f"annotated_{filename}")
            with open(annotated_path, 'w', encoding='utf-8') as f:
                f.write(annotated_code)
            print(f"  ✓ Inline annotations added: {annotated_path}")

            for alt in self.resolution_results:
                # Save alternative code to sidecar file
                alt_filename = f"alt_{alt.get('issue_type', 'issue')}_{datetime.now().strftime('%H%M%S')}.py"
                alt_path = os.path.join(self.config.alternatives_dir, alt_filename)
                with open(alt_path, 'w', encoding='utf-8') as f:
                    f.write(alt.get('alternative_snippet', ''))
                alt['sidecar_file'] = alt_path

                self.legal_generator.add_audit_entry(
                    "RESOLVE",
                    f"Generated alternative for issue",
                    {"original_snippet": alt.get('original_snippet', 'N/A')[:100] if alt.get('original_snippet') else "N/A",
                     "alternative_snippet": alt.get('alternative_snippet', 'N/A')[:100] if alt.get('alternative_snippet') else "N/A",
                     "trade_offs_count": len(alt.get('trade_offs', []))},
                    alt.get('risk_level')
                )
        else:
            print("  → No issues to resolve")
        
        # Phase 4: Impact
        print("\n[PHASE 4/5] IMPACT: Estimating carbon footprint delta...")
        if self.resolution_results:
            for resolution in self.resolution_results:
                orig = resolution.get('original_snippet', '')
                alt = resolution.get('alternative_snippet', '')
                if orig and alt:
                    impact = self.impact_analyzer.analyze_code(orig, alt)
                    self.impact_results.append(impact)
                    print(f"  ✓ Impact analyzed: {impact.delta_co2e:+.4f} kg CO2e")
                    
                    self.legal_generator.add_audit_entry(
                        "IMPACT",
                        "Carbon footprint analysis",
                        {"original_co2e": impact.original_co2e,
                         "alternative_co2e": impact.alternative_co2e,
                         "delta_co2e": impact.delta_co2e,
                         "percentage_change": impact.percentage_change},
                        None
                    )
        else:
            print("  → No alternatives to analyze")
        
        # Phase 5: Legalize
        print("\n[PHASE 5/5] LEGALIZE: Generating legal documentation...")
        
        # Generate GDPR compliance doc
        gdpr_doc = self.legal_generator.generate_gdpr_compliance_doc(issues)
        self.legal_documents.append(gdpr_doc)
        gdpr_path = self.legal_generator.save_document(gdpr_doc)
        print(f"  ✓ GDPR compliance document: {gdpr_path}")
        
        # Generate CCPA disclosure
        ccpa_doc = self.legal_generator.generate_ccpa_disclosure(issues)
        self.legal_documents.append(ccpa_doc)
        ccpa_path = self.legal_generator.save_document(ccpa_doc)
        print(f"  ✓ CCPA disclosure document: {ccpa_path}")
        
        # Generate Terms of Service
        tos_doc = self.legal_generator.generate_terms_of_service(issues)
        self.legal_documents.append(tos_doc)
        tos_path = self.legal_generator.save_document(tos_doc)
        print(f"  ✓ Terms of Service document: {tos_path}")
        
        # Generate audit trail
        audit_doc = self.legal_generator.generate_audit_trail()
        self.legal_documents.append(audit_doc)
        audit_path = self.legal_generator.save_document(audit_doc)
        audit_json_path = self.legal_generator.save_audit_trail_json()
        print(f"  ✓ Audit trail document: {audit_path}")
        print(f"  ✓ Audit trail JSON: {audit_json_path}")
        
        self.legal_generator.add_audit_entry(
            "LEGALIZE",
            "Generated legal documentation",
            {"documents_created": len(self.legal_documents),
             "gdpr_path": gdpr_path,
             "ccpa_path": ccpa_path,
             "tos_path": tos_path,
             "audit_path": audit_path},
            None
        )
        
        print(f"\n{'='*60}")
        print(f"AXIOM Pipeline Complete")
        print(f"{'='*60}\n")
        
        # Return comprehensive results
        results = {
            "filename": filename,
            "timestamp": self.timestamp,
            "detection": {
                "issues_count": len(issues),
                "overall_risk": overall_risk,
                "issues": issues
            },
            "debate": {
                "debates_count": len(self.debate_results),
                "debates": self.debate_results
            },
            "resolution": {
                "alternatives_count": len(self.resolution_results),
                "alternatives": self.resolution_results
            },
            "impact": {
                "analyses_count": len(self.impact_results),
                "total_delta_co2e": sum(i.delta_co2e for i in self.impact_results) if self.impact_results else 0,
                "analyses": [{
                    "original_co2e": i.original_co2e,
                    "alternative_co2e": i.alternative_co2e,
                    "delta_co2e": i.delta_co2e,
                    "percentage_change": i.percentage_change
                } for i in self.impact_results]
            },
            "legal": {
                "documents_count": len(self.legal_documents),
                "documents": [
                    {
                        "type": d.document_type,
                        "title": d.title,
                        "timestamp": d.timestamp,
                        "file_path": d.file_path
                    }
                    for d in self.legal_documents
                ]
            }
        }
        return results

    def _add_inline_annotations(self, code: str, issues: List[Dict]) -> str:
        """Add ethical risk annotations as comments in the code."""
        lines = code.split('\n')
        # Sort issues by line number in reverse to avoid offset issues
        sorted_issues = sorted(issues, key=lambda x: x.get('line_number', 0), reverse=True)
        
        for issue in sorted_issues:
            line_idx = issue.get('line_number', 1) - 1
            if 0 <= line_idx < len(lines):
                # Use // format as specified in acceptance criteria
                annotation = f"  # ⚖️ AXIOM FLAG: {issue.get('risk_level', 'RISK')} — {issue.get('description', 'Ethical concern')}"
                lines[line_idx] += annotation
        
        return '\n'.join(lines)


def save_master_report(results: dict, output_dir: str) -> Tuple[str, str]:
    """Generate and save master ethics report."""
    timestamp = datetime.now().isoformat()
    
    report = []
    report.append("# AXIOM ETHICS REPORT")
    report.append(f"**Generated**: {timestamp}")
    report.append(f"**Target**: {results.get('filename', 'Unknown')}")
    report.append("")
    
    # Executive Summary
    report.append("## Executive Summary")
    detection = results.get('detection', {})
    report.append(f"- **Total Issues Detected**: {detection.get('issues_count', 0)}")
    report.append(f"- **Overall Risk Level**: {detection.get('overall_risk', 'N/A')}")
    report.append(f"- **Debates Conducted**: {results.get('debate', {}).get('debates_count', 0)}")
    report.append(f"- **Alternatives Generated**: {results.get('resolution', {}).get('alternatives_count', 0)}")
    
    impact = results.get('impact', {})
    total_delta = impact.get('total_delta_co2e', 0)
    report.append(f"- **Carbon Impact**: {total_delta:+.4f} kg CO2e")
    
    legal = results.get('legal', {})
    report.append(f"- **Legal Documents Generated**: {legal.get('documents_count', 0)}")
    report.append("")
    
    # Phase 1: Detection Summary
    report.append("## Phase 1: Detection Results")
    if detection.get('issues'):
        report.append("### Detected Issues")
        for issue in detection['issues']:
            report.append(f"#### {issue.get('id', 'Unknown')}")
            report.append(f"- **Category**: {issue.get('category', 'Unknown')}")
            report.append(f"- **Risk Level**: {issue.get('risk_level', 'Unknown')}")
            report.append(f"- **Description**: {issue.get('description', 'No description')}")
            report.append(f"- **Line Number**: {issue.get('line_number', 'N/A')}")
            if issue.get('code_snippet'):
                report.append(f"- **Code Snippet**:")
                report.append(f"```python\n{issue.get('code_snippet')}\n```")
            report.append("")
    else:
        report.append("No ethical issues detected.")
    report.append("")
    
    # Phase 2: Debate Summary
    report.append("## Phase 2: Debate Results")
    debate_results = results.get('debate', {})
    if debate_results.get('debates'):
        report.append(f"**Total Debates**: {debate_results.get('debates_count', 0)}")
        for debate in debate_results['debates']:
            # Handle both DebateRound objects and dicts
            if hasattr(debate, 'issue'):
                desc = debate.issue
                consensus = getattr(debate, 'consensus_reached', False)
                resolution = getattr(debate, 'synthesis', 'No resolution')
            elif isinstance(debate, dict):
                desc = debate.get('issue', debate.get('issue_description', 'Unknown'))
                consensus = debate.get('consensus_reached', False)
                resolution = debate.get('synthesis', debate.get('resolution', 'No resolution'))
            else:
                desc = str(debate)
                consensus = False
                resolution = 'Unknown'
            report.append(f"### Debate: {desc[:50]}...")
            report.append(f"- **Consensus Reached**: {consensus}")
            report.append(f"- **Resolution**: {resolution}")
            report.append("")
    else:
        report.append("No debates conducted (no MEDIUM+ risk issues).")
    report.append("")
    
    # Phase 3: Resolution Summary
    report.append("## Phase 3: Resolution Results")
    resolution_results = results.get('resolution', {})
    if resolution_results.get('alternatives'):
        report.append(f"**Alternatives Generated**: {resolution_results.get('alternatives_count', 0)}")
        for alt in resolution_results['alternatives']:
            report.append(f"### Alternative for: {alt.get('issue_type', 'Unknown')[:50]}...")
            report.append(f"- **Compliance Gain**: {alt.get('compliance_gains', 'N/A')}")
            report.append(f"- **Complexity**: {alt.get('complexity', 'N/A')}")
            report.append("")
            if alt.get('trade_offs'):
                report.append("**Trade-offs**:")
                for key, val in alt.get('trade_offs', {}).items():
                    report.append(f"- {key}: {val}")
            report.append("")
    else:
        report.append("No alternatives generated.")
    report.append("")
    
    # Phase 4: Impact Summary
    report.append("## Phase 4: Impact Results")
    impact_results = results.get('impact', {})
    if impact_results.get('analyses'):
        report.append(f"**Analyses Conducted**: {impact_results.get('analyses_count', 0)}")
        report.append(f"**Total Carbon Delta**: {impact_results.get('total_delta_co2e', 0):+.4f} kg CO2e")
        report.append("")
        for i, analysis in enumerate(impact_results.get('analyses', []), 1):
            report.append(f"### Analysis {i}")
            report.append(f"- **Original CO2e**: {analysis.get('original_co2e', 0):.6f} kg")
            report.append(f"- **Alternative CO2e**: {analysis.get('alternative_co2e', 0):.6f} kg")
            report.append(f"- **Delta**: {analysis.get('delta_co2e', 0):+.6f} kg")
            report.append(f"- **Change**: {analysis.get('percentage_change', 0):+.2f}%")
            report.append("")
    else:
        report.append("No impact analyses conducted.")
    report.append("")
    
    # Phase 5: Legal Summary
    report.append("## Phase 5: Legal Documentation")
    legal_results = results.get('legal', {})
    report.append(f"**Documents Generated**: {legal_results.get('documents_count', 0)}")
    report.append("")
    for doc in legal_results.get('documents', []):
        report.append(f"- **{doc.get('title', 'Unknown')}** ({doc.get('type', 'Unknown')})")
        report.append(f"  - File: {doc.get('file_path', 'N/A')}")
        report.append("")
    
    # Final Summary
    report.append("## Final Assessment")
    report.append("")
    report.append("### Risk Summary")
    risk_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
    for issue in detection.get('issues', []):
        risk = issue.get('risk_level', 'LOW')
        risk_counts[risk] = risk_counts.get(risk, 0) + 1
    
    for risk, count in risk_counts.items():
        if count > 0:
            report.append(f"- **{risk}**: {count} issues")
    
    report.append("")
    report.append("### Compliance Status")
    if risk_counts["HIGH"] > 0 or risk_counts["CRITICAL"] > 0:
        report.append("⚠️ **Action Required**: High-risk issues must be addressed")
    elif risk_counts["MEDIUM"] > 0:
        report.append("📋 **Review Recommended**: Medium-risk issues should be reviewed")
    else:
        report.append("✅ **Compliant**: No significant ethical risks detected")
    
    report.append("")
    report.append("---")
    report.append(f"*Report generated by AXIOM v1.0.0 on {timestamp}*")
    report.append("*Autonomous Ethics Auditing Agent powered by HyperNova-60B-2602*")
    
    report_str = "\n".join(report)
    
    # Save master report
    report_path = os.path.join(output_dir, "AXIOM_ETHICS_REPORT.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_str)
    
    return report_path, report_str
