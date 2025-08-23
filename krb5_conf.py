#!/usr/bin/env python3

"""
Script to generate /etc/krb5.conf file for Kerberos configuration.
Takes 3 arguments: FQDN, domain name, and IP address.
This script is especially useful for evil-winrm, by providing a domain fqdn, a domain name and the associated IP address.
```bash
export KRB5CCNAME=xxxxxxx.ccache
evil-winrm -i dc01.mirage.htb -r mirage.htb
```
Usage: python3 krb5_conf.py <fqdn> <domain_name> <ip_address>

"""


import sys
import os
import argparse
from pathlib import Path


def create_krb5_conf(fqdn, domain_name, ip_address, output_path="/etc/krb5.conf"):
    """
    Create a krb5.conf file with the provided parameters.
    
    Args:
        fqdn (str): Fully Qualified Domain Name of the KDC server
        domain_name (str): Domain name (realm)
        ip_address (str): IP address of the KDC server
        output_path (str): Path where to create the krb5.conf file
    """
    
    # Convert domain name to uppercase for realm
    realm = domain_name.upper()
    
    # krb5.conf template
    krb5_conf_content = f"""[logging]
 default = FILE:/var/log/krb5libs.log
 kdc = FILE:/var/log/krb5kdc.log
 admin_server = FILE:/var/log/kadmind.log

[libdefaults]
 dns_lookup_realm = false
 ticket_lifetime = 24h
 renew_lifetime = 7d
 forwardable = true
 rdns = false
 pkinit_anchors = FILE:/etc/pki/tls/certs/ca-bundle.crt
 default_realm = {realm}
 default_ccache_name = KEYRING:persistent:%{{uid}}

[realms]
 {realm} = {{
  kdc = {fqdn}:88
  kdc = {ip_address}:88
  admin_server = {fqdn}:749
  admin_server = {ip_address}:749
 }}

[domain_realm]
 .{domain_name} = {realm}
 {domain_name} = {realm}
 .{fqdn} = {realm}
 {fqdn} = {realm}
"""
    
    try:
        # Create directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, mode=0o755)
        
        # Write the configuration file
        with open(output_path, 'w') as f:
            f.write(krb5_conf_content)
        
        # Set appropriate permissions (readable by all, writable by root only)
        os.chmod(output_path, 0o644)
        
        print(f"Successfully created krb5.conf at {output_path}")
        print(f"Configuration details:")
        print(f"  Realm: {realm}")
        print(f"  KDC Server: {fqdn} ({ip_address})")
        print(f"  Domain: {domain_name}")
        
    except PermissionError:
        print(f"Error: Permission denied. You may need to run this script with sudo to write to {output_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error creating krb5.conf: {e}")
        sys.exit(1)


def validate_inputs(fqdn, domain_name, ip_address):
    """
    Basic validation of input parameters.
    
    Args:
        fqdn (str): Fully Qualified Domain Name
        domain_name (str): Domain name
        ip_address (str): IP address
    
    Returns:
        bool: True if inputs are valid
    """
    import re
    
    # Basic FQDN validation
    fqdn_pattern = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    )
    if not fqdn_pattern.match(fqdn):
        print(f"Error: Invalid FQDN format: {fqdn}")
        return False
    
    # Basic domain name validation
    domain_pattern = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z]{2,}$'
    )
    if not domain_pattern.match(domain_name):
        print(f"Error: Invalid domain name format: {domain_name}")
        return False
    
    # Basic IP address validation
    ip_pattern = re.compile(
        r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    )
    if not ip_pattern.match(ip_address):
        print(f"Error: Invalid IP address format: {ip_address}")
        return False
    
    return True


def main():
    """Main function to handle command line arguments and create krb5.conf"""
    
    parser = argparse.ArgumentParser(
        description='Generate /etc/krb5.conf file for Kerberos configuration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 krb5_conf.py dc01.mirage.htb mirage.htb 10.10.11.78
  python3 krb5_conf.py --output /tmp/krb5.conf kdc.mydomain.org mydomain.org 10.0.0.5
        """
    )
    
    parser.add_argument('fqdn', 
                       help='Fully Qualified Domain Name of the KDC server (e.g., dc1.mirage.htb)')
    parser.add_argument('domain_name', 
                       help='Domain name / realm (e.g., mirage.htb)')
    parser.add_argument('ip_address', 
                       help='IP address of the KDC server (e.g., 10.10.11.78)')
    parser.add_argument('-o', '--output', 
                       default='/etc/krb5.conf',
                       help='Output path for krb5.conf file (default: /etc/krb5.conf)')

    # Parse arguments
    args = parser.parse_args()
    
    # Validate inputs
    if not validate_inputs(args.fqdn, args.domain_name, args.ip_address):
        sys.exit(1)
    
    
    # Create the krb5.conf file
    create_krb5_conf(args.fqdn, args.domain_name, args.ip_address, args.output)


if __name__ == "__main__":
    main()
