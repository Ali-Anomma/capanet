#gerekli paketleri yukler.socket iletisim icin,select giris cikis islemleri icin beklemeyi saglar,sys uygulamadan cikmak gibi sistem fonksiyonlari icindir,datetime ise saati ve tarihi gosterir,thread sayesinde her kullanici icin bellekte ayri yer ayriilir,bu sayede bircok kullanici varken tek bir bellege yuklenip yavaslatmaz.
import socket
import select
import sys
import datetime
from thread import *
#sunucu ayarlari.AF INET adres belirtir,IP icin AF INET kullanacagiz. SOCK STREAM sayesinde bilgisayar surekli baglantilara bakmaya devam eder.
sunucu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sunucu.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
kullanici_listesi=[]
da=open("mesajlar.txt","a")
IP_adresi = str(raw_input("Sunucuyu baslatacaginiz IP adresini giriniz:" ))
port = int(input("Sunucuyu baslatacaginiz portu giriniz: "))
#IP adresi ve port belirtilen sunucuyu dinler.
sunucu.bind((IP_adresi, port))
sunucu.listen(100)
print("Sunucu baglandi")
def kullaniciparcacigi(baglanti,adres):
	kullanici_soket.send("Sohbete hosgeldin!")
	while True:
	#hata var mi diye kontrol ediyoruz
		try:	
			#1024 mb(1gb) hafiza kullanarak istemcinin gonderdigi mesaji aliyoruz.
			mesaj=baglanti.recv(1024)
			#eger mesaj dogru alinmissa yaziyoruz.mesaj bos degilse if'i tetikliyor.
			if mesaj:
				print("["+adres[0]+"] "+mesaj)
				gonderilecek_mesaj="["+adres[0]+"] "+mesaj
				da.write(gonderilecek_mesaj+" { "+str(datetime.datetime.now())+" }")
				#mesaji ayrica butun kullanicilara gonderiyoruz
				mesajgonder(gonderilecek_mesaj,baglanti)
			else:
				#hata cikmissa baglantiyi kaldir.mesela bir kullanicinin ayrilmasi durumunda kullanicinin kalmis verisini siler.
				cikar(baglanti)
		except:
		#hepsi tamamlandiktan sonra fonkisyonu bitir.
			continue
def mesajgonder(mesaj,baglanti):
	#listedeki tum kullanicilari kontrol eder.
	for kullanici in kullanici_listesi:
		#goneren kullanici haric herkese mesaji iletir.gonderen kullanici zaten gonderdigi mesaji gorebiliyor.
		if kullanici!=baglanti:
			try:
				kullanici.send(mesaj)
			except:
				#tekrardan mesajin hata vermesini kontrol eder ve veriyorsa yukaridaki gibi baglantiyi kaldirir.
				kullanici.close()
				kaldir(kullanici)
def kaldir(baglanti):
	if baglanti in kullanici_listesi:
		kullanici_listesi.remove(baglanti)
while True:
	#sunucuya baglanan istemciden adres bilgisi alip bunlari isliyoruz.
	kullanici_soket,kullanici_ip=sunucu.accept()
	kullanici_listesi.append(kullanici_soket)
	print(kullanici_ip[0]+" baglandi")
	#her kullanici icin yeni parcacik olusturuyoruz
	start_new_thread(kullaniciparcacigi(kullanici_soket,kullanici_ip))
kullanici_soket.close()
sunucu.close()