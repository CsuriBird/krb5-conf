Have you ever struggled to create a krb5.conf file in the etc directory? Have you ever had difficulties in deciding whether you should use a single domain name or the FQDN? Then I hope that this simple Python script will help you.
It is especially useful if you are a CTF enthusiast and the NTLM mechanism is disabled when tackling an Active Directory, and the only way to log in is via Kerberos.
E.g., First you request a ticket/ccache file with Imapcket, export it, make sure it is in the system with klist, then issue the command kinit and type in the user's password.
After all of this, run this script, and then if port 5985 is open, you can log in with evil-winrm -i fqdn -r domain -k xxxx.ccache.
Enjoy it!
