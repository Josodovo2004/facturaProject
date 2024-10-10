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


def generate_ticket(outputPath, imagePath, data):
    initialHeight = 16*cm
    width, height = (8*cm, initialHeight)
    c = canvas.Canvas(outputPath, pagesize=(width, height))
    
    #--------teniendo en cuenta el numero de items y el largo de sus descripciones aumentamos el largo del ticket de forma dinamica------#
    style = ParagraphStyle(
        name="CustomStyle",
        fontName="Helvetica",
        fontSize=6,
        textColor=colors.black,
        leading=7,  # Line height
        alignment=0,  # Left alignment
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
    
    
    #---------------datos inicio--------------#
    separation = 11
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString(width/2, currentY, data['negocio']['nombre'])
    currentY -= separation
    c.setFont("Helvetica", 6)
    c.drawCentredString(width/2, currentY, f"Correo electronico: {data['negocio']['correo']}")
    currentY -= separation
    c.drawCentredString(width/2, currentY, f"Telefono: {data['negocio']['telefono']}")
    currentY -= separation
    c.drawCentredString(width/2, currentY, data['cabecera']['rucEmisor'])
    currentY -= separation
    
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString(width/2, currentY, data['cabecera']['tipoDocumento'])
    currentY -= separation
    c.drawCentredString(width/2, currentY, data['cabecera']['serieYNumero'])
    currentY -= 0.5*cm
    
    #--------------fecha y datos cliente----------------#
    
    c.drawString(lLeft, currentY, data['cabecera2']['fecha'])
    currentY -= 0.2*cm
    c.line(lLeft, currentY, lRight, currentY)
    currentY -= 0.4*cm
    
    for key, value in data['cabecera2'].items():
        key: str
        value: str = str(value)
        if key == 'fecha':
            continue
        c.setFont("Helvetica-Bold", 6)
        titleLen = c.stringWidth(f'{key.capitalize()}: ', "Helvetica-Bold", 6)
        c.drawString(lLeft, currentY, f'{key.capitalize()}: ')
        c.setFont("Helvetica", 6)
        c.drawString(lLeft + titleLen, currentY, value)
        currentY -= 0.4*cm
    
    c.setFont("Helvetica-Bold", 6)
    titleLen = c.stringWidth(f'Items: ', "Helvetica-Bold", 6)
    c.drawString(lLeft, currentY, f'Items: ')
    c.setFont("Helvetica", 6)
    c.drawString(lLeft + titleLen, currentY, str(len(data['items'])))
    
    #----------------nombres columnas----------------#
    c.setFont("Helvetica-Bold", 6)
    currentY -= 0.4*cm
    c.line(lLeft, currentY, lRight, currentY)
    currentY -= 0.4*cm
    c.drawString(lLeft, currentY, 'Cant.')
    c.drawString(lLeft+ 1*cm, currentY, 'DESCRIPCIÓN')
    c.drawString(lLeft+5.5*cm, currentY, 'P. Unit')
    c.drawString(lLeft+6.68*cm, currentY, 'TOTAL')
    
    currentY -= 0.2*cm
    c.line(lLeft, currentY, lRight, currentY)
    
    #--------------items------------------------#
    c.setFont("Helvetica", 6)
    currentY -= 0.3*cm
    
    
    for value in data['items']:
        c.drawString(lLeft, currentY, str(value[0]))
        
        paragraph = Paragraph(value[3], style)
        paragraph.wrap(3*cm, 1000)
        paragraph.drawOn(c, lLeft+ 1*cm, currentY +6 - paragraph.height)
        
        c.drawCentredString(lLeft + 5.7*cm, currentY, str(value[4]))
        length = c.stringWidth(str(value[0]*value[4]), "Helvetica", 6)
        c.drawString(lRight-length, currentY, str(value[0]*value[4]))
        
        currentY -= paragraph.height + 0.2*cm
    currentY += paragraph.height -0.2*cm
    c.line(lLeft, currentY, lRight, currentY)
    #-----------total-----------------#
    currentY -= 0.4*cm
    
    for value in data['total']:
        value: str
        title=value.capitalize()
        number=data['total'][value]
        strWidht = c.stringWidth(str(number), "Helvetica", 6)
        c.setFont("Helvetica", 6)
        if value == 'total':
            c.setFont("Helvetica-Bold", 6)
        c.drawString(lLeft, currentY, title)
        c.drawString(lRight - 2*cm, currentY, 'S/')
        c.drawString(lRight - strWidht, currentY, str(number))
        
        currentY -= 0.4*cm
    
    currentY -= 0.2*cm
    
    #--------------------datos finales----------------#
    
    entero, decimal = str(f"{data['total']['total']:.2f}").split(".")
    
    # Convertimos la parte entera a palabras
    palabras_entero = num2words(int(entero), lang='es').capitalize()

    # Convertimos la parte decimal a fracción (dos decimales)
    if int(decimal) == 0:
        resultado = f"{palabras_entero} con 00/100"
    else:
        resultado = f"{palabras_entero} con {decimal}/100"
    
    # Draw "IMPORTE EN LETRAS"
    c.setFont("Helvetica-Bold", 6)
    c.drawString(lLeft, currentY, f"IMPORTE EN LETRAS: ")
    
    numeroParagraph = Paragraph(f'{resultado.upper()} NUEVOS SOLES', style)
    numeroParagraph.wrap(width -3.3*cm, 1000)
    numeroParagraph.drawOn(c, 2.7*cm, currentY - numeroParagraph.height + 6)
    currentY -= 0.1*cm + numeroParagraph.height
    
    c.drawString(lLeft, currentY, 'RESUMEN: ')
    c.setFont("Helvetica", 6)
    c.drawString( 2.7*cm, currentY, data['hashCode'])
    
    currentY -= 0.4*cm
    
    c.setFont("Helvetica-Bold", 6)
    c.drawString(lLeft, currentY, 'FORMA DE PAGO: ')
    c.setFont("Helvetica", 6)
    c.drawString(2.7*cm, currentY, data['formaPago'])
    
    #---------------codigo qr----------------#
    
    currentY -= (0.6 * cm) + 80
    
    
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
    
    c.drawImage(qr_image, (width/2) - 40, currentY, width=80, height=80)
    
    #--------------pie del ticket-------------------#
    c.setFont("Helvetica-Bold", 6)
    
    currentY -= 0.2*cm
    c.drawCentredString(width/2, currentY, '!Gracias por su preferencia¡')
    c.setFont("Helvetica", 6)
    currentY -= 0.2*cm
    c.drawCentredString(width/2, currentY, 'www.quikcart.com')
    
    currentY -= 0.4*cm
    c.drawCentredString(width/2, currentY, 'Repesentación impresa de la Boleta de Venta')
    currentY -= 0.2*cm
    c.drawCentredString(width/2, currentY, 'electrónica. Consulte su documento en:')
    currentY -= 0.2*cm
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString(width/2, currentY, 'https://consulta.quikcart.com')    
    
    c.save()
    
    return outputPath



if __name__ == '__main__':

    data = {
        'cabecera': {
        'rucEmisor': "R.U.C. N° 10123456789",
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

    generate_ticket("pdf/scripts/ticker_boleta_venta_electronica.pdf", "pdf/scripts/logo.png", data)
    