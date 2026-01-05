import argparse
import hashlib
import time
import itertools
import string
from datetime import datetime

class PasswordTester:
    def __init__(self):
        self.common_passwords = [
            'password', '123456', '12345678', '1234', 'qwerty', '12345',
            'dragon', 'baseball', 'football', 'letmein', 'monkey',
            'abc123', 'master', 'hello', 'secret', 'admin', 'welcome',
            'password1', 'superman', 'qazwsx', 'trustno1', 'admin123'
        ]
    
    def hash_password(self, password, algorithm='md5'):
        """Hash a password using specified algorithm"""
        if algorithm == 'md5':
            return hashlib.md5(password.encode()).hexdigest()
        elif algorithm == 'sha1':
            return hashlib.sha1(password.encode()).hexdigest()
        elif algorithm == 'sha256':
            return hashlib.sha256(password.encode()).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    def dictionary_attack(self, target_hash, algorithm='md5', dictionary=None):
        """Perform dictionary attack"""
        print(f"🔑 Starting dictionary attack ({algorithm})...")
        
        dictionary = dictionary or self.common_passwords
        attempts = 0
        start_time = time.time()
        
        for word in dictionary:
            attempts += 1
            hashed = self.hash_password(word, algorithm)
            
            if attempts % 1000 == 0:
                elapsed = time.time() - start_time
                print(f"  Tested {attempts} passwords | {attempts/elapsed:.0f} p/s", end='\r')
            
            if hashed == target_hash:
                elapsed = time.time() - start_time
                print(f"\n✅ CRACKED: {word}")
                print(f"   Time: {elapsed:.2f}s | Attempts: {attempts}")
                return word
        
        print(f"\n❌ Password not found in dictionary")
        return None
    
    def brute_force_attack(self, target_hash, max_length=4, algorithm='md5'):
        """Perform brute force attack"""
        print(f"🔑 Starting brute force attack (max length: {max_length})...")
        
        chars = string.ascii_lowercase + string.digits
        attempts = 0
        start_time = time.time()
        
        for length in range(1, max_length + 1):
            for combination in itertools.product(chars, repeat=length):
                password = ''.join(combination)
                attempts += 1
                hashed = self.hash_password(password, algorithm)
                
                if attempts % 10000 == 0:
                    elapsed = time.time() - start_time
                    print(f"  Length {length}: {attempts} tested | {attempts/elapsed:.0f} p/s", end='\r')
                
                if hashed == target_hash:
                    elapsed = time.time() - start_time
                    print(f"\n✅ CRACKED: {password}")
                    print(f"   Time: {elapsed:.2f}s | Attempts: {attempts}")
                    return password
        
        print(f"\n❌ Password not found (max length: {max_length})")
        return None
    
    def password_strength_check(self, password):
        """Check password strength"""
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 3
        elif len(password) >= 8:
            score += 2
        elif len(password) >= 6:
            score += 1
        else:
            feedback.append("Too short (minimum 8 characters recommended)")
        
        # Character variety
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        char_types = sum([has_upper, has_lower, has_digit, has_special])
        
        if char_types == 4:
            score += 3
        elif char_types == 3:
            score += 2
        elif char_types == 2:
            score += 1
        else:
            feedback.append("Add more character types (upper, lower, digits, special)")
        
        # Common password check
        if password.lower() in [p.lower() for p in self.common_passwords]:
            score = 0
            feedback.append("Password is too common")
        
        # Sequential characters check
        if any(password[i:i+3] in string.ascii_lowercase or 
               password[i:i+3] in string.ascii_uppercase or
               password[i:i+3] in string.digits for i in range(len(password)-2)):
            score -= 1
            feedback.append("Avoid sequential characters")
        
        # Determine strength
        if score >= 5:
            strength = "STRONG"
        elif score >= 3:
            strength = "MEDIUM"
        else:
            strength = "WEAK"
        
        return {
            'strength': strength,
            'score': score,
            'feedback': feedback,
            'length': len(password),
            'has_upper': has_upper,
            'has_lower': has_lower,
            'has_digit': has_digit,
            'has_special': has_special
        }
    
    def generate_secure_password(self, length=12):
        """Generate a secure password"""
        import secrets
        
        if length < 8:
            length = 8
        
        # Ensure at least one of each character type
        chars = string.ascii_letters + string.digits + string.punctuation
        
        while True:
            password = ''.join(secrets.choice(chars) for _ in range(length))
            
            # Check if it meets criteria
            if (any(c.islower() for c in password) and
                any(c.isupper() for c in password) and
                any(c.isdigit() for c in password) and
                any(c in string.punctuation for c in password)):
                return password

class SecurityAuditor:
    def __init__(self):
        self.findings = []
    
    def check_file_permissions(self, path):
        """Check file permissions (Unix-like systems)"""
        print(f"📁 Checking permissions for: {path}")
        
        import os
        import stat
        
        try:
            st = os.stat(path)
            mode = st.st_mode
            
            # Check world-writable files
            if mode & stat.S_IWOTH:
                self.findings.append({
                    'type': 'World-writable file',
                    'risk': 'HIGH',
                    'path': path,
                    'description': 'File is writable by anyone'
                })
                print(f"  ⚠️  World-writable: {path}")
            
            # Check setuid/setgid
            if mode & stat.S_ISUID:
                self.findings.append({
                    'type': 'SetUID file',
                    'risk': 'MEDIUM',
                    'path': path,
                    'description': 'File has SetUID bit set'
                })
                print(f"  ⚠️  SetUID: {path}")
            
            if mode & stat.S_ISGID:
                self.findings.append({
                    'type': 'SetGID file',
                    'risk': 'MEDIUM',
                    'path': path,
                    'description': 'File has SetGID bit set'
                })
                print(f"  ⚠️  SetGID: {path}")
            
        except Exception as e:
            print(f"  ❌ Error checking {path}: {e}")
    
    def check_sudo_permissions(self):
        """Check sudo permissions (Unix-like systems)"""
        print("🔐 Checking sudo permissions...")
        
        try:
            import subprocess
            
            # Check sudoers file
            result = subprocess.run(['sudo', '-l'], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("  Current user can run sudo commands:")
                print(f"  {result.stdout}")
            else:
                print("  Current user cannot run sudo commands")
        
        except Exception as e:
            print(f"  ❌ Error checking sudo: {e}")

def main():
    parser = argparse.ArgumentParser(description='Password Security & System Auditing Tools')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Password crack command
    crack_parser = subparsers.add_parser('crack', help='Password cracking tools')
    crack_parser.add_argument('hash', help='Hash to crack')
    crack_parser.add_argument('-a', '--algorithm', choices=['md5', 'sha1', 'sha256'], 
                             default='md5', help='Hash algorithm')
    crack_parser.add_argument('-m', '--mode', choices=['dictionary', 'bruteforce'], 
                             default='dictionary', help='Attack mode')
    crack_parser.add_argument('-l', '--length', type=int, default=4, 
                             help='Max length for brute force')
    
    # Password strength command
    strength_parser = subparsers.add_parser('strength', help='Check password strength')
    strength_parser.add_argument('password', help='Password to check')
    
    # Generate password command
    generate_parser = subparsers.add_parser('generate', help='Generate secure password')
    generate_parser.add_argument('-l', '--length', type=int, default=12, 
                                help='Password length')
    
    # Audit command
    audit_parser = subparsers.add_parser('audit', help='System security audit')
    audit_parser.add_argument('-p', '--path', default='.', help='Path to check')
    
    args = parser.parse_args()
    
    print("="*80)
    print("🔐 PASSWORD & SECURITY AUDITING TOOLS")
    print("="*80)
    
    if args.command == 'crack':
        tester = PasswordTester()
        
        if args.mode == 'dictionary':
            result = tester.dictionary_attack(args.hash, args.algorithm)
        else:
            result = tester.brute_force_attack(args.hash, args.length, args.algorithm)
        
        if not result:
            print("\n💡 TIPS:")
            print("  • Try a different attack mode")
            print("  • Use a larger dictionary")
            print("  • Increase max length for brute force")
            print("  • Modern passwords should be resistant to these attacks")
    
    elif args.command == 'strength':
        tester = PasswordTester()
        result = tester.password_strength_check(args.password)
        
        print(f"\nPassword: {'*' * len(args.password)}")
        print(f"Strength: {result['strength']} (Score: {result['score']}/6)")
        print(f"Length: {result['length']} characters")
        print(f"Character Types:")
        print(f"  • Uppercase: {'✓' if result['has_upper'] else '✗'}")
        print(f"  • Lowercase: {'✓' if result['has_lower'] else '✗'}")
        print(f"  • Digits: {'✓' if result['has_digit'] else '✗'}")
        print(f"  • Special: {'✓' if result['has_special'] else '✗'}")
        
        if result['feedback']:
            print(f"\n⚠️  Recommendations:")
            for item in result['feedback']:
                print(f"  • {item}")
        
        print(f"\n💡 For strong passwords:")
        print("  • Use at least 12 characters")
        print("  • Mix character types")
        print("  • Avoid common words")
        print("  • Use passphrases: 'CorrectHorseBatteryStaple'")
    
    elif args.command == 'generate':
        tester = PasswordTester()
        password = tester.generate_secure_password(args.length)
        
        print(f"\nGenerated Password: {password}")
        print(f"\nHash values (for testing):")
        print(f"  MD5:    {tester.hash_password(password, 'md5')}")
        print(f"  SHA1:   {tester.hash_password(password, 'sha1')}")
        print(f"  SHA256: {tester.hash_password(password, 'sha256')}")
        
        # Check its strength
        strength = tester.password_strength_check(password)
        print(f"\nStrength: {strength['strength']} (Score: {strength['score']}/6)")
    
    elif args.command == 'audit':
        auditor = SecurityAuditor()
        
        print("🔍 System Security Audit")
        print("-"*80)
        
        # Check file permissions
        import os
        if os.path.exists(args.path):
            if os.path.isfile(args.path):
                auditor.check_file_permissions(args.path)
            else:
                # Check first few files in directory
                for root, dirs, files in os.walk(args.path):
                    for file in files[:10]:  # Limit to first 10 files
                        filepath = os.path.join(root, file)
                        auditor.check_file_permissions(filepath)
        
        # Check sudo permissions
        auditor.check_sudo_permissions()
        
        if auditor.findings:
            print("\n" + "="*80)
            print("⚠️  SECURITY FINDINGS")
            print("="*80)
            
            for finding in auditor.findings:
                print(f"\n[{finding['risk']}] {finding['type']}")
                print(f"   Path: {finding['path']}")
                print(f"   Description: {finding['description']}")
        else:
            print("\n✅ No security issues found!")
    
    else:
        parser.print_help()
    
    print("\n" + "="*80)
    print("⚠️  ETHICAL USE ONLY")
    print("="*80)
    print("These tools are for authorized security testing only.")
    print("Unauthorized use against systems you don't own is illegal.")
    print("Always get proper authorization before testing.")

if __name__ == "__main__":
    main()
