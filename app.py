import streamlit as st
import random
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

MAX_TRINOMIALS = 300
COLUMNS_PER_PAGE = 2
TRINOMIAL_FONT_SIZE = 14

def generate_quadratic_trinomials(num_trinomials, k, r):
    trinomials = []
    for i in range(1, num_trinomials + 1):
        # Generate two distinct random integer solutions within the specified range
        solution1 = random.randint(k, r)
        solution2 = random.randint(k, r)
        while solution1 == solution2:
            solution2 = random.randint(k, r)

        a = -(solution1 + solution2)
        c = solution1 * solution2

        # Handle the signs of the coefficients separately
        a_sign = "-" if a < 0 else "+"
        c_sign = "-" if c < 0 else "+"

        # Include the "+" sign for the c term if it's not zero
        c_str = f" {c_sign} {abs(c)}" if c != 0 else ""
        trinomial = f"{i}. X^2 {a_sign} {abs(a)}X{c_str} ="
        trinomials.append(trinomial)

    return trinomials

def create_pdf(trinomials):
    doc = SimpleDocTemplate("trinomials.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    num_trinomials = len(trinomials)
    num_full_pages = num_trinomials // (COLUMNS_PER_PAGE * 20)
    remaining_trinomials = num_trinomials % (COLUMNS_PER_PAGE * 20)

    for _ in range(num_full_pages):
        page_data = [trinomials.pop(0) for _ in range(COLUMNS_PER_PAGE * 20)]
        data = [[Paragraph(trinomial, styles['Normal']) for trinomial in page_data[j:j+COLUMNS_PER_PAGE]] for j in range(0, len(page_data), COLUMNS_PER_PAGE)]
        table = Table(data, colWidths=[250] * COLUMNS_PER_PAGE, spaceBefore=10)
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), TRINOMIAL_FONT_SIZE),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(table)

    if remaining_trinomials > 0:
        rows = min(20, (remaining_trinomials + COLUMNS_PER_PAGE - 1) // COLUMNS_PER_PAGE)
        data = [[Paragraph(trinomials.pop(0), styles['Normal']) for _ in range(min(COLUMNS_PER_PAGE, remaining_trinomials))] for _ in range(rows)]
        table = Table(data, colWidths=[250] * min(COLUMNS_PER_PAGE, remaining_trinomials), spaceBefore=10)
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), TRINOMIAL_FONT_SIZE),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(table)

    doc.build(story)

def main():
    st.title("Quadratic Trinomial Generator")

    num_trinomials = st.number_input("Number of Trinomials (up to 300):", min_value=1, max_value=300, value=10)
    lower_bound = st.number_input("Lower Bound (K) for Integer Solutions:", value=-15)
    upper_bound = st.number_input("Upper Bound (R) for Integer Solutions:", value=15)

    if st.button("Generate PDF"):
        if num_trinomials > MAX_TRINOMIALS:
            num_trinomials = MAX_TRINOMIALS

        # Ensure R is greater than K
        while upper_bound <= lower_bound:
            lower_bound, upper_bound = upper_bound, lower_bound

        quadratic_trinomials = generate_quadratic_trinomials(num_trinomials, lower_bound, upper_bound)
        create_pdf(quadratic_trinomials)
        st.success("PDF with trinomials generated successfully.")

        # Provide a link to download the generated PDF
        with open("trinomials.pdf", "rb") as f:
            pdf_data = f.read()
        st.markdown(get_pdf_download_link(pdf_data), unsafe_allow_html=True)

def get_pdf_download_link(pdf_data):
    from base64 import b64encode
    encoded_pdf = b64encode(pdf_data).decode('utf-8')
    href = f'<a href="data:application/pdf;base64,{encoded_pdf}" download="trinomials.pdf">Click here to download the PDF</a>'
    return href

if __name__ == "__main__":
    main()
