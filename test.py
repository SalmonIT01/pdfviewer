import base64

def pdf_to_base64(name):
    
    pdf_path = f"/app/static/document/{name}.pdf"
    # เปิดไฟล์ PDF ในโหมดอ่านแบบไบนารี
    with open(pdf_path, "rb") as pdf_file:
        # อ่านข้อมูลในไฟล์ PDF
        pdf_data = pdf_file.read()
        # เข้ารหัสข้อมูลเป็น base64
        base64_encoded_data = base64.b64encode(pdf_data)
        # แปลงข้อมูล base64 จาก bytes เป็น string
        base64_string = base64_encoded_data.decode('utf-8')
    return base64_string   

    
