import sqlite3

kimlikNo = 0
parola = 0
bakiye = 0.0

#Yusuf Eren Taşkaya 201213069

baglan = sqlite3.connect('veritabani.db')
imlec = baglan.cursor()
imlec.execute("CREATE TABLE IF NOT EXISTS banka(TC int PRIMARY KEY,Parola int,Bakiye FLOAT)")


def Menu():
    while True:
        print("\nMenu")
        print("1-Bakiye Göster")
        print("2-Nakit Ekle")
        print("3-Nakit Çek")
        print("4-Nakit Gönder")
        print("5-Çıkış")

        menusecim = int(input("Menu işlemini seçiniz:"))
 
        if menusecim == 1:
            imlec.execute("SELECT * FROM banka WHERE TC = ? AND parola = ?",(kimlikNo,parola))
            rows = imlec.fetchall()
            print("Toplam bakiyeniz:",rows[0][2])
        elif menusecim == 2:
            eklenecekbakiye = float(input("Lutfen eklenecek bakiye degerini giriniz:"))
            if eklenecekbakiye < 0:
                print("Eksi değer olduğu için iptal edildi.")
                continue
            imlec.execute("SELECT * FROM banka WHERE TC = ? AND parola = ?",(kimlikNo,parola))
            rows = imlec.fetchall()
            bakiye = rows[0][2] + eklenecekbakiye
            imlec.execute("UPDATE banka SET Bakiye = ? WHERE TC = ? AND parola = ?",(bakiye,kimlikNo,parola))
        elif menusecim == 3:
            cekilecekbakiye = float(input("Lutfen çekilecek bakiye degerini giriniz:"))
            if cekilecekbakiye < 0:
                print("Eksi değer olduğu için iptal edildi.")
                continue
            imlec.execute("SELECT * FROM banka WHERE TC = ? AND parola = ?",(kimlikNo,parola))
            rows = imlec.fetchall()
            bakiye = rows[0][2] - cekilecekbakiye
            if bakiye < 0:
                print("Yetersiz bakiye.")
                print("Toplam bakiyeniz:",rows[0][2])
                continue
            imlec.execute("UPDATE banka SET Bakiye = ? WHERE TC = ? AND parola = ?",(bakiye,kimlikNo,parola))
        elif menusecim == 4:
            gonderilecekbakiye = float(input("Lutfen gönderilecek bakiye degerini giriniz:"))
            if gonderilecekbakiye < 0:
                print("Eksi değer olduğu için iptal edildi.")
                continue
            imlec.execute("SELECT * FROM banka WHERE TC = ? AND parola = ?",(kimlikNo,parola))
            rows = imlec.fetchall()
            bakiye = rows[0][2] - gonderilecekbakiye
            if bakiye < 0:
                print("Yetersiz bakiye.")
                print("Toplam bakiyeniz:",rows[0][2])
                continue
            
            gonderkimlikNo = int(input("Gönderilecek hesabın TC kimlik numarasını giriniz:"))

            imlec.execute("SELECT * FROM banka WHERE TC = ?",(gonderkimlikNo,))
            gonderhesapdizisi = imlec.fetchall()
            if len(gonderhesapdizisi) != 0 and kimlikNo != gonderkimlikNo:
                imlec.execute("UPDATE banka SET Bakiye = Bakiye + ? WHERE TC = ?",(gonderilecekbakiye,gonderkimlikNo))
                imlec.execute("UPDATE banka SET Bakiye = ? WHERE TC = ? AND parola = ?",(bakiye,kimlikNo,parola))
                print("Gönderim işlemi başarılı bir şekilde gerçekleşti.")
            else:
                print("Hesap bulunamadı ve iptal edildi.")
        elif menusecim == 5:
            baglan.commit()
            break
        else:
            print("Lütfen geçerli bir değer giriniz.")
        
        baglan.commit()


while True:
    #print("Lutfen tam sayi degerleri giriniz.")
    #print("Menü işlemlerine girdikten sonra tamamlamadan bitirmek için -1 değerini giriniz.")
    anaekransecim = int(input("\nAna Ekran\n1-Giriş\n2-Kayıt ol\n3-Çıkış\nYapmak istediğiniz seçeneği yazınız:"))
    if anaekransecim == 1:
        kimlikNo = int(input("\nLütfen giriş için TC kimlik numarasını giriniz:"))
        parola = int(input("Parolanızı giriniz:"))
        imlec.execute("SELECT * FROM banka WHERE TC = ? AND parola = ?",(kimlikNo,parola))
        rows = imlec.fetchall()
        if len(rows) != 0:
            Menu()
    elif anaekransecim == 2:
        kimlikNo = int(input("\nKayıt olmak TC kimlik numarasını giriniz:"))
        parola = int(input("Parolanızı giriniz:"))
        imlec.execute("INSERT INTO banka VALUES(?,?,0)",(kimlikNo,parola))
        Menu()
    elif anaekransecim == 3:
        break
    else:
        print("Lütfen geçerli bir değer giriniz.")


baglan.commit()
baglan.close()
