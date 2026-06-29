import os
import tempfile
import streamlit as st
from extractor import extract_bill_data
from excel_filler import fill_excel

st.set_page_config(
    page_title="Energybae — Solar Load Calculator",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ Energybae — Solar Load Calculator")
st.caption("Upload your MSEDCL bill — we extract the data and calculate your solar system size")

st.info("💡 Enter your Gemini or Claude API key and upload your MSEDCL bill")


# ----------------------------
# API Key + Method Selection
# ----------------------------
api_key = st.text_input(
    "API Key (As per selected options)",
    type="password",
    placeholder="sk-ant-api03-... or AIzaSy..."
)

method = st.selectbox(
    "Extraction Method",
    options=["gemini", "claude"],
    format_func=lambda x: {
        "gemini": "✨ Gemini Vision (free API key)",
        "claude": "🤖 Claude Vision (most accurate)"
    }[x]
)

# ----------------------------
# 1. File Uploader
# ----------------------------
uploaded_file = st.file_uploader(
    "Upload MSEDCL Bill",
    type=["jpg", "jpeg", "png"]
)

if "bill_data" not in st.session_state:
    st.session_state.bill_data = None

# ----------------------------
# 2. Extract Button
# ----------------------------
if uploaded_file is not None:
    st.success("Bill uploaded successfully!")

    if st.button("🔍 Extract & Calculate"):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(uploaded_file.getbuffer())
            temp_image = tmp.name

        try:
            with st.spinner(f"Reading bill using {method.upper()}..."):
                data = extract_bill_data(
                    image_path=temp_image,
                    api_key=api_key if api_key else None,
                    method=method   # ✅ now passing method correctly
                )
                st.session_state.bill_data = data

            st.success("Extraction Complete!")
            st.subheader("Extracted Data")
            st.json(st.session_state.bill_data)

        except Exception as e:
            st.error(f"Error: {e}")

        finally:
            if os.path.exists(temp_image):
                os.remove(temp_image)

# ----------------------------
# 3. Download Excel
# ----------------------------
if st.session_state.bill_data is not None:
    if st.button("📄 Generate Excel"):

        template_path = "Copy_of_Pranay_HOME_E-Bill_Analysis.xlsx"

        output_path = fill_excel(
            template_path=template_path,
            data=st.session_state.bill_data,
            output_path="filled_bill.xlsx"
        )

        with open(output_path, "rb") as f:
            excel_bytes = f.read()

        st.download_button(
            label="⬇ Download Excel",
            data=excel_bytes,
            file_name="Solar_Load_Calculation.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )