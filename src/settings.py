LDAP_SERVER = "ldap.epfl.ch"
LDAP_BASE_DN = "o=epfl,c=ch"
LDAP_SEARCH_FILTER = '(&(description=*Laboratoire*)(objectClass=OrganizationalUnit))'
LDAP_ATTRIBUTES_TO_RETURN = ['cn', 'OU', 'unitManager', 'description']
OUTPUT_FILE = "../out/output.csv"
