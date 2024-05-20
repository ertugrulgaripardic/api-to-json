import requests
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128

url = 'https://maxmerter.com/index.php?route=api/wkrestapi/customer/getOrders'
payload = {
    "wk_token": "931a1bbe51a7eeb39f98c7b702cd4d8f"
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    
    order_list = []

    for order in data['orderData']:
        order_id = order['orderId']
        name = order['name']
        email = order['email']
        status = order['status']
        date_added = order['dateAdded']
        total = order['total']
        payment_address = order['orderDetails']['payment_address']
        payment_city = order['orderDetails']['payment_city']
        payment_zone = order['orderDetails']['payment_zone']
        payment_country = order['orderDetails']['payment_country']
        payment_method = order['orderDetails']['payment_method']
        shipping_address = order['orderDetails']['shipping_address']
        shipping_city = order['orderDetails']['shipping_city']
        shipping_zone = order['orderDetails']['shipping_zone']
        shipping_country = order['orderDetails']['shipping_country']
        shipping_method = order['orderDetails']['shipping_method']

        # Ürün bilgilerini işleme
        for product in order['orderDetails']['products']:
            product_id = product['product_id']
            product_name = product['name']
            product_quantity = product['quantity']
            product_price = product['price']
            product_total = product['total']
            seller_id = product['seller_id']
            seller_name = product['seller_name']

            order_list.append({
                'Order ID': order_id,
                'Name': name,
                'Email': email,
                'Status': status,
                'Date Added': date_added,
                'Total': total,
                'Payment Address': payment_address,
                'Payment City': payment_city,
                'Payment Zone': payment_zone,
                'Payment Country': payment_country,
                'Payment Method': payment_method,
                'Shipping Address': shipping_address,
                'Shipping City': shipping_city,
                'Shipping Zone': shipping_zone,
                'Shipping Country': shipping_country,
                'Shipping Method': shipping_method,
                'Product ID': product_id,
                'Product Name': product_name,
                'Product Quantity': product_quantity,
                'Product Price': product_price,
                'Product Total': product_total,
                'Seller ID': seller_id,
                'Seller Name': seller_name,
            })

    df = pd.DataFrame(order_list)

    for _, row in df.iterrows():
        c = canvas.Canvas(f"{row['Order ID']}.pdf", pagesize=letter)
        width, height = letter
        
        c.drawString(1 * inch, height - 1 * inch, f"Order ID: {row['Order ID']}")
        c.drawString(1 * inch, height - 1.5 * inch, f"Name: {row['Name']}")
        c.drawString(1 * inch, height - 2 * inch, f"Email: {row['Email']}")
        c.drawString(1 * inch, height - 2.5 * inch, f"Status: {row['Status']}")
        c.drawString(1 * inch, height - 3 * inch, f"Date Added: {row['Date Added']}")
        c.drawString(1 * inch, height - 3.5 * inch, f"Total: {row['Total']}")
        c.drawString(1 * inch, height - 4 * inch, f"Payment Address: {row['Payment Address']}")
        c.drawString(1 * inch, height - 4.5 * inch, f"Payment City: {row['Payment City']}")
        c.drawString(1 * inch, height - 5 * inch, f"Payment Zone: {row['Payment Zone']}")
        c.drawString(1 * inch, height - 5.5 * inch, f"Payment Country: {row['Payment Country']}")
        c.drawString(1 * inch, height - 6 * inch, f"Payment Method: {row['Payment Method']}")
        c.drawString(1 * inch, height - 6.5 * inch, f"Shipping Address: {row['Shipping Address']}")
        c.drawString(1 * inch, height - 7 * inch, f"Shipping City: {row['Shipping City']}")
        c.drawString(1 * inch, height - 7.5 * inch, f"Shipping Zone: {row['Shipping Zone']}")
        c.drawString(1 * inch, height - 8 * inch, f"Shipping Country: {row['Shipping Country']}")
        c.drawString(1 * inch, height - 8.5 * inch, f"Shipping Method: {row['Shipping Method']}")
        c.drawString(1 * inch, height - 9 * inch, f"Product Name: {row['Product Name']}")
        c.drawString(1 * inch, height - 9.5 * inch, f"Product Quantity: {row['Product Quantity']}")
        c.drawString(1 * inch, height - 10 * inch, f"Product Price: {row['Product Price']}")
        c.drawString(1 * inch, height - 10.5 * inch, f"Product Total: {row['Product Total']}")
        c.drawString(1 * inch, height - 11 * inch, f"Seller ID: {row['Seller ID']}")
        c.drawString(1 * inch, height - 11.5 * inch, f"Seller Name: {row['Seller Name']}")

        # Barkod ekleme
        barcode_value = row['Order ID']
        barcode = code128.Code128(barcode_value, barHeight=0.5*inch, barWidth=1.5)
        barcode.drawOn(c, 1 * inch, height - 12.5 * inch)

        c.save()

    print("Sipariş etiketleri oluşturuldu.")
else:
    print(f"Hata: {response.status_code}, Mesaj: {response.text}")
