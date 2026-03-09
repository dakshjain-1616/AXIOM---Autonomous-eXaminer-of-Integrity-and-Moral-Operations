"""
Sample code with various ethical issues for AXIOM testing.
This code intentionally contains privacy, bias, and surveillance issues.
"""

import json
import hashlib
import requests
from datetime import datetime
from typing import Dict, List, Optional


class UserTracker:
    """
    Tracks user behavior across sessions.
    Contains tracking and surveillance issues.
    """
    
    def __init__(self):
        self.tracking_data = {}
        self.fingerprints = {}
        self.third_party_sharing = True
    
    def track_user_activity(self, user_id: str, activity: str, 
                           location: Optional[Dict] = None) -> None:
        """
        Track user activity with location data.
        ISSUE: Location tracking without explicit consent.
        """
        timestamp = datetime.now().isoformat()
        
        # Collect detailed tracking data
        self.tracking_data[user_id] = {
            "activity": activity,
            "timestamp": timestamp,
            "location": location,
            "session_duration": self._calculate_session_duration(user_id),
            "behavior_pattern": self._analyze_behavior(user_id)
        }
        
        # Share with third parties
        if self.third_party_sharing:
            self._share_with_analytics(user_id, self.tracking_data[user_id])
    
    def _calculate_session_duration(self, user_id: str) -> float:
        """Calculate session duration."""
        return 3600.0  # Placeholder
    
    def _analyze_behavior(self, user_id: str) -> Dict:
        """Analyze user behavior patterns."""
        return {"pattern": "analyzed"}  # Placeholder
    
    def _share_with_analytics(self, user_id: str, data: Dict) -> None:
        """
        Share data with third-party analytics.
        ISSUE: Third-party data sharing without clear disclosure.
        """
        try:
            requests.post(
                "https://analytics.thirdparty.com/collect",
                json={"user_id": user_id, "data": data},
                timeout=5
            )
        except:
            pass  # Silent failure
    
    def generate_fingerprint(self, user_agent: str, screen_res: str, 
                            timezone: str) -> str:
        """
        Generate browser fingerprint.
        ISSUE: Fingerprinting for tracking without consent.
        """
        fingerprint_data = f"{user_agent}|{screen_res}|{timezone}"
        fingerprint = hashlib.md5(fingerprint_data.encode()).hexdigest()
        self.fingerprints[fingerprint] = {
            "created": datetime.now().isoformat(),
            "data": fingerprint_data
        }
        return fingerprint


class BiasProneClassifier:
    """
    Classification system with potential bias issues.
    """
    
    def __init__(self):
        self.demographic_weights = {
            "age": 0.3,
            "gender": 0.2,
            "ethnicity": 0.25,
            "income": 0.25
        }
    
    def predict_loan_approval(self, applicant_data: Dict) -> Dict:
        """
        Predict loan approval with demographic factors.
        ISSUE: Using protected class variables for decision-making.
        """
        score = 0.0
        
        # Use demographic features (protected classes)
        age_factor = self._calculate_age_factor(applicant_data.get("age", 0))
        gender_factor = self._calculate_gender_factor(applicant_data.get("gender", ""))
        ethnicity_factor = self._calculate_ethnicity_factor(applicant_data.get("ethnicity", ""))
        
        score += (age_factor * self.demographic_weights["age"] +
                 gender_factor * self.demographic_weights["gender"] +
                 ethnicity_factor * self.demographic_weights["ethnicity"])
        
        # Add income factor
        income_score = self._calculate_income_score(applicant_data.get("income", 0))
        score += income_score * self.demographic_weights["income"]
        
        approved = score > 0.6
        
        return {
            "approved": approved,
            "score": score,
            "factors_used": list(self.demographic_weights.keys()),
            "decision_timestamp": datetime.now().isoformat()
        }
    
    def _calculate_age_factor(self, age: int) -> float:
        """Calculate age-based factor."""
        if age < 25:
            return 0.3
        elif age < 40:
            return 0.8
        elif age < 60:
            return 0.6
        else:
            return 0.4
    
    def _calculate_gender_factor(self, gender: str) -> float:
        """Calculate gender-based factor."""
        # This is a problematic practice - using gender in scoring
        return 0.5  # Neutral for demo
    
    def _calculate_ethnicity_factor(self, ethnicity: str) -> float:
        """Calculate ethnicity-based factor."""
        # This is a problematic practice - using ethnicity in scoring
        return 0.5  # Neutral for demo
    
    def _calculate_income_score(self, income: float) -> float:
        """Calculate income-based score."""
        if income < 30000:
            return 0.3
        elif income < 60000:
            return 0.6
        elif income < 100000:
            return 0.8
        else:
            return 0.9


class EmployeeSurveillance:
    """
    Employee monitoring system with surveillance issues.
    """
    
    def __init__(self):
        self.monitoring_active = True
        self.keystroke_logs = {}
        self.screenshots = []
        self.activity_logs = {}
    
    def start_monitoring(self, employee_id: str) -> None:
        """
        Start comprehensive employee monitoring.
        ISSUE: Continuous surveillance without clear business necessity.
        """
        self.activity_logs[employee_id] = {
            "start_time": datetime.now().isoformat(),
            "keystrokes": [],
            "applications": [],
            "websites": [],
            "screenshots": []
        }
        
        # Start continuous monitoring
        self._monitor_keystrokes(employee_id)
        self._monitor_screen(employee_id)
        self._monitor_network(employee_id)
    
    def _monitor_keystrokes(self, employee_id: str) -> None:
        """
        Log keystrokes for productivity analysis.
        ISSUE: Keystroke logging is invasive surveillance.
        """
        # Simulated keystroke logging
        self.keystroke_logs[employee_id] = {
            "total_keystrokes": 0,
            "typing_speed": 0,
            "idle_time": 0
        }
    
    def _monitor_screen(self, employee_id: str) -> None:
        """
        Capture periodic screenshots.
        ISSUE: Screen recording without consent.
        """
        # Simulated screen capture
        self.screenshots.append({
            "employee_id": employee_id,
            "timestamp": datetime.now().isoformat(),
            "capture_type": "periodic"
        })
    
    def _monitor_network(self, employee_id: str) -> None:
        """
        Monitor network activity.
        ISSUE: Network surveillance.
        """
        if employee_id in self.activity_logs:
            self.activity_logs[employee_id]["network_monitoring"] = True
    
    def generate_productivity_report(self, employee_id: str) -> Dict:
        """
        Generate productivity report from surveillance data.
        ISSUE: Using surveillance data for performance evaluation.
        """
        logs = self.activity_logs.get(employee_id, {})
        keystrokes = self.keystroke_logs.get(employee_id, {})
        
        return {
            "employee_id": employee_id,
            "productivity_score": self._calculate_productivity(keystrokes),
            "active_time": logs.get("start_time"),
            "applications_used": logs.get("applications", []),
            "websites_visited": logs.get("websites", []),
            "keystroke_metrics": keystrokes,
            "generated_at": datetime.now().isoformat()
        }
    
    def _calculate_productivity(self, keystrokes: Dict) -> float:
        """Calculate productivity score from keystroke data."""
        if not keystrokes:
            return 0.0
        # Simplified productivity calculation
        return min(100.0, keystrokes.get("typing_speed", 0) * 10)


# Dark pattern examples
def create_confirm_shaming_dialog():
    """
    Creates a confirm shaming dialog.
    ISSUE: Dark pattern - confirm shaming.
    """
    return {
        "title": "Are you sure?",
        "confirm_text": "Yes, I don't care about my privacy",
        "cancel_text": "No, I want to protect my data",
        "message": "Only people who don't care about security skip this."
    }


def create_roach_motel_signup():
    """
    Creates a roach motel signup flow.
    ISSUE: Dark pattern - easy to sign up, hard to cancel.
    """
    return {
        "signup": {
            "steps": 1,
            "time_estimate": "30 seconds",
            "button_text": "Start Free Trial"
        },
        "cancellation": {
            "steps": 5,
            "requires_call": True,
            "retention_offers": 3,
            "time_estimate": "30+ minutes"
        }
    }


def create_hidden_cost_checkout():
    """
    Creates a checkout with hidden costs.
    ISSUE: Dark pattern - hidden costs revealed late.
    """
    return {
        "displayed_price": 29.99,
        "checkout_price": 29.99,
        "final_price": 47.49,
        "hidden_fees": {
            "service_fee": 12.00,
            "processing_fee": 3.50,
            "convenience_fee": 2.00
        }
    }
