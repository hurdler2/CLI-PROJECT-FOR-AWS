from flask import Flask
from redis import Redis
import os

app = Flask(__name__)

# REDIS_HOST ortam değişkeninden Redis host adresini al.
# Varsayılan olarak 'redis' kullanırız, çünkü Docker Compose içindeki servis adı bu olacak.
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_client = Redis(host=redis_host, port=6379) # Redis varsayılan portu

@app.route('/')
def hello():
    try:
        visits = redis_client.incr('visits') # Redis'te ziyaret sayısını artır
        return f'Merhaba Docker Compose! Bu sayfayı {visits} kez ziyaret ettin.'
    except Exception as e:
        return f'Redis bağlantı hatası: {e}. Lütfen Redis servisinin çalıştığından emin olun.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) # debug=True geliştirme için uygundur
