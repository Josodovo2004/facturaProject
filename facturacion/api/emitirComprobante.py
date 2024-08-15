from lxml import etree as ET
import xmlsec
from django.http import JsonResponse
from facturacion.api.getpfx import extract_pfx_details
from facturacion.api.dxmlFromString import dxmlFromString
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from datetime import timedelta
import io
import zipfile
import base64
import os
import xmlsec
import requests
from facturacion.models import Comprobante, Entidad, Item, ItemImpuesto, ComprobanteItem
import zipfile
import io

def modify_xml(file_path):

    pfx_path = "facturacion/api/certificate/certificado.pfx"  # Replace with your .pfx file path
    pfx_password = b'Jose_d@vid2004'  # Replace with your .pfx password

    with open(pfx_path, "rb") as pfx_file:
        pfx_data = pfx_file.read()

    # Extract the certificate and private key
    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(pfx_data, pfx_password)

    # Read the XML file into a string
    with open(file_path, 'rb') as file:
        xml_string = file.read()


    # Parse the XML string using lxml.etree
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return

    # Create a KeysManager and add the key and certificate
    ctx = xmlsec.KeysManager()
    key = xmlsec.Key.from_memory(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ),
        xmlsec.KeyFormat.PEM,
        None
    )
    ctx.add_key(key)

    # Create a signature template
    signature_node = xmlsec.template.create(
        root, xmlsec.Transform.EXCL_C14N, xmlsec.Transform.RSA_SHA1, ns="ds"
    )

    # Add a reference to the document and apply transforms
    ref = xmlsec.template.add_reference(
        signature_node, xmlsec.Transform.SHA1
    )
    ref.set('URI', "")
    xmlsec.template.add_transform(ref, xmlsec.Transform.ENVELOPED)

    # Add KeyInfo and X509Data
    key_info = xmlsec.template.ensure_key_info(signature_node)
    x509_data = xmlsec.template.add_x509_data(key_info)
    
    # Add X509Certificate within X509Data
    x509_certificate = ET.SubElement(x509_data, '{http://www.w3.org/2000/09/xmldsig#}X509Certificate')
    x509_certificate.text = base64.b64encode(certificate.public_bytes(serialization.Encoding.DER)).decode('ascii')

    # Append the signature to the specified element
    doc_element = root.findall('.//{urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2}ExtensionContent')[0]
    doc_element.append(signature_node)

    # Sign the document
    sign_ctx = xmlsec.SignatureContext(ctx)
    sign_ctx.key = key
    sign_ctx.sign(signature_node)

    # Set the ID attribute for the Signature element
    signature_node.set('Id', 'SignatureSP')

    # Save the signed XML document back to the file
    with open(file_path, 'wb') as file:
        file.write(ET.tostring(root, pretty_print=True))


def zip_and_encode_base64(xml_file_path: str):
    nombrexml = xml_file_path.split('/')[1]  # Extract the XML file name from the path
    carpetaxml = 'xml/'  # Path to the directory containing the XML file
    rutaxml = os.path.join(carpetaxml, nombrexml)
    nombrezip = nombrexml.replace('.xml', '.zip')
    rutazip = os.path.join(carpetaxml, nombrezip)

    # Step 03: Zip the XML file
    with zipfile.ZipFile(rutazip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(rutaxml, arcname=nombrexml)

    # Step 04: Prepare the message to send to SUNAT (Envelope)
    with open(rutazip, 'rb') as f:
        contenido_del_zip = base64.b64encode(f.read()).decode('utf-8')

    return contenido_del_zip

def emitirComprobanteAPI(request):
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

    for value in itemsDict:
        value : dict
        for key,item in value.items():
            print(f'{key}:{item}')


    comprobanteDict = {
        "serieDocumento": comprobante.serie,
        "numeroDocumento": comprobante.numeroComprobante,
        "fechaEmision": comprobante.fechaEmision,
        "DueDate" : comprobante.fechaEmision + timedelta(weeks=1),
        "codigoMoneda": comprobante.codigoMoneda.codigo,
        "tipoComprobante" : comprobante.tipoComprobante.codigo,  
        'ImporteTotalVenta': round(totalValorSinImpuestos,2),
        'MontoTotalImpuestos': round(taxTotal,2),
        "totalOperacionesGravadas": round(totalOperacionesGravadas,2),
        "totalOperacionesExoneradas": round(totalValorSinImpuestos - totalOperacionesGravadas, 2),
        "totalOperacionesInafectas": '0.00',
        "totalConImpuestos" : round(totalValorSinImpuestos + taxTotal,2),
        'cantidadItems' : numItems,
    }


    data = {'emisor': emisorDict, 'adquiriente' : adquirienteDict, 'comprobante' : comprobanteDict, 'taxes': taxesDict, 'Items' : itemsDict}

    fileName = f'{emisor.numeroDocumento}-{comprobante.tipoComprobante.codigo}-{comprobante.serie}-{comprobante.numeroComprobante}.xml'

    filePath = dxmlFromString(data, fileName)

    pfx_path = "facturacion/api/certificate/certificado.pfx"  
    pfx_password = b'Jose_d@vid2004' 

    with open(pfx_path, "rb") as pfx_file:
        pfx_data = pfx_file.read()

    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(pfx_data, pfx_password)
    
    modify_xml(filePath)

    encodedZip = zip_and_encode_base64(filePath)

    xml_envio =f'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
        xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://service.sunat.gob.pe" 
        xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
     <soapenv:Header>
            <wsse:Security>
                <wsse:UsernameToken>
                    <wsse:Username>{emisor.numeroDocumento}{emisor.usuarioSol}</wsse:Username>
	<wsse:Password>{emisor.claveSol}</wsse:Password>
                </wsse:UsernameToken>
           </wsse:Security>
 </soapenv:Header>
 <soapenv:Body>
	<ser:sendBill>
		<fileName>{filePath.replace(".xml", ".ZIP").split('/')[1]}</fileName>
		<contentFile>{encodedZip}</contentFile>
	</ser:sendBill>
 </soapenv:Body>
</soapenv:Envelope>'''
    
        # The web service URL
    ws = "https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService"

    # Headers
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "Accept": "text/xml",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "SOAPAction": "",
        "Content-Length": str(len(xml_envio))

    }

    zipData = base64.b64decode(encodedZip)

    with open("decoded_file.zip", "wb") as file:
        file.write(zipData)

    # SSL verification (use your .pfk file here)
    certPath = "facturacion/api/certificate/certificado.pfx"  # Replace with your .pfk file path

    # Check if the certificate file exists
    if not os.path.isfile(certPath):
        raise FileNotFoundError(f"Certificate file not found: {certPath}")

    # Path to the CA bundle
    ca_bundle_path = "facturacion/api/certificate/cacert.pem"  # Replace with the path to your cacert.pem file



    # Send the request
    response = requests.post(url=ws, data=xml_envio, headers=headers, verify=ca_bundle_path)


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

                        # Return a success message as a JSON response
                        return JsonResponse({'message': 'ZIP file processed and extracted successfully.'})
                    except zipfile.BadZipFile:
                        return JsonResponse({'error': 'The file is not a valid ZIP file.'}, status=400)
                else:
                    return JsonResponse({'error': 'Decoded content does not appear to be a ZIP file.'}, status=400)
            else:
                return JsonResponse({'error': "applicationResponse element not found in the XML."}, status=500)
            
        except ET.XMLSyntaxError as e:
            return JsonResponse({'error': f"Failed to parse XML: {e}"}, status=500)
    else:
        return JsonResponse({'error': f"HTTP request failed with status code {response.status_code}"}, status=response.status_code)