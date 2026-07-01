import streamlit as st
import requests

st.set_page_config(page_title="Enterprise AI Copywriter", page_icon="📈", layout="wide")

st.title("Pro AI E-Commerce Content Suite")
st.write("Construct market-ready listings utilizing localized open-source model inference execution pipelines.")

st.markdown("---")

# Organized Multi-Column Layout Architecture
with st.sidebar:
    st.header("Model Tuning Parameters")
    creativity = st.slider("Creativity Level (Temperature)", min_value=0.1, max_value=1.0, value=0.7, step=0.1)
    st.caption("Lower settings yield structured variations; higher levels boost unique configurations.")

    st.markdown("---")
    st.info(" **Tip:** Clear your temporary terminal runtime caches if performance drops across bulk listings.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(" Input Specifications")
    prod_name = st.text_input(" Core Product Identification Name", value="Wireless Earbuds", key="p_name_input")
    cat_name = st.text_input(" Department Category Classification", value="Electronics", key="c_name_input")
    keywords_list = st.text_area(" Targeted Core SEO Keywords", placeholder="e.g., lightweight frame, aerodynamic design, 11-speed gears")

    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        voice_tone = st.selectbox(" Editorial Tone", ["High-End Luxury", "Engaging & Creative", "Informative & Tech-focused", "Direct & Urgent"])
    with sub_col2:
        target_channel = st.selectbox(" Layout Channel Framework", ["Amazon Enhanced Brand Content", "Shopify Listing Page", "Social Commerce Ad Grid"])

with col2:
    st.subheader(" Real-Time Generated Output Workspace")

    if st.button(" Execute Content Generation Pipeline", use_container_width=True):
        if not prod_name.strip() or not cat_name.strip():
            st.warning(" Action Required: Populate minimum descriptive validation variables (Name & Category).")
        else:
            with st.spinner(" Routing arrays via transformation layers..."):
                payload = {
                    "product_name": prod_name.strip(),
                    "category": cat_name.strip(),
                    "keywords": keywords_list if keywords_list else "premium utility",
                    "tone": voice_tone,
                    "platform": target_channel,
                    "creativity_bias": creativity
                }

                try:
                    api_call = requests.post("http://127.0.0.1:8000/generate", json=payload)

                    if api_call.status_code == 200:
                        data_payload = api_call.json()

                        # Organized Tab Display Layout
                        tab1, tab2, tab3 = st.tabs(["📝 Complete Copy Draft", " Core Bullet Highlights", "💾 Export Data"])

                        with tab1:
                            st.markdown("### Product Overview Narrative")
                            st.info("💡 Tip: Double-click or click-and-drag below to copy the generated text.")
                            st.code(data_payload["narrative"], language="text")

                        with tab2:
                            st.markdown("### Structured Performance Highlights")
                            for bullet in data_payload["bullets"]:
                                st.markdown(f"• {bullet}")

                        with tab3:
                            compiled_file_contents = f"PRODUCT NAME: {prod_name}\n\nOVERVIEW DESCRIPTION:\n{data_payload['narrative']}\n\nBULLET FEATURES:\n" + "\n".join([f"- {b}" for b in data_payload["bullets"]])

                            st.download_button(
                                label="📥 Export to .txt File",
                                data=compiled_file_contents,
                                file_name=f"{prod_name.lower().replace(' ', '_')}_listing.txt",
                                mime="text/plain"
                            )
                            st.success("File compilation ready for download.")

                    else:
                        st.error(f"Inference Engine Exception: {api_call.json().get('detail')}")

                except requests.exceptions.ConnectionError:
                    st.error("🔌 Error: Local host backend connection refusal. Check your FastAPI pipeline execution terminal on port 8000.")


