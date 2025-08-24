<p>Have you ever struggled to create a krb5.conf file in the etc directory? Have you ever had difficulties deciding whether you should use a single domain name or the FQDN? Then I hope that this simple Python script will help you.</p> 

<p>It is handy if you are a CTF enthusiast and the <strong>NTLM mechanism is disabled when tackling an Active Directory</strong>, and the only way to <strong>log in is via Kerberos</strong>.</p>
<p>For example, first, you request a ticket/ccache file with <code>Imapcket</code>, <code>export</code> it, and ensure it is in the system using <code>klist</code>. Then, issue the command <code>kinit</code> and enter the user's password.</p>
<p>After all of this, run this script, <code>python3 krb5_conf.py <<fqdn>> <<domain_name>> <<ip_address>></code> and then if port 5985 is open, you can log in with <code>evil-winrm -i fqdn -r domain -k xxxx.ccache</code>.</p>
<p>Enjoy it!</p>

 
