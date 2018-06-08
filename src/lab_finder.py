from ldap3 import ALL, Connection, Server
import csv
import settings
import os


def get_longest_string(strings: list) -> str:
    """Returns the longest string of strings passed as parameter"""
    return max(strings, key=len)


def reverse_dn(dn: str) -> str:
    """
    Turns the LDAP DN of the entry into EPFL specific hierarchy

    e.g. ou=lc,ou=imx,ou=sti,o=epfl,c=ch -> EPFL STI IMX LC
    """
    return_value = ''

    for element in list(reversed(dn.split(','))):
        if element != 'c=ch':
            return_value += element.split('=')[1].upper()
            return_value += ' '

    return return_value.strip()


if __name__ == "__main__":
    LDAP_server = Server(settings.LDAP_SERVER, use_ssl=True, get_info=ALL)
    conn = Connection(LDAP_server, auto_bind=True)
    conn.search(settings.LDAP_BASE_DN, settings.LDAP_SEARCH_FILTER, attributes=settings.LDAP_ATTRIBUTES_TO_RETURN)

    # Finds the
    current_running_path = os.path.dirname(__file__)
    absolute_output_path = os.path.join(current_running_path, settings.OUTPUT_FILE)
    with open(settings.OUTPUT_FILE, 'w', newline='') as csvfile:
        entryWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for entry in conn.entries:
            full_lab_name = get_longest_string(entry.ou.values)
            short_lab_name = entry.cn.value.upper()
            epfl_path = reverse_dn(entry.entry_dn)

            entryWriter.writerow([epfl_path, short_lab_name, full_lab_name])
