

from .api.comprobantes.emitirComprobante import emitirComprobanteAPI
from .api.notaCredito.emitirNotaCredito import emitirNotaCredito
from .api.resumenComprobantes.emitirResumenComprobante import emitirResumenComprobante
from .api.notaDebito.emitirNotaDebito import emitirNotaDedito
from .api.guiaRemision.emitirGuiaRemision import emitirGuiaRemision
from .api.comunicadoDeBajas.emitirComunicadoBajas import emitirComunicadoBajas
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from facturaProject.decorators import jwt_required
from rest_framework.response import Response
# CRUD views for Entidad

# Define serializers for the input data structure
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'comprobante': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'serieDocumento': openapi.Schema(type=openapi.TYPE_STRING, description='Serie del documento'),
                    'numeroDocumento': openapi.Schema(type=openapi.TYPE_STRING, description='Número del documento'),
                    'fechaEmision': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de emisión'),
                    'DueDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de vencimiento'),
                    'tipoComprobante': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de comprobante'),
                    'cantidadItems': openapi.Schema(type=openapi.TYPE_INTEGER, description='Cantidad de ítems'),
                    'MontoTotalImpuestos': openapi.Schema(type=openapi.TYPE_STRING, description='Monto total de impuestos'),
                    'ImporteTotalVenta': openapi.Schema(type=openapi.TYPE_STRING, description='Importe total de la venta'),
                    'totalConImpuestos': openapi.Schema(type=openapi.TYPE_STRING, description='Total con impuestos'),
                },
                required=['serieDocumento', 'numeroDocumento', 'fechaEmision', 'DueDate', 'tipoComprobante', 'cantidadItems', 'MontoTotalImpuestos', 'ImporteTotalVenta', 'totalConImpuestos']
            ),
            'emisor': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'TipoDocumento': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de documento del emisor'),
                    'DocumentoEmisor': openapi.Schema(type=openapi.TYPE_STRING, description='Documento del emisor'),
                    'RazonSocialEmisor': openapi.Schema(type=openapi.TYPE_STRING, description='Razón social del emisor'),
                    'ubigeo': openapi.Schema(type=openapi.TYPE_STRING, description='Ubigeo del emisor'),
                    'calle': openapi.Schema(type=openapi.TYPE_STRING, description='Calle del emisor'),
                    'distrito': openapi.Schema(type=openapi.TYPE_STRING, description='Distrito del emisor'),
                    'provincia': openapi.Schema(type=openapi.TYPE_STRING, description='Provincia del emisor'),
                    'departamento': openapi.Schema(type=openapi.TYPE_STRING, description='Departamento del emisor'),
                },
                required=['TipoDocumento', 'DocumentoEmisor', 'RazonSocialEmisor', 'ubigeo', 'calle', 'distrito', 'provincia', 'departamento']
            ),
            'adquiriente': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'TipoDocumentoAdquiriente': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de documento del adquiriente'),
                    'NumeroDocumentoAdquiriente': openapi.Schema(type=openapi.TYPE_STRING, description='Número de documento del adquiriente'),
                    'razonSocial': openapi.Schema(type=openapi.TYPE_STRING, description='Razón social del adquiriente'),
                    'CalleComprador': openapi.Schema(type=openapi.TYPE_STRING, description='Calle del comprador'),
                    'distritoComprador': openapi.Schema(type=openapi.TYPE_STRING, description='Distrito del comprador'),
                    'provinciaComprador': openapi.Schema(type=openapi.TYPE_STRING, description='Provincia del comprador'),
                    'departamentoComprador': openapi.Schema(type=openapi.TYPE_STRING, description='Departamento del comprador'),
                },
                required=['TipoDocumentoAdquiriente', 'NumeroDocumentoAdquiriente', 'razonSocial', 'CalleComprador', 'distritoComprador', 'provinciaComprador', 'departamentoComprador']
            ),
            'taxes': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'Tax': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'operacionesGravadas': openapi.Schema(type=openapi.TYPE_STRING, description='Operaciones gravadas'),
                            'MontoTotalImpuesto': openapi.Schema(type=openapi.TYPE_STRING, description='Monto total del impuesto'),
                            'cod1': openapi.Schema(type=openapi.TYPE_STRING, description='Código 1'),
                            'cod2': openapi.Schema(type=openapi.TYPE_STRING, description='Código 2'),
                            'cod3': openapi.Schema(type=openapi.TYPE_STRING, description='Código 3'),
                            'cod4': openapi.Schema(type=openapi.TYPE_STRING, description='Código 4', nullable=True),
                        },
                        required=['operacionesGravadas', 'MontoTotalImpuesto', 'cod1', 'cod2', 'cod3']
                    )
                }
            ),
            'Items': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'unidadMedida': openapi.Schema(type=openapi.TYPE_STRING, description='Unidad de medida'),
                        'CantidadUnidadesItem': openapi.Schema(type=openapi.TYPE_INTEGER, description='Cantidad de unidades'),
                        'totalValorVenta': openapi.Schema(type=openapi.TYPE_STRING, description='Valor total de venta'),
                        'precioUnitarioConImpuestos': openapi.Schema(type=openapi.TYPE_STRING, description='Precio unitario con impuestos'),
                        'tipoPrecio': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de precio'),
                        'totalTax': openapi.Schema(type=openapi.TYPE_STRING, description='Total del impuesto'),
                        'DescripcionItem': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del ítem'),
                        'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID del ítem'),
                        'precioUnitario': openapi.Schema(type=openapi.TYPE_STRING, description='Precio unitario'),
                        'tax': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'operacionesGravadas': openapi.Schema(type=openapi.TYPE_STRING, description='Operaciones gravadas'),
                                'MontoTotalImpuesto': openapi.Schema(type=openapi.TYPE_STRING, description='Monto total del impuesto'),
                                'cod1': openapi.Schema(type=openapi.TYPE_STRING, description='Código 1'),
                                'cod2': openapi.Schema(type=openapi.TYPE_STRING, description='Código 2'),
                                'cod3': openapi.Schema(type=openapi.TYPE_STRING, description='Código 3'),
                                'cod4': openapi.Schema(type=openapi.TYPE_STRING, description='Código 4', nullable=True),
                            },
                            required=['operacionesGravadas', 'MontoTotalImpuesto', 'cod1', 'cod2', 'cod3']
                        )
                    },
                    required=['unidadMedida', 'CantidadUnidadesItem', 'totalValorVenta', 'precioUnitarioConImpuestos', 'tipoPrecio', 'totalTax', 'DescripcionItem', 'id', 'precioUnitario', 'tax']
                )
            )
        },
        required=['comprobante', 'emisor', 'adquiriente', 'taxes', 'Items']
    ),
    responses={
        '200': openapi.Response(
            description='Comprobante aceptado',
            examples={
                'application/json': {
                    'message': 'Comprobante aceptado',
                    'hash_code': 'string'
                }
            }
        ),
        '400': openapi.Response(
            description='Bad request',
            examples={
                'application/json': {
                    'error': 'Error en los datos de entrada'
                }
            }
        )
    }
)
@api_view(['POST'])      
def emitirComprobante(request):
    return emitirComprobanteAPI(request)



@swagger_auto_schema(
    method='post',
    operation_description="Emitir Nota de Crédito",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['emisor', 'comprobante', 'adquiriente', 'taxes', 'Items', 'documentoRelacionado'],
        properties={
            'emisor': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=['DocumentoEmisor', 'RazonSocialEmisor', 'TipoDocumento', 'ubigeo', 'calle', 'distrito', 'provincia', 'departamento'],
                properties={
                    'DocumentoEmisor': openapi.Schema(type=openapi.TYPE_STRING, description="Documento del Emisor"),
                    'RazonSocialEmisor': openapi.Schema(type=openapi.TYPE_STRING, description="Razón Social del Emisor"),
                    'TipoDocumento': openapi.Schema(type=openapi.TYPE_STRING, description="Tipo de Documento"),
                    'ubigeo': openapi.Schema(type=openapi.TYPE_STRING, description="Ubigeo"),
                    'calle': openapi.Schema(type=openapi.TYPE_STRING, description="Calle"),
                    'distrito': openapi.Schema(type=openapi.TYPE_STRING, description="Distrito"),
                    'provincia': openapi.Schema(type=openapi.TYPE_STRING, description="Provincia"),
                    'departamento': openapi.Schema(type=openapi.TYPE_STRING, description="Departamento"),
                }
            ),
            'comprobante': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=['serieDocumento', 'numeroDocumento', 'fechaEmision', 'MontoTotalImpuestos', 'ImporteTotalVenta', 'totalConImpuestos'],
                properties={
                    'serieDocumento': openapi.Schema(type=openapi.TYPE_STRING, description="Serie del Comprobante"),
                    'numeroDocumento': openapi.Schema(type=openapi.TYPE_STRING, description="Número del Comprobante"),
                    'fechaEmision': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description="Fecha de Emisión"),
                    'MontoTotalImpuestos': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="Monto Total de Impuestos"),
                    'ImporteTotalVenta': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="Importe Total de la Venta"),
                    'totalConImpuestos': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="Total con Impuestos"),
                }
            ),
            'adquiriente': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=['TipoDocumentoAdquiriente', 'NumeroDocumentoAdquiriente', 'razonSocial'],
                properties={
                    'TipoDocumentoAdquiriente': openapi.Schema(type=openapi.TYPE_STRING, description="Tipo de Documento del Adquiriente"),
                    'NumeroDocumentoAdquiriente': openapi.Schema(type=openapi.TYPE_STRING, description="Número de Documento del Adquiriente"),
                    'razonSocial': openapi.Schema(type=openapi.TYPE_STRING, description="Razón Social del Adquiriente"),
                }
            ),
            'taxes': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                additional_properties=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=['operacionesGravadas', 'MontoTotalImpuesto', 'cod1', 'cod2', 'cod3', 'cod4'],
                    properties={
                        'operacionesGravadas': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="Operaciones Gravadas"),
                        'MontoTotalImpuesto': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="Monto Total de Impuesto"),
                        'cod1': openapi.Schema(type=openapi.TYPE_STRING, description="Código 1"),
                        'cod2': openapi.Schema(type=openapi.TYPE_STRING, description="Código 2"),
                        'cod3': openapi.Schema(type=openapi.TYPE_STRING, description="Código 3"),
                        'cod4': openapi.Schema(type=openapi.TYPE_STRING, description="Código 4"),
                    }
                )
            ),
            'Items': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=['unidadMedida', 'CantidadUnidadesItem', 'totalValorVenta', 'precioUnitarioConImpuestos', 'tipoPrecio', 'totalTax', 'DescripcionItem', 'id', 'precioUnitario'],
                    properties={
                        'unidadMedida': openapi.Schema(type=openapi.TYPE_STRING, description="Unidad de Medida"),
                        'CantidadUnidadesItem': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="Cantidad de Unidades del Ítem"),
                        'totalValorVenta': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="Total del Valor de Venta"),
                        'precioUnitarioConImpuestos': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="Precio Unitario con Impuestos"),
                        'tipoPrecio': openapi.Schema(type=openapi.TYPE_STRING, description="Tipo de Precio"),
                        'totalTax': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="Total del Impuesto"),
                        'DescripcionItem': openapi.Schema(type=openapi.TYPE_STRING, description="Descripción del Ítem"),
                        'id': openapi.Schema(type=openapi.TYPE_STRING, description="ID del Ítem"),
                        'precioUnitario': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="Precio Unitario"),
                        'tax': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            additional_properties=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                required=['operacionesGravadas', 'MontoTotalImpuesto', 'cod1', 'cod2', 'cod3'],
                                properties={
                                    'operacionesGravadas': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="Operaciones Gravadas"),
                                    'MontoTotalImpuesto': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="Monto Total de Impuesto"),
                                    'cod1': openapi.Schema(type=openapi.TYPE_STRING, description="Código 1"),
                                    'cod2': openapi.Schema(type=openapi.TYPE_STRING, description="Código 2"),
                                    'cod3': openapi.Schema(type=openapi.TYPE_STRING, description="Código 3"),
                                }
                            )
                        ),
                    }
                )
            ),
            'documentoRelacionado': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=['serieDocumento', 'numeroDocumento', 'tipoComprobante'],
                properties={
                    'serieDocumento': openapi.Schema(type=openapi.TYPE_STRING, description="Serie del Documento Relacionado"),
                    'numeroDocumento': openapi.Schema(type=openapi.TYPE_STRING, description="Número del Documento Relacionado"),
                    'tipoComprobante': openapi.Schema(type=openapi.TYPE_STRING, description="Tipo de Comprobante del Documento Relacionado"),
                }
            ),
        }
    ),
    responses={200: openapi.Response(description="Nota de Crédito emitida correctamente")}
)
@api_view(['POST'])
def emitirNota_Credito(request):
    return emitirNotaCredito(request)

@api_view(['POST'])
def emitirNota_Debito(request):
    return emitirNotaDedito(request)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'cabecera': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'tipo_comprobante': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de comprobante'),
                    'fecha_envio': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de envío'),
                    'serie': openapi.Schema(type=openapi.TYPE_STRING, description='Serie del comprobante'),
                    'correlativo': openapi.Schema(type=openapi.TYPE_STRING, description='Correlativo del comprobante'),
                    'fecha_referencia': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de referencia'),
                }
            ),
            'emisor': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'ruc': openapi.Schema(type=openapi.TYPE_STRING, description='RUC del emisor'),
                    'razon_social': openapi.Schema(type=openapi.TYPE_STRING, description='Razón social del emisor'),
                }
            ),
            'documentos': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'document_type_code': openapi.Schema(type=openapi.TYPE_STRING, description='Código del tipo de documento'),
                        'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID del documento'),
                        'condition_code': openapi.Schema(type=openapi.TYPE_STRING, description='Código de condición'),
                        'total_amount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Monto total'),
                        'paid_amount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Monto pagado'),
                        'instruction_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID de instrucción'),
                        'currency': openapi.Schema(type=openapi.TYPE_STRING, description='Moneda'),
                        'tax_amount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Monto del impuesto'),
                        'tax': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'tax_amount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Monto del impuesto'),
                                    'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID del impuesto'),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del impuesto'),
                                    'tax_type_code': openapi.Schema(type=openapi.TYPE_STRING, description='Código del tipo de impuesto'),
                                }
                            )
                        )
                    }
                )
            )
        }
    ),
    responses={
        200: openapi.Response(
            description='Resumen de comprobantes procesado correctamente',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'response': openapi.Schema(type=openapi.TYPE_STRING, description='Mensaje de respuesta')
                }
            )
        ),
        400: openapi.Response(
            description='Error en la solicitud',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'response': openapi.Schema(type=openapi.TYPE_STRING, description='Mensaje de error')
                }
            )
        ),
        500: openapi.Response(
            description='Error en el servidor',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'response': openapi.Schema(type=openapi.TYPE_STRING, description='Mensaje de error')
                }
            )
        )
    }
)
@api_view(['POST'])
def emitir_resumen_diario(request):
    return emitirResumenComprobante(request) 


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'emisor': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'DocumentoEmisor': openapi.Schema(type=openapi.TYPE_STRING, description='RUC del emisor'),
                    'razon_social': openapi.Schema(type=openapi.TYPE_STRING, description='Razón social del emisor'),
                    'tipodoc': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de documento del emisor')
                },
                required=['DocumentoEmisor', 'razon_social', 'tipodoc']
            ),
            'comprobante': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'serieDocumento': openapi.Schema(type=openapi.TYPE_STRING, description='Serie del comprobante'),
                    'numeroDocumento': openapi.Schema(type=openapi.TYPE_STRING, description='Número del comprobante')
                },
                required=['serieDocumento', 'numeroDocumento']
            ),
            'cabecera': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'serie': openapi.Schema(type=openapi.TYPE_STRING, description='Serie del comprobante'),
                    'correlativo': openapi.Schema(type=openapi.TYPE_STRING, description='Número correlativo del comprobante'),
                    'fecha_emision': openapi.Schema(type=openapi.TYPE_STRING, description='Fecha de emisión en formato YYYY-MM-DD'),
                    'tipo_comprobante': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de comprobante'),
                    'codigo_motivo_traslado': openapi.Schema(type=openapi.TYPE_STRING, description='Código de motivo de traslado'),
                    'unidad_peso': openapi.Schema(type=openapi.TYPE_STRING, description='Unidad de medida del peso'),
                    'peso': openapi.Schema(type=openapi.TYPE_STRING, description='Peso total'),
                    'modo_transporte': openapi.Schema(type=openapi.TYPE_STRING, description='Modo de transporte'),
                    'fecha_envio': openapi.Schema(type=openapi.TYPE_STRING, description='Fecha de envío en formato YYYY-MM-DD'),
                    'destino_ubigeo': openapi.Schema(type=openapi.TYPE_STRING, description='Ubigeo del destino'),
                    'destino_direccion': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección de destino'),
                    'partida_ubigeo': openapi.Schema(type=openapi.TYPE_STRING, description='Ubigeo de partida'),
                    'partida_direccion': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección de partida'),
                    'vehiculo_placa': openapi.Schema(type=openapi.TYPE_STRING, description='Placa del vehículo'),
                    'transportista_tipo_doc': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de documento del transportista'),
                    'transportista_nro_doc': openapi.Schema(type=openapi.TYPE_STRING, description='Número de documento del transportista'),
                    'transportista_nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del transportista'),
                    'conductor_tipo_doc': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de documento del conductor'),
                    'conductor_nro_doc': openapi.Schema(type=openapi.TYPE_STRING, description='Número de documento del conductor'),
                    'conductor_nombres': openapi.Schema(type=openapi.TYPE_STRING, description='Nombres del conductor'),
                    'conductor_apellidos': openapi.Schema(type=openapi.TYPE_STRING, description='Apellidos del conductor'),
                    'conductor_licencia': openapi.Schema(type=openapi.TYPE_STRING, description='Número de licencia del conductor')
                },
                required=['serie', 'correlativo', 'fecha_emision', 'tipo_comprobante', 'codigo_motivo_traslado', 'unidad_peso', 'peso', 'modo_transporte', 'fecha_envio', 'destino_ubigeo', 'destino_direccion', 'partida_ubigeo', 'partida_direccion']
            ),
            'items': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'item': openapi.Schema(type=openapi.TYPE_STRING, description='ID del ítem'),
                        'cantidad': openapi.Schema(type=openapi.TYPE_STRING, description='Cantidad entregada'),
                        'unidad': openapi.Schema(type=openapi.TYPE_STRING, description='Unidad de medida'),
                        'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del ítem'),
                        'codigo': openapi.Schema(type=openapi.TYPE_STRING, description='Código del ítem')
                    },
                    required=['item', 'cantidad', 'unidad', 'nombre', 'codigo']
                )
            )
        },
        required=['emisor', 'comprobante', 'cabecera', 'items']
    ),
    responses={
        '200': openapi.Response(
            description='Guía de Remisión aceptada',
            examples={
                'application/json': {
                    'message': 'Guía de Remisión aceptada',
                    'hash_code': 'string'
                }
            }
        ),
        '400': openapi.Response(
            description='Error en los datos de entrada',
            examples={
                'application/json': {
                    'error': 'Error en los datos de entrada'
                }
            }
        ),
        '500': openapi.Response(
            description='Error en el servidor',
            examples={
                'application/json': {
                    'error': 'Error en el servidor'
                }
            }
        )
    }
)
@api_view(['POST'])
def emitir_guia_remision(request):
    return emitirGuiaRemision(request)


@api_view(['POST'])
def emitir_comunicado_de_bajas(request):
    return emitirComunicadoBajas(request)