from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from num2words import num2words
import qrcode
from PIL import Image
from io import BytesIO
from reportlab.lib.utils import ImageReader
import boto3
import os

client = boto3.client('s3')

def generate_ticket(bucket_name, s3_key, imagePath, data):
    # Use BytesIO to keep PDF in memory
    temp_pdf_path = f"./{data['cabecera']['serieYNumero']}-Ticket.pdf"
    
    # Create a new PDF file

    
    initialHeight = 16 * cm
    width, height = (8 * cm, initialHeight)
    c = canvas.Canvas(temp_pdf_path, pagesize=(width, height))

    # Dynamic height based on the number of items
    style = ParagraphStyle(
        name="CustomStyle",
        fontName="Helvetica",
        fontSize=6,
        textColor=colors.black,
        leading=7,
        alignment=0,
    )
    extraHeight = 0
    for value in data['items']:
        paragraph = Paragraph(value[3], style)
        paragraph.wrap(3*cm, 1000)
        extraHeight += paragraph.height + 0.15*cm

    c.setPageSize((width, initialHeight + extraHeight))
    lLeft = 0.3*cm
    lRight = width - (0.3*cm)
    lTop = initialHeight + extraHeight - (0.3*cm)
    lBot = 0.3*cm
    
    c.drawImage(imagePath, (width/2) - 1.5*cm, lTop-(2*cm), 3*cm, 2*cm)
    
    currentY = lTop - 2.4*cm
    
    # Start drawing the ticket details
    separation = 11
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString(width/2, currentY, data['negocio']['nombre'])
    currentY -= separation
    c.setFont("Helvetica", 6)
    c.drawCentredString(width/2, currentY, f"Correo electronico: {data['negocio']['correo']}")
    currentY -= separation
    c.drawCentredString(width/2, currentY, f"Telefono: {data['negocio']['telefono']}")
    currentY -= separation
    c.drawCentredString(width/2, currentY, f'R.U.C. N° {data["cabecera"]["rucEmisor"]}')
    currentY -= separation
    
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString(width/2, currentY, data['cabecera']['tipoDocumento'])
    currentY -= separation
    c.drawCentredString(width/2, currentY, data['cabecera']['serieYNumero'])
    currentY -= 0.5*cm
    
    # Date and client information
    c.drawString(lLeft, currentY, data['cabecera2']['fecha'])
    currentY -= 0.2*cm
    c.line(lLeft, currentY, lRight, currentY)
    currentY -= 0.4*cm
    
    for key, value in data['cabecera2'].items():
        if key == 'fecha':
            continue
        c.setFont("Helvetica-Bold", 6)
        titleLen = c.stringWidth(f'{key.capitalize()}: ', "Helvetica-Bold", 6)
        c.drawString(lLeft, currentY, f'{key.capitalize()}: ')
        c.setFont("Helvetica", 6)
        c.drawString(lLeft + titleLen, currentY, str(value))
        currentY -= 0.4*cm
    
    # Item count
    c.setFont("Helvetica-Bold", 6)
    titleLen = c.stringWidth(f'Items: ', "Helvetica-Bold", 6)
    c.drawString(lLeft, currentY, f'Items: ')
    c.setFont("Helvetica", 6)
    c.drawString(lLeft + titleLen, currentY, str(len(data['items'])))

    # Column names
    c.setFont("Helvetica-Bold", 6)
    currentY -= 0.4*cm
    c.line(lLeft, currentY, lRight, currentY)
    currentY -= 0.4*cm
    c.drawString(lLeft, currentY, 'Cant.')
    c.drawString(lLeft + 1*cm, currentY, 'DESCRIPCIÓN')
    c.drawString(lLeft + 5.5*cm, currentY, 'P. Unit')
    c.drawString(lLeft + 6.68*cm, currentY, 'TOTAL')
    
    currentY -= 0.2*cm
    c.line(lLeft, currentY, lRight, currentY)
    
    # Items
    c.setFont("Helvetica", 6)
    currentY -= 0.3*cm

    for value in data['items']:
        c.drawString(lLeft, currentY, str(value[0]))
        
        paragraph = Paragraph(value[3], style)
        paragraph.wrap(3*cm, 1000)
        paragraph.drawOn(c, lLeft + 1*cm, currentY + 6 - paragraph.height)
        
        c.drawCentredString(lLeft + 5.7*cm, currentY, str(value[4]))
        length = c.stringWidth(str(value[0] * value[4]), "Helvetica", 6)
        c.drawString(lRight - length, currentY, str(value[0] * value[4]))
        
        currentY -= paragraph.height + 0.2*cm
    currentY += paragraph.height - 0.2*cm
    c.line(lLeft, currentY, lRight, currentY)

    # Total
    currentY -= 0.4*cm
    
    for value in data['total']:
        title = value.capitalize()
        number = data['total'][value]
        strWidth = c.stringWidth(str(number), "Helvetica", 6)
        c.setFont("Helvetica", 6)
        if value == 'total':
            c.setFont("Helvetica-Bold", 6)
        c.drawString(lLeft, currentY, title)
        c.drawString(lRight - 2 * cm, currentY, 'S/')
        c.drawString(lRight - strWidth, currentY, str(number))
        
        currentY -= 0.4*cm
    
    currentY -= 0.2*cm
    
    # Final data
    entero, decimal = str(f"{data['total']['total']:.2f}").split(".")
    palabras_entero = num2words(int(entero), lang='es').capitalize()

    if int(decimal) == 0:
        resultado = f"{palabras_entero} con 00/100"
    else:
        resultado = f"{palabras_entero} con {decimal}/100"
    
    c.setFont("Helvetica-Bold", 6)
    c.drawString(lLeft, currentY, f"IMPORTE EN LETRAS: ")
    
    numeroParagraph = Paragraph(f'{resultado.upper()} NUEVOS SOLES', style)
    numeroParagraph.wrap(width - 3.3 * cm, 1000)
    numeroParagraph.drawOn(c, 2.7 * cm, currentY - numeroParagraph.height + 6)
    currentY -= 0.1 * cm + numeroParagraph.height
    
    c.drawString(lLeft, currentY, 'RESUMEN: ')
    c.setFont("Helvetica", 6)
    c.drawString(2.7 * cm, currentY, data['hashCode'])
    
    currentY -= 0.4 * cm
    
    c.setFont("Helvetica-Bold", 6)
    c.drawString(lLeft, currentY, 'FORMA DE PAGO: ')
    c.setFont("Helvetica", 6)
    c.drawString(2.7 * cm, currentY, data['formaPago'])
    
    # QR code
    currentY -= (0.6 * cm) + 80
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data['codigoQr'])
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    qr_bytes = BytesIO()
    img.save(qr_bytes)
    qr_bytes.seek(0)
    
    qr_image = ImageReader(qr_bytes)
    c.drawImage(qr_image, (width / 2) - 40, currentY, width=80, height=80)
    
    # Ticket footer
    c.setFont("Helvetica-Bold", 6)
    
    currentY -= 0.2 * cm
    c.drawCentredString(width / 2, currentY, '!Gracias por su preferencia¡')
    c.setFont("Helvetica", 6)
    currentY -= 0.2 * cm
    c.drawCentredString(width / 2, currentY, 'Su opinión es importante para nosotros')
    
    c.save()

    # Upload to S3
    try:
        client.upload_file(temp_pdf_path, bucket_name, s3_key)
        print("Upload Successful")
    except Exception as e:
        print(f"Upload failed: {e}")
        return None

    # Delete the local PDF file
    os.remove(temp_pdf_path)

    # Return the S3 URL
    return f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
    


if __name__ == '__main__':

    data = {
        'cabecera': {
        'rucEmisor': "10123456789",
        'tipoDocumento': 'BOLETA DE VENTA',
        'serieYNumero' : 'BE001-001',
        },
        'cabecera2': {
            'fecha': '21/10/2024',
            'cliente': 'Franco Martines',
            'dni': '12345678',
            'direccion': '-',
        },
        'negocio': {
            'nombre': 'NEGOCIO PRUEBA',
            'correo' : 'negocioprueba@gmail.com',
            'telefono': '00000000',
        },
        
        'items' : [
            [1, 'Unidad', 'MF465', 'Mochila de Negocios de Gran Capacidad de 15.6 Pulgadas', 150],
            [1, 'Unidad', 'WPddj', 'Whisky Premium Blue Label de 750 ml, Edición Exclusiva', 777],
            [1, 'Unidad', 'MF465', 'Mochila de Negocios de Gran Capacidad de 15.6 Pulgadas', 150],
            [1, 'Unidad', 'WPddj', 'Whisky Premium Blue Label de 750 ml, Edición Exclusiva', 777],
            [1, 'Unidad', 'MF465', 'Mochila de Negocios de Gran Capacidad de 15.6 Pulgadas', 150],
            [1, 'Unidad', 'WPddj', 'Whisky Premium Blue Label de 750 ml, Edición Exclusiva', 777],
            [1, 'Unidad', 'MF465', 'Mochila de Negocios de Gran Capacidad de 15.6 Pulgadas', 150],
            [1, 'Unidad', 'WPddj', 'Whisky Premium Blue Label de 750 ml, Edición Exclusiva', 777],
            [1, 'Unidad', 'MF465', 'Mochila de Negocios de Gran Capacidad de 15.6 Pulgadas', 150],
            [1, 'Unidad', 'WPddj', 'Whisky Premium Blue Label de 750 ml, Edición Exclusiva', 777],
        ],
        
        'total': {
            'subtotal' : 785.59, 
            'I.G.V.': 141.61, 
            'total' : 927.21,
        },
        
        'hashCode' : 'hJ8hSHOAndV0Ex0gPnDtaNyIVTI=',
        'observaciones': '',
        'formaPago': 'CONTADO',
        
        'codigoQr': '20608841599|01|F001|1234|200.00|36.00|2024-10-09|6|20123456789',
    }
    
    bucket_name = 'qickartbucket'
    s3_key = f"media/{data['cabecera']['rucEmisor']}/reportes/{data['cabecera']['serieYNumero']}-ticket.pdf"
    image_path = 'pdf/scripts/logo.png'
    
    generate_ticket(bucket_name, s3_key, image_path, data)
    