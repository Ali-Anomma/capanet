da=open("mesajlar.txt","a")
while True:
	mesaj=input("Mesajinizi yaziniz: ")
	da.write(mesaj+"\n")