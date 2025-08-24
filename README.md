Have you ever struggled to create a krb5.conf file in the etc directory? Have you ever had difficulties deciding whether you should use a single domain name or the FQDN? Then I hope that this simple Python script will help you.
It is handy if you are a CTF enthusiast and the NTLM mechanism is disabled when tackling an Active Directory, and the only way to log in is via Kerberos.
For example, first, you request a ticket/ccache file with Imapcket, export it, and ensure it is in the system using klist. Then, issue the command kinit and enter the user's password.
After all of this, run this script, and then if port 5985 is open, you can log in with evil-winrm -i fqdn -r domain -k xxxx.ccache.
Enjoy it!


<code> evil-winrm -i fqdn -r domain -k xxxx.ccache</code>
