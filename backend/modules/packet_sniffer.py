from scapy.all import sniff

def packet_sniffer(interface="eth0", count=10):
    packets = sniff(iface=interface, count=count)
    return [str(packet.summary()) for packet in packets]
