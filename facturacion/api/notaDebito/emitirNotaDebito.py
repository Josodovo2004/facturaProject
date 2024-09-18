from lxml import etree as ET
from django.http import JsonResponse
from facturacion.api.zip_and_encode_base64 import zip_and_encode_base64
from facturacion.api.modify_xml import modify_xml
from facturacion.api.xml_envio import envio_xml
import base64
import io
import zipfile
import json
from .stringNotaDebito import stringNotaDebito

def emitirNotaDedito(request):
    # Parse JSON data from the request body
    data = json.loads(request.body)
    
    emisorDict = data['emisor']
    comprobanteDict = data['comprobante']
    
    # Generate the file name based on the emisor and comprobante data
    fileName = f'{emisorDict["DocumentoEmisor"]}-08-{comprobanteDict["serieDocumento"]}-{comprobanteDict["numeroDocumento"]}.xml'
    
    # Generate the credit note XML and get its path
    filePath = stringNotaDebito(data, fileName)

    # Modify the XML if necessary
    modify_xml(filePath)

    # Encode the XML file as ZIP and Base64
    encodedZip = zip_and_encode_base64(filePath)

    # Send the XML file via SOAP request
    response = envio_xml(fileName, encodedZip, True)

    zipData = base64.b64decode(encodedZip)

    with open("decoded_file.zip", "wb") as file:
        file.write(zipData)

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

                            responseFile = ET.parse(f'facturacion/api/response/R-{fileName}')

                            namespaces = {'cbc' : 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}

                            response_code = responseFile.findtext('.//cbc:ResponseCode', namespaces=namespaces)
                            description = responseFile.findtext('.//cbc:Description', namespaces=namespaces)

                            # Return a success message as a JSON response
                            if response_code == '0':
                                return JsonResponse({'message': 'Nota de Debito aceptada'})
                            else:
                                return JsonResponse({'error': f'{response_code}', 'descripcion': f'{description}'})
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
