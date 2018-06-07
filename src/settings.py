LDAP_SERVER = "ldap.epfl.ch"
LDAP_BASE_DN = "c=ch"
LDAP_SEARCH_FILTER = '(&(description=*Laboratoire*)(objectClass=OrganizationalUnit))'
LDAP_ATTRIBUTES_TO_RETURN = ['cn', 'OU']
OUTPUT_FILE = "../out/output.csv"
