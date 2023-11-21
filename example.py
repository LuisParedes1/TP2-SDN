from mininet.topo import Topo

class MyTopo(Topo):
    def __init__(self, n_switches=1, **opts):
        super(MyTopo, self).__init__(**opts)

        if n_switches < 1:
            raise Exception("ERROR: Number of switches must be at least 1")

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
        else:
            for i in range(2, n_switches + 1):
                s2 = self.addSwitch('switch_' + str(i))
                self.addLink(s1, s2)
                s1 = s2
            self.addLink(s2, h3)
            self.addLink(s2, h4)

topos = {'mytopo': MyTopo}


