import re
import string
from typing import Dict, List, Tuple


class PasswordStrengthChecker:
    def __init__(self):
        self.common_passwords = {
            'password', 'password123', '123456', 'qwerty', 'abc123',
            'letmein', 'welcome', 'admin', 'user', 'test', 'guest',
            'login', 'password1', '12345678', 'sunshine', 'princess',
            'dragon', 'monkey', 'football', 'baseball', 'master'
        }
        
        self.common_patterns = [
            r'(.)\1{2,}',  # Repeated characters (aaa, 111)
            r'(012|123|234|345|456|567|678|789|890)',  # Sequential numbers
            r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)',  # Sequential letters
            r'(qwerty|asdfgh|zxcvbn)',  # Keyboard patterns
        ]
    
    def analyze_password(self, password: str) -> Dict:
        analysis = {
            'length': len(password),
            'has_lowercase': bool(re.search(r'[a-z]', password)),
            'has_uppercase': bool(re.search(r'[A-Z]', password)),
            'has_numbers': bool(re.search(r'[0-9]', password)),
            'has_special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
            'is_common': password.lower() in self.common_passwords,
            'has_patterns': self._has_common_patterns(password),
            'entropy': self._calculate_entropy(password)
        }
        return analysis
    
    def _has_common_patterns(self, password: str) -> bool:
        for pattern in self.common_patterns:
            if re.search(pattern, password.lower()):
                return True
        return False
    
    def _calculate_entropy(self, password: str) -> float:
        charset_size = 0
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'[0-9]', password):
            charset_size += 10
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            charset_size += 32
        
        if charset_size == 0:
            return 0
        
        import math
        return len(password) * math.log2(charset_size)
    
    def calculate_strength(self, password: str) -> Tuple[str, int, List[str]]:
        analysis = self.analyze_password(password)
        score = 0
        suggestions = []
        
        # Length scoring
        if analysis['length'] >= 12:
            score += 25
        elif analysis['length'] >= 8:
            score += 15
        elif analysis['length'] >= 6:
            score += 5
        else:
            suggestions.append("Use at least 8 characters (12+ recommended)")
        
        # Character variety scoring
        if analysis['has_lowercase']:
            score += 5
        else:
            suggestions.append("Include lowercase letters")
        
        if analysis['has_uppercase']:
            score += 5
        else:
            suggestions.append("Include uppercase letters")
        
        if analysis['has_numbers']:
            score += 5
        else:
            suggestions.append("Include numbers")
        
        if analysis['has_special']:
            score += 10
        else:
            suggestions.append("Include special characters (!@#$%^&*)")
        
        # Penalty for common passwords
        if analysis['is_common']:
            score -= 25
            suggestions.append("Avoid common passwords")
        
        # Penalty for patterns
        if analysis['has_patterns']:
            score -= 15
            suggestions.append("Avoid predictable patterns")
        
        # Entropy bonus
        if analysis['entropy'] > 60:
            score += 20
        elif analysis['entropy'] > 40:
            score += 10
        
        # Determine strength level
        if score >= 80:
            strength = "Very Strong"
        elif score >= 60:
            strength = "Strong"
        elif score >= 40:
            strength = "Moderate"
        elif score >= 20:
            strength = "Weak"
        else:
            strength = "Very Weak"
        
        return strength, max(0, min(100, score)), suggestions
    
    def generate_report(self, password: str) -> str:
        strength, score, suggestions = self.calculate_strength(password)
        analysis = self.analyze_password(password)
        
        report = f"""
Password Strength Analysis
{'='*50}
Password: {'*' * len(password)}
Length: {analysis['length']} characters
Strength: {strength} ({score}/100)
Entropy: {analysis['entropy']:.1f} bits

Character Analysis:
- Lowercase letters: {'✓' if analysis['has_lowercase'] else '✗'}
- Uppercase letters: {'✓' if analysis['has_uppercase'] else '✗'}
- Numbers: {'✓' if analysis['has_numbers'] else '✗'}
- Special characters: {'✓' if analysis['has_special'] else '✗'}

Security Checks:
- Common password: {'✗ AVOID' if analysis['is_common'] else '✓'}
- Predictable patterns: {'✗ AVOID' if analysis['has_patterns'] else '✓'}
"""
        
        if suggestions:
            report += "\nSuggestions for improvement:\n"
            for i, suggestion in enumerate(suggestions, 1):
                report += f"{i}. {suggestion}\n"
        
        return report