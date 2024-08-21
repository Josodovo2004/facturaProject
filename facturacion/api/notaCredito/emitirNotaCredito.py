from lxml import etree as ET
import xmlsec
from django.http import JsonResponse
from facturacion.api.getpfx import extract_pfx_details
from facturacion.api.comprobantes.dxmlFromString import dxmlFromString
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from datetime import timedelta
from facturacion.zip_and_encode_base64 import zip_and_encode_base64
from facturacion.modify_xml import modify_xml
from facturacion.xml_envio import envio_xml
from facturacion.api.consultarTicket import consultarTicket
import base64
import io
import os
import xmlsec
import requests
from facturacion.models import Comprobante, Entidad, Item, ItemImpuesto, ComprobanteItem
import zipfile
import io
from .notaCreditoStringAnulacion import stringNotaCreditoAnulacion

def emitirNotaCredito(request):
    idComprobante = request.GET.get('comprobante_id')
    comprobante: Comprobante = Comprobante.objects.filter(id = idComprobante).first()

    emisor: Entidad = comprobante.emisor
    adquiriente: Entidad = comprobante.adquiriente
    ItemsComprobante = ComprobanteItem.objects.filter(comprobante_id = comprobante.id)


    emisorDict = {
        "DocumentoEmisor": emisor.numeroDocumento,
        "RazonSocialEmisor": emisor.razonSocial,
        "NombreComercialEmisor": emisor.nombreComercial,
        "ubigeo": emisor.ubigeo.codigo,
        "codigoPais": emisor.codigoPais.codigo,
        "usuarioSol": emisor.usuarioSol,
        "claveSol": emisor.claveSol,
        "TipoDocumento": emisor.tipoDocumento.codigo,  # Assuming 6 is for RUC
        "provincia" : emisor.ubigeo.provincia,
        "departamento" : emisor.ubigeo.departamento,
        "distrito" : emisor.ubigeo.distrito,
        "calle" : emisor.direccion,	
        }
    

    adquirienteDict = {
        "TipoDocumentoAdquiriente": adquiriente.tipoDocumento.codigo,  # Assuming 6 is for RUC
        "NumeroDocumentoAdquiriente": adquiriente.numeroDocumento,
        "razonSocial": adquiriente.razonSocial,
        'CalleComprador' : adquiriente.direccion,
        'distritoComprador' : adquiriente.ubigeo.distrito,
        'departamentoComprador' : adquiriente.ubigeo.departamento,
        'provinciaComprador' : adquiriente.ubigeo.provincia,
        }
    

    itemsDict = []

    taxesDict = {}
    numItems = 0
    taxTotal = 0
    totalOperacionesGravadas = 0
    totalValorSinImpuestos = 0

    for item in ItemsComprobante:
        item : ComprobanteItem
        itemTax = ItemImpuesto.objects.filter(item_id = item.item.id)
        tax = {}
        
        taxTotalitem = 0

        for impuesto in itemTax:
            impuesto: ItemImpuesto
            tax[f'{impuesto.impuesto.nombre}'] = {
                'MontoTotalImpuesto': round((impuesto.porcentaje/100) * impuesto.valorGravado * item.cantidad,2),  # Total del IGV aplicado
                "tasaImpuesto": impuesto.porcentaje,  # Tasa del IGV en porcentaje
                "operacionesGravadas": impuesto.valorGravado * item.cantidad,  # Total de operaciones gravadas sujetas a IGV
                'cod1' : impuesto.impuesto.codigo,
                'cod2' : impuesto.impuesto.nombre,
                'cod3' : impuesto.impuesto.un_ece_5153,
            }
            taxTotal += (impuesto.porcentaje/100) * impuesto.valorGravado * item.cantidad
            taxTotalitem += (impuesto.porcentaje/100) * impuesto.valorGravado * item.cantidad
            totalOperacionesGravadas += impuesto.valorGravado * item.cantidad
            

            if f'{impuesto.impuesto.nombre}' in taxesDict:
                taxesDict[f'{impuesto.impuesto.nombre}']['MontoTotalImpuesto'] += round((impuesto.porcentaje/100) * impuesto.valorGravado * item.cantidad, 2)
                taxesDict[f'{impuesto.impuesto.nombre}']["operacionesGravadas"] += round(impuesto.valorGravado * item.cantidad,2)
            else:
                taxesDict[f'{impuesto.impuesto.nombre}'] = {
                'MontoTotalImpuesto': round((impuesto.porcentaje/100) * impuesto.valorGravado * item.cantidad,2),  # Total del IGV aplicado
                "tasaImpuesto": impuesto.porcentaje,  # Tasa del IGV en porcentaje
                "operacionesGravadas": round(impuesto.valorGravado * item.cantidad,2),  # Total de operaciones gravadas sujetas a IGV
                'cod1' : impuesto.impuesto.codigo,
                'cod2' : impuesto.impuesto.nombre,
                'cod3' : impuesto.impuesto.un_ece_5153,
                'cod4' : impuesto.impuesto.un_ece_5305,
            }

        itemsDict.append({
            "unidadMedida": item.item.unidadMedida.codigo,  # Assuming NIU for product unit
            'CantidadUnidadesItem': item.cantidad,
            "id": item.item.id,
            'NombreItem': item.item.nombre,
            'DescripcionItem': item.item.descripcion,
            "tipoPrecio": item.item.tipoPrecio.codigo,  # Assuming 01 is for unit price with taxes
            'precioUnitario' :item.item.valorUnitario,  
            'precioUnitarioConImpuestos':item.item.valorUnitario + (taxTotalitem/item.cantidad),
            "totalValorVenta": round(item.item.valorUnitario*item.cantidad,2),
            'ValorVentaItem': round(((item.item.valorUnitario) *item.cantidad) + taxTotalitem,2),
            'totalTax': round(taxTotalitem,2),
            'tax' : tax,
            })
    
        numItems += item.cantidad
        totalValorSinImpuestos += item.item.valorUnitario*item.cantidad

    comprobanteDict = {
        "serieDocumento": str(comprobante.serie).replace('F0', 'FN'),
        "numeroDocumento": comprobante.numeroComprobante,
        "fechaEmision": comprobante.fechaEmision,
        "DueDate" : comprobante.fechaEmision + timedelta(weeks=1),
        "codigoMoneda": comprobante.codigoMoneda.codigo,
        "tipoComprobante" : '07',  
        'ImporteTotalVenta': round(totalValorSinImpuestos,2),
        'MontoTotalImpuestos': round(taxTotal,2),
        "totalConImpuestos" : round(totalValorSinImpuestos + taxTotal,2),
        'cantidadItems' : numItems,
    }

    referencia = {
        "serieDocumento": comprobante.serie,
        "numeroDocumento": comprobante.numeroComprobante,
        "tipoComprobante": comprobante.tipoComprobante.codigo  
    }


    data = {'emisor': emisorDict, 'adquiriente' : adquirienteDict, 'comprobante' : comprobanteDict, 'taxes': taxesDict, 'Items' : itemsDict, 'documentoRelacionado': referencia}

    fileName = f'{emisor.numeroDocumento}-07-{(comprobante.serie).replace('F0', 'FN')}-{comprobante.numeroComprobante}.xml'

    #generamos la nota de credito y obtenemos su path
    filePath = stringNotaCreditoAnulacion(data, fileName)

    modify_xml(filePath)

    print(filePath)

    encodedZip = zip_and_encode_base64(filePath)

    #obtener la respuesta de sunat
    response = envio_xml(comprobante, fileName, encodedZip, True)

    zipData = base64.b64decode(encodedZip)

    with open("decoded_file.zip", "wb") as file:
        file.write(zipData)

    print(response.content)

    if response.status_code == 200:
        try:
            # Parse the XML response using lxml
            root = ET.fromstring(response.content)

            # Find the element that contains the base64 encoded content
            application_response_element = root.find('.//{*}applicationResponse')
            
            if application_response_element is not None:
                # Decode the base64 content
                decoded_content = base64.b64decode(application_response_element.text)

                # Verify if the decoded content starts with the ZIP file signature
                if decoded_content.startswith(b'PK'):
                    try:
                        # Create a BytesIO object to treat the bytes as a file
                        file_like_object = io.BytesIO(decoded_content)

                        # Open the ZIP file
                        with zipfile.ZipFile(file_like_object, 'r') as zip_ref:
                            # List all the contents in the ZIP file
                            zip_ref.printdir()

                            # Extract all the files to the specified directory
                            zip_ref.extractall('facturacion/api/response')

                            responseFile: ET = ET.parse(f'facturacion/api/response/R-{fileName}')

                            namespaces = {'cbc' : 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}

                            response_code = responseFile.findtext('.//cbc:ResponseCode', namespaces=namespaces)
                            description = responseFile.findtext('.//cbc:Description', namespaces=namespaces)

                        # Return a success message as a JSON response
                            if response_code == '0':
                                return JsonResponse({'message': 'Comprobante aceptado'})
                            else:
                                return JsonResponse({'error': f'{response_code}', 'descripcion': f'{description}'})
                    except zipfile.BadZipFile:
                        return JsonResponse({'error': 'The file is not a valid ZIP file.'}, status=400)
                else:
                    return JsonResponse({'error': 'Decoded content does not appear to be a ZIP file.'}, status=400)
            else:
                print(response.content)
                return JsonResponse({'error': "applicationResponse element not found in the XML."}, status=500)
            
        except ET.XMLSyntaxError as e:
            return JsonResponse({'error': f"Failed to parse XML: {e}"}, status=500)
    else:
        return JsonResponse({'error': f"HTTP request failed with status code {response.status_code}"}, status=response.status_code)