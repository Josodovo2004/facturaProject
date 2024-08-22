import xmlsec
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import serialization
import base64
from lxml import etree as ET

def modify_xml(file_path):
    try:
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
    except Exception as e:
        print(e)