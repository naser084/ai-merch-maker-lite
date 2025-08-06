import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import time

# Load .env to get keys
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
SHOPIFY_STORE_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN")

# Gemini & Shopify API endpoints
GEMINI_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
SHOPIFY_PRODUCT_URL = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-04/products.json"

# Generate product from Gemini
def generate_product(retries=3, delay=5):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "Generate one fun T-shirt product with name, price, and color. "
                            "Respond only in JSON like this: "
                            "{\"name\": \"Cool Tee\", \"price\": 199, \"color\": \"Black\"}"
                        )
                    }
                ]
            }
        ]
    }
    params = {"key": GEMINI_API_KEY}

    for attempt in range(retries):
        response = requests.post(GEMINI_URL, headers=headers, json=payload, params=params)

        if response.status_code == 200:
            try:
                raw_text = response.json()['candidates'][0]['content']['parts'][0]['text']
                cleaned = raw_text.strip().replace("```json", "").replace("```", "").strip()
                return json.loads(cleaned)
            except Exception as e:
                st.error(f"❌ Failed to parse response: {e}")
                st.code(response.text)
                return None
        elif response.status_code == 503:
            st.warning(f"⚠️ Gemini overloaded. Retrying {attempt+1}/{retries} in {delay} seconds...")
            time.sleep(delay)
        else:
            st.error(f"❌ Gemini API error: {response.status_code}")
            st.code(response.text)
            return None
    st.error("❌ All retries failed. Gemini still overloaded.")
    return None

# Send product to Shopify
def send_to_shopify(product_data):
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN
    }

    product_payload = {
        "product": {
            "title": product_data["name"],
            "body_html": f"<strong>Color:</strong> {product_data['color']}",
            "vendor": "AI Merch",
            "product_type": "T-Shirt",
            "variants": [
                {
                    "price": str(product_data["price"]),
                    "option1": product_data["color"]
                }
            ],
            "options": [
                {
                    "name": "Color",
                    "values": [product_data["color"]]
                }
            ]
        }
    }

    response = requests.post(SHOPIFY_PRODUCT_URL, headers=headers, json=product_payload)
    if response.status_code == 201:
        return response.json()
    else:
        st.error("❌ Shopify API Error")
        st.code(response.text)
        return None

# Streamlit App UI
st.title("👕 AI Merch Generator (Gemini + Shopify)")
st.write("Click below to generate a T-shirt product using Gemini and publish it to your Shopify store.")

if st.button("🚀 Generate and Publish Product"):
    with st.spinner("Talking to Gemini..."):
        product = generate_product()

    if product:
        st.success("✅ Product Generated:")
        st.json(product)

        with st.spinner("Publishing to Shopify..."):
            result = send_to_shopify(product)
        
        if result:
            st.success("✅ Product Published on Shopify!")
            st.json(result)




# import streamlit as st
# import requests
# import json
# import os
# from dotenv import load_dotenv
# import time

# # Load .env to get Gemini key
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # Gemini & Publisher endpoints
# GEMINI_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
# FAKE_PUBLISHER_URL = "http://localhost:8000"

# # Generate product from Gemini
# def generate_product(retries=3, delay=5):
#     headers = {"Content-Type": "application/json"}
#     payload = {
#         "contents": [
#             {
#                 "parts": [
#                     {
#                         "text": (
#                             "Generate one fun T-shirt product with name, price, and color. "
#                             "Respond only in JSON like this: "
#                             "{\"name\": \"Cool Tee\", \"price\": 199, \"color\": \"Black\"}"
#                         )
#                     }
#                 ]
#             }
#         ]
#     }
#     params = {"key": GEMINI_API_KEY}

#     for attempt in range(retries):
#         response = requests.post(GEMINI_URL, headers=headers, json=payload, params=params)

#         if response.status_code == 200:
#             try:
#                 raw_text = response.json()['candidates'][0]['content']['parts'][0]['text']
#                 cleaned = raw_text.strip().replace("```json", "").replace("```", "").strip()
#                 return json.loads(cleaned)
#             except Exception as e:
#                 st.error(f"❌ Failed to parse response: {e}")
#                 st.code(response.text)
#                 return None
#         elif response.status_code == 503:
#             st.warning(f"⚠️ Gemini overloaded. Retrying {attempt+1}/{retries} in {delay} seconds...")
#             time.sleep(delay)
#         else:
#             st.error(f"❌ Gemini API error: {response.status_code}")
#             st.code(response.text)
#             return None
#     st.error("❌ All retries failed. Gemini still overloaded.")
#     return None

# # Send product to Fake Publisher
# def send_to_publisher(product_data):
#     headers = {"Content-Type": "application/json"}
#     response = requests.post(FAKE_PUBLISHER_URL, headers=headers, json=product_data)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         st.error("❌ Publisher error")
#         st.code(response.text)
#         return None

# # Streamlit App UI
# st.title("👕 AI Merch Generator (Gemini 1.5 Flash)")
# st.write("Click below to generate a fun T-shirt product and send it to the fake publisher.")

# if st.button("🚀 Generate and Publish Product"):
#     with st.spinner("Talking to Gemini..."):
#         product = generate_product()

#     if product:
#         st.success("✅ Product Generated:")
#         st.json(product)

#         with st.spinner("Sending to Fake Publisher..."):
#             result = send_to_publisher(product)
        
#         if result:
#             st.success("✅ Product Published!")
#             st.json(result)
