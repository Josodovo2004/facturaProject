import os, zipfile, base64


def zip_and_encode_base64(xml_file_path: str):
    nombrexml = xml_file_path.split('/')[-1]  # Extract the XML file name from the path
    carpetaxml = f'xml/{nombrexml.replace('.xml', '')}'  # Path to the directory containing the XML file
    rutaxml = os.path.join(carpetaxml, nombrexml)
    nombrezip = nombrexml.replace('.xml', '.zip')
    # Ensure the folder exists
    os.makedirs(carpetaxml, exist_ok=True)
    rutazip = os.path.join(carpetaxml, nombrezip)

    # Step 03: Zip the XML file
    with zipfile.ZipFile(rutazip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(rutaxml, arcname=nombrexml)

    # Step 04: Prepare the message to send to SUNAT (Envelope)
    with open(rutazip, 'rb') as f:
        contenido_del_zip = base64.b64encode(f.read()).decode('utf-8')

    return contenido_del_zip