from ldap3 import ALL, Connection, Server
import csv
import settings
import os
from lab import Lab


def get_longest_string(strings: list) -> str:
    return max(strings, key=len)


def reverse_dn(dn: str) -> str:
    return_value = ''

    for element in list(reversed(dn.split(','))):
        if element != 'c=ch':
            return_value += element.split('=')[1].upper()
            return_value += ' '

    return return_value.strip()


def get_faculty_name(entry_dn):
    entry_dn = reverse_dn(entry_dn)
    return entry_dn.split(" ")[1]
    pass


def get_shortest_string(strings):
    return min(strings, key=len)


def get_professors(sciper):
    return_value = list();

    LDAP_server = Server(settings.LDAP_SERVER, use_ssl=True, get_info=ALL)
    conn = Connection(LDAP_server, auto_bind=True)
    conn.search(settings.LDAP_BASE_DN,
                '(uniqueIdentifier={})'.format(sciper),
                attributes=['sn', 'givenName'],
                size_limit=1)
    assert len(conn.entries) == 1
    for entry in conn.entries:
        if isinstance(entry.givenName.value, list):
            givenName = get_shortest_string(entry.givenName.value)
        else:
            givenName = entry.givenName.value

        if isinstance(entry.sn.value, list):
            sn = get_shortest_string(entry.sn.value)
        else:
            sn = entry.sn.value

        return "{} {}".format(givenName, sn)


if __name__ == "__main__":
    labs = list()

    LDAP_server = Server(settings.LDAP_SERVER, use_ssl=True, get_info=ALL)
    conn = Connection(LDAP_server, auto_bind=True)
    conn.search(settings.LDAP_BASE_DN, settings.LDAP_SEARCH_FILTER, attributes=settings.LDAP_ATTRIBUTES_TO_RETURN)

    for entry in conn.entries:
        lab = Lab()
        lab.name = entry.cn.value.upper()
        lab.description = get_longest_string(entry.ou.values)
        lab.url = "https://{}.epfl.ch".format(entry.cn.value)
        lab.faculties=get_faculty_name(entry.entry_dn)
        lab.professors = get_professors(entry.unitManager.value)

        labs.append(lab)

    # Finds the
    current_running_path = os.path.dirname(__file__)
    absolute_output_path = os.path.join(current_running_path, settings.OUTPUT_FILE)
    with open(settings.OUTPUT_FILE, 'w', newline='') as csvfile:
        entryWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for lab in labs:
            full_lab_name = lab.description
            short_lab_name = lab.name.upper()
            epfl_path = "" #reverse_dn(entry.entry_dn)

            entryWriter.writerow([epfl_path, short_lab_name, full_lab_name])
