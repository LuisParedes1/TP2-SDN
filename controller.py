from enum import Enum

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os

from pox.lib.addresses import IPAddr
import pox.lib.packet as pkt

import json

log = core.getLogger()

class NetworkProtocols(Enum):
    TCP = pkt.ipv4.TCP_PROTOCOL
    UDP = pkt.ipv4.UDP_PROTOCOL

#EventMixin -> Clase generica que levanta eventos en pox
class Firewall(EventMixin) :
    def __init__(self):
        #Se queda escuchando al componente central, escucho todos los switches
        self.listenTo(core.openflow)
        self.config = self.load_config("rules.json")

    #Se establecio conexion con un switch
    def _handle_ConnectionUp(self, event):
        #Cada evento tiene un dpid, usando mininet y pox a la vez, el dpif corresponde con
        #el numero de switch que asigna mininet
        if event.dpid == self.config["firewall_switch"]:
            log.debug("Firewall switch: {}".format(dpidToStr(event.dpid)))
            for rule in self.config["rules"]:
                self.apply_rule(event, rule["rule"])
                log.debug("Rule: {} was installed on firewall switch".format(rule["name"]))

    def apply_rule(self, event, rule):
        #Creo la estructura que me permite indicar los campos del header con los cual matchear
        match = of.ofp_match()

        Firewall.set_header_matching_parameters(match, rule)

        #Creo el mensaje que le indica la flow table a un switch
        flow_mod_msg = of.ofp_flow_mod()
        #Le paso las reglas 
        flow_mod_msg.match = match

        #OBS: Al no indicarse ninguna accion, se defaultea a dropear el paquete, pero si se quiere ser
        #mas explicito se tiene que hacer lo siguiente:
        #action = of.ofp_action_output(port=of.OFPP_NONE)
        #flow_mod_msg.actions.append(action)

        #Cada evento tiene un objeto conection asociado que hace referencia al datapath (switch)
        #correspondiente, lo uso para enviar el mensaje acerca de las nuevas reglas
        event.connection.send(flow_mod_msg)

    def set_header_matching_parameters(match, rule):
        if "ip_type" in rule:
            match.dl_type = pkt.ethernet.IP_TYPE if rule["ip_type"] == "ipv4" else pkt.ethernet.IPV6_TYPE

        if "mac_src" in rule:
            match.dl_src = EthAddr(rule["mac_src"])

        if "mac_dst" in rule:
            match.dl_dst = EthAddr(rule["mac_dst"])

        if "protocol" in rule:
            if rule["protocol"] == "tcp":
                match.nw_proto = pkt.ipv4.TCP_PROTOCOL
            elif rule["protocol"] == "udp":
                match.nw_proto = pkt.ipv4.UDP_PROTOCOL

        if "src_ip" in rule:
            match.nw_src = IPAddr(rule["src_ip"])

        if "dst_ip" in rule:
            match.nw_dst = IPAddr(rule["dst_ip"])

        if "src_port" in rule:
            match.tp_src = rule["src_port"]
        
        if "dst_port" in rule:
            match.tp_dst = rule["dst_port"]


    def load_config(self, config_file):
        with open(config_file, "r") as f:
            config = json.load(f)
        return config

def launch():
    #Registra un nuevo componente el core
    core.registerNew(Firewall)
