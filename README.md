<p>Have you ever struggled to create the <strong>krb5.conf</strong> file in the etc directory? Have you ever had difficulties deciding whether you should use a single domain name or the FQDN? Then I hope that this simple Python script will help you.</p> 

<p>It is handy if you are a CTF enthusiast and the <strong>NTLM mechanism is disabled when tackling an Active Directory</strong>, and the only way to <strong>login is via Kerberos</strong>.</p>
<p>For example, first, you request a ticket/ccache file with <code>Impacket</code>, <code>export</code> it, and ensure it is in the system using <code>klist</code>.</p>
<p>Then run this script, <code>python3 krb5_conf.py fqdn domain_name ip_address </code>, and issue the command <code>kinit</code> and enter the user's password. If port 5985 is open, you can log in with <code>evil-winrm -i fqdn -r domain (-k xxxx.ccache)</code>.</p>
<p>Enjoy it!</p>
<h2>Example</h2>

 


https://github.com/user-attachments/assets/e4c41532-47c0-4a81-b035-ee0b39604162

