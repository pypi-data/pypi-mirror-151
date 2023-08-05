from .models import (PORT_MAPPING_DB, PORTS_TABLE)
from ..utils.databases import (
    create_db,
    create_table_in_db
)


def gen_junos_interfaces_list(int_number):
    """
    Generates list of interface names of Junos device.

    Input:
            int_number: maximum number of interfaces of emulated device
    Output:
            interface_list: list of available interface names
    """
    default_int_name = 'ge-0/0/'
    interface_list = []
    for i in range(int_number):
        interface_name = default_int_name+str(i)
        interface_list.append(interface_name)
    return interface_list


def get_interface(int_list):
    """
    Get interface from list of interface names.

    Input:
            int_list: list of interfaces
    Output:
            name of interface
    """
    return int_list.pop(0)


def create_port_map_db():
    """
    Create port mapping interface database (DB) and table in DB.
    """
    create_db(PORT_MAPPING_DB)
    table_values = {
        'po_interface': 'TEXT',
        'lo_interface': 'TEXT',
    }
    create_table_in_db(PORT_MAPPING_DB, PORTS_TABLE, table_values)
    return


def map_po_2_lo_configs(configs_list, port_map):
    """
    Maps configuration statements <configs_list> from Physical Object to Logical Object 
    (based on <port_map>).

    Input:
            configs_list: list of configuration statements from Physical Object
            port_map: list of tuples of port mapping (id, po_interface, lo_interface, ...)
    Output:
            configs_list: list of configuration statement to Logical Object
    """
    po_interfaces = []
    lo_interfaces = []
    for map in port_map['values']:
        po_interfaces.append(map[1])
        lo_interfaces.append(map[2])
    stat_pos = 0
    for statement in configs_list:
        change_statement = False
        po_int_pos = 0
        for int_name in po_interfaces:
            if int_name in statement:
                change_statement = True
                change_po_int = po_int_pos
            po_int_pos += 1
        if change_statement:
            configs_list[stat_pos] = configs_list[stat_pos].replace(
                po_interfaces[change_po_int], 
                lo_interfaces[change_po_int]
            )
        stat_pos += 1
    return configs_list