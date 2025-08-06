import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

# ------------------------------
# 1. Load Gemini API Key
# ------------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

# ------------------------------
# 2. Configure Gemini
# ------------------------------
genai.configure(api_key=api_key)

# Use Gemini 1.5 Flash (free & fast)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# ------------------------------
# 3. Prompt to Generate Product Content
# ------------------------------
prompt = """
Generate a creative product title, short description, and 5 tags for a trendy printed t-shirt.
Output in this JSON format:
{
  "title": "...",
  "description": "...",
  "tags": ["...", "...", "...", "...", "..."]
}
"""

# ------------------------------
# 4. Generate Content from Gemini
# ------------------------------
try:
    response = model.generate_content(prompt)
    generated_text = response.text
    print("📤 Raw Output:\n", generated_text)
except Exception as e:
    print(f"❌ Error generating content: {e}")
    exit(1)

# ------------------------------
# 5. Parse JSON from Output
# ------------------------------
try:
    product_data = json.loads(generated_text)
except json.JSONDecodeError:
    json_text = re.findall(r'\{.*?\}', generated_text, re.DOTALL)
    if json_text:
        product_data = json.loads(json_text[0])
    else:
        print("❌ Could not extract valid JSON.")
        product_data = {}

# ------------------------------
# 6. Add Image URL
# ------------------------------
product_data["image_url"] = "https://image.made-in-china.com/202f0j00iIlbmtGCZUcw/Men-prime-S-Sublimation-Sports-Running-Short-Sleeve-T-Shirt.webp"

# ------------------------------
# 7. Save JSON Output to File
# ------------------------------
os.makedirs("product_generator", exist_ok=True)

output_path = "product_generator/generated_product.json"
with open(output_path, "w") as f:
    json.dump(product_data, f, indent=2)

print(f"\n✅ Product data saved to {output_path}")
