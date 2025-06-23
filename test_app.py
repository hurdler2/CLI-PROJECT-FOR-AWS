import os
from flask import Flask
from redis import Redis

# Flask uygulamasının import edilebilir olduğunu test edelim
try:
    from app import app as flask_app
    print("Flask uygulaması başarıyla import edildi.")
except ImportError:
    print("Hata: Flask uygulaması import edilemedi.")
    exit(1) # Hata olursa çık

# Redis bağlantısını test edelim (ortam değişkenini kullanarak)
redis_host = os.getenv('REDIS_HOST', 'localhost') # Test ortamı için localhost veya farklı bir Redis hostu
try:
    redis_client = Redis(host=redis_host, port=6379, decode_responses=True)
    redis_client.ping()
    print("Redis bağlantısı başarılı.")
except Exception as e:
    print(f"Hata: Redis bağlantısı kurulamadı. {e}")
    exit(1) # Hata olursa çık

print("Tüm temel testler başarıyla geçti!")
