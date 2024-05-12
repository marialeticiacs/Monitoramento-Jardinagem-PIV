def do_connect(ssid, key):
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando à rede Wi-Fi...')
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            pass
        print('Conexão estabelecida com sucesso!')

def collect_data():
    import dht
    import machine
    from machine import Pin, ADC
    import time
    
    # Configuração do sensor DHT11 para temperatura e umidade do ar
    dht11 = dht.DHT11(machine.Pin(4))
    dht11.measure()
    time.sleep(0.5)
    umidade_ar = dht11.humidity()
    temperatura = dht11.temperature()
    
    # Configuração do sensor de umidade do solo
    pin_umidade_solo = 35  # Suponha que o sensor de umidade do solo esteja conectado ao pino 32 (ADC)
    adc = ADC(Pin(pin_umidade_solo))
    umidade_solo = adc.read()  # Faça a leitura analógica do sensor de umidade do solo
    
    return temperatura, umidade_ar, umidade_solo

def send_data_to_thingspeak(temperatura, umidade_ar, umidade_solo):
    import urequests
    import time
    
    HTTP_HEADERS = {'Content-Type': 'application/json'}
    THINGSPEAK_WRITE_API_KEY = "ILF0J9NXSSUGFAZ0"
    UPDATE_TIME_INTERVAL = 5000  # em ms
    last_update = time.ticks_ms()
    
    while True:
        if time.ticks_ms() - last_update >= UPDATE_TIME_INTERVAL:
            json_readings = {'field1': temperatura, 'field2': umidade_ar, 'field3': umidade_solo}
            request = urequests.post('http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json=json_readings, headers=HTTP_HEADERS)
            request.close()
            print('Dados enviados para ThingSpeak:', json_readings)
            print('Aguardando 5 minutos...')
            last_update = time.ticks_ms()
            time.sleep(300)  # Dorme por 5 minutos antes de enviar novamente

def send_data_to_mongodb(temperatura, umidade_ar, umidade_solo):
    from pymongo import MongoClient
    import time
    
    # Configuração da conexão com o MongoDB Atlas
    uri = "mongodb+srv://marialeticia:ml2005@cluster-piv.rr2y51m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-PIV"
    client = MongoClient(uri)

    # Escolha o banco de dados e a coleção
    db = client["DB_PIV"]
    collection = db["MONITORA"]

    while True:
        json_readings = {
            'temperatura': temperatura,
            'umidade_ar': umidade_ar,
            'umidade_solo': umidade_solo,
            'timestamp': time.time()  # Adicionando um carimbo de data/hora para o registro
        }

        try:
            # Inserindo os dados na coleção MongoDB
            collection.insert_one(json_readings)
            print('Dados enviados para MongoDB:', json_readings)
        except Exception as e:
            print('Erro ao enviar dados para MongoDB:', e)

        print('Aguardando 5 minutos...')
        time.sleep(300)  # Dorme por 5 minutos antes de enviar novamente



do_connect('NET_NET', '12345678')
temperatura, umidade_ar, umidade_solo = collect_data()
send_data_to_thingspeak(temperatura, umidade_ar, umidade_solo)
send_data_to_mongodb(temperatura, umidade_ar, umidade_solo)
