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
    pdf_data["total"]['subtotal'] = 0
    
    for item in data['items']:
        pdf_data['items'].append([item['CantidadUnidadesItem'], item['unidadMedida'], item['codProducto'], item['descripcion'], item['totalValorVenta'] + item['totalTax']])
        pdf_data["total"]['subtotal'] += item['totalValorVenta']
        tax: dict = item['tax']
        for value in tax.keys():
            if value not in pdf_data['total'].keys():
                pdf_data["total"][value] = tax[value]['MontoTotalImpuesto']
            else:
                pdf_data["total"][value] += tax[value]['MontoTotalImpuesto']
    
    print(pdf_data['items'])
        
    pdf_data['total']['total'] = 0        
    for value in pdf_data["total"].values():
        pdf_data['total']['total'] += value
        
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
    
    if tipoPDF == 'A4':
        s3_key = f"media/{data['emisor']['DocumentoEmisor']}/reportes/{data['comprobante']['serieDocumento']}-{data['comprobante']['numeroDocumento']}-A4.pdf"
        url_pdf = generate_pdf('qickartbucket', s3_key,data['image_path'], pdf_data)
    else: 
        s3_key = f"media/{data['emisor']['DocumentoEmisor']}/reportes/{data['comprobante']['serieDocumento']}-{data['comprobante']['numeroDocumento']}-Ticket.pdf"
        url_pdf = generate_ticket('qickartbucket', s3_key,data['image_path'], pdf_data)
    
    return Response(url_pdf)

