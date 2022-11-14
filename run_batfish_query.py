#!/usr/bin/env python3

# Batfish Documentation
# https://batfish.readthedocs.io/en/latest/notebooks/interacting.html

import pandas as pd
from pybatfish.client.session import Session
from pybatfish.datamodel import *
from pybatfish.datamodel.answer import *
from pybatfish.datamodel.flow import *

bf = Session(host="localhost")
bf.set_network('example_dc')
SNAPSHOT_DIR = 'batfish'
bf.init_snapshot(SNAPSHOT_DIR, name='configs', overwrite=True)
bf.set_network('example_dc')
bf.set_snapshot('configs')

# Query Examples

def Init_issues():
    # Find init issues
    result = bf.q.initIssues().answer()
    return result

def Parsed_files_status():
    # Getting status of parsed files
    result = bf.q.fileParseStatus().answer().frame()
    return result

def Routing_tables():
    # Return routing tables
    result = bf.q.routes().answer().frame()
    return result

def Interface_property():
    # Fetch specific properties of specific interfaces
    default_interface = "loopback"
    interface = input(f"Enter interface name [{default_interface}]: ") or default_interface
    result = bf.q.interfaceProperties(interfaces=f"/{interface}/", properties="Bandwidth,VRF,Primary_Address").answer().frame()
    return result

def Undefined_config():
    # List references to undefined structures
    # Common indicators of buggy configurations include references to structures that are not defined anywhere
    result = bf.q.undefinedReferences().answer().frame()
    return result

def Run_traceroute():
    # Run a traceroute from a host to a remote network host
    default_from_host = "edge_srx_r1"
    from_host = input(f"Enter hostname to ping from [{default_from_host}]: ") or default_from_host
    default_to_network = "10.1.2.2/24"
    to_network = input(f"Enter destination network IP and mask [{default_to_network}]: ") or default_to_network
    result = bf.q.traceroute(startLocation=from_host, headers=HeaderConstraints(dstIps=to_network)).answer().frame()
    # Display results using customizations to handle large string values
    return result

def Get_all_routes():
    default_nodes = "edge_srx_r1"
    nodes = input(f"Enter hostname [{default_nodes}]: ") or default_nodes
    default_network = "10.100.202.0/24"
    network = input(f"Enter network and mask [{default_network}]: ") or default_network
    # Get all routes for a network e.g.: 90.90.90.0/24 on core routers
    result = bf.q.routes(nodes=nodes, network=network).answer().frame()
    return result

def query():
    while True:
        list_menu = [
            "Init_issues",
            "Parsed_files_status",
            "Routing_tables",
            "Interface_property",
            "Undefined_config",
            "Run_traceroute",
            "Get_all_routes"
        ]
        print("-"*42)
        for index, option in enumerate(list_menu, start=1):
            print(f"[{index}]", option)
        print("[0] Exit script")
        choice = int(input(f"Select a number associated to an option: "))
        print("-"*42)
        if choice == 0:
            exit()
        try:
            result = eval(f"{list_menu[choice-1]}()")
            print(result)
        except Exception as e:
            print(e)

query()
