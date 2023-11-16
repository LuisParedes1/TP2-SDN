from enum import Enum
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
import json

from pox.lib.addresses import IPAddr
import pox.lib.packet as pkt

log = core.getLogger()

class NetworkProtocols(Enum):
    TCP = pkt.ipv4.TCP_PROTOCOL
    UDP = pkt.ipv4.UDP_PROTOCOL


class Firewall(EventMixin) :
    def __init__(self):
        self.listenTo(core.openflow)
        config = self.load_configuration("rules.json")
        self.firewall_switch = config["firewall_switch"]
        self.rules = config["rules"]


    def _handle_ConnectionUp(self, event):
        if event.dpid == self.firewall_switch:
            for rule in self.rules:
                self.apply_rule(event, rule["rule"])
                log.debug("Firewall Rule: %s installed on Switch %s", rule["name"], dpidToStr(event.dpid))

    def apply_rule(self, event, rule):
        match = of.ofp_match()

        if "data_link" in rule:
            self.process_data_link_rule(rule["data_link"], match)
        if "network" in rule:
            self.process_network_rule(rule["network"], match)
        if "transport" in rule:
            self.process_transport_rule(rule["transport"], match)

        flow_mod_msg = of.ofp_flow_mod()
        flow_mod_msg.match = match
        event.connection.send(flow_mod_msg)

    def process_data_link_rule(self, rule, match):
        if "ip_type" in rule:
            match.dl_type = pkt.ethernet.IP_TYPE if rule["ip_type"] == "ipv4" else pkt.ethernet.IPV6_TYPE
        if "mac" in rule:
            match.dl_src = EthAddr(rule["mac"]["src"]) if "src" in rule["mac"] else None
            match.dl_dst = EthAddr(rule["mac"]["dst"]) if "dst" in rule["mac"] else None

    def process_network_rule(self, rule, match):
        protocol_enum = NetworkProtocols[rule["protocol"].upper()]
        match.nw_proto = protocol_enum.value if protocol_enum else None

        match.nw_src = IPAddr(rule["src_ip"]) if "src_ip" in rule else None
        match.nw_dst = IPAddr(rule["dst_ip"]) if "dst_ip" in rule else None

    def process_transport_rule(self, rule, match):
        match.tp_src = rule["src_port"] if "src_port" in rule else None
        match.tp_dst = rule["dst_port"] if "dst_port" in rule else None

    def load_configuration(self, config_file):
        with open(config_file, "r") as f:
            config = json.load(f)
        return config

def launch():
    core.registerNew(Firewall)
