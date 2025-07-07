# Password Strength Checker

A Python command-line tool to analyze password strength and security. This tool evaluates passwords based on length, character variety, common patterns, and entropy to provide comprehensive security assessments.

## Features

- **Comprehensive Analysis**: Checks length, character types, entropy, and common patterns
- **Security Warnings**: Detects common passwords and predictable patterns
- **Multiple Modes**: Interactive, single password, and batch processing
- **Colored Output**: Visual feedback with colored strength indicators
- **Detailed Reports**: Clear analysis with actionable suggestions

## Installation

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Interactive Mode (Recommended)
```bash
python cli.py
```
This mode hides your password input for security and allows multiple checks.

### Single Password Check
```bash
python cli.py -p "your_password_here"
```
**Note**: Using this method may expose your password in shell history.

### Batch Mode
```bash
python cli.py --batch
```
Enter multiple passwords (one per line), then press Ctrl+D to finish.

### Additional Options
```bash
python cli.py --help              # Show help
python cli.py --no-color          # Disable colored output
python cli.py --score-only        # Output only numeric scores
```

## Examples

### Example 1: Weak Password
```
Password: password123
Strength: Weak (25/100)
Suggestions:
1. Use at least 8 characters (12+ recommended)
2. Include uppercase letters
3. Include special characters (!@#$%^&*)
4. Avoid common passwords
```

### Example 2: Strong Password
```
Password: MySecureP@ssw0rd2024!
Strength: Very Strong (95/100)
✓ All security requirements met
```

## Password Strength Scoring

The tool evaluates passwords based on:

- **Length**: 8+ characters (12+ recommended)
- **Character Variety**: Lowercase, uppercase, numbers, special characters
- **Security**: Not common passwords, no predictable patterns
- **Entropy**: Measure of randomness and unpredictability

## Strength Levels

- **Very Strong (80-100)**: Excellent security
- **Strong (60-79)**: Good security
- **Moderate (40-59)**: Acceptable but could be improved
- **Weak (20-39)**: Poor security, should be changed
- **Very Weak (0-19)**: Extremely insecure

## Running Tests

```bash
python test_password_checker.py
```

## Security Note

This tool is designed for educational and security assessment purposes. Never share your real passwords with any online tools or store them in plain text.

## License

This project is open source and available under the MIT License.