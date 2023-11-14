from mininet.topo import Topo

class MyTopo( Topo ):
    def __init__( self ):
        # Initialize topology
        Topo.__init__( self )
        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        switch = self.addSwitch( 's1' )
        # Add links
        self.addLink( leftHost, switch )
        self.addLink( switch, rightHost )


topos = { 'mytopo': ( lambda: MyTopo() ) }

