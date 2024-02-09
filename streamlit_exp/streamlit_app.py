import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Jan du Plessis Experiment",
)

html = """
<style>
.gradient-text {
    background: linear-gradient(45deg, #204E82, #B2D5E3, #71A3BF);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-size: 3em;
    font-weight: bold;
}
</style>
<div class="gradient-text">Jan du Plessis Experiment</div> 
"""
# Render the HTML in the Streamlit app
st.markdown(html, unsafe_allow_html=True)

# Create a container
with st.container():
    st.header("Container")
    st.write("This is the content inside the container.")


with st.container(height=200):
    st.chat_message("user").write("Hello world")


def embed_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
        st.components.v1.html(pdf_display, width=700, height=1000)


# Path to your PDF file
pdf_path = "../../images/file.pdf"

# Display the PDF
embed_pdf(pdf_path)
