#!/usr/bin/env python3
import argparse
import sys
import getpass
from password_checker import PasswordStrengthChecker

try:
    from colorama import init, Fore, Style
    init()
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False


def colorize_strength(strength: str, text: str) -> str:
    if not COLORS_AVAILABLE:
        return text
    
    color_map = {
        'Very Strong': Fore.GREEN,
        'Strong': Fore.LIGHTGREEN_EX,
        'Moderate': Fore.YELLOW,
        'Weak': Fore.LIGHTYELLOW_EX,
        'Very Weak': Fore.RED
    }
    
    color = color_map.get(strength, '')
    return f"{color}{text}{Style.RESET_ALL}"


def main():
    parser = argparse.ArgumentParser(
        description='Check password strength and security',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s                    # Interactive mode (recommended)
  %(prog)s -p mypassword      # Check specific password
  %(prog)s --batch            # Batch mode for multiple passwords
  %(prog)s --help             # Show this help
        '''
    )
    
    parser.add_argument(
        '-p', '--password',
        help='Password to check (not recommended for security reasons)'
    )
    
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Check multiple passwords (one per line, Ctrl+D to finish)'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    
    parser.add_argument(
        '--score-only',
        action='store_true',
        help='Output only the numeric score (0-100)'
    )
    
    args = parser.parse_args()
    
    # Disable colors if requested
    global COLORS_AVAILABLE
    if args.no_color:
        COLORS_AVAILABLE = False
    
    checker = PasswordStrengthChecker()
    
    if args.batch:
        handle_batch_mode(checker, args.score_only)
    elif args.password:
        handle_single_password(checker, args.password, args.score_only)
    else:
        handle_interactive_mode(checker, args.score_only)


def handle_single_password(checker, password, score_only):
    if score_only:
        _, score, _ = checker.calculate_strength(password)
        print(score)
    else:
        report = checker.generate_report(password)
        strength, score, _ = checker.calculate_strength(password)
        colored_report = colorize_strength(strength, report)
        print(colored_report)


def handle_interactive_mode(checker, score_only):
    print("Password Strength Checker")
    print("=" * 50)
    print("Enter a password to check its strength (input will be hidden)")
    print("Press Ctrl+C to exit\n")
    
    try:
        while True:
            try:
                password = getpass.getpass("Enter password: ")
                if not password:
                    print("Please enter a password\n")
                    continue
                
                if score_only:
                    _, score, _ = checker.calculate_strength(password)
                    print(f"Score: {score}")
                else:
                    report = checker.generate_report(password)
                    strength, score, _ = checker.calculate_strength(password)
                    colored_report = colorize_strength(strength, report)
                    print(colored_report)
                
                print("\n" + "-" * 50 + "\n")
                
            except EOFError:
                break
                
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)


def handle_batch_mode(checker, score_only):
    print("Batch mode: Enter passwords (one per line), Ctrl+D when done")
    print("-" * 50)
    
    try:
        passwords = []
        while True:
            try:
                password = input()
                if password:
                    passwords.append(password)
            except EOFError:
                break
        
        if not passwords:
            print("No passwords entered.")
            return
        
        for i, password in enumerate(passwords, 1):
            if score_only:
                _, score, _ = checker.calculate_strength(password)
                print(f"Password {i}: {score}")
            else:
                print(f"\nPassword {i}:")
                report = checker.generate_report(password)
                strength, score, _ = checker.calculate_strength(password)
                colored_report = colorize_strength(strength, report)
                print(colored_report)
                print("-" * 50)
                
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)


if __name__ == '__main__':
    main()