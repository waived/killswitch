
   ////////////////////////////////////
  /// MAC FLOODING/SPOOFING ATTACK ///
 ////////////////////////////////////

Overview:
    The program "KillSwitch" simulates a MAC Flooding (aka: MAC Spoofing) attack
    on a switched network. The idea of this attack is that the attacker will
    generate a large overhead of Ethernet Frames. Each frame contains a randomly
    generated (spoofed) MAC address.

    Network Switches have something called a "MAC Table" which stores information
    about the MAC Addresses/Ethernet-interfaces belonging to connected devices
    on a network.
    
    The idea is simple: overload the MAC Table with a barrage of spoofed MAC
    addresses until the table cannot hold anymore. At this point, the switch
    will go into a Broadcast-Mode and any time it receives data from a device,
    instead of switching it to the recipient device, it send the data to ALL
    devices connected to the switch.
