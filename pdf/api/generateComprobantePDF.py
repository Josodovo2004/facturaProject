from pdf.scripts.comprobanteA4 import generate_pdf
from pdf.scripts.comprobanteTicket import generate_ticket
import json
from datetime import date
from facturacion.api.comprobantes.emitirComprobante import emitirComprobanteAPI
from rest_framework.request import Request
from django.http import JsonResponse
from rest_framework.response import Response



def generateComprobantePDF(request):
    data = json.loads(request.body)
    tipoPDF = data['tipo_pdf']
    
    pdf_data = {}
    
    tipoDocumento = 'FACTURA' if data['comprobante']['tipoComprobante'] == '01' else 'BOLETA DE VENTA'
    
    pdf_data['cabecera'] = {
        'rucEmisor': data['emisor']['DocumentoEmisor'],
        'tipoDocumento': tipoDocumento,
        'serieYNumero' : f"{data['comprobante']['serieDocumento']}-{data['comprobante']['numeroDocumento']}",
        }
    
    pdf_data["cabecera2"] = {
            'fecha': str(date.today()),
            'cliente': data['adquiriente']['razonSocial'],
            'dni': data['adquiriente']['NumeroDocumentoAdquiriente'],
            'direccion': data['emisor']['calle'],
        }
    
    pdf_data["negocio"] = {
            'nombre': data['emisor']["RazonSocialEmisor"],
            'correo' : data['emisor']["email"],
            'telefono': data['emisor']["telefono"],
        }
    
    pdf_data['items'] = []
    pdf_data['total'] = {}
    
    # Initialize subtotal and taxes
    subtotal = 0
    total_taxes = 0
    
    for item in data['items']:
        # Calculate item's total (value without tax)
        item_total = item['totalValorVenta']
        subtotal += item_total 
        
        # Add item to PDF data
        pdf_data['items'].append([
            item['CantidadUnidadesItem'], 
            item['unidadMedida'], 
            item['codProducto'], 
            item['descripcion'], 
            item_total  # Use the value without tax
        ])
        
        # Calculate and accumulate taxes
        tax: dict = item['tax']
        for tax_name, tax_details in tax.items():
            tax_amount = tax_details['MontoTotalImpuesto']
            total_taxes += tax_amount
            
            # Add or update tax in total
            if tax_name not in pdf_data['total']:
                pdf_data['total'][tax_name] = tax_amount
            else:
                pdf_data['total'][tax_name] += tax_amount
    
    # Set subtotal
    pdf_data['total']['subtotal'] = subtotal
    
    # Calculate total (subtotal + taxes)
    pdf_data['total']['total'] = subtotal + total_taxes
    
    if tipoDocumento == 'FACTURA':
        hashcode = emitirComprobanteAPI(data)
        if type(hashcode) == JsonResponse:
            return hashcode
        pdf_data['hashCode'] = hashcode
    else:
        pdf_data['hashCode'] = ''
        
    pdf_data['observaciones'] = data['observaciones']
    pdf_data['formaPago'] = data['formaPago']
    pdf_data['codigoQr'] = f"{data['adquiriente']['NumeroDocumentoAdquiriente']}|{data['comprobante']['tipoComprobante']}|{data['comprobante']['serieDocumento']}|{data['comprobante']['numeroDocumento']}|{data['comprobante']['ImporteTotalVenta']}|{data['comprobante']['MontoTotalImpuestos']}|{data['comprobante']['fechaEmision']}|{data['emisor']['TipoDocumento']}|{data['emisor']['DocumentoEmisor']}"
    
    print(pdf_data)
    
    if tipoPDF == 'A4':
        s3_key = f"media/{data['emisor']['DocumentoEmisor']}/reportes/{data['comprobante']['serieDocumento']}-{data['comprobante']['numeroDocumento']}-A4.pdf"
        url_pdf = generate_pdf('qickartbucket', s3_key, data['image_path'], pdf_data)
    else: 
        s3_key = f"media/{data['emisor']['DocumentoEmisor']}/reportes/{data['comprobante']['serieDocumento']}-{data['comprobante']['numeroDocumento']}-Ticket.pdf"
        url_pdf = generate_ticket('qickartbucket', s3_key, data['image_path'], pdf_data)
    
    return Response(url_pdf)