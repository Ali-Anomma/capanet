#gerekli paketleri yukler.socket iletisim icin,select giris cikis islemleri icin beklemeyi saglar,sys uygulamadan cikmak gibi sistem fonksiyonlari icindir,datetime ise saati ve tarihi gosterir.
import socket
import select
import sys
import datetime
#sunucu ayarlari.AF INET adres belirtir,IP icin AF INET kullanacagiz. SOCK STREAM sayesinde bilgisayar surekli baglantilara bakmaya devam eder.
sunucu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_adresi = (str(raw_input("Baglanacaginiz sunucunun IP adresini giriniz: ")))
port = int(input("Baglanacaginiz sunucunun portunu giriniz: "))
#belirlenen adrese baglanir.
sunucu.connect((IP_adresi, port))
while True:
	#giren ve cikan veriler icin listeler olusturur.
	soket_listesi=[sys.stdin,sunucu]
	#okuma,yazma ve hata mesajlari icin ayri elemanlar olusturur.select komutu ile bilgisayari, okuyup yazana kadar bekletiyor.
	okuma_soketi,yazma_soketi, hata_soketi = select.select(soket_listesi,[],[])
	for soket in okuma_soketi:
	#tum listeye bakar ve sunucu verisini bulursa zaten gonderdigi mesaji ekrana yazdirir.
        	if soket == sunucu:
        		#1024 mb (1gb) bellek ayirarak mesaj gonderir.
        		mesaj = soket.recv(1024)
        		print (mesaj)
        	#eger listede yoksa girilen bilgiyi mesaj olarak belirleyip gonderir.
        	else:
        	    mesaj = sys.stdin.readline()
        	    sunucu.send(mesaj)
        	    sys.stdout.write("<Sen> ")
        	    sys.stdout.write(mesaj)
        	    #stdout ile belirlenmis tum veriyi yazdir.
        	    sys.stdout.flush()
sunucu.close()
