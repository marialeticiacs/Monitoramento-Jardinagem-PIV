import network
import dht
from machine import Pin, ADC
import time
import urequests

def do_connect(ssid, key):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando à rede Wi-Fi...')
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            pass
    print('Conexão estabelecida com sucesso!')
    print('Configurações de rede:', wlan.ifconfig())

def collect_data():
    dht11 = dht.DHT11(Pin(4))
    dht11.measure()
    umidade_ar = dht11.humidity()
    temperatura = dht11.temperature()
    
    pin_umidade_solo = 35
    adc = ADC(Pin(pin_umidade_solo))
    umidade_solo = adc.read()
    umidade_solo_percent = int((4095 - umidade_solo) * 100 / 2175) 
    print(umidade_solo_percent)
    return temperatura, umidade_ar, umidade_solo_percent

def send_data_to_api(temperatura, umidade_ar, umidade_solo_percent):
    API_URL = 'http://192.168.0.11:5002/api/receive_data'  # Substitua pelo endpoint correto da sua API
    json_readings = {
        'temperatura_ambiente': temperatura,
        'umidade_ar': umidade_ar,
        'umidade_solo': umidade_solo_percent,
        'planta_id': '1234',  # ID da planta
        'timestamp': time.time()
    }
    
    try:
        request = urequests.post(API_URL, json=json_readings)
        request.close()
        print('Dados enviados para API:', json_readings)
    except Exception as e:
        print('Erro ao enviar dados para API:', e)

def main():
    ssid = 'CLARO_2GBBAD1E'
    password = 'E7BBAD1E'
    do_connect(ssid, password)
    
    while True:
        temperatura, umidade_ar, umidade_solo_percent = collect_data()
        send_data_to_api(temperatura, umidade_ar, umidade_solo_percent)
        print('Aguardando 3 minutos...')
        time.sleep(180) 

if __name__ == "__main__":
    main()

