import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import hashlib

@dataclass
class CodeAlternative:
    original_code: str
    alternative_code: str
    issue_type: str
    risk_level: str
    trade_offs: Dict[str, str]
    compliance_gains: List[str]
    functionality_losses: List[str]
    implementation_complexity: str
    timestamp: str = None
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class AXIOMResolver:
    def __init__(self, config=None):
        self.config = config
        self.alternatives: List[CodeAlternative] = []
        self.resolution_patterns = self._load_patterns()
    def _load_patterns(self):
        return {
            'tracking': {
                'patterns': [(r'track|collect|analytics', 'Use privacy-preserving aggregation')],
                'compliance_gains': ['GDPR Article 5, 6', 'CCPA Section 1798.100'],
                'functionality_losses': ['Granular user tracking']
            },
            'bias': {
                'patterns': [(r'demographic|race|gender|ethnicity', 'Remove protected class variables')],
                'compliance_gains': ['GDPR Article 22', 'CCPA Section 1798.125'],
                'functionality_losses': ['Demographic-based personalization']
            },
            'surveillance': {
                'patterns': [(r'monitor|keystroke|screen|record', 'Implement transparency and necessity checks')],
                'compliance_gains': ['GDPR Article 5', 'Privacy Rights'],
                'functionality_losses': ['Continuous monitoring']
            },
            'dark_patterns': {
                'patterns': [(r'confirm|shame|roach|motel|hidden|cost', 'Use clear, neutral UX patterns')],
                'compliance_gains': ['GDPR Article 7', 'Consumer Protection'],
                'functionality_losses': ['Conversion pressure']
            }
        }

    def resolve(self, detection_results):
        self.alternatives = []
        issues = detection_results.get('issues', []) if isinstance(detection_results, dict) else detection_results
        for r in issues:
            if isinstance(r, dict) and r.get('risk_level') in ['MEDIUM', 'HIGH', 'CRITICAL']:
                alt = self._generate(r)
                if alt:
                    self.alternatives.append(alt)
        return {'alternatives': [self._alt_to_dict(a) for a in self.alternatives]}

    def _alt_to_dict(self, alt):
        return {
            'original_snippet': alt.original_code,
            'alternative_snippet': alt.alternative_code,
            'issue_type': alt.issue_type,
            'risk_level': alt.risk_level,
            'trade_offs': alt.trade_offs,
            'compliance_gains': alt.compliance_gains,
            'functionality_losses': alt.functionality_losses,
            'complexity': alt.implementation_complexity,
            'timestamp': alt.timestamp
        }

    def _generate(self, det):
        # Map category to pattern key
        cat = det.get('category', 'unknown')
        it = det.get('issue_type', 'unknown')
        oc = det.get('code_snippet', '')
        rl = det.get('risk_level', 'MEDIUM')
        
        # Try category first, then issue_type (case-insensitive)
        pc = (self.resolution_patterns.get(cat.lower()) or
              self.resolution_patterns.get(it.lower()))
        
        if not pc:
            # Default pattern if nothing matches
            pc = {
                'patterns': [(r'.*', 'Apply privacy-by-design principles')],
                'compliance_gains': ['General Compliance'],
                'functionality_losses': ['None']
            }
            
        ac = self._create(oc, pc['patterns'], cat)
        to = self._analyze(oc, ac, cat)
        
        return CodeAlternative(
            original_code=oc,
            alternative_code=ac,
            issue_type=cat,
            risk_level=rl,
            trade_offs=to,
            compliance_gains=pc['compliance_gains'],
            functionality_losses=pc['functionality_losses'],
            implementation_complexity=self._complexity(ac)
        )
    def _create(self, orig, pats, it):
        a = f'# Alternative - {it}\n'
        for p, r in pats:
            if re.search(p, orig):
                a += f'# {p}->{r}\n'
        return a
    def _complexity(self, code):
        return 'LOW'
    def _analyze(self, o, a, it):
        return {'imp': 'yes'}