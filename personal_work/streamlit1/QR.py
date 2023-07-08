import streamlit as st
import qrcode
from PIL import Image

st.title("QRコード作成アプリ")

url = st.text_input("QRコードを作成したいURL")

if st.button("QRコード作成"):
    _img = qrcode.make(url)
    _img.save('qrcode.png')
    img =Image.open('qrcode.png')
    st.image(img)