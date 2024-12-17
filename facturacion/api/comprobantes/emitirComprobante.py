from lxml import etree as ET
from django.http import JsonResponse
from facturacion.api.comprobantes.dxmlFromString import dxmlFromString
from facturacion.api.zip_and_encode_base64 import zip_and_encode_base64
from facturacion.api.modify_xml import modify_xml
from facturacion.api.xml_envio import envio_xml
from facturacion.api.exctractHashCode import extract_digest_value
import base64
import io
import zipfile
import json
from requests.exceptions import HTTPError, ConnectionError, Timeout
import boto3
import os

def emitirComprobanteAPI(request):
    client = boto3.client('s3')
    try:
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
        except:
            data = request    
        emisorDict = data['emisor']
        comprobanteDict = data['comprobante']
        # Generate file name
        fileName = f'{emisorDict["DocumentoEmisor"]}-{comprobanteDict["tipoComprobante"]}-{comprobanteDict["serieDocumento"]}-{comprobanteDict["numeroDocumento"]}.xml'
        print('1')
        # Construct the XML file path
        filePath = dxmlFromString(data, fileName) 
        print('2')  
        # Modify XML (if necessary)
        modify_xml(filePath)
        print('3')
        # Encode the XML file as ZIP and Base64
        encodedZip = zip_and_encode_base64(filePath)
        print('4')
        # Send the XML file via SOAP request
        try:
            response = envio_xml(fileName, encodedZip, tipo=True)
            response.raise_for_status() 
            # Raise an HTTPError for bad responses
        except (HTTPError, ConnectionError, Timeout) as e:
            return JsonResponse({'error': f"HTTP request failed: {str(e)}"}, status=500)
        print('5')
        # Handle the SOAP response
        root: ET = ET.fromstring(response.content)
        if response.status_code == 200:
            try:
                # Parse the XML response using lxml
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
                                    hashCode = extract_digest_value(filePath)
                                    try:
                                        bucket_name = 'qickartbucket'
                                        s3_key = f"media/xml/{emisorDict['DocumentoEmisor']}/{fileName}"
                                        client.upload_file(filePath, bucket_name, s3_key)
                                        print("Upload Successful")
                                    except Exception as e:
                                        print(f"Upload failed: {e}")
                                        return None

                                    # Delete the local PDF file
                                    os.remove(filePath)

                                    # Return the S3 URL
                                    
                                    return hashCode
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
            print(response.content)
            print(root.tostring())
            return JsonResponse({'error': f"HTTP request failed with status code {response.status_code}"}, status=response.status_code)
    except (json.JSONDecodeError, FileNotFoundError, KeyError, ValueError) as e:
        return JsonResponse({'error': f"Error processing request: {str(e)}"}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({'error': f"An unexpected error occurred: {str(e)}"}, status=500)
