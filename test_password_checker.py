#!/usr/bin/env python3
import unittest
from password_checker import PasswordStrengthChecker


class TestPasswordStrengthChecker(unittest.TestCase):
    def setUp(self):
        self.checker = PasswordStrengthChecker()
    
    def test_very_weak_passwords(self):
        weak_passwords = ['123', 'abc', 'password', '12345']
        for password in weak_passwords:
            strength, score, _ = self.checker.calculate_strength(password)
            self.assertIn(strength, ['Very Weak', 'Weak'])
            self.assertLess(score, 40)
    
    def test_strong_passwords(self):
        strong_passwords = [
            'MySecureP@ssw0rd!',
            'C0mpl3x&S3cur3!',
            'Tr0ub4dor&3'
        ]
        for password in strong_passwords:
            strength, score, _ = self.checker.calculate_strength(password)
            self.assertIn(strength, ['Strong', 'Very Strong'])
            self.assertGreaterEqual(score, 60)
    
    def test_length_analysis(self):
        analysis = self.checker.analyze_password('testpassword')
        self.assertEqual(analysis['length'], 12)
        
        analysis = self.checker.analyze_password('short')
        self.assertEqual(analysis['length'], 5)
    
    def test_character_type_detection(self):
        analysis = self.checker.analyze_password('Test123!')
        self.assertTrue(analysis['has_lowercase'])
        self.assertTrue(analysis['has_uppercase'])
        self.assertTrue(analysis['has_numbers'])
        self.assertTrue(analysis['has_special'])
    
    def test_common_password_detection(self):
        analysis = self.checker.analyze_password('password')
        self.assertTrue(analysis['is_common'])
        
        analysis = self.checker.analyze_password('MyUniqueP@ssw0rd!')
        self.assertFalse(analysis['is_common'])
    
    def test_pattern_detection(self):
        analysis = self.checker.analyze_password('aaa111')
        self.assertTrue(analysis['has_patterns'])
        
        analysis = self.checker.analyze_password('RandomStr1ng!')
        self.assertFalse(analysis['has_patterns'])
    
    def test_entropy_calculation(self):
        analysis = self.checker.analyze_password('A1!')
        self.assertGreater(analysis['entropy'], 0)
        
        # Longer, more complex password should have higher entropy
        analysis1 = self.checker.analyze_password('abc')
        analysis2 = self.checker.analyze_password('AbC123!@#')
        self.assertGreater(analysis2['entropy'], analysis1['entropy'])
    
    def test_suggestions_generation(self):
        _, _, suggestions = self.checker.calculate_strength('abc')
        self.assertIn('Use at least 8 characters (12+ recommended)', suggestions)
        
        _, _, suggestions = self.checker.calculate_strength('abcdefgh')
        self.assertIn('Include uppercase letters', suggestions)
        self.assertIn('Include numbers', suggestions)
        self.assertIn('Include special characters (!@#$%^&*)', suggestions)
    
    def test_empty_password(self):
        analysis = self.checker.analyze_password('')
        self.assertEqual(analysis['length'], 0)
        self.assertEqual(analysis['entropy'], 0)
        
        strength, score, _ = self.checker.calculate_strength('')
        self.assertEqual(strength, 'Very Weak')
        self.assertEqual(score, 0)
    
    def test_report_generation(self):
        report = self.checker.generate_report('TestP@ss123')
        self.assertIn('Password Strength Analysis', report)
        self.assertIn('Character Analysis:', report)
        self.assertIn('Security Checks:', report)
    
    def test_score_bounds(self):
        # Test that scores are always between 0 and 100
        test_passwords = [
            '', 'a', 'password', 'MyVerySecureP@ssw0rd123!',
            '123456789', 'ABCDEFGH', 'abcdefgh', '!@#$%^&*()'
        ]
        
        for password in test_passwords:
            _, score, _ = self.checker.calculate_strength(password)
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 100)


if __name__ == '__main__':
    unittest.main()