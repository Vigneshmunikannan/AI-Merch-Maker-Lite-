import logging
import requests

# ==== CONFIGURE THESE VALUES ====
SHOPIFY_URL = "replace_with_your_shop.myshopify.com"  # your Shopify store URL
SHOPIFY_ADMIN_TOKEN = ""  # your admin API token
IMAGE_PUBLIC_URL = "https://images.pexels.com/photos/4734304/pexels-photo-4734304.jpeg?_gl=1*1heta1w*_ga*MTg3MjA5MjE3NS4xNzU0MTE3ODEz*_ga_8JE65Q40S6*czE3NTQxMTc4MTIkbzEkZzEkdDE3NTQxMTc4OTYkajQ4JGwwJGgw"

# ==== PRODUCT DATA DEFINITIONS ====
PRODUCT_TITLE = "Vintage Sunset Graphic Tee"
PRODUCT_DESCRIPTION = (
    "A nostalgic blend of retro aesthetics and modern comfort. "
    "This eye-catching t-shirt features a vibrant sunset design that captures the essence of golden hour. "
    "Perfect for casual outings, music festivals, or adding a pop of color to your wardrobe."
)
PRODUCT_TAGS = ["vintage", "retro", "sunset", "graphic", "comfortable", "casual", "trendy"]
PRICE = "29.99"

# ==== SETUP LOGGING ====
logging.basicConfig(
    filename='shopify_upload.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def upload_to_shopify():
    url = f"https://{SHOPIFY_URL}/admin/api/2023-07/products.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ADMIN_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "product": {
            "title": PRODUCT_TITLE,
            "body_html": PRODUCT_DESCRIPTION,
            "tags": ", ".join(PRODUCT_TAGS),
            "images": [
                { "src": IMAGE_PUBLIC_URL }
            ],
            "variants": [
                { "price": PRICE }
            ]
        }
    }
    print("Uploading product to Shopify...")
    try:
        resp = requests.post(url, headers=headers, json=payload)
        print(f"Shopify response status: {resp.status_code}")
        if resp.ok:
            prod = resp.json()["product"]
            print(f"✅ Uploaded to Shopify: {prod['title']} (ID: {prod['id']})")
            print(f"➡️ See your product: https://{SHOPIFY_URL}/admin/products/{prod['id']}")
            logging.info(f"Uploaded product '{prod['title']}' successfully with ID {prod['id']} and image {IMAGE_PUBLIC_URL}")
        else:
            print("❌ Shopify upload failed:", resp.text)
            logging.error(f"Shopify upload failed: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        logging.error(f"Exception during Shopify upload: {e}")

if __name__ == "__main__":
    upload_to_shopify()
