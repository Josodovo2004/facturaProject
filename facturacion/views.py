from rest_framework import generics
from django.http import response
from django.views.decorators.csrf import csrf_exempt

from .api.comprobantes.emitirComprobante import emitirComprobanteAPI
from .api.notaCredito.emitirNotaCredito import emitirNotaCredito
from .api.resumenComprobantes.emitirResumenComprobante import emitirResumenComprobante
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema

# CRUD views for Entidad

# Define serializers for the input data structure
class TaxSerializer(serializers.Serializer):
    operacionesGravadas = serializers.DecimalField(max_digits=10, decimal_places=2)
    MontoTotalImpuesto = serializers.DecimalField(max_digits=10, decimal_places=2)
    cod1 = serializers.CharField(max_length=10)
    cod2 = serializers.CharField(max_length=10)
    cod3 = serializers.CharField(max_length=10)
    cod4 = serializers.CharField(max_length=10, required=False)

class ItemSerializer(serializers.Serializer):
    unidadMedida = serializers.CharField(max_length=10)
    CantidadUnidadesItem = serializers.IntegerField()
    totalValorVenta = serializers.DecimalField(max_digits=10, decimal_places=2)
    precioUnitarioConImpuestos = serializers.DecimalField(max_digits=10, decimal_places=2)
    tipoPrecio = serializers.CharField(max_length=10)
    totalTax = serializers.DecimalField(max_digits=10, decimal_places=2)
    DescripcionItem = serializers.CharField(max_length=255)
    id = serializers.CharField(max_length=20)
    precioUnitario = serializers.DecimalField(max_digits=10, decimal_places=2)
    tax = TaxSerializer()

class ComprobanteSerializer(serializers.Serializer):
    serieDocumento = serializers.CharField(max_length=10)
    numeroDocumento = serializers.CharField(max_length=20)
    fechaEmision = serializers.DateField()
    DueDate = serializers.DateField()
    tipoComprobante = serializers.CharField(max_length=5)
    cantidadItems = serializers.IntegerField()
    MontoTotalImpuestos = serializers.DecimalField(max_digits=10, decimal_places=2)
    ImporteTotalVenta = serializers.DecimalField(max_digits=10, decimal_places=2)
    totalConImpuestos = serializers.DecimalField(max_digits=10, decimal_places=2)

class EmisorSerializer(serializers.Serializer):
    TipoDocumento = serializers.CharField(max_length=5)
    DocumentoEmisor = serializers.CharField(max_length=20)
    RazonSocialEmisor = serializers.CharField(max_length=255)
    ubigeo = serializers.CharField(max_length=10)
    calle = serializers.CharField(max_length=255)
    distrito = serializers.CharField(max_length=100)
    provincia = serializers.CharField(max_length=100)
    departamento = serializers.CharField(max_length=100)

class AdquirienteSerializer(serializers.Serializer):
    TipoDocumentoAdquiriente = serializers.CharField(max_length=5)
    NumeroDocumentoAdquiriente = serializers.CharField(max_length=20)
    razonSocial = serializers.CharField(max_length=255)
    CalleComprador = serializers.CharField(max_length=255)
    distritoComprador = serializers.CharField(max_length=100)
    provinciaComprador = serializers.CharField(max_length=100)
    departamentoComprador = serializers.CharField(max_length=100)

class TaxesSerializer(serializers.Serializer):
    Tax = TaxSerializer()

class EmitirComprobanteSerializer(serializers.Serializer):
    comprobante = ComprobanteSerializer()
    emisor = EmisorSerializer()
    adquiriente = AdquirienteSerializer()
    taxes = TaxesSerializer()
    Items = ItemSerializer(many=True)

@swagger_auto_schema(
    method='post',
    request_body=EmitirComprobanteSerializer,
    responses={200: 'Comprobante aceptado', 400: 'Bad request'},
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
def anular_factura(request):
    return emitirNotaCredito(request)




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
def resumen_diario(request):
    return emitirResumenComprobante(request)