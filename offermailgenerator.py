import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
from io import BytesIO
from datetime import datetime

# 1. Configure Gemini API key
genai.configure(api_key="AIzaSyBp9npZeUo2QnR-wWdISXUqLIzSSWajp5I")

# 2. Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# 3. Function to generate email from Gemini
def generate_email(name, designation, tone, format_style, company=None, joining_date=None, template=None):
    prompt = f"""
    You are an HR executive generating a job offer email.

    Candidate Name: {name}
    Designation: {designation}
    Tone: {tone}
    Format: {format_style}
    Template Style: {template if template else 'Professional'}

    {"Company Name: " + company if company else ""}
    {"Joining Date: " + joining_date.strftime('%B %d, %Y') if joining_date else ""}

    Generate a concise, polite, and professional offer letter email.
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# 4. Convert email text to PDF
def convert_to_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf_output = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin-1')  # Output as string then encode
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output

# 5. Streamlit UI
st.set_page_config(page_title="Job Offer Email Generator", layout="centered")
st.title("📩 AI Job Offer Email Generator")
st.markdown("Generate professional job offer emails using Gemini AI. Fill in the details below.")

# User Inputs
name = st.text_input("👤 Candidate's Name")
designation = st.text_input("💼 Designation")
company = st.text_input("🏢 Company Name (optional)")
joining_date = st.date_input("📅 Joining Date (optional)")

# Format and Tone
tone = st.radio("🗣️ Select Tone", ["Formal", "Friendly", "Neutral"])
format_style = st.selectbox("📄 Select Format", ["Standard", "Bulleted", "Compact"])

# Template Preview (Visual only)
template = st.selectbox("🧾 Select Template Style", ["Professional", "Creative", "Simple"])
with st.expander("📌 Template Preview"):
    if template == "Professional":
        st.markdown("""
        **Subject**: Job Offer for [Designation] at [Company]  
        **Body**: Formal tone, structured paragraphs, and key dates.
        """)
    elif template == "Creative":
        st.markdown("""
        **Subject**: Your Next Adventure Starts Here!  
        **Body**: Friendly tone, informal language, excitement-driven.
        """)
    else:
        st.markdown("""
        **Subject**: Job Offer Letter  
        **Body**: Simple tone, clear and concise format.
        """)

# Generate email button
if "email_text" not in st.session_state:
    st.session_state.email_text = ""

if st.button("✉️ Generate Email"):
    if name and designation:
        st.session_state.email_text = generate_email(name, designation, tone, format_style, company, joining_date, template)
    else:
        st.warning("Please provide at least Name and Designation.")

# Display generated email
if st.session_state.email_text:
    st.subheader("📬 Generated Email")
    st.text_area("Generated Job Offer Email", st.session_state.email_text, height=300)

    # Download as PDF
    pdf_data = convert_to_pdf(st.session_state.email_text)
    st.download_button("📥 Download as PDF", data=pdf_data, file_name=f"{name}_Offer_Letter.pdf", mime="application/pdf")

    # Regenerate button
    if st.button("🔁 Regenerate with New Format/Tone"):
        st.session_state.email_text = generate_email(name, designation, tone, format_style, company, joining_date, template)


