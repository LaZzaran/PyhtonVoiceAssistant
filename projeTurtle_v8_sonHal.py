import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import time
import webbrowser
import requests
import turtle
import datetime
import json
from bs4 import BeautifulSoup
import pyaudio
import google.generativeai as genai
import api_keys
import subprocess

api_keyim =api_keys.gemini_api_keyim 
model_id = api_keys.model_id
haber_apikey=api_keys.haber_apikey
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

recognizer = sr.Recognizer()


def textWrite(text):
    turtle.clear()
    turtle.write(text, font=("Arial", 20, "normal"), align="center")


def ses_tani():

    with sr.Microphone() as source:
        textWrite("Lazzaran başlatılıyor...")
        textWrite("Mikrofon kalibre ediliyor...")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        textWrite("Lazzaran() seni dinliyor")
        metinden_sese("Lazzaran seni dinliyor")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language='tr-TR')
            textWrite(f"Sen: {text}")
            return text
        except sr.UnknownValueError:
            textWrite("Ne dediğinizi anlayamadım.")
            metinden_sese("Ne dediğinizi anlayamadım.")
            return ""
        except sr.RequestError:
            textWrite("Servise erişilemiyor.")
            metinden_sese("Servise erişilemiyor.")
            return ""
        except sr.WaitTimeoutError:
            textWrite("Dinleme zaman aşımına uğradı.Lazzaran Kapanıyor.")
            metinden_sese("Dinleme zaman aşımına uğradı.Lazzaran Kapanıyor.")
            quit()
            

def gemini_ai_chatBot():

    genai.configure(
    api_key=api_keyim
    )
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])


    while(True):
        question = input("Sen: ")

        if(question.strip() ==' '):
            break
        #gemini burada cevap veriyor hem sesli hem metinden
        response = chat.send_message(question)
        textWrite(response)
        metinden_sese(response)
  

def bilgisayari_kapat():
    os.system("shutdown /s /t 1")

def metinden_sese(text):
    #Oluşturulan metni sese çevirir.
    tts = gTTS(text=text, lang='tr')
    tts.save("response.mp3")
    pygame.mixer.init()
    try:
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    except pygame.error as e:
        textWrite(f"Ses oynatma hatası: {e}")
    finally:
        if pygame.mixer.get_init():
            pygame.mixer.quit()
        try:
            # Cevap için bir ses dosyası oluşturulup o ses dosyası başlatıldıktan sonra ,
            # ses dosyası siliniyor ta ki bir sonraki işlem başlayana kadar başka ses dosyası olmuyor

            os.remove("response.mp3")
        except PermissionError:
            textWrite("Dosya silinemedi, yeniden deniyor...")
            time.sleep(1)
            os.remove("response.mp3")

'''
    #Oluşturlan cevap metinden sese çevirme.
    #Bir ses dosyası üretip bu dosyayı kullanıp daha sonra bu dosyayı sildirme işlemleri.
    '''

'''def metinden_sese(text):
    
    tts = gTTS(text=text, lang='tr')
    tts.save("response.mp3")
    pygame.mixer.init()
    try:
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    except pygame.error as e:
        textWrite(f"Ses oynatma hatası: {e}")
    finally:
        if pygame.mixer.get_init():
            pygame.mixer.quit()
        try:
            os.remove("response.mp3")
        except PermissionError:
            textWrite("Dosya silinemedi, yeniden deniyor...")
            time.sleep(1)
            os.remove("response.mp3")
'''

def haberleri_getir():


    url = f"https://newsapi.org/v2/top-headlines?country=tr&apiKey={haber_apikey}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 'ok':
            articles = data['articles']
            for article in articles:
                title = article['title']
                textWrite(title)
                metinden_sese(title)
                time.sleep(2)
        else:
            metinden_sese("Haberler alınamadı.")
            textWrite("Haberler alınamadı.")
    except requests.exceptions.RequestException as e:
        textWrite(f"Hata oluştu: {e}")
        metinden_sese(f"Hata oluştu: {e}")


def not_yaz():
    desktop_path = "C:\\Users\\MONSTER\\OneDrive\\Masaüstü"
    
    # Dosya adını kullanıcıdan alma
    metinden_sese("Notunuzu hangi dosyaya kaydetmek istersiniz?")
    dosya_adi = ses_tani().strip()
    metinden_sese("Dosyanızın adı"+dosya_adi+" oldu dosyanıza neler kaydetmek istiyorsanız devam edin")
    # Dosya adı kontrolü ve dosyaya yazma işlemi
    if dosya_adi:
        dosya_yolu = os.path.join(desktop_path, f"{dosya_adi}.txt")
        metinden_sese(f"{dosya_adi} dosyasına notlarınız kaydediliyor.")
        while True:
            text = ses_tani()
            if "kaydet" in text.lower():
                break
            with open(dosya_yolu, 'a', encoding='utf-8') as f:
                f.write(text + '\n')
    else:
        metinden_sese("Dosya adı belirtilmedi, işlem iptal ediliyor.")
        return not_yaz


def hava_durumu(city):
    # İnternetten alınan hava durmu 
    try:
        url = f"https://wttr.in/{city}?format=%t+%C+%w"
        response = requests.get(url)
        
        if response.status_code == 200:
            weather_data = response.text.strip()
            textWrite(weather_data)
            return weather_data
        else:
            return "Hava durumu bilgisi alınamadı."
    
    except requests.exceptions.RequestException as e:
        return f"Hata oluştu: {e}"

# Varsayılan kullanım
city = 'Istanbul'
hava_durumu_bilgisi = hava_durumu(city)
textWrite(f"{city} hava durumu: {hava_durumu_bilgisi}")


def saat_tarih():
    #Şu anki tarih ve saati döndürür.
    now = datetime.datetime.now()
    tarih_saat = now.strftime("%d-%m-%Y %H:%M:%S")
    metinden_sese(f"Şu anki tarih ve saat: {tarih_saat}")
    textWrite(f"Şu anki tarih ve saat: {tarih_saat}")

def bilgisayari_yeniden_baslat():
    os.system("shutdown /r /t 1")

def clear():
    # os kütüphanesi ile terminal ekranını temizler ve asistanı çalıştırır
    os.system('cls' if os.name == 'nt' else 'clear')
    textWrite("Terminal temizlendi.")
    metinden_sese("Terminal Temizlendi.")

def verilen_cevabi_getir(user_input):

    if "Google'ı aç" in user_input or "Google aç" in user_input:
        webbrowser.open("https://www.google.com")
        return "Google açılıyor."
    
    elif "YouTube'u aç" in user_input:
        webbrowser.open("https://www.youtube.com")
        return "YouTube açılıyor."
    
    elif "uygulama aç" in user_input:
        #sadece istenen uygulamanın ismi söylenmeli yoksa farklı hatalar ile karşılaşılma olsılığı yüksek

        baslat=user_input.strip()+".exe"
        subprocess.Popen([baslat])


    elif "haber oku" in user_input.lower() or "güncel haberler" in user_input.lower():
        haberleri_getir()
        return "Güncel haberler okunuyor."

    elif "bilgisayarı kapat" in user_input.lower():
        bilgisayari_kapat()
        return "Bilgisayar kapatılıyor."
    
    elif "bilgisayarı yeniden başlat" or"restart bilgisayar" in user_input.lower():
        bilgisayari_yeniden_baslat()
        return "Bilgisayar yeniden başlatılıyor."
    
    elif "hava durumu" in user_input.lower():
        metinden_sese("Hangi şehir için hava durumu öğrenmek istersiniz?")
        city = ses_tani().strip()
        if city:
            hava_durumu_bilgisi = hava_durumu(city)
            metinden_sese(f"{city} hava durumu: {hava_durumu_bilgisi}")
            return f"{city} hava durumu bilgileri gösteriliyor."
        else:
            metinden_sese("Şehir bilgisi alınamadı.")
            return "Şehir bilgisi alınamadı."

    elif "saat kaç" in user_input.lower() or "tarih nedir" in user_input.lower():
        saat_tarih()
        return "Saat ve tarih bilgisi verildi."

    elif "not yaz" in user_input.lower():
        not_yaz()
        return "Notunuz kaydedildi."
    

    elif any(keyword in user_input.lower() for keyword in ["bul", "aç", "ne", "nedir", "ne demek", "kimdir"]):
        for keyword in ["bul", "aç", "ne", "nedir", "ne demek", "kimdir"]:
            if keyword in user_input.lower():
                query = user_input.replace(keyword, "").strip()
                if keyword == "kimdir":
                    query += " kimdir"
                elif keyword in ["ne", "nedir", "ne demek"]:
                    query += " nedir"
                url = f"https://www.google.com/search?q={query}"
                webbrowser.open(url)
                return f"{query} Google'da aranıyor."
            

    elif "hesap makinesini aç" in user_input.lower():

        subprocess.Popen(['calc.exe'])
    
    elif any(keyword in user_input.lower() for keyword in ["sohbet edelim", "konuşalım seninle biraz", "canım sıkıldı",
            "bir şeyler yapalım", "nasılsın", "neler yapıyorsun","lazzaran beni dinle","konuşmamız lazım"]):
        
        gemini_ai_chatBot()
       
    

    return "Bu komutu anlayamadım."



def main():
    turtle.setup(width=600, height=400)
    turtle.title("Lazzaran-A.M.Ş")
    turtle.hideturtle()
    turtle.speed(0)
    turtle.penup()
    
    textWrite("Lazzaran başlatıldı. Çıkmak için 'çık' veya 'çıkış' deyin.")
    while True:
        kullanci_girisi = ses_tani()
        if kullanci_girisi:
            if "çık" in kullanci_girisi.lower() or "çıkış" in kullanci_girisi.lower():
                textWrite("Çıkış yapılıyor...")
                metinden_sese("Çıkış yapılıyor...")
                break

            # generate_text_response fonksiyonunu kullanarak verilen cevabı buradan alınır 
            verilen_cevap = gemini_ai_chatBot(kullanci_girisi)
            
            # Eğer API'den bir yanıt alınamazsa, manuel komutları kontrol edilir
            if verilen_cevap is None:
                verilen_cevap = verilen_cevabi_getir(kullanci_girisi)

            if verilen_cevap:
                metinden_sese(verilen_cevap)
            else:
                metinden_sese("Bir hata oluştu, lütfen tekrar deneyin.")

            textWrite(f"Lazzaran : {verilen_cevap}")
            metinden_sese(verilen_cevap)





if __name__ == "__main__":
    main()
