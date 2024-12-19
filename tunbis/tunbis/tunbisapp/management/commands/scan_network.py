import socket
import nmap
import openpyxl
import ipaddress
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Ağdaki cihazları tarar ve sonuçları Excel dosyasına kaydeder'

    def handle(self, *args, **kwargs):
        # Cihazın IP adresini al
        ip_address = self.get_ip_address()
        self.stdout.write(f"Bilgisayarınızın IP adresi: {ip_address}")

        # IP aralığını bul
        network = self.get_network_range(ip_address)
        self.stdout.write(f"Tarama yapılacak ağ aralığı: {network}")

        # Nmap tarayıcıyı başlat
        nm = nmap.PortScanner()

        # Nmap ile tarama yap
        self.stdout.write(f"Nmap taraması başlatılıyor: {network}")
        nm.scan(hosts=network, arguments="-sn")  # -sn: Ping taraması

        # Excel dosyasını oluştur
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["IP Adresi", "Cihaz İsmi", "Durum"])

        # Tarama sonuçlarını işleyin
        for host in nm.all_hosts():
            if nm[host].state() == "up":  # Eğer cihaz aktifse
                hostname = nm[host].hostname() if nm[host].hostname() else "Bulunamadı"
                ws.append([host, hostname, "Aktif"])
                self.stdout.write(f"Bulunan Cihaz: {host} - {hostname}")

        # Excel dosyasını kaydedin
        wb.save("nmap_tarama_sonuclari.xlsx")
        self.stdout.write(self.style.SUCCESS('Nmap taraması tamamlandı ve sonuçlar Excel dosyasına kaydedildi.'))

    def get_ip_address(self):
        """Cihazın IP adresini alır"""
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address

    def get_network_range(self, ip_address):
        """Cihazın IP adresinden ağ aralığını bulur"""
        # Ağ maskesi ile birlikte ağ aralığını oluşturmak için IPv4Network kullanın
        ip_obj = ipaddress.IPv4Address(ip_address)
        network = ipaddress.IPv4Network(f"{ip_address}/24", strict=False)  # /24 ağ maskesi
        return str(network.network_address)  # Örneğin 192.168.1.0 şeklinde dönecek
