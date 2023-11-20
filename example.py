from mininet.topo import Topo
import json

class MyTopo(Topo):
    def __init__(self, n_switches=1, **opts):
        super(MyTopo, self).__init__(**opts)
        config = self.load_configuration("rules.json")

        if n_switches < 1:
            raise Exception("number of switches must be at least 1")

        cantidad_switches_seteados = config["firewall_switch"]

        if n_switches < cantidad_switches_seteados:
            raise Exception("number of switches must be at least " + str(cantidad_switches_seteados))
        
        h1 = self.addHost('host_1')
        h2 = self.addHost('host_2')
        h3 = self.addHost('host_3')
        h4 = self.addHost('host_4')

        s1 = self.addSwitch('switch_1')
        self.addLink(h1, s1)
        self.addLink(h2, s1)

        if n_switches == 1:
            self.addLink(h3, s1)
            self.addLink(h4, s1)
            return
        else:
            for i in range(2, n_switches + 1):
                s2 = self.addSwitch('switch_' + str(i))
                self.addLink(s1, s2)
                s1 = s2
            self.addLink(s2, h3)
            self.addLink(s2, h4)

    def load_configuration(self, config_file):
        with open(config_file, "r") as f:
            config = json.load(f)
        return config
    
topos = {'mytopo': MyTopo}


