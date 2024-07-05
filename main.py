from flask import Flask, request, send_file, make_response
from flask_cors import CORS
from fpdf import FPDF
import os
from time import strftime
import json
import tempfile

app = Flask(__name__)
CORS(app)

class PDF(FPDF):
    def footer(self):
        self.set_font('poppins-regular', '', 6)
        self.set_y(-40)
        self.multi_cell(0, 3, "Web3DPrint Ltd (Company No. [INSERT NUMBER]) is a platform connecting makers and 3D printer owners worldwide. Our registered address is [INSERT UK ADDRESS]. Web3DPrint Ltd is registered in England and Wales. We facilitate transactions between users but do not directly provide 3D printing services. We are not responsible for the quality of 3D printed items or any damages resulting from their use. Payment processing is handled by Stripe Payments UK Ltd, which is authorised by the Financial Conduct Authority under the Payment Services Regulations 2017 for the provision of payment services (Firm Reference Number: 900461). Web3DPrint Ltd is committed to protecting your personal data in accordance with applicable data protection laws, including the UK General Data Protection Regulation (UK GDPR) and the Data Protection Act 2018. For disputes related to 3D printing services, please contact the service provider directly. For platform-related issues, contact our customer support at SUPPORT@WEB3DPRINT.COM. By using Web3DPrint, you agree to our Terms of Service and Privacy Policy, available at WEB3DPRINT.COM.", 0, 'L', False)
        self.set_y(-15)
        self.set_font('poppins-medium', '', 8)
        self.cell(0, 10, f"{strftime('%Y')} Web3DPrint Ltd. All rights reserved.", 0, 0, 'L')
        self.set_x(-40)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, 'R')

def setup_pdf():
    pdf = PDF()
    pdf.add_page()
    pdf.set_margin(10)
    font_path = os.path.join(os.path.dirname(__file__), 'fonts')
    pdf.add_font('poppins-bold', '', os.path.join(font_path, 'Poppins-Bold.ttf'))
    pdf.add_font('poppins-medium', '', os.path.join(font_path, 'Poppins-Medium.ttf'))
    pdf.add_font('poppins-regular', '', os.path.join(font_path, 'Poppins-Regular.ttf'))
    return pdf

def add_header(pdf):
    page_width = pdf.w - 2 * pdf.l_margin
    half_page_width = page_width / 2
    pdf.set_font('poppins-medium', size=18)
    pdf.set_x(10)
    pdf.cell(half_page_width, 10, "Web3DPrint", 0, 0, 'L')
    pdf.set_x(10 + half_page_width)
    pdf.cell(half_page_width, 10, "Order Summary", 0, 1, 'R')
    pdf.set_font('poppins-regular', size=8)
    pdf.cell(page_width, 4, f"Generated On: {strftime('%Y-%m-%d')}", 0, 1, 'R')
    pdf.cell(page_width, 4, "Web3DPrint Limited", 0, 1, 'R')
    pdf.ln(10)

def add_customer_info(pdf, name, address, order_id, date_of_order, payment_terms, currency):
    page_width = pdf.w - 2 * pdf.l_margin
    pdf.set_font('poppins-medium', size=11)
    pdf.cell(page_width, 10, name, 0, 1, 'L')
    pdf.set_font('poppins-medium', size=8)
    pdf.multi_cell(page_width, 4, address, 0, 'L')
    pdf.ln(0)
    column_width = page_width / 6
    pdf.set_x(pdf.w - pdf.r_margin - 2 * column_width)
    pdf.set_font('poppins-medium', size=8)
    pdf.cell(column_width, 4, "Order Number:", 0, 0, 'L')
    pdf.set_font('poppins-regular', size=8)
    pdf.cell(column_width, 4, order_id, 0, 1, 'L')
    pdf.set_x(pdf.w - pdf.r_margin - 2 * column_width)
    pdf.set_font('poppins-medium', size=8)
    pdf.cell(column_width, 4, "Date Of Order:", 0, 0, 'L')
    pdf.set_font('poppins-regular', size=8)
    pdf.cell(column_width, 4, date_of_order, 0, 1, 'L')
    pdf.set_x(pdf.w - pdf.r_margin - 2 * column_width)
    pdf.set_font('poppins-medium', size=8)
    pdf.cell(column_width, 4, "Payment Method:", 0, 0, 'L')
    pdf.set_font('poppins-regular', size=8)
    pdf.cell(column_width, 4, payment_terms, 0, 1, 'L')
    pdf.set_x(pdf.w - pdf.r_margin - 2 * column_width)
    pdf.set_font('poppins-medium', size=8)
    pdf.cell(column_width, 4, "Currency:", 0, 0, 'L')
    pdf.set_font('poppins-regular', size=8)
    pdf.cell(column_width, 4, currency, 0, 1, 'L')
    pdf.ln(10)

def add_delivery_info(pdf, delivery_method, estimated_delivery_date, shipping_address, tracking_number, special_instructions):
    page_width = pdf.w - 2 * pdf.l_margin
    pdf.set_font('poppins-medium', size=10)  # Reduced from 12
    pdf.cell(0, 8, "Delivery Information", 0, 1, 'L')  # Reduced height from 10 to 8
    
    pdf.set_font('poppins-medium', size=8)  # Reduced from 9
    pdf.cell(page_width/4, 4, "Delivery Method:", 0, 0, 'L')  # Reduced height from 5 to 4
    pdf.set_font('poppins-regular', size=8)  # Reduced from 9
    pdf.cell(page_width/4, 4, delivery_method, 0, 1, 'L')
    
    pdf.set_font('poppins-medium', size=8)
    pdf.cell(page_width/4, 4, "Estimated Delivery Date:", 0, 0, 'L')
    pdf.set_font('poppins-regular', size=8)
    pdf.cell(page_width/4, 4, estimated_delivery_date, 0, 1, 'L')
    
    if tracking_number:
        pdf.set_font('poppins-medium', size=8)
        pdf.cell(page_width/4, 4, "Tracking Number:", 0, 0, 'L')
        pdf.set_font('poppins-regular', size=8)
        pdf.cell(page_width/4, 4, tracking_number, 0, 1, 'L')
    
    pdf.set_font('poppins-medium', size=8)
    pdf.cell(page_width/4, 4, "Shipping Address:", 0, 1, 'L')
    pdf.set_font('poppins-regular', size=8)
    pdf.multi_cell(page_width, 4, shipping_address, 0, 'L')
    pdf.ln(0)  # Reduced from 5
    
    if special_instructions:
        pdf.set_font('poppins-medium', size=8)
        pdf.cell(page_width/2, 4, "Special Instructions:", 0, 1, 'L')
        pdf.set_font('poppins-regular', size=8)
        pdf.multi_cell(page_width, 4, special_instructions, 0, 'L')
    
    pdf.ln(6)  # Reduced from 10

def add_order_summary(pdf, products, currency):
    page_width = pdf.w - 2 * pdf.l_margin
    
    # Check if there's enough space on the current page
    if pdf.get_y() > 180:  # Adjust this value as needed
        pdf.add_page()
    
    column_widths = [page_width * 0.4, page_width * 0.15, page_width * 0.15, page_width * 0.15, page_width * 0.15]
    
    pdf.set_font('poppins-medium', size=10)  # Reduced from 12
    pdf.cell(0, 8, "Items Ordered", 0, 1, 'L')  # Reduced height from 10 to 8
    
    pdf.set_font('poppins-medium', size=9)  # Reduced from 10
    pdf.set_draw_color(64, 64, 64)
    pdf.set_line_width(0.5)
    
    headers = ['Product', 'Quantity', 'Price', 'Tax', 'Total']
    for i, header in enumerate(headers):
        pdf.cell(column_widths[i], 8, header, border=0, align='LCCCR'[i])  # Reduced height from 10 to 8
    pdf.ln(8)
    
    end_y = pdf.get_y()
    pdf.line(10, end_y, 10 + page_width, end_y)
    
    pdf.set_font('poppins-regular', size=7)  # Reduced from 8
    pdf.set_line_width(0.25)
    
    total_amount = 0
    for product in products:
        for i, key in enumerate(['name', 'quantity', 'unit_price', 'tax', 'total']):
            value = str(product[key]) if key == 'quantity' else product[key]
            if key in ['unit_price', 'tax', 'total']:
                value = f"{currency}{value.lstrip('£')}"
            pdf.cell(column_widths[i], 8, value, border=0, align='LCCCR'[i])  # Reduced height from 10 to 8
            if key == 'total':
                total_amount += float(value.lstrip(currency))
        pdf.ln(8)
        end_y = pdf.get_y()
        pdf.line(10, end_y, 10 + page_width, end_y)

    pdf.set_font('poppins-medium', size=9)  # Reduced from 10
    formatted_total_amount = f"{currency}{total_amount:.2f}"
    pdf.cell(column_widths[4], 8, "Total Amount", border=0, align='L')  # Reduced height from 10 to 8
    
    for i in range(3):
        pdf.cell(column_widths[i], 8, "", border=0)
    
    pdf.cell(column_widths[4], 8, formatted_total_amount, border=0, align='R')
    pdf.ln(8)
    
    end_y = pdf.get_y()
    pdf.line(10, end_y, 10 + page_width, end_y)

    pdf.ln(6)  # Reduced from 10
    pdf.set_font('poppins-regular', size=7)  # Reduced from 8
    pdf.multi_cell(0, 4, "Thank you for your order! For questions about this order, please contact our customer support at support@web3dprint.com", 0, 'L')
    pdf.ln(3)  # Reduced from 5
    pdf.multi_cell(0, 4, "For more information about our services and policies, please visit our website at WEB3DPRINT.COM", 0, 'L')

@app.route('/generate_pdf', methods=['POST', 'OPTIONS'])
def generate_pdf_api():
    if request.method == "OPTIONS":  # CORS preflight
        return build_preflight_response()
    elif request.method == "POST":
        json_data = request.json

        if not json_data:
            return "No JSON data provided", 400

        # Extract existing information
        full_name = json_data.get('full_name', '')
        address = json_data.get('address', '')
        order_id = json_data.get('order_id', '')
        date_of_order = json_data.get('date_of_order', '')
        payment_terms = json_data.get('payment_terms', '')
        products = json_data.get('products', [])
        currency = json_data.get('currency', '£')  # Default to GBP if not provided

        # Extract new delivery information
        delivery_method = json_data.get('delivery_method', 'Standard Shipping')
        estimated_delivery_date = json_data.get('estimated_delivery_date', 'Not available')
        shipping_address = json_data.get('shipping_address', address)  # Default to billing address if not provided
        tracking_number = json_data.get('tracking_number', '')
        special_instructions = json_data.get('special_instructions', '')

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            temp_filename = tmp_file.name

        pdf = setup_pdf()
        add_header(pdf)
        add_customer_info(pdf, full_name, address, order_id, date_of_order, payment_terms, currency)
        add_delivery_info(pdf, delivery_method, estimated_delivery_date, shipping_address, tracking_number, special_instructions)
        add_order_summary(pdf, products, currency)
        pdf.output(temp_filename)

        return send_file(
            temp_filename,
            as_attachment=True,
            download_name=f'order_summary_{order_id}.pdf',
            mimetype='application/pdf'
        )

def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))