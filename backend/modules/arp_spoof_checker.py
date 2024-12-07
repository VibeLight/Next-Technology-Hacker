from scapy.all import ARP, sniff

def detect_arp_spoof():
    def arp_display(packet):
        if packet[ARP].op == 2:
            try:
                real_mac = getmacbyip(packet[ARP].psrc)
                response_mac = packet[ARP].hwsrc
                if real_mac != response_mac:
                    return f"ARP Spoofing Detected: {packet[ARP].psrc} - {response_mac}"
            except Exception:
                pass

    sniff(filter="arp", prn=arp_display, store=0, count=10)
