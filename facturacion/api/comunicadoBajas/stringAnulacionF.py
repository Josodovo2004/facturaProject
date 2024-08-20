import os

def stringAnulacionF(data : dict, fileName : str) -> str:
    try:
        comprobante = data['comunicado']
        emisor = data['emisor']
        facturaAAnular = data['comprobante']

        ubl = f'''
            <ext:UBLExtensions>
            <ext:UBLExtension>
                <ext:ExtensionContent/>
            </ext:UBLExtension>
        </ext:UBLExtensions>
        <cbc:UBLVersionID>2.0</cbc:UBLVersionID>
        <cbc:CustomizationID>1.0</cbc:CustomizationID>
        <cbc:ID>{comprobante["id"]}</cbc:ID>
        <cbc:ReferenceDate>{facturaAAnular["fecha"]}</cbc:ReferenceDate>
        <cbc:IssueDate>{comprobante["fecha"]}</cbc:IssueDate>            
    '''
        signature = f'''
        <cac:Signature>
            <cbc:ID>{emisor["documento"]}</cbc:ID>
            <cac:SignatoryParty>
            <cac:PartyIdentification>
                <cbc:ID>{emisor["documento"]}</cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyName>
                <cbc:Name><![CDATA[{emisor["RazonSocial"]}]]></cbc:Name>
            </cac:PartyName>
            </cac:SignatoryParty>
            <cac:DigitalSignatureAttachment>
            <cac:ExternalReference>
                <cbc:URI>#SignatureSP</cbc:URI>
            </cac:ExternalReference>
            </cac:DigitalSignatureAttachment>
        </cac:Signature>
    '''
        datosEmisor = f'''
        <cac:AccountingSupplierParty>
            <cbc:CustomerAssignedAccountID>{emisor["documento"]}</cbc:CustomerAssignedAccountID>
            <cbc:AdditionalAccountID>{emisor["tipoDocumento"]}</cbc:AdditionalAccountID>
            <cac:Party>
                <cac:PartyLegalEntity>
                    <cbc:RegistrationName><![CDATA[{emisor["RazonSocial"]}]]></cbc:RegistrationName>
                </cac:PartyLegalEntity>
            </cac:Party>
        </cac:AccountingSupplierParty>
    '''  

        datosFacturaAAnular = F'''
        <sac:VoidedDocumentsLine>
            <cbc:LineID>1</cbc:LineID>
            <cbc:DocumentTypeCode>{facturaAAnular["tipoDocumento"]}</cbc:DocumentTypeCode>
            <sac:DocumentSerialID>{facturaAAnular["serie"]}</sac:DocumentSerialID>
            <sac:DocumentNumberID>{facturaAAnular["numero"]}</sac:DocumentNumberID>
            <sac:VoidReasonDescription><![CDATA[{facturaAAnular["motivo"]}]]></sac:VoidReasonDescription>
        </sac:VoidedDocumentsLine>
    '''
        body = ubl + signature + datosEmisor + datosFacturaAAnular
        base = f'''<?xml version="1.0" encoding="ISO-8859-1" standalone="no"?>
        <VoidedDocuments xmlns="urn:sunat:names:specification:ubl:peru:schema:xsd:VoidedDocuments-1" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2" xmlns:sac="urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
        {body}
        </VoidedDocuments>'''


        folder_path = f"xml/{fileName.replace('.xml', '')}"

        os.makedirs(folder_path, exist_ok=True)

        with open(f'{folder_path}/{fileName}', 'w', encoding='ISO-8859-1') as file:
            file.write(base)

        return f'{folder_path}/{fileName}'
    except Exception as e:
        print(e)