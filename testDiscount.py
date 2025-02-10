import os
from dotenv import load_dotenv
import requests
import json
import random
import string
import time

# Cargar variables de entorno desde el archivo .env
load_dotenv()
SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY')
SHOPIFY_PASSWORD = os.getenv('SHOPIFY_PASSWORD')
SHOPIFY_SHOP_NAME = os.getenv('SHOPIFY_SHOP_NAME')
MY_ACCESS_TOKEN = os.getenv('MY_ACCESS_TOKEN')

print(f'SHOPIFY_API_KEY: {SHOPIFY_API_KEY}')
print(f'SHOPIFY_PASSWORD: {SHOPIFY_PASSWORD}')
print(f'SHOPIFY_SHOP_NAME: {SHOPIFY_SHOP_NAME}')
print(f'MY_ACCESS_TOKEN: {MY_ACCESS_TOKEN}')

previous_stock = {}

def generate_discount_code(length=15):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def create_initial_price_rules():
    discount_percentages = [5, 10, 15, 20]
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": MY_ACCESS_TOKEN
    }
    for discount_percentage in discount_percentages:
        price_rule_url = f"https://{SHOPIFY_SHOP_NAME}.myshopify.com/admin/api/2024-10/price_rules.json"
        price_rule_payload = {
            "price_rule": {
                "title": f"{discount_percentage}% off",
                "target_type": "line_item",
                "target_selection": "all",
                "allocation_method": "across",
                "value_type": "percentage",
                "value": f"-{discount_percentage}",
                "customer_selection": "all",
                "starts_at": "2023-01-01T00:00:00Z",
                "usage_limit": 1
            }
        }
        response = requests.post(price_rule_url, headers=headers, data=json.dumps(price_rule_payload))
        if response.status_code == 201:
            print(f'Regla de precio del {discount_percentage}% creada con éxito.')
        else:
            print(f'Error al crear la regla de precio del {discount_percentage}%.')
            print(response.json())

def create_discount_code(discount_percentage):
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": MY_ACCESS_TOKEN
    }
    price_rules_url = f"https://{SHOPIFY_SHOP_NAME}.myshopify.com/admin/api/2024-10/price_rules.json"
    response = requests.get(price_rules_url, headers=headers)
    if response.status_code == 200:
        price_rules = response.json()["price_rules"]
        price_rule = next((rule for rule in price_rules if rule["title"] == f"{discount_percentage}% off"), None)
        if price_rule:
            discount_code = generate_discount_code()
            discount_code_url = (
                f"https://{SHOPIFY_SHOP_NAME}.myshopify.com/admin/api/2024-10/"
                f"price_rules/{price_rule['id']}/discount_codes.json"
            )
            discount_code_payload = {
                "discount_code": {
                    "code": discount_code
                }
            }
            response = requests.post(discount_code_url, headers=headers, data=json.dumps(discount_code_payload))
            if response.status_code == 201:
                return response.json()["discount_code"]["code"]
            else:
                print('Error al crear el código de descuento.')
                print(response.json())
        else:
            print(f'No se encontró la regla de precio del {discount_percentage}%.')
    else:
        print('Error al obtener las reglas de precios.')
        print(response.json())
    return None

def get_price_rules():
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": MY_ACCESS_TOKEN
    }
    price_rules_url = f"https://{SHOPIFY_SHOP_NAME}.myshopify.com/admin/api/2024-10/price_rules.json"
    response = requests.get(price_rules_url, headers=headers)
    if response.status_code == 200:
        price_rules = response.json()["price_rules"]
        for rule in price_rules:
            print(rule["title"])
    else:
        print('Error al obtener las reglas de precios.')
        print(response.json())

def get_product_ids():
    product_ids = []
    products_url = f"https://{SHOPIFY_SHOP_NAME}.myshopify.com/admin/api/2024-10/products.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": MY_ACCESS_TOKEN
    }
    params = {"limit": 250}
    while products_url:
        response = requests.get(products_url, headers=headers, params=params)
        if response.status_code == 200:
            products = response.json()["products"]
            for product in products:
                if product["status"] == "active":
                    product_ids.append(product["id"])
            products_url = response.links.get('next', {}).get('url')
        else:
            print('Error al obtener los IDs de los productos.')
            print(response.text)
            break
    return product_ids

def get_inventory_item_ids(product_ids):
    inventory_items_map = {}
    for product_id in product_ids:
        product_url = f"https://{SHOPIFY_SHOP_NAME}.myshopify.com/admin/api/2024-10/products/{product_id}.json"
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": MY_ACCESS_TOKEN
        }
        response = requests.get(product_url, headers=headers)
        if response.status_code == 200:
            product = response.json()["product"]
            product_title = product.get("title", "Unknown Title")
            for variant in product["variants"]:
                inventory_item_ids = variant["inventory_item_id"]
                inventory_items_map[inventory_item_ids] = product_title
        else:
            print(f'Error al obtener items de inventario para el producto {product_id}.')
            print(response.text)
    return inventory_items_map

def check_stock_increase():
    product_ids = get_product_ids()
    if not product_ids:
        return []
    inventory_items_map = get_inventory_item_ids(product_ids)
    all_inventory_item_ids = list(inventory_items_map.keys())
    if not all_inventory_item_ids:
        return []

    stock_increases = []
    for i in range(0, len(all_inventory_item_ids), 100):
        batch_ids = all_inventory_item_ids[i:i+100]
        inventory_url = f"https://{SHOPIFY_SHOP_NAME}.myshopify.com/admin/api/2024-10/inventory_levels.json"
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": MY_ACCESS_TOKEN
        }
        params = {"inventory_item_ids": ",".join(map(str, batch_ids))}
        response = requests.get(inventory_url, headers=headers, params=params)
        if response.status_code == 200:
            try:
                inventory_levels = response.json()["inventory_levels"]
            except json.JSONDecodeError:
                print('Error al decodificar la respuesta JSON.')
                print(response.text)
                continue
            for level in inventory_levels:
                item_id = level["inventory_item_id"]
                available = level["available"]
                if item_id in previous_stock:
                    prev_available = previous_stock[item_id]
                    if available > prev_available:
                        product_name = inventory_items_map.get(item_id, "Unknown Title")
                        stock_increases.append((product_name, available - prev_available))
                previous_stock[item_id] = available
        else:
            print('Error al obtener los niveles de inventario.')
            print(response.text)
    return stock_increases

def monitor_stock_changes(interval=3600, callback=None):
    while True:
        stock_increases = check_stock_increase()
        if stock_increases and callback:
            callback(stock_increases)
        time.sleep(interval)