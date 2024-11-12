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
def generate_pdf(bucket_name, s3_key, imagePath, data):
    temp_pdf_path = './ticket.pdf'
    # Create a canvas
    c = canvas.Canvas(temp_pdf_path, pagesize=A4)
    width, height = A4
    
    lLeft = cm
    lRight = width - cm
    lTop = height - cm
    lBot = cm
    
    c.drawImage(imagePath, lLeft + 2.5*cm, lTop - 3*cm, 6*cm, 3*cm)
    

   #-----------------cabecera gris---------------#
    box_width = 8 * cm
    box_height = 3 * cm
    box_center = (lRight- (box_width/2), lTop - (box_height/2))

    # Draw the gray box
    c.setFillColor(colors.lightgrey)
    c.roundRect(box_center[0] - (box_width/2), box_center[1]- box_height/2, box_width, box_height, fill=1, radius=3)

    text_y = box_center[1] + 18
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    
    # Inside the box, we can draw text using data
    for value in data['cabecera']:
        c.drawCentredString(box_center[0], text_y, data['cabecera'][value])
        text_y -= 20
        
    #--------------cabecera blanca---------------------#
    box_width = 8 * cm
    box_height = 2.5 * cm
    box_center = (lRight- (box_width/2), lTop - (box_height/2) - 4*cm)

    # Draw the gray box
    c.setFillColor(colors.white)
    c.roundRect(box_center[0] - (box_width/2), box_center[1]- box_height/2, box_width, box_height, fill=1, radius=3)
    c.setFillColor(colors.black)
    text_y = box_center[1] + 18
       
    
    for item, value in data['cabecera2'].items():
        item: str
        c.setFont("Helvetica-Bold", 10)
        c.drawString(box_center[0] - (box_width/2) + 10, text_y, item.capitalize())
        c.setFont("Helvetica", 10) 
        c.drawString(box_center[0] + 10, text_y, f': {value}')
        
        text_y -= 15
    


    #------------------------datos negocio---------------------------#
    c.setFont("Helvetica-Bold", 10)
    c.drawString(lLeft, height - 5.8 * cm, f"{data['negocio']['nombre']}")
    c.setFont("Helvetica", 10)
    c.drawString(lLeft, height - 6.4 * cm, f"Telefono: {data['negocio']['telefono']}")
    c.drawString(lLeft, height - 7 * cm, f"E-mail: {data['negocio']['correo']}")

    currentY = height - 7.4 * cm
    currentY -= cm *1.3
    #--------------------nombres columnas-----------------#
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1.5 * cm, currentY , "Cant.")
    c.drawString(3.3 * cm, currentY , "Unidad")
    c.drawString(5.5 * cm, currentY , "Codigo")
    c.drawString(8 * cm, currentY , "Descripcion")
    c.drawString(17.5 * cm, currentY , "P.U.")
    c.drawString(18.75 * cm, currentY , "Total")
    
    
    #-------------------datos de los items-------------------#
    currentY -= 30
    style = ParagraphStyle(
    name="CustomStyle",
    fontName="Helvetica-Bold",
    fontSize=10,
    textColor=colors.black,
    leading=14,  # Line height
    alignment=0,  # Left alignment
)
    totalFrameHeight = 50
    grey= False
    for value in data['items']:
        
        paragrph = Paragraph(value[3], style)
        paragrph.wrapOn(c, 9*cm, 1000*cm)
        
        if grey:
            c.setFillColor(colors.lightgrey)
            c.rect(lLeft, currentY-20, width - 2*cm,paragrph.height+10, fill=1)
            grey=False
        else:
            c.rect(lLeft, currentY-20, width - 2*cm,paragrph.height+10)
            grey=True
        #datos#
        c.setFillColor(colors.black)
        c.drawString(1.5 * cm, currentY , str(value[0]))
        c.drawString(3.3 * cm, currentY ,str(value[1]))
        c.drawString(5.5 * cm, currentY ,str(value[2]))
        paragrph.drawOn(c, 8*cm, currentY - paragrph.height + 20)
        c.drawString(17.5 * cm, currentY , str(value[4]))
        c.drawString(19 * cm, currentY , str(value[4] * value[0]))
        
        currentY -= paragrph.height + 10
        
        totalFrameHeight += paragrph.height + 10
    
    currentY -= 10
    
    for value in data['total']:
        value: str
        title=value.capitalize()
        number=data['total'][value]
        strWidht = c.stringWidth(title, "Helvetica", 12)
        c.setFont("Helvetica", 12)
        if value == 'total':
            c.setFont("Helvetica-Bold", 12)
        c.drawString(14*cm - strWidht, currentY, title)
        c.drawString(16.3*cm, currentY, 'S/')
        c.drawString(18*cm, currentY, str(number))
        
        currentY -= 20
        totalFrameHeight += 20
    currentY += 10
    c.roundRect(lLeft, currentY, width - 2*cm, totalFrameHeight, 3)

    
    
    #-----------------datos extra----------------#
    currentY -=40
    
    entero, decimal = str(f"{data['total']['total']:.2f}").split(".")
    
    # Convertimos la parte entera a palabras
    palabras_entero = num2words(int(entero), lang='es').capitalize()

    # Convertimos la parte decimal a fracción (dos decimales)
    if int(decimal) == 0:
        resultado = f"{palabras_entero} con 00/100"
    else:
        resultado = f"{palabras_entero} con {decimal}/100"
    
    # Draw "IMPORTE EN LETRAS"
    c.setFont("Helvetica", 9)
    c.drawString(lLeft + 0.5*cm, currentY, f"IMPORTE EN LETRAS: {resultado.capitalize()}")
    currentY -= 20
    # Draw "RESUMEN"
    c.drawString(lLeft + 0.5*cm, currentY, f"RESUMEN: {data['hashCode']}")
    currentY -= 50
    c.setStrokeColor(colors.lightgrey)
    c.roundRect(lLeft, currentY, width - 2*cm, 90, 3)
    
    
    qr = qrcode.QRCode(
        version=1,  # Adjust according to the size of the content
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of the boxes
        border=4,  # Size of the border
    )
    # Add data to the QR code
    qr.add_data(data['codigoQr'])
    qr.make(fit=True)

    # Create the QR image
    img = qr.make_image(fill="black", back_color="white")

    # Save the image to a BytesIO object
    qr_bytes = BytesIO()
    img.save(qr_bytes)
    qr_bytes.seek(0)  
    
    qr_image = ImageReader(qr_bytes)
    
    c.drawImage(qr_image, lRight -55 -(1*cm), currentY + 8, width=80, height=80)
    currentY -= 30
    #----------observaciones------------#
    # Draw "Observaciones" and payment method
    c.drawString(lLeft + 0.5*cm,currentY, f"OBSERVACIONES: {data['observaciones']}")
    currentY -= 20
    c.roundRect(lLeft, currentY, width - 2*cm, 30, 3)
    
    currentY -= 20
    #--------------forma de pago-------------#
    c.drawString(lLeft + 0.5*cm ,currentY, f"Forma de pago: {data['formaPago']}")
    currentY -= 7
    c.roundRect(lLeft, currentY, width - 2*cm, 20, 3)
    currentY -= 15


    #-------------pie de pagina-----------#
    # Draw footer
    c.drawString(2 * cm, currentY, "Representación impresa de la Boleta de Venta electrónica. Consulte su documento en https://consulta.quikcart.com")

    # Save the PDF
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

# Generate the PDF

if __name__ == '__main__':

    data = {
        'cabecera': {
        'rucEmisor': "10123456789",
        'tipoDocumento': 'BOLETA DE VENTA ',
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
        ],
        
        'total': {
            'subtotal' : 785.59, 
            'I.G.V.': 141.41, 
            'total' : 927.00,
        },
        'hashCode' : 'hJ8hSHOAndV0Ex0gPnDtaNyIVTI=',
        'observaciones': '',
        'formaPago': 'CONTADO',
        
        'codigoQr': '20608841599|01|F001|1234|200.00|36.00|2024-10-09|6|20123456789',
    }

    bucket_name = 'qickartbucket'
    s3_key = f"media/reportes/{data['cabecera']['rucEmisor']}/{data['cabecera']['serieYNumero']}-A4.pdf"
    image_path = 'pdf/scripts/logo.png'
    
    generate_pdf(bucket_name, s3_key, image_path, data)
