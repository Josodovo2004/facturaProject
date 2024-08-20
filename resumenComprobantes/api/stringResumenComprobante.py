

def stringResumenComprobante(data):

    cabecera = data['cabecera']
    emisor = data['emisor']
    documentos = data['documentos']
    

    xml = f'''<?xml version="1.0" encoding="iso-8859-1" standalone="no"?>
<SummaryDocuments xmlns="urn:sunat:names:specification:ubl:peru:schema:xsd:SummaryDocuments-1" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2" xmlns:sac="urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1" xmlns:qdt="urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2" xmlns:udt="urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2">
    <ext:UBLExtensions>
        <ext:UBLExtension>
            <ext:ExtensionContent/>
        </ext:UBLExtension>
    </ext:UBLExtensions>
    <cbc:UBLVersionID>2.0</cbc:UBLVersionID>
    <cbc:CustomizationID>1.1</cbc:CustomizationID>
    <cbc:ID>{cabecera['tipo_comprobante']}-{cabecera['serie']}-{cabecera['correlativo']}</cbc:ID>
    <cbc:ReferenceDate>{cabecera['fecha_referencia']}</cbc:ReferenceDate>
    <cbc:IssueDate>{cabecera['fecha_envio']}</cbc:IssueDate>
    <cac:Signature>
        <cbc:ID>{cabecera['tipo_comprobante']}-{cabecera['serie']}-{cabecera['correlativo']}</cbc:ID>
        <cac:SignatoryParty>
            <cac:PartyIdentification>
                <cbc:ID>{emisor['ruc']}</cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyName>
                <cbc:Name><![CDATA[{emisor['razon_social']}]]></cbc:Name>
            </cac:PartyName>
        </cac:SignatoryParty>
        <cac:DigitalSignatureAttachment>
            <cac:ExternalReference>
                <cbc:URI>{cabecera['tipo_comprobante']}-{cabecera['serie']}-{cabecera['correlativo']}</cbc:URI>
            </cac:ExternalReference>
        </cac:DigitalSignatureAttachment>
    </cac:Signature>
    <cac:AccountingSupplierParty>
        <cbc:CustomerAssignedAccountID>{emisor['ruc']}</cbc:CustomerAssignedAccountID>
        <cbc:AdditionalAccountID>6</cbc:AdditionalAccountID>
        <cac:Party>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName><![CDATA[{emisor['razon_social']}]]></cbc:RegistrationName>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:AccountingSupplierParty>'''

    for i, documento in enumerate(documentos, start=1):
        xml += f'''
        <sac:SummaryDocumentsLine>
            <cbc:LineID>{i}</cbc:LineID>
            <cbc:DocumentTypeCode>{documento['document_type_code']}</cbc:DocumentTypeCode>
            <cbc:ID>{documento['id']}</cbc:ID>
            <cac:Status>
                <cbc:ConditionCode>{documento['condition_code']}</cbc:ConditionCode>
            </cac:Status>
            <sac:TotalAmount currencyID="{documento['currency']}">{documento['total_amount']}</sac:TotalAmount>
            <sac:BillingPayment>
                <cbc:PaidAmount currencyID="{documento['currency']}">{documento['paid_amount']}</cbc:PaidAmount>
                <cbc:InstructionID>{documento['instruction_id']}</cbc:InstructionID>
            </sac:BillingPayment>
            <cac:TaxTotal>
                <cbc:TaxAmount currencyID="{documento['currency']}">{documento['tax_amount']}</cbc:TaxAmount>
                <cac:TaxSubtotal>
                    <cbc:TaxAmount currencyID="{documento['currency']}">{documento['tax_amount']}</cbc:TaxAmount>
                    <cac:TaxCategory>
                        <cac:TaxScheme>
                            <cbc:ID>{documento['tax_scheme']['id']}</cbc:ID>
                            <cbc:Name>{documento['tax_scheme']['name']}</cbc:Name>
                            <cbc:TaxTypeCode>{documento['tax_scheme']['tax_type_code']}</cbc:TaxTypeCode>
                        </cac:TaxScheme>
                    </cac:TaxCategory>
                </cac:TaxSubtotal>
            </cac:TaxTotal>
        </sac:SummaryDocumentsLine>'''

    xml += '''
    </SummaryDocuments>'''