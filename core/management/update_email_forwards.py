# Virtual alias file syntax:
# email, space, email, (space, email, space, email,) newline, (repeat)
# Example:
# groep@arenbergorkest.be 	jef@gmail.com jos@hotmail.com
# jef@arenbergokest.be 		jef@gmail.com

# Catchall alias email = '@arenbergorkest.be'

from email_aliases import aliases

c = '' # New content of postfix virtual aliases file
for alias in aliases:
	c += '{} {}\n'.format(alias.email+'@arenbergorkest.be', ' '.join(alias.destinations))


from subprocess import call

VIRTUAL_ALIAS_FILE = '/etc/postfix/virtual'
with open(VIRTUAL_ALIAS_FILE, 'w') as f:
	f.write(c)
call(['sudo', 'postmap', VIRTUAL_ALIAS_FILE])
