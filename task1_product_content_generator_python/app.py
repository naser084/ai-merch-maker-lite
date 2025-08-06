import os
import json
import re
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# ------------------------------
# 1. Load Gemini API Key
# ------------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY not found in .env file")
    st.stop()

# ------------------------------
# 2. Configure Gemini Model
# ------------------------------
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# ------------------------------
# 3. Streamlit Page Settings
# ------------------------------
st.set_page_config(
    page_title="AI Merch Maker Lite",
    page_icon="🧠",
    layout="centered",
)

# ------------------------------
# 4. Sidebar Info
# ------------------------------
with st.sidebar:
    st.title("🎨 AI Merch Maker")
    st.markdown("This app generates creative t-shirt ideas using Google Gemini AI.")
    st.markdown("---")
    st.subheader("💡 How It Works")
    st.markdown("""
    - Click the **Generate** button  
    - Get a unique title, description & tags  
    - Preview a sample product image  
    - Download the data as a JSON file
    """)
    st.markdown("---")
    st.caption("🚀 Built with Streamlit + Gemini 1.5 Flash")

# ------------------------------
# 5. Main Interface
# ------------------------------
st.title("👕 AI T-shirt Idea Generator")
st.markdown("Click below to create a unique, trendy t-shirt idea using AI!")

if st.button("✨ Generate T-shirt Idea"):
    with st.spinner("Talking to Gemini... 🤖"):
        prompt = """
        Generate a creative product title, short description, and 5 tags for a trendy printed t-shirt.
        Output in this JSON format:
        {
          "title": "...",
          "description": "...",
          "tags": ["...", "...", "...", "...", "..."]
        }
        """
        try:
            # ------------------------------
            # 6. Generate from Gemini
            # ------------------------------
            response = model.generate_content(prompt)
            generated_text = response.text

            # ------------------------------
            # 7. Parse JSON
            # ------------------------------
            try:
                product_data = json.loads(generated_text)
            except json.JSONDecodeError:
                json_text = re.findall(r'\{.*?\}', generated_text, re.DOTALL)
                product_data = json.loads(json_text[0]) if json_text else {}

            # ------------------------------
            # 8. Add Image URL
            # ------------------------------
            product_data["image_url"] = "https://image.made-in-china.com/202f0j00iIlbmtGCZUcw/Men-prime-S-Sublimation-Sports-Running-Short-Sleeve-T-Shirt.webp"

            # ------------------------------
            # 9. Save JSON
            # ------------------------------
            os.makedirs("product_generator", exist_ok=True)
            output_path = "product_generator/generated_product.json"
            with open(output_path, "w") as f:
                json.dump(product_data, f, indent=2)

            # ------------------------------
            # 10. Display Output
            # ------------------------------
            st.success("✅ T-shirt idea generated!")
            st.image(product_data["image_url"], width=250, caption="🔖 Sample Product Image")
            st.subheader(f"🧢 {product_data.get('title', 'No Title')}")
            st.markdown(f"**📝 Description:** {product_data.get('description', 'No Description')}")
            st.markdown(f"**🏷️ Tags:** `{', '.join(product_data.get('tags', []))}`")

            # ------------------------------
            # 11. Download Button
            # ------------------------------
            st.download_button(
                label="📥 Download Product JSON",
                data=json.dumps(product_data, indent=2),
                file_name="generated_product.json",
                mime="application/json"
            )

        except Exception as e:
            st.error(f"❌ Error generating content: {e}")
else:
    st.info("Click the button above to generate your first idea! 🎉")
