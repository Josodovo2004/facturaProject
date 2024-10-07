from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm

def generate_pdf(outputPath, imagePath, data):
    # Create a canvas
    c = canvas.Canvas(outputPath, pagesize=A4)
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
    c.rect(box_center[0] - (box_width/2), box_center[1]- box_height/2, box_width, box_height, fill=1)

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
    c.rect(box_center[0] - (box_width/2), box_center[1]- box_height/2, box_width, box_height, fill=1)
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
    c.setFont("Helvetica-Bold", 12)
    c.drawString(lLeft, height - 5.8 * cm, f"{data['negocio']['nombre']}")
    c.setFont("Helvetica", 12)
    c.drawString(lLeft, height - 6.6 * cm, f"E-mail: {data['negocio']['correo']}")
    c.drawString(lLeft, height - 7.4 * cm, f"Telefono: {data['negocio']['telefono']}")

    currentY = height - 7.4 * cm
    currentY -= cm *1.3
    #--------------------nombres columnas-----------------#
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1.5 * cm, currentY , "Cant.")
    c.drawString(3.3 * cm, currentY , "Unidad")
    c.drawString(5.5 * cm, currentY , "Codigo")
    c.drawString(8 * cm, currentY , "Descripcion")
    c.drawString(17.5 * cm, currentY , "P.U.")
    c.drawString(19 * cm, currentY , "Total")

    # Draw table content (items)
    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, height - 11.5 * cm, "1.00     Unidad   MF465    Mochila de Negocios de Gran Capacidad de 15.6 Pulgadas  150.00   150.00")
    c.drawString(2 * cm, height - 12.1 * cm, "1.00     Unidad   WPddj    Whisky Premium Blue Label de 750 ml, Edición Exclusiva  777.00   777.00")

    # Draw subtotal, IGV, total
    c.drawString(14 * cm, height - 13.5 * cm, "SUBTOTAL")
    c.drawString(16 * cm, height - 13.5 * cm, "785.59")
    c.drawString(14 * cm, height - 14.1 * cm, "I.G.V.")
    c.drawString(16 * cm, height - 14.1 * cm, "141.41")
    c.drawString(14 * cm, height - 14.7 * cm, "TOTAL")
    c.drawString(16 * cm, height - 14.7 * cm, "927.00")

    # Draw "IMPORTE EN LETRAS"
    c.drawString(2 * cm, height - 15.9 * cm, "IMPORTE EN LETRAS:  NOVECIENTOS VEINTE Y SIETE CON 20/100 SOLES")

    # Draw "RESUMEN"
    c.drawString(2 * cm, height - 16.5 * cm, "RESUMEN: hJ8hSHOAndV0Ex0gPnDtaNyIVTI=")

    # Draw "Observaciones" and payment method
    c.drawString(2 * cm, height - 17.7 * cm, "Observaciones:")
    c.drawString(2 * cm, height - 18.3 * cm, "Forma de pago: Contado")

    # Draw footer
    c.drawString(2 * cm, height - 19.5 * cm, "Representación impresa de la Boleta de Venta electrónica. Consulte su documento en https://consulta.quikcart.com")

    # Save the PDF
    c.save()

# Generate the PDF

if __name__ == '__main__':

    data = {
        'cabecera': {
        'rucEmisor': "R.U.C. N° 10123456789",
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
        
        'items' : {
            [1, 'Unidad', 'MF465', 'Mochila de Negocios de Gran Capacidad de 15.6 Pulgadas', 150],
            [1, 'Unidad', 'WPddj', 'Whisky Premium Blue Label de 750 ml, Edición Exclusiva', 777],
        },
        
        
        
    }

    generate_pdf("boleta_venta_electronica.pdf", "pdf/scripts/logo.png", data)
