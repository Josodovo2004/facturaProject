import os

def stringNotaCreditoAnulacion(data, fileName):

    comprobante = data["comprobante"]
    emisor = data["emisor"]
    adquiriente = data["adquiriente"]
    taxes = data["taxes"]
    items = data["Items"]
    documentoRelacionado = data["documentoRelacionado"]

    signature = f'''<?xml version="1.0" encoding="utf-8"?>
<CreditNote xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
         xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
         xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" 
         xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" 
         xmlns:ccts="urn:un:unece:uncefact:documentation:2" 
         xmlns:ds="http://www.w3.org/2000/09/xmldsig#" 
         xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2" 
         xmlns:qdt="urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2" 
         xmlns:udt="urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2" 
         xmlns="urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2">
    <ext:UBLExtensions>
        <ext:UBLExtension>
            <ext:ExtensionContent/>
        </ext:UBLExtension>
    </ext:UBLExtensions>
    <cbc:UBLVersionID>2.1</cbc:UBLVersionID>
    <cbc:CustomizationID schemeAgencyName="PE:SUNAT">2.0</cbc:CustomizationID>
    <cbc:ID>{comprobante["serieDocumento"]}-{comprobante["numeroDocumento"]}</cbc:ID>
    <cbc:IssueDate>{comprobante["fechaEmision"]}</cbc:IssueDate>
    <cbc:DocumentCurrencyCode listID="ISO 4217 Alpha" listName="Currency" 
                              listAgencyName="United Nations Economic Commission for Europe">PEN</cbc:DocumentCurrencyCode>
    <cac:DiscrepancyResponse>
        <cbc:ReferenceID>{documentoRelacionado["serieDocumento"]}-{documentoRelacionado["numeroDocumento"]}</cbc:ReferenceID>
        <cbc:ResponseCode listAgencyName="PE:SUNAT" 
                          listURI="urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo09">01</cbc:ResponseCode>
        <cbc:Description><![CDATA[Anulación de la operación]]></cbc:Description>
    </cac:DiscrepancyResponse>

    <cac:BillingReference>
        <cac:InvoiceDocumentReference>
            <cbc:ID>{documentoRelacionado["serieDocumento"]}-{documentoRelacionado["numeroDocumento"]}</cbc:ID>
            <cbc:DocumentTypeCode listAgencyName="PE:SUNAT" 
                                  listName="Tipo de Documento" 
                                  listURI="urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo01">{documentoRelacionado["tipoComprobante"]}</cbc:DocumentTypeCode>
        </cac:InvoiceDocumentReference>
    </cac:BillingReference>
    <cac:Signature>
        <cbc:ID>{comprobante["serieDocumento"]}-{comprobante["numeroDocumento"]}</cbc:ID>
        <cac:SignatoryParty>
            <cac:PartyIdentification>
                <cbc:ID>{emisor["DocumentoEmisor"]}</cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyName>
                <cbc:Name><![CDATA[{emisor["RazonSocialEmisor"]}]]></cbc:Name>
            </cac:PartyName>
        </cac:SignatoryParty>
        <cac:DigitalSignatureAttachment>
            <cac:ExternalReference>
                <cbc:URI>#SignatureSP</cbc:URI>
            </cac:ExternalReference>
        </cac:DigitalSignatureAttachment>
    </cac:Signature>'''

    emisordata = f'''<cac:AccountingSupplierParty>
        <cac:Party>
            <cac:PartyIdentification>
                <cbc:ID schemeID="{emisor["TipoDocumento"]}" schemeName="Documento de Identidad" 
                        schemeAgencyName="PE:SUNAT" 
                        schemeURI="urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo06">{emisor["DocumentoEmisor"]}</cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyName>
                <cbc:Name><![CDATA[{emisor["RazonSocialEmisor"]}]]></cbc:Name>
            </cac:PartyName>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName><![CDATA[{emisor["RazonSocialEmisor"]}]]></cbc:RegistrationName>
                <cac:RegistrationAddress>
                    <cbc:ID schemeName="Ubigeos" schemeAgencyName="PE:INEI">{emisor["ubigeo"]}</cbc:ID>
                    <cbc:AddressTypeCode listAgencyName="PE:SUNAT" listName="Establecimientos anexos">0000</cbc:AddressTypeCode>
                    <cac:AddressLine>
                        <cbc:Line><![CDATA[{emisor["calle"]} - {emisor["distrito"]} - {emisor["provincia"]} - {emisor["departamento"]}]]></cbc:Line>
                    </cac:AddressLine>
                    <cac:Country>
                        <cbc:IdentificationCode listID="ISO 3166-1" 
                                                listAgencyName="United Nations Economic Commission for Europe" 
                                                listName="Country">PE</cbc:IdentificationCode>
                    </cac:Country>
                </cac:RegistrationAddress>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:AccountingSupplierParty>'''

    compradorData = f'''<cac:AccountingCustomerParty>
        <cac:Party>
            <cac:PartyIdentification>
                <cbc:ID schemeID="{adquiriente["TipoDocumentoAdquiriente"]}" schemeName="Documento de Identidad" 
                        schemeAgencyName="PE:SUNAT" 
                        schemeURI="urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo06">{adquiriente["NumeroDocumentoAdquiriente"]}</cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName><![CDATA[{adquiriente["razonSocial"]}]]></cbc:RegistrationName>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:AccountingCustomerParty>'''

    taxSubtotal = ''
    for tax in taxes.values():
        taxSubtotal += f'''<cac:TaxSubtotal>
            <cbc:TaxableAmount currencyID="PEN">{tax["operacionesGravadas"]}</cbc:TaxableAmount>
            <cbc:TaxAmount currencyID="PEN">{tax["MontoTotalImpuesto"]}</cbc:TaxAmount>
            <cac:TaxCategory>
                <cbc:ID schemeID="UN/ECE 5305" schemeName="Tax Category Identifier" 
                        schemeAgencyName="United Nations Economic Commission for Europe">{tax["cod4"]}</cbc:ID>
                <cac:TaxScheme>
                    <cbc:ID schemeID="UN/ECE 5153" schemeAgencyID="6">{tax["cod1"]}</cbc:ID>
                    <cbc:Name>{tax["cod2"]}</cbc:Name>
                    <cbc:TaxTypeCode>{tax["cod3"]}</cbc:TaxTypeCode>
                </cac:TaxScheme>
            </cac:TaxCategory>
        </cac:TaxSubtotal>'''

    taxTotal = f'''   
    <cac:TaxTotal>
        <cbc:TaxAmount currencyID="PEN">{comprobante["MontoTotalImpuestos"]}</cbc:TaxAmount>
        {taxSubtotal}
    </cac:TaxTotal>'''

    legalMonetaryTotal = f'''
    <cac:LegalMonetaryTotal>
        <cbc:LineExtensionAmount currencyID="PEN">{comprobante["ImporteTotalVenta"]}</cbc:LineExtensionAmount>
        <cbc:TaxInclusiveAmount currencyID="PEN">{comprobante["totalConImpuestos"]}</cbc:TaxInclusiveAmount>
        <cbc:PayableAmount currencyID="PEN">{comprobante["totalConImpuestos"]}</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>'''

    thing = ''
    innerId = 1
    for item in items:
        itemTaxSubtotal = ''
        for tax in item["tax"].values():
            itemTaxSubtotal += f'''<cac:TaxSubtotal>
                <cbc:TaxableAmount currencyID="PEN">{tax["operacionesGravadas"]}</cbc:TaxableAmount>
                <cbc:TaxAmount currencyID="PEN">{tax["MontoTotalImpuesto"]}</cbc:TaxAmount>
                <cac:TaxCategory>
                    <cbc:ID schemeID="UN/ECE 5305" schemeName="Tax Category Identifier" 
                            schemeAgencyName="United Nations Economic Commission for Europe">S</cbc:ID>
                    <cbc:Percent>18</cbc:Percent>
                    <cbc:TaxExemptionReasonCode listAgencyName="PE:SUNAT" 
                                                listName="Afectacion del IGV" 
                                                listURI="urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo07">10</cbc:TaxExemptionReasonCode>
                    <cac:TaxScheme>
                        <cbc:ID schemeID="UN/ECE 5153" schemeName="Codigo de tributos" 
                                schemeAgencyID="6">{tax["cod1"]}</cbc:ID>
                        <cbc:Name>{tax["cod2"]}</cbc:Name>
                        <cbc:TaxTypeCode>{tax["cod3"]}</cbc:TaxTypeCode>
                    </cac:TaxScheme>
                </cac:TaxCategory>
            </cac:TaxSubtotal>'''

        thing += f'''
        <cac:CreditNoteLine>
            <cbc:ID>{innerId}</cbc:ID>
            <cbc:CreditedQuantity unitCode="{item["unidadMedida"]}">{item["CantidadUnidadesItem"]}</cbc:CreditedQuantity>
            <cbc:LineExtensionAmount currencyID="PEN">{item["totalValorVenta"]}</cbc:LineExtensionAmount>
            <cac:PricingReference>
                <cac:AlternativeConditionPrice>
                    <cbc:PriceAmount currencyID="PEN">{item["precioUnitarioConImpuestos"]}</cbc:PriceAmount>
                    <cbc:PriceTypeCode listAgencyName="PE:SUNAT" 
                                       listName="Tipo de Precio" 
                                       listURI="urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo16">{item["tipoPrecio"]}</cbc:PriceTypeCode>
                </cac:AlternativeConditionPrice>
            </cac:PricingReference>
            <cac:TaxTotal>
                <cbc:TaxAmount currencyID="PEN">{item["totalTax"]}</cbc:TaxAmount>
                {itemTaxSubtotal}
            </cac:TaxTotal>
            <cac:Item>
                <cbc:Description><![CDATA[{item["DescripcionItem"]}]]></cbc:Description>
                <cac:SellersItemIdentification>
                    <cbc:ID>{item["id"]}</cbc:ID>
                </cac:SellersItemIdentification>
            </cac:Item>
            <cac:Price>
                <cbc:PriceAmount currencyID="PEN">{item["precioUnitario"]}</cbc:PriceAmount>
            </cac:Price>
        </cac:CreditNoteLine>'''
        innerId+=1

    fullXML = signature + emisordata + compradorData + taxTotal + legalMonetaryTotal   + thing + "</CreditNote>"

    folder_path = f"xml/{fileName.replace('.xml', '')}"

    os.makedirs(folder_path, exist_ok=True)

    with open(f'{folder_path}/{fileName}', 'w', encoding='utf-8') as file:
        file.write(fullXML)

    return f'{folder_path}/{fileName}'
    