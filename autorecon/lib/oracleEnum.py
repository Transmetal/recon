#!/usr/bin/env python3

import os
from sty import fg
from autorecon.lib import nmapParser
from subprocess import call
from autorecon.utils import config_parser


class OracleEnum:
    """OracleEnum Will Enumerate Oracle on it's default port of 1521. I've never seen oracle's vulnerable service running
    on different ports besides 1521 so the port is hard coded to avoid other oracle ports. Perhaps it would be best to eventually
    change this to have some logic in the nmapParser to also include other oracle ports. Time will tell."""

    def __init__(self, target):
        self.target = target
        self.processes = ""

    def OraclePwn(self):
        """OraclePwn will run a helper lib/oracle.sh bash script which will attempt to bruteforce
        Oracle if any valid SID's are found from the Scan() Functions results."""
        np = nmapParser.NmapParserFunk(self.target)
        np.openPorts()
        oracle_tns_ports = np.oracle_tns_ports
        if len(oracle_tns_ports) == 0:
            pass
        else:
            c = config_parser.CommandParser(f"{os.path.expanduser('~')}/.config/autorecon/config.yaml", self.target)
            oracle_pwn = f"""bash {c.getPath("oracle","oracleBrute")} {self.target}"""
            call(oracle_pwn, shell=True)

    def Scan(self):
        """This Scan() Function will run various oracle scanning tools and attempt to find
        valid SID's along with other useful information. The following tools will be used,
        Nmap, tnscmd10g, osscanner, and ODAT."""
        np = nmapParser.NmapParserFunk(self.target)
        np.openPorts()
        oracle_tns_ports = np.oracle_tns_ports
        if len(oracle_tns_ports) == 0:
            pass
        else:
            c = config_parser.CommandParser(f"{os.path.expanduser('~')}/.config/autorecon/config.yaml", self.target)
            if not os.path.exists(c.getPath("oracle", "oracleDir")):
                os.makedirs(c.getPath("oracle", "oracleDir"))
            print(fg.cyan + "Enumerating ORACLE, Running the following commands:" + fg.rs)
            # string_oracle_ports = ",".join(map(str, oracle_tns_ports))
            commands = []
            commands.append(c.getCmd("oracle", "nmapOracle"))
            commands.append(c.getCmd("oracle", "tnscmd10g", mode="ping"))
            commands.append(c.getCmd("oracle", "tnscmd10g", mode="version"))
            commands.append(c.getCmd("oracle", "oscanner"))
            commands.append(c.getCmd("oracle", "odatTNS", mode="ping"))
            commands.append(c.getCmd("oracle", "odatTNS", mode="version"))
            commands.append(c.getCmd("oracle", "odatTNS", mode="status"))
            self.processes = tuple(commands)
