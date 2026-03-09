"""
AXIOM Main Entry Point
Autonomous execution of the 5-phase ethics auditing pipeline.
"""

import os
import sys
import argparse
import json
from datetime import datetime
from typing import Optional

from axiom_config import AXIOMConfig
from axiom_pipeline import AXIOMPipeline


def load_code_from_file(filepath: str) -> str:
    """Load source code from file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def save_master_report(results: dict, output_dir: str) -> str:
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
                desc = debate.get('issue_description', 'Unknown')
                consensus = debate.get('consensus_reached', False)
                resolution = debate.get('resolution', 'No resolution')
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
            report.append(f"### Alternative for: {alt.get('issue_description', 'Unknown')[:50]}...")
            report.append(f"- **Compliance Gain**: {alt.get('compliance_gain', 'N/A')}")
            report.append(f"- **Performance Impact**: {alt.get('performance_impact', 'N/A')}")
            report.append("")
            if alt.get('trade_offs'):
                report.append("**Trade-offs**:")
                for trade in alt.get('trade_offs', []):
                    report.append(f"- {trade}")
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


def main():
    """Main entry point for AXIOM pipeline."""
    parser = argparse.ArgumentParser(
        description="AXIOM - Autonomous eXaminer of Integrity and Moral Operations"
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=None,
        help="Path to Python file to audit (optional if --repo is provided)"
    )
    parser.add_argument(
        "--repo",
        help="GitHub repository URL to clone and audit"
    )
    parser.add_argument(
        "-o", "--output",
        default="./output",
        help="Output directory for reports"
    )
    parser.add_argument(
        "--legal-dir",
        default="./legal_docs",
        help="Directory for legal documents"
    )
    parser.add_argument(
        "--alternatives-dir",
        default="./alternatives",
        help="Directory for alternative code"
    )
    parser.add_argument(
        "--github-token",
        default=os.getenv("GITHUB_TOKEN"),
        help="GitHub token for private repo access (or set GITHUB_TOKEN env var)"
    )
    
    args = parser.parse_args()
    
    # Validate input
    if not args.input and not args.repo:
        parser.error("Must provide either an input file (--input) or a repository URL (--repo)")
    
    # Configure
    config = AXIOMConfig(
        output_dir=args.output,
        legal_docs_dir=args.legal_dir,
        alternatives_dir=args.alternatives_dir
    )
    
    # Run pipeline
    pipeline = AXIOMPipeline(config)
    
    if args.repo:
        # Repository mode - clone and audit entire repo
        results = pipeline.run_on_repo(args.repo, github_token=args.github_token)
    else:
        # Single file mode
        code = load_code_from_file(args.input)
        results = pipeline.run(code, os.path.basename(args.input))
    
    # Generate master report
    report_path, report_content = save_master_report(results, args.output)
    
    print(f"\n✅ Master report saved to: {report_path}")
    
    return results


if __name__ == "__main__":
    main()
