import streamlit as st
import qrcode
import numpy as np
import cv2
from PIL import Image
import io
import re

# Function to check if the decoded text is a valid URL
def is_valid_url(text):
    url_pattern = re.compile(r'^(https?://[^\s]+)$')
    return bool(url_pattern.match(text))

# Streamlit app title
st.title("🔳 QR Code Encoder & Decoder")

# Tabs for Encoding & Decoding
tab1, tab2 = st.tabs(["📤 Generate QR Code", "📥 Decode QR Code"])

# --- QR Code Generator ---
with tab1:
    st.subheader("📤 Generate QR Code")
    text = st.text_input("Enter text or URL to generate QR code:")

    if st.button("Generate QR Code"):
        try:
            if not text.strip():
                st.warning("⚠ Please enter text or URL to generate a QR code.")
            else:
                # Generate QR code
                qr = qrcode.QRCode(box_size=10, border=4)
                qr.add_data(text)
                qr.make(fit=True)
                qr_img = qr.make_image(fill="black", back_color="white")

                # Convert QR code to a byte stream for display
                img_byte_array = io.BytesIO()
                qr_img.save(img_byte_array, format="PNG")
                img_byte_array.seek(0)

                # Display QR code image
                st.image(img_byte_array, caption="Generated QR Code", use_container_width=True)

                # Download button for QR code
                st.download_button("⬇ Download QR Code", img_byte_array, file_name="qrcode.png", mime="image/png")

        except Exception as e:
            st.error(f"⚠ Error generating QR Code: {e}")

# --- QR Code Decoder ---
with tab2:
    st.subheader("📥 Decode QR Code from Image")
    uploaded_file = st.file_uploader("Upload a QR code image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        try:
            # Read image
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Use OpenCV to detect and decode QR code
            qr_detector = cv2.QRCodeDetector()
            decoded_text, _, _ = qr_detector.detectAndDecode(gray)

            if decoded_text:
                st.success("✅ QR Code Decoded Successfully!")
                
                # Display decoded text or clickable link
                if is_valid_url(decoded_text):
                    st.markdown(f"🔗 **Decoded Link:** [Click here]({decoded_text})", unsafe_allow_html=True)
                else:
                    st.write(f"📜 **Decoded Text:** `{decoded_text}`")
            else:
                st.error("⚠ No QR Code detected in the image. Please try another.")

        except Exception as e:
            st.error(f"⚠ Error decoding QR Code: {e}")

# Footer
st.markdown("---")
st.markdown("💻 **Developed by Muhammad Mudasir** 🎨")
