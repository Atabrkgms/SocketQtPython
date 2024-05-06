import socket
import io
import base64
import cv2
import numpy as np

# Bölgelerin koordinatları
regions ={
        "1.bolge": (30, 58, 77, 104),
        "2.bolge": (31, 134, 75, 179),
        "3.bolge": (31, 208, 77, 254),
        "4.bolge": (32, 286, 77, 330),
        "5.bolge": (50, 384, 89, 422),
        "6.bolge": (94, 127, 120, 259), #(107, 127, 119, 259),
        "7.bolge": (195, 38, 345, 60),  #(194, 48, 340, 60),
        "8.bolge": (211, 372, 366, 395),
        "9.bolge": (498, 0, 551, 60),   #(501, 7, 544, 48),
        "10.bolge": (502, 135, 542, 176),
        "11.bolge": (506, 192, 539, 208),
        "12.bolge": (120, 59, 447, 321),
        "13.bolge": (325, 144, 475, 240), 
        "14.bolge": (216, 240, 326, 370), 
        "15.bolge": (120, 141, 216, 240), 
        "16.bolge": (216, 60, 325, 144) 
    } 

# Şablon resimlerin dosya yolları
template_paths = ["/home/ubuntu/Desktop/icidoluyildiz.png", "/home/ubuntu/Desktop/sagbosok.png","/home/ubuntu/Desktop/elma.png","/home/ubuntu/Desktop/avakado.png","/home/ubuntu/Desktop/cizgisembol.png","/home/ubuntu/Desktop/icidolukalp.png","/home/ubuntu/Desktop/iciboskalp.png","/home/ubuntu/Desktop/caprazcubuk.png","/home/ubuntu/Desktop/icibosdavutyildizi.png","/home/ubuntu/Desktop/uclusembol.png","/home/ubuntu/Desktop/tamdolubar.png","/home/ubuntu/Desktop/yarimdolubar.png","/home/ubuntu/Desktop/sagBuyukOk.png","/home/ubuntu/Desktop/solBuyukOk.png","/home/ubuntu/Desktop/yukariBuyukOk.png","/home/ubuntu/Desktop/asagiBuyukOk.png","/home/ubuntu/Desktop/barAsagiOk.png","/home/ubuntu/Desktop/barSagOk.png"]

#Sembol resimlerin adları ve dosya yolları
symbols_paths = [
        ("İci dolu yildiz","/Users/ataberkgumus/Desktop/symbolsAndSablons/icidoluyildiz.png"),
        ("Sag bos ok","/Users/ataberkgumus/Desktop/symbolsAndSablons/sagbosok.png"),
        ("Elma","/Users/ataberkgumus/Desktop/symbolsAndSablons/elma.png"),
        ("Avakado","/Users/ataberkgumus/Desktop/symbolsAndSablons/avakado.png"),
        ("Ici dolu kalp","/Users/ataberkgumus/Desktop/symbolsAndSablons/icidolukalp.png"),
        ("Ici bos kalp","/Users/ataberkgumus/Desktop/symbolsAndSablons/iciboskalp.png"),
        ("Capraz cubuk","/Users/ataberkgumus/Desktop/symbolsAndSablons/caprazcubuk.png"),
        ("Davut yildizi","/Users/ataberkgumus/Desktop/symbolsAndSablons/icibosdavutyildizi.png"),
        ("Tam dolu bar","/Users/ataberkgumus/Desktop/symbolsAndSablons/tamdolubar.png"),
        ("Yarim dolu bar","/Users/ataberkgumus/Desktop/symbolsAndSablons/yarimdolubar.png"),
        ("Sag buyuk ok","/Users/ataberkgumus/Desktop/symbolsAndSablons/sagBuyukOk.png"),
        ("Sol buyuk ok","/Users/ataberkgumus/Desktop/symbolsAndSablons/solBuyukOk.png"),
        ("Yukari buyuk ok", "/Users/ataberkgumus/Desktop/symbolsAndSablons/yukariBuyukOk.png"),
        ("Asagi buyuk ok","/Users/ataberkgumus/Desktop/symbolsAndSablons/asagiBuyukOk.png"),
        ("Bar asagi ok","/Users/ataberkgumus/Desktop/symbolsAndSablons/barAsagiOk.png"),
        ("Bar sag ok", "/Users/ataberkgumus/Desktop/symbolsAndSablons/barSagOk.png")             
]

# Bölgelerde sembol tespiti yapan fonksiyon
def find_symbol_in_region(image_path, template_paths, detected_symbol, region):

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    sift = cv2.SIFT_create()

    bf = cv2.BFMatcher()

    tespit_edilen_semboller = {}  # Tespit edilen sembollerin koordinatlarını saklamak için bir sözlük

    en_yakin_eslesme = None
    en_dusuk_mesafe = float("inf")

    bolge_resim = image[region[1]:region[3], region[0]:region[2]]
    kp1, des1 = sift.detectAndCompute(bolge_resim,None)
    for sembol_name, sembol_path in template_paths:
        sembol = cv2.imread(sembol_path,0)
        kp2, des2 = sift.detectAndCompute(sembol,None)
        if des2 is None:
            continue
        eslesmeler = bf.knnMatch(des1,des2,k=2)
        for m,n in eslesmeler:
            if m.distance < 0.73*n.distance:
                mesafe = m.distance
                if mesafe < en_dusuk_mesafe:
                    en_dusuk_mesafe = mesafe
                    en_yakin_eslesme = sembol_name
                    if en_yakin_eslesme == detected_symbol:
                        return True
                    
    if en_yakin_eslesme == detected_symbol:
        return True
    else:
        return False

#sunucu socket tarafının oluşturulması ve çalıştırılması 
server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = "/tmp/python_unix_socket"  # Sunucu adresi
server_socket.bind(server_address)
server_socket.listen(1)

print("Sunucu başlatıldı. İstemci bekleniyor...")

connection, address = server_socket.accept()

# Bölge numarasını al
bolgeNo = connection.recv(1024).decode()
print("Bölge numarası alındı:", bolgeNo)

# Bölge numarası başarılı bir şekilde alındı mesajını gönder
connection.send("Basarili Bolge".encode())

# Semblol adını al
sembolAdi = connection.recv(1024).decode()
print("Sembol adı alındı:", sembolAdi)

# Sembol adı başarılı bir şekilde alındı mesajını gönder
connection.send("Basarili Sembol".encode())

image_path = "/Users/ataberkgumus/Desktop/received_image.png"
# Resmi al
with open(image_path, "wb") as f:
    while True:
        imageData = connection.recv(1024)
        if not imageData:
            break
        f.write(imageData)

print("Resim alındı. Cevap gönderiliyor...")

result = find_symbol_in_region(image_path, symbols_paths, sembolAdi, regions[bolgeNo])

if result == true:
    connection.send("1".encode())
else:
    connection.send("0".encode())
# İstemciye cevap gönder

connection.close()
server_socket.close() # Socketi kapat

