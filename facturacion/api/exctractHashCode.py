import xml.etree.ElementTree as ET

def extract_digest_value(file_path):
    
    with open(file_path, 'rb') as file:
            xml_string = file.read()

    # Parsear el XML
    root = ET.fromstring(xml_string)
    
    # Buscar el elemento DigestValue usando el namespace adecuado
    namespace = {'ds': 'http://www.w3.org/2000/09/xmldsig#'}
    digest_value_element = root.find('.//ds:DigestValue', namespace)
    
    if digest_value_element is not None:
        return digest_value_element.text
    else:
        return None