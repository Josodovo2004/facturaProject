

def emitirNotaCredito(data):

    emisor = data["emisor"]
    cabecera = data["cabecera"]
    cliente = data["cliente"]
    items = data["items"]


    nombrexml = f"{emisor['ruc']}-{cabecera['tipo_comprobante']}-{cabecera['serie']}-{cabecera['correlativo']}"

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <CreditNote xmlns="urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:ccts="urn:un:unece:uncefact:documentation:2" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2" xmlns:qdt="urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2" xmlns:sac="urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1" xmlns:udt="urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <ext:UBLExtensions>
            <ext:UBLExtension>
                <ext:ExtensionContent/>
            </ext:UBLExtension>
        </ext:UBLExtensions>
        <cbc:UBLVersionID>2.1</cbc:UBLVersionID>
        <cbc:CustomizationID>2.0</cbc:CustomizationID>
        <cbc:ID>{cabecera['serie']}-{cabecera['correlativo']}</cbc:ID>
        <cbc:IssueDate>{cabecera['fecha_emision']}</cbc:IssueDate>
        <cbc:IssueTime>00:00:00</cbc:IssueTime>
        <cbc:DocumentCurrencyCode>{cabecera['moneda']}</cbc:DocumentCurrencyCode>
        <cac:DiscrepancyResponse>
            <cbc:ReferenceID>{cabecera['serie_comp_ref']}-{cabecera['correlativo_comp_ref']}</cbc:ReferenceID>
            <cbc:ResponseCode>{cabecera['codigo_motivo']}</cbc:ResponseCode>
            <cbc:Description><![CDATA[{cabecera['descripcion_motivo']}]]></cbc:Description>
        </cac:DiscrepancyResponse>
        <cac:BillingReference>
            <cac:InvoiceDocumentReference>
                <cbc:ID>{cabecera['serie_comp_ref']}-{cabecera['correlativo_comp_ref']}</cbc:ID>
                <cbc:DocumentTypeCode>{cabecera['tipo_comp_ref']}</cbc:DocumentTypeCode>
            </cac:InvoiceDocumentReference>
        </cac:BillingReference>
        <cac:Signature>
            <cbc:ID>IDSignST</cbc:ID>
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
                    <cbc:URI>#SignatureSP</cbc:URI>
                </cac:ExternalReference>
            </cac:DigitalSignatureAttachment>
        </cac:Signature>
        <cac:AccountingSupplierParty>
            <cac:Party>
                <cac:PartyIdentification>
                    <cbc:ID schemeID="6" schemeAgencyName="PE:SUNAT" schemeURI="urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo06">{emisor['ruc']}</cbc:ID>
                </cac:PartyIdentification>
                <cac:PartyName>
                    <cbc:Name><![CDATA[{emisor['razon_social']}]]></cbc:Name>
                </cac:PartyName>
                <cac:PartyLegalEntity>
                    <cbc:RegistrationName><![CDATA[{emisor['razon_social']}]]></cbc:RegistrationName>
                    <cac:RegistrationAddress>
                        <cbc:AddressTypeCode>{cabecera['anexo_sucursal']}</cbc:AddressTypeCode>
                    </cac:RegistrationAddress>
                </cac:PartyLegalEntity>
            </cac:Party>
        </cac:AccountingSupplierParty>
        <cac:AccountingCustomerParty>
            <cac:Party>
                <cac:PartyIdentification>
                    <cbc:ID schemeID="{cliente['tipo_documento']}" schemeAgencyName="PE:SUNAT" schemeURI="urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo06">{cliente['ruc']}</cbc:ID>
                </cac:PartyIdentification>
                <cac:PartyLegalEntity>
                    <cbc:RegistrationName><![CDATA[{cliente['razon_social']}]]></cbc:RegistrationName>
                </cac:PartyLegalEntity>
            </cac:Party>
        </cac:AccountingCustomerParty>
        <cac:TaxTotal>
            <cbc:TaxAmount currencyID="{cabecera['moneda']}">{cabecera['total_impuestos']}</cbc:TaxAmount>
            <cac:TaxSubtotal>
            <cbc:TaxableAmount currencyID="{cabecera['moneda']}">{cabecera['total_op_gravadas']}</cbc:TaxableAmount>
            <cbc:TaxAmount currencyID="{cabecera['moneda']}">{cabecera['igv']}</cbc:TaxAmount>
            <cac:TaxCategory>
                <cbc:ID schemeID="UN/ECE 5305" schemeName="Tax Category Identifier" schemeAgencyName="United Nations Economic Commission for Europe">S</cbc:ID>
                <cac:TaxScheme>
                    <cbc:ID schemeID="UN/ECE 5153" schemeAgencyID="6">1000</cbc:ID>
                    <cbc:Name>IGV</cbc:Name>
                    <cbc:TaxTypeCode>VAT</cbc:TaxTypeCode>
                </cac:TaxScheme>
            </cac:TaxCategory>
            </cac:TaxSubtotal>"""

    # Add conditional tax subtotals based on the PHP code logic
    if float(cabecera['total_op_exoneradas']) > 0:
        xml += f"""
            <cac:TaxSubtotal>
                <cbc:TaxableAmount currencyID="{cabecera['moneda']}">{cabecera['total_op_exoneradas']}</cbc:TaxableAmount>
                <cbc:TaxAmount currencyID="{cabecera['moneda']}">0.00</cbc:TaxAmount>
                <cac:TaxCategory>
                    <cbc:ID schemeID="UN/ECE 5305" schemeName="Tax Category Identifier" schemeAgencyName="United Nations Economic Commission for Europe">E</cbc:ID>
                    <cac:TaxScheme>
                        <cbc:ID schemeID="UN/ECE 5153" schemeAgencyID="6">9997</cbc:ID>
                        <cbc:Name>EXO</cbc:Name>
                        <cbc:TaxTypeCode>VAT</cbc:TaxTypeCode>
                    </cac:TaxScheme>
                </cac:TaxCategory>
            </cac:TaxSubtotal>"""

    if float(cabecera['total_op_inafectas']) > 0:
        xml += f"""
            <cac:TaxSubtotal>
                <cbc:TaxableAmount currencyID="{cabecera['moneda']}">{cabecera['total_op_inafectas']}</cbc:TaxableAmount>
                <cbc:TaxAmount currencyID="{cabecera['moneda']}">0.00</cbc:TaxAmount>
                <cac:TaxCategory>
                    <cbc:ID schemeID="UN/ECE 5305" schemeName="Tax Category Identifier" schemeAgencyName="United Nations Economic Commission for Europe">O</cbc:ID>
                    <cac:TaxScheme>
                        <cbc:ID schemeID="UN/ECE 5153" schemeAgencyID="6">9998</cbc:ID>
                        <cbc:Name>INA</cbc:Name>
                        <cbc:TaxTypeCode>FRE</cbc:TaxTypeCode>
                    </cac:TaxScheme>
                </cac:TaxCategory>
            </cac:TaxSubtotal>"""

    if float(cabecera['icbper']) > 0:
        xml += f"""
            <cac:TaxSubtotal>
                <cbc:TaxableAmount currencyID="{cabecera['moneda']}">0.00</cbc:TaxableAmount>
                <cbc:TaxAmount currencyID="{cabecera['moneda']}">{cabecera['icbper']}</cbc:TaxAmount>
                <cac:TaxCategory>
                    <cbc:ID schemeID="UN/ECE 5305" schemeName="Tax Category Identifier" schemeAgencyName="United Nations Economic Commission for Europe">S</cbc:ID>
                    <cac:TaxScheme>
                        <cbc:ID schemeID="UN/ECE 5153" schemeAgencyID="6">7152</cbc:ID>
                        <cbc:Name>ICBPER</cbc:Name>
                        <cbc:TaxTypeCode>OTH</cbc:TaxTypeCode>
                    </cac:TaxScheme>
                </cac:TaxCategory>
            </cac:TaxSubtotal>"""

    # Continue with XML
    xml += f"""
        </cac:TaxTotal>
        <cac:LegalMonetaryTotal>
            <cbc:LineExtensionAmount currencyID="{cabecera['moneda']}">{cabecera['total_op_gravadas']}</cbc:LineExtensionAmount>
            <cbc:TaxInclusiveAmount currencyID="{cabecera['moneda']}">{cabecera['total_a_pagar']}</cbc:TaxInclusiveAmount>
            <cbc:PayableAmount currencyID="{cabecera['moneda']}">{cabecera['total_a_pagar']}</cbc:PayableAmount>
        </cac:LegalMonetaryTotal>"""

    # Loop through each item
    for item in items:
        xml += f"""
        <cac:CreditNoteLine>
            <cbc:ID>{item['item']}</cbc:ID>
            <cbc:CreditedQuantity unitCode="{item['unidad']}">{item['cantidad']}</cbc:CreditedQuantity>
            <cbc:LineExtensionAmount currencyID="{cabecera['moneda']}">{item['total_antes_impuestos']}</cbc:LineExtensionAmount>
            <cac:PricingReference>
                <cac:AlternativeConditionPrice>
                    <cbc:PriceAmount currencyID="{cabecera['moneda']}">{item['precio_lista']}</cbc:PriceAmount>
                    <cbc:PriceTypeCode>01</cbc:PriceTypeCode>
                </cac:AlternativeConditionPrice>
            </cac:PricingReference>
            <cac:TaxTotal>
                <cbc:TaxAmount currencyID="{cabecera['moneda']}">{item['total_impuestos']}</cbc:TaxAmount>
                <cac:TaxSubtotal>
                    <cbc:TaxableAmount currencyID="{cabecera['moneda']}">{item['valor_total']}</cbc:TaxableAmount>
                    <cbc:TaxAmount currencyID="{cabecera['moneda']}">{item['igv']}</cbc:TaxAmount>
                    <cac:TaxCategory>
                        <cbc:ID schemeID="UN/ECE 5305" schemeName="Tax Category Identifier" schemeAgencyName="United Nations Economic Commission for Europe">{item['codigos'][0]}</cbc:ID>
                        <cac:TaxScheme>
                            <cbc:ID schemeID="UN/ECE 5153" schemeAgencyID="6">{item['codigos'][1]}</cbc:ID>
                            <cbc:Name>{item['codigos'][2]}</cbc:Name>
                            <cbc:TaxTypeCode>{item['codigos'][4]}</cbc:TaxTypeCode>
                        </cac:TaxScheme>
                    </cac:TaxCategory>
                </cac:TaxSubtotal>"""

        if float(item['icbper']) > 0:
            xml += f"""
                <cac:TaxSubtotal>
                    <cbc:TaxAmount currencyID="{cabecera['moneda']}">{item['icbper']}</cbc:TaxAmount>
                    <cac:TaxCategory>
                        <cbc:ID schemeID="UN/ECE 5305" schemeName="Tax Category Identifier" schemeAgencyName="United Nations Economic Commission for Europe">S</cbc:ID>
                        <cac:TaxScheme>
                            <cbc:ID schemeID="UN/ECE 5153" schemeAgencyID="6">7152</cbc:ID>
                            <cbc:Name>ICBPER</cbc:Name>
                            <cbc:TaxTypeCode>OTH</cbc:TaxTypeCode>
                        </cac:TaxScheme>
                    </cac:TaxCategory>
                </cac:TaxSubtotal>"""
        xml += f"""
            </cac:TaxTotal>
            <cac:Item>
                <cbc:Description><![CDATA[DESCRIPCION PRUEBA]]></cbc:Description>
            </cac:Item>
            <cac:Price>
                <cbc:PriceAmount currencyID="{cabecera['moneda']}">{item['valor_total']}</cbc:PriceAmount>
            </cac:Price>
        </cac:CreditNoteLine>"""

    # Closing the XML
    xml += "</CreditNote>"