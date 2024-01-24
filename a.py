import os
from ldap3 import Server, Connection, ALL, NTLM

# Define your domain controller and base DN here
DC_HOST = 'your-dc-host'
BASE_DN = 'DC=example,DC=com'

def get_user_realname():
    # Connect to the DC using NTLM authentication
    s = Server(DC_HOST, get_info=ALL)
    c = Connection(s, user='domain\\username', password='password', auto_bind=True)

    # Search for the user by their username
    filter_str = f'(sAMAccountName={os.getlogin()})'
    attributes = ['givenName', 'sn']
    c.search(BASE_DN, filter_str, attributes=attributes)

    # Extract the givenName and sn attributes and join them together
    result = c.entries[0].entry_to_dict()
    first_name = result['givenName'][0]
    last_name = result['sn'][0]
    realname = f"{first_name} {last_name}"

    return realname

if __name__ == "__main__":
    print("Real Name:", get_user_realname())