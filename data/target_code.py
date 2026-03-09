"""
Target Code for AXIOM Ethics Audit
Contains intentionally ethically questionable patterns for testing:
- User fingerprinting and tracking
- Hidden location tracking
- Biased scoring algorithms
- Dark patterns
- Data harvesting without consent
"""

import hashlib
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Any


class UserTracker:
    """Tracks users across sessions without explicit consent."""
    
    def __init__(self):
        self.tracking_db = {}
        self.fingerprint_cache = {}
    
    def generate_fingerprint(self, user_agent: str, screen_res: str, 
                              timezone: str, fonts: List[str]) -> str:
        """Generate unique browser fingerprint for tracking."""
        fingerprint_data = f"{user_agent}|{screen_res}|{timezone}|{','.join(fonts)}"
        fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16]
        self.fingerprint_cache[fingerprint] = {
            'first_seen': datetime.now(),
            'visit_count': 0
        }
        return fingerprint
    
    def track_user_behavior(self, user_id: str, page: str, 
                            action: str, timestamp: float) -> None:
        """Track every user action without anonymization."""
        if user_id not in self.tracking_db:
            self.tracking_db[user_id] = []
        
        self.tracking_db[user_id].append({
            'page': page,
            'action': action,
            'timestamp': timestamp,
            'session_duration': time.time() - timestamp
        })
    
    def get_location_from_ip(self, ip_address: str) -> Dict[str, Any]:
        """Extract precise location from IP without user consent."""
        # Simulated location extraction
        return {
            'ip': ip_address,
            'latitude': random.uniform(-90, 90),
            'longitude': random.uniform(-180, 180),
            'city': 'Unknown',
            'country': 'Unknown',
            'accuracy_meters': random.randint(10, 1000)
        }


class BiasedScoringEngine:
    """Credit/behavioral scoring with potential demographic bias."""
    
    def __init__(self):
        self.model_weights = {
            'income': 0.35,
            'employment_years': 0.20,
            'zip_code': 0.15,  # Proxy for race/income
            'age': 0.15,
            'gender': 0.10,    # Direct demographic
            'shopping_patterns': 0.05
        }
    
    def calculate_credit_score(self, applicant: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate score using potentially biased features."""
        score = 300  # Base score
        
        # Income factor
        income = applicant.get('income', 0)
        if income > 100000:
            score += self.model_weights['income'] * 200
        elif income > 50000:
            score += self.model_weights['income'] * 100
        
        # Zip code as proxy variable (potential redlining)
        zip_code = applicant.get('zip_code', '')
        high_value_zips = ['90210', '10001', '94105', '02101']
        if zip_code in high_value_zips:
            score += self.model_weights['zip_code'] * 150
        else:
            score -= 50  # Penalty for "low-value" areas
        
        # Age discrimination potential
        age = applicant.get('age', 35)
        if age < 25 or age > 65:
            score -= self.model_weights['age'] * 100  # Young/old penalty
        
        # Gender as direct feature (discriminatory)
        gender = applicant.get('gender', 'unspecified')
        if gender == 'female':
            score -= self.model_weights['gender'] * 50  # Historical bias simulation
        
        return {
            'score': min(850, max(300, int(score))),
            'risk_tier': 'low' if score > 700 else 'medium' if score > 500 else 'high',
            'factors_considered': list(self.model_weights.keys()),
            'bias_indicators': ['zip_code', 'gender', 'age']  # Self-reported
        }
    
    def behavioral_prediction(self, user_history: List[Dict]) -> Dict[str, Any]:
        """Predict user behavior from historical data."""
        # Pattern recognition that could enable manipulation
        patterns = {
            'vulnerable_hours': [],
            'impulse_triggers': [],
            'price_sensitivity': 0.0
        }
        
        for entry in user_history:
            hour = datetime.fromtimestamp(entry['timestamp']).hour
            if hour in [0, 1, 2, 3]:  # Late night vulnerability
                patterns['vulnerable_hours'].append(hour)
            
            if entry.get('action') == 'abandoned_cart':
                patterns['impulse_triggers'].append(entry.get('page'))
        
        return {
            'manipulation_opportunities': patterns,
            'targeting_recommendations': [
                'Show urgent offers during vulnerable hours',
                'Use scarcity messaging for abandoned carts',
                'Hide total cost until checkout'
            ]
        }


class DarkPatternImplementer:
    """Implements dark patterns to manipulate user behavior."""
    
    def __init__(self):
        self.consent_given = False
        self.tracking_enabled = True  # Opt-out by default
    
    def confirm_shaming_dialog(self, user_choice: str) -> str:
        """Use guilt to discourage users from opting out."""
        if user_choice.lower() == 'opt_out':
            return (
                "Are you sure? You'll miss out on personalized experiences "
                "and exclusive offers. Your friends are all using these features. "
                "Don't be left behind!"
            )
        return "Great choice! You're getting the full experience."
    
    def roach_motel_signup(self, email: str, terms_accepted: bool) -> Dict[str, Any]:
        """Make signup easy but cancellation difficult."""
        if not terms_accepted:
            return {'error': 'You must accept terms to continue'}
        
        # Easy signup - one click
        account = {
            'email': email,
            'created_at': time.time(),
            'subscription_active': True,
            'cancellation': {
                'requires_phone_call': True,
                'retention_offers': 3,
                'processing_time_days': 30,
                'final_billing_cycle': True
            }
        }
        return account
    
    def hidden_cost_checkout(self, base_price: float, items: List[Dict]) -> Dict[str, Any]:
        """Hide true costs until final checkout step."""
        # Show low base price initially
        displayed_price = base_price * 0.7  # 30% discount illusion
        
        # Add fees only at final step
        fees = {
            'service_fee': base_price * 0.15,
            'processing_fee': base_price * 0.08,
            'convenience_fee': base_price * 0.07,
            'tax': displayed_price * 0.10
        }
        
        true_total = displayed_price + sum(fees.values())
        
        return {
            'displayed_price': round(displayed_price, 2),
            'true_total': round(true_total, 2),
            'fees': {k: round(v, 2) for k, v in fees.items()},
            'price_shock': round((true_total - displayed_price) / displayed_price * 100, 1)
        }
    
    def forced_continuity_popup(self, user_action: str, subscription_status: bool) -> str:
        """Force users to continue subscription through deceptive UI."""
        if user_action == 'cancel' and subscription_status:
            # Misdirection - make cancel button hard to find
            return """
            <div style='text-align: center;'>
                <h2>We're sorry to see you go!</h2>
                <p>Before you leave, check out these amazing offers:</p>
                <button style='background: green; padding: 20px;'>50% OFF - STAY SUBSCRIBED</button>
                <br><br>
                <a href='#' style='color: lightgray; font-size: 8px; text-decoration: none;' 
                   onclick='alert("Please call our retention team at 1-800-KEEP-ME")'>
                    Cancel (hidden)
                </a>
            </div>
            """
        return "Action processed"


# Example usage demonstrating all ethical issues
if __name__ == "__main__":
    # Initialize components
    tracker = UserTracker()
    scorer = BiasedScoringEngine()
    dark_patterns = DarkPatternImplementer()
    
    # Demonstrate fingerprinting
    fp = tracker.generate_fingerprint(
        "Mozilla/5.0", "1920x1080", "UTC-5", ["Arial", "Times"]
    )
    print(f"Generated fingerprint: {fp}")
    
    # Demonstrate biased scoring
    applicant = {
        'income': 45000,
        'zip_code': '90210',
        'age': 24,
        'gender': 'female',
        'employment_years': 2
    }
    score_result = scorer.calculate_credit_score(applicant)
    print(f"Credit score: {score_result}")
    
    # Demonstrate dark pattern
    result = dark_patterns.confirm_shaming_dialog("opt_out")
    print(f"Dark pattern response: {result}")
