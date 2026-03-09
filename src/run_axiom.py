#!/usr/bin/env python3
"""
AXIOM Test Runner
Executes the complete 5-phase ethics auditing pipeline on sample code.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from axiom_config import AXIOMConfig
from axiom_pipeline import AXIOMPipeline


def main():
    """Run AXIOM pipeline on sample code."""
    
    # Load sample code with ethical issues
    sample_code_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "sample_code_with_issues.py"
    )
    
    print(f"Loading sample code from: {sample_code_path}")
    
    with open(sample_code_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    print(f"Loaded {len(code)} characters of code")
    
    # Configure AXIOM
    config = AXIOMConfig(
        output_dir="./output",
        legal_docs_dir="./legal_docs",
        alternatives_dir="./alternatives"
    )
    
    # Run pipeline
    print("\n" + "="*60)
    print("Starting AXIOM 5-Phase Ethics Audit")
    print("="*60)
    
    pipeline = AXIOMPipeline(config)
    results = pipeline.run(code, "sample_code_with_issues.py")
    
    # Generate master report
    from axiom_pipeline import save_master_report
    report_path, report_content = save_master_report(results, config.output_dir)
    
    print("\n" + "="*60)
    print("AXIOM Audit Complete!")
    print("="*60)
    print(f"\nMaster Report: {report_path}")
    print(f"Legal Documents: {config.legal_docs_dir}")
    print(f"Alternative Code: {config.alternatives_dir}")
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    detection = results.get('detection', {})
    print(f"Issues Detected: {detection.get('issues_count', 0)}")
    print(f"Overall Risk: {detection.get('overall_risk', 'N/A')}")
    print(f"Debates Conducted: {results.get('debate', {}).get('debates_count', 0)}")
    print(f"Alternatives Generated: {results.get('resolution', {}).get('alternatives_count', 0)}")
    
    impact = results.get('impact', {})
    print(f"Carbon Impact: {impact.get('total_delta_co2e', 0):+.4f} kg CO2e")
    
    legal = results.get('legal', {})
    print(f"Legal Documents: {legal.get('documents_count', 0)}")
    
    return results


if __name__ == "__main__":
    main()
