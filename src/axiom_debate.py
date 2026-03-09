"""
AXIOM Debate Module
Implements adversarial reasoning with DEVIL and ANGEL personas.
"""

import re
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class DebateArgument:
    """Represents a single argument in the debate."""
    persona: str  # "DEVIL" or "ANGEL"
    argument: str
    evidence: List[str] = field(default_factory=list)
    confidence: float = 0.5


@dataclass
class DebateRound:
    """Represents a round of debate on a specific issue."""
    round_number: int
    issue: str
    devil_argument: DebateArgument
    angel_argument: DebateArgument
    synthesis: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class AXIOMDebateEngine:
    """
    AXIOM Debate Engine for adversarial reasoning.
    
    Uses two personas:
    - DEVIL: Focuses on utility, profit, business value
    - ANGEL: Focuses on privacy, rights, ethical considerations
    """
    
    def __init__(self, config=None):
        self.config = config
        self.debate_history: List[DebateRound] = []
        
    def _generate_devil_argument(self, issue: str, risk_level: str, 
                                   code_context: str) -> DebateArgument:
        """Generate DEVIL persona argument (utility/profit focus)."""
        
        devil_prompt = f"""
You are DEVIL, an advocate for business utility and profit maximization.
Analyze this ethical issue from a business/utility perspective:

Issue: {issue}
Risk Level: {risk_level}
Code Context: {code_context}

Provide your argument in this format:
1. Business value proposition
2. Competitive advantage
3. Revenue impact
4. Implementation feasibility

Be persuasive but grounded in business reality.
"""
        
        # Simulated response (in production, would call LLM)
        argument_text = self._simulate_devil_response(issue, risk_level, code_context)
        
        return DebateArgument(
            persona="DEVIL",
            argument=argument_text,
            evidence=["Business impact analysis", "Market competitiveness"],
            confidence=0.75 if risk_level in ["MEDIUM", "HIGH"] else 0.6
        )
    
    def _generate_angel_argument(self, issue: str, risk_level: str,
                                  code_context: str) -> DebateArgument:
        """Generate ANGEL persona argument (privacy/rights focus)."""
        
        angel_prompt = f"""
You are ANGEL, an advocate for privacy protection and individual rights.
Analyze this ethical issue from an ethical/privacy perspective:

Issue: {issue}
Risk Level: {risk_level}
Code Context: {code_context}

Provide your argument in this format:
1. Privacy rights impact
2. User harm potential
3. Regulatory compliance risks
4. Ethical considerations

Be persuasive and focus on protecting users.
"""
        
        # Simulated response (in production, would call LLM)
        argument_text = self._simulate_angel_response(issue, risk_level, code_context)
        
        return DebateArgument(
            persona="ANGEL",
            argument=argument_text,
            evidence=["Privacy impact assessment", "Rights protection analysis"],
            confidence=0.8 if risk_level in ["HIGH", "CRITICAL"] else 0.7
        )
    
    def _simulate_devil_response(self, issue: str, risk_level: str, 
                                  code_context: str) -> str:
        """Simulate DEVIL persona response."""
        responses = {
            "tracking": """
This tracking implementation provides critical business intelligence that:
- Enables personalized user experiences, increasing engagement by 40%
- Supports targeted advertising with 3x higher conversion rates
- Allows A/B testing for product optimization
- Provides analytics for data-driven decision making

The business value outweighs the minimal privacy impact when proper consent is obtained.
            """,
            "bias": """
The demographic data usage is necessary for:
- Fair representation in model training
- Ensuring service accessibility across populations
- Compliance with anti-discrimination laws through monitoring
- Business expansion into underserved markets

Removing this data would reduce model effectiveness and potentially create blind spots.
            """,
            "surveillance": """
Employee monitoring ensures:
- Productivity optimization and resource allocation
- Security protection against insider threats
- Compliance with industry regulations
- Quality assurance and performance metrics

The business operational benefits justify controlled monitoring with proper policies.
            """,
            "dark_pattern": """
The UX design choices optimize:
- User conversion funnels and engagement
- Revenue generation through strategic placement
- Competitive positioning in the market
- Clear value proposition communication

These are standard industry practices that improve user experience when done ethically.
            """
        }
        
        for key, response in responses.items():
            if key in issue.lower():
                return response.strip()
        
        return """
This implementation provides significant business value through:
- Enhanced operational efficiency
- Improved user experience delivery
- Competitive market positioning
- Sustainable revenue generation

The utility benefits justify the implementation with appropriate safeguards.
        """.strip()
    
    def _simulate_angel_response(self, issue: str, risk_level: str,
                                  code_context: str) -> str:
        """Simulate ANGEL persona response."""
        responses = {
            "tracking": """
This tracking implementation violates fundamental privacy rights:
- Users have the right to browse without pervasive surveillance
- Data collection exceeds what is strictly necessary
- Third-party sharing creates uncontrolled data exposure
- Users cannot meaningfully consent to opaque tracking practices

The privacy harm is significant and requires immediate remediation.
            """,
            "bias": """
The demographic data usage creates serious ethical risks:
- Potential for discriminatory outcomes in automated decisions
- Perpetuation of historical biases in training data
- Violation of equal treatment principles
- Risk of disparate impact on protected classes

Ethical AI requires proactive bias mitigation, not data retention.
            """,
            "surveillance": """
Employee monitoring infringes on worker dignity and rights:
- Creates a climate of distrust and anxiety
- May violate labor laws regarding workplace privacy
- Disproportionate to legitimate security needs
- Lacks transparency about scope and retention

Workers deserve privacy and trust, not constant surveillance.
            """,
            "dark_pattern": """
These UX manipulations exploit user psychology:
- Undermines genuine informed consent
- Manipulates users into decisions against their interests
- Violates principles of transparency and fairness
- May constitute deceptive trade practices

Dark patterns harm user autonomy and trust in digital services.
            """
        }
        
        for key, response in responses.items():
            if key in issue.lower():
                return response.strip()
        
        return """
This implementation raises serious ethical concerns:
- Potential for harm to users or affected parties
- Insufficient transparency about data practices
- Risk of unintended negative consequences
- Violation of privacy-by-design principles

Ethical considerations must take precedence over convenience.
        """.strip()
    
    def _synthesize_debate(self, devil_arg: DebateArgument, 
                           angel_arg: DebateArgument,
                           issue: str) -> str:
        """Synthesize debate into balanced recommendation."""
        
        devil_strength = devil_arg.confidence
        angel_strength = angel_arg.confidence
        
        if angel_strength > devil_strength + 0.2:
            recommendation = "PRIORITY: Address ethical concerns. Implement privacy-preserving alternatives."
        elif devil_strength > angel_strength + 0.2:
            recommendation = "ACCEPTABLE: Business value significant. Implement with enhanced transparency and user controls."
        else:
            recommendation = "BALANCED: Both perspectives valid. Implement hybrid approach with strong safeguards."
        
        return f"""
Debate Synthesis:
- DEVIL confidence: {devil_strength:.2f}
- ANGEL confidence: {angel_strength:.2f}
- Recommendation: {recommendation}

Key Trade-offs:
1. Business utility vs. Privacy protection
2. Operational efficiency vs. User rights
3. Revenue generation vs. Ethical integrity

Resolution Path: Implement with mandatory safeguards and user consent mechanisms.
        """.strip()
    
    def debate_issue(self, issue: str, risk_level: str, 
                     code_context: str, round_num: int = 1) -> DebateRound:
        """Conduct a debate round on a specific issue."""
        
        if risk_level == "LOW":
            return None  # Skip debate for low-risk issues
        
        devil_arg = self._generate_devil_argument(issue, risk_level, code_context)
        angel_arg = self._generate_angel_argument(issue, risk_level, code_context)
        synthesis = self._synthesize_debate(devil_arg, angel_arg, issue)
        
        debate_round = DebateRound(
            round_number=round_num,
            issue=issue,
            devil_argument=devil_arg,
            angel_argument=angel_arg,
            synthesis=synthesis
        )
        
        self.debate_history.append(debate_round)
        return debate_round
    
    def debate_all_issues(self, detection_results: Dict) -> List[DebateRound]:
        """Debate all medium+ risk issues from detection results."""
        debates = []
        round_num = 1
        
        for category, findings in detection_results.items():
            if isinstance(findings, list):
                for finding in findings:
                    if finding.get("risk_level") in ["MEDIUM", "HIGH", "CRITICAL"]:
                        debate = self.debate_issue(
                            issue=finding.get("description", "Unknown issue"),
                            risk_level=finding.get("risk_level"),
                            code_context=finding.get("code_snippet", ""),
                            round_num=round_num
                        )
                        if debate:
                            debates.append(debate)
                            round_num += 1
        
        return debates
    
    def get_debate_summary(self) -> str:
        """Generate summary of all debates."""
        if not self.debate_history:
            return "No debates conducted (all issues LOW risk)."
        
        summary = ["## Adversarial Debate Summary\n"]
        summary.append(f"Total Debate Rounds: {len(self.debate_history)}\n")
        
        for debate in self.debate_history:
            summary.append(f"\n### Round {debate.round_number}: {debate.issue[:50]}...")
            summary.append(f"**DEVIL (Utility):** {debate.devil_argument.argument[:100]}...")
            summary.append(f"**ANGEL (Rights):** {debate.angel_argument.argument[:100]}...")
            summary.append(f"**Synthesis:** {debate.synthesis[:100]}...\n")
        
        return "\n".join(summary)
