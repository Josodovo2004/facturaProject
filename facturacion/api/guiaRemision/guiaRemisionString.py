
def crear_xml_guia_remision(data, nombre_xml):

    emisor = data['emisor']
    cliente = data['cliente']
    cabecera = data['cabecera']
    items = data['items']
    # Crear el XML en formato de cadena usando raw strings para evitar problemas con los caracteres especiales
    header = f'''<?xml version="1.0" encoding="utf-8"?>
<DespatchAdvice xmlns:ds="http://www.w3.org/2000/09/xmldsig#" 
                xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" 
                xmlns:qdt="urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2" 
                xmlns:ccts="urn:un:unece:uncefact:documentation:2" 
                xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                xmlns:udt="urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2" 
                xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2" 
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" 
                xmlns:sac="urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1" 
                xmlns="urn:oasis:names:specification:ubl:schema:xsd:DespatchAdvice-2">
    <ext:UBLExtensions>
        <ext:UBLExtension>
            <ext:ExtensionContent/>
        </ext:UBLExtension>
    </ext:UBLExtensions>
    <cbc:UBLVersionID>2.1</cbc:UBLVersionID>
    <cbc:CustomizationID>2.0</cbc:CustomizationID>
    <cbc:ID>{cabecera['serie']}-{cabecera['correlativo']}</cbc:ID>
    <cbc:IssueDate>{cabecera['fecha_emision']}</cbc:IssueDate>
    <cbc:IssueTime>10:10:10</cbc:IssueTime>
    <cbc:DespatchAdviceTypeCode>09</cbc:DespatchAdviceTypeCode> 
    <cbc:Note>--</cbc:Note>
    <cac:Signature>
        <cbc:ID>{cabecera['serie']}-{cabecera['correlativo']}</cbc:ID>
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
                <cbc:URI>#{cabecera['serie']}-{cabecera['correlativo']}</cbc:URI>
            </cac:ExternalReference>
        </cac:DigitalSignatureAttachment>
    </cac:Signature>'''

    emisord = f'''<cac:DespatchSupplierParty>
        <cac:Party>
            <cac:PartyIdentification>
                <cbc:ID schemeID="{emisor['tipo_documento']}" schemeName="Documento de Identidad" schemeAgencyName="PE:SUNAT" schemeURI="urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo06">{emisor['ruc']}</cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName><![CDATA[{emisor['razon_social']}]]></cbc:RegistrationName>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:DespatchSupplierParty>'''
    comprador = f'''
    <cac:DeliveryCustomerParty>
        <cac:Party>
            <cac:PartyIdentification>
                <cbc:ID schemeID="{cliente['tipo_documento']}" schemeName="Documento de Identidad" schemeAgencyName="PE:SUNAT" schemeURI="urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo06">{cliente['ruc']}</cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName><![CDATA[{cliente['razon_social']}]]></cbc:RegistrationName>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:DeliveryCustomerParty>
    '''
    
    #---------------------------shipment start------------------------#
    shipment_parts = []

    # Parte base del XML para Shipment
    shipment_parts.append('''
    <cac:Shipment>
        <cbc:ID>1</cbc:ID>
        <cbc:HandlingCode>{codigo_motivo_traslado}</cbc:HandlingCode>
        <cbc:GrossWeightMeasure unitCode="{unidad_peso}">{peso}</cbc:GrossWeightMeasure>
        <cac:ShipmentStage>
            <cbc:TransportModeCode>{modo_transporte}</cbc:TransportModeCode>
            <cac:TransitPeriod>
                <cbc:StartDate>{fecha_envio}</cbc:StartDate>
            </cac:TransitPeriod>
    '''.format(
        codigo_motivo_traslado=cabecera['codigo_motivo_traslado'],
        unidad_peso=cabecera['unidad_peso'],
        peso=cabecera['peso'],
        modo_transporte=cabecera['modo_transporte'],
        fecha_envio=cabecera['fecha_envio']
    ))

    # Condicional para CarrierParty o DriverPerson
    if cabecera['modo_transporte'] == '01':
        shipment_parts.append('''
            <cac:CarrierParty>
                <cac:PartyIdentification>
                    <cbc:ID schemeID="{transportista_tipo_doc}">{transportista_nro_doc}</cbc:ID>
                </cac:PartyIdentification>
                <cac:PartyName>
                    <cbc:Name><![CDATA[{transportista_nombre}]]></cbc:Name>
                </cac:PartyName>
            </cac:CarrierParty>
        '''.format(
            transportista_tipo_doc=cabecera['transportista_tipo_doc'],
            transportista_nro_doc=cabecera['transportista_nro_doc'],
            transportista_nombre=cabecera['transportista_nombre']
        ))
    elif cabecera['modo_transporte'] == '02':
        shipment_parts.append('''
            <cac:DriverPerson>
                <cbc:ID schemeID="{conductor_tipo_doc}">{conductor_nro_doc}</cbc:ID>
                <cbc:FirstName><![CDATA[{conductor_nombres}]]></cbc:FirstName>
                <cbc:FamilyName>{conductor_apellidos}</cbc:FamilyName>
                <cbc:JobTitle>Principal</cbc:JobTitle>
                <cac:IdentityDocumentReference>
                    <cbc:ID><![CDATA[{conductor_licencia}]]></cbc:ID>
                </cac:IdentityDocumentReference>
            </cac:DriverPerson>
        '''.format(
            conductor_tipo_doc=cabecera['conductor_tipo_doc'],
            conductor_nro_doc=cabecera['conductor_nro_doc'],
            conductor_nombres=cabecera['conductor_nombres'],
            conductor_apellidos=cabecera['conductor_apellidos'],
            conductor_licencia=cabecera['conductor_licencia']
        ))

    # Agregar la sección Delivery
    shipment_parts.append('''
        </cac:ShipmentStage>
        <cac:Delivery>
            <cac:DeliveryAddress>
                <cbc:ID>{destino_ubigeo}</cbc:ID>
                <cbc:AddressTypeCode listID="{cliente_ruc}" listAgencyName="PE:SUNAT" listName="Establecimientos anexos">0</cbc:AddressTypeCode>
                <cac:AddressLine>
                    <cbc:Line><![CDATA[{destino_direccion}]]></cbc:Line>
                </cac:AddressLine>
            </cac:DeliveryAddress>
            <cac:Despatch>
                <cac:DespatchAddress>
                    <cbc:ID schemeName="Ubigeos" schemeAgencyName="PE:INEI">{partida_ubigeo}</cbc:ID>
                    <cbc:AddressTypeCode listID="{emisor_ruc}" listAgencyName="PE:SUNAT" listName="Establecimientos anexos">0</cbc:AddressTypeCode>
                    <cac:AddressLine>
                        <cbc:Line><![CDATA[{partida_direccion}]]></cbc:Line>
                    </cac:AddressLine>
                </cac:DespatchAddress>
            </cac:Despatch>
        </cac:Delivery>
    '''.format(
        destino_ubigeo=cabecera['destino_ubigeo'],
        cliente_ruc=cliente['ruc'],
        destino_direccion=cabecera['destino_direccion'],
        partida_ubigeo=cabecera['partida_ubigeo'],
        emisor_ruc=emisor['ruc'],
        partida_direccion=cabecera['partida_direccion']
    ))

    # Condicional para TransportHandlingUnit
    if cabecera['modo_transporte'] == '02':
        shipment_parts.append('''
            <cac:TransportHandlingUnit>
                <cac:TransportEquipment>
                    <cbc:ID><![CDATA[{vehiculo_placa}]]></cbc:ID>
                </cac:TransportEquipment>
            </cac:TransportHandlingUnit>
        '''.format(
            vehiculo_placa=cabecera['vehiculo_placa']
        ))

    # Cerrar la etiqueta principal
    shipment_parts.append('</cac:Shipment>')
    
    #--------------------shipment finish---------------------#
    # Agregar las líneas de despacho
    for item in items:
        xml += f'''<cac:DespatchLine>
    <cbc:ID>{item['item']}</cbc:ID>
    <cbc:DeliveredQuantity unitCode="{item['unidad']}">{item['cantidad']}</cbc:DeliveredQuantity>
    <cac:OrderLineReference>
        <cbc:LineID>{item['item']}</cbc:LineID>
    </cac:OrderLineReference>
    <cac:Item>
        <cbc:Description><![CDATA[{item['nombre']}]]></cbc:Description>
        <cac:SellersItemIdentification>
            <cbc:ID>{item['codigo']}</cbc:ID>
        </cac:SellersItemIdentification>
    </cac:Item>
</cac:DespatchLine>
'''
    shipment_parts = ''.join(shipment_parts)

    # Cerrar la etiqueta principal
    xml =header + emisord+ comprador + shipment_parts + '</DespatchAdvice>'

    # Guardar el XML en un archivo
    with open(f'{nombre_xml}.xml', 'w', encoding='utf-8') as file:
        file.write(xml)
