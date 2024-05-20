import requests
import json

url = 'https://maxmerter.com/index.php?route=api/wkrestapi/customer/getOrders'
payload = {
    "wk_token": "931a1bbe51a7eeb39f98c7b702cd4d8f"
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    orders = response.json()
    
    # JSON verisini bir dosyaya kaydetme
    with open('orders.json', 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=4)
        
    print("Veri 'orders.json' dosyasına kaydedildi.")
else:
    print(f"Hata: {response.status_code}, Mesaj: {response.text}")
