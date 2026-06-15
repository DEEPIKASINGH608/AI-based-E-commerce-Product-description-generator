import streamlit as st
import requests

# Page UI configurations
st.set_page_config(page_title="AI E-Commerce Copywriter", page_icon="🛍️", layout="centered")

st.title("🛍️ AI Product Description Generator")
st.write("Generate high-converting, SEO-optimized listings instantaneously using free open-source LLMs.")

st.markdown("---")

# Setup Input Forms / Columns
col1, col2 = st.columns(2)

with col1:
    product_name = st.text_input("📦 Product Name", placeholder="e.g., Ergonomic Wireless Mouse")
    category = st.text_input("🏷️ Product Category", placeholder="e.g., Electronics / Office Supplies")
    keywords = st.text_area("🔑 SEO Keywords (Comma separated)", placeholder="e.g., bluetooth 5.0, rechargeable, wrist-pain relief")

with col2:
    tone = st.selectbox(
        "🎭 Tone of Voice",
        ["Professional / Corporate", "Witty & Humorous", "Luxury & Elegant", "Bold & Bold", "Casual / Friendly"]
    )
    platform = st.selectbox(
        "📱 Target Platform Layout",
        ["Amazon Listing", "Shopify Store", "Etsy Shop", "Instagram / Social Commerce Ad"]
    )

# Generation Core Logic Trigger
st.markdown("---")
if st.button("✨ Generate Optimized Description", use_container_width=True):
    if not product_name or not category:
        st.error("⚠️ Please fill out at least the Product Name and Category to construct your prompt context!")
    else:
        with st.spinner("🤖 Processing data pipeline & inference models... please wait..."):
            # Construct JSON data payload matching FastAPI's structure exactly
            payload = {
                "product_name": product_name,
                "category": category,
                "keywords": keywords if keywords else "high quality",
                "tone": tone,
                "platform": platform
            }

            try:
                # Direct local loop request to Backend API
                response = requests.post("http://127.0.0.1:8000/generate", json=payload)

                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Generated Successfully!")

                    # Output Render Box
                    st.subheader("📋 Generated Copywriting Draft:")
                    st.info(result["description"])

                    # Added Feature: Quick Copy Button functionality
                    st.text_copy_button("📋 Copy text to clipboard", result["description"])
                else:
                    st.error(f"Backend Error: {response.json().get('detail', 'Unknown error occurrence.')}")

            except requests.exceptions.ConnectionError:
                st.error("🔌 Could not connect to backend server. Make sure your FastAPI backend engine is running on terminal port 8000!")


                