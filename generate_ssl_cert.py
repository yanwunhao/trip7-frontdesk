#!/usr/bin/env python3
"""
Generate self-signed SSL certificates for HTTPS testing.
For production, use certificates from a trusted CA.
"""

import subprocess
import sys
import os

def generate_certificates():
    """Generate self-signed SSL certificates."""
    try:
        # Generate private key
        subprocess.run([
            "openssl", "genrsa", "-out", "key.pem", "2048"
        ], check=True)
        
        # Generate certificate
        subprocess.run([
            "openssl", "req", "-new", "-x509", "-key", "key.pem", 
            "-out", "cert.pem", "-days", "365", "-subj", 
            "/C=CN/ST=State/L=City/O=Organization/CN=localhost"
        ], check=True)
        
        print("✅ SSL certificates generated successfully!")
        print("Files created: key.pem, cert.pem")
        print("⚠️  These are self-signed certificates for development only.")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating certificates: {e}")
        print("Make sure OpenSSL is installed: apt-get install openssl")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ OpenSSL not found. Please install OpenSSL first.")
        print("Ubuntu/Debian: sudo apt-get install openssl")
        print("macOS: brew install openssl")
        sys.exit(1)

if __name__ == "__main__":
    if os.path.exists("cert.pem") or os.path.exists("key.pem"):
        response = input("SSL certificates already exist. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Certificate generation cancelled.")
            sys.exit(0)
    
    generate_certificates()