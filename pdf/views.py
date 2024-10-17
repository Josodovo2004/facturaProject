from django.shortcuts import render
from rest_framework.decorators import api_view
from facturaProject.decorators import CustomJWTAuthentication, jwt_required
from rest_framework.views  import APIView
from .api.generateComprobantePDF import generateComprobantePDF
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class PDFGenerator(APIView):
    authentication_classes=[CustomJWTAuthentication]
    permission_classes=[]
    @swagger_auto_schema(
        operation_description="Generar comprobante PDF",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'image_path': openapi.Schema(type=openapi.TYPE_STRING, description='Path to the logo image'),
                'tipo_pdf': openapi.Schema(type=openapi.TYPE_STRING, description='Type of PDF'),
                'comprobante': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'serieDocumento': openapi.Schema(type=openapi.TYPE_STRING, description='Serie del documento'),
                        'numeroDocumento': openapi.Schema(type=openapi.TYPE_STRING, description='Número del documento'),
                        'fechaEmision': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de emisión'),
                        'DueDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de vencimiento'),
                        'tipoComprobante': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de comprobante'),
                        'cantidadItems': openapi.Schema(type=openapi.TYPE_INTEGER, description='Cantidad de ítems'),
                        'MontoTotalImpuestos': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Monto total de impuestos'),
                        'ImporteTotalVenta': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Importe total de la venta'),
                        'totalConImpuestos': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Total con impuestos')
                    }
                ),
                'emisor': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'TipoDocumento': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de documento del emisor'),
                        'DocumentoEmisor': openapi.Schema(type=openapi.TYPE_STRING, description='Documento del emisor'),
                        'RazonSocialEmisor': openapi.Schema(type=openapi.TYPE_STRING, description='Razón social del emisor'),
                        'ubigeo': openapi.Schema(type=openapi.TYPE_STRING, description='Ubigeo del emisor'),
                        'calle': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección del emisor'),
                        'distrito': openapi.Schema(type=openapi.TYPE_STRING, description='Distrito del emisor'),
                        'provincia': openapi.Schema(type=openapi.TYPE_STRING, description='Provincia del emisor'),
                        'departamento': openapi.Schema(type=openapi.TYPE_STRING, description='Departamento del emisor'),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email del emisor'),
                        'telefono': openapi.Schema(type=openapi.TYPE_STRING, description='Teléfono del emisor')
                    }
                ),
                'adquiriente': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'TipoDocumentoAdquiriente': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de documento del adquirente'),
                        'NumeroDocumentoAdquiriente': openapi.Schema(type=openapi.TYPE_STRING, description='Número de documento del adquirente'),
                        'razonSocial': openapi.Schema(type=openapi.TYPE_STRING, description='Razón social del adquirente'),
                        'CalleComprador': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección del adquirente'),
                        'distritoComprador': openapi.Schema(type=openapi.TYPE_STRING, description='Distrito del adquirente'),
                        'provinciaComprador': openapi.Schema(type=openapi.TYPE_STRING, description='Provincia del adquirente'),
                        'departamentoComprador': openapi.Schema(type=openapi.TYPE_STRING, description='Departamento del adquirente')
                    }
                ),
                'taxes': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'IGV': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'operacionesGravadas': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Operaciones gravadas'),
                                'MontoTotalImpuesto': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Monto total del impuesto'),
                                'cod1': openapi.Schema(type=openapi.TYPE_STRING, description='Código 1 del impuesto'),
                                'cod2': openapi.Schema(type=openapi.TYPE_STRING, description='Código 2 del impuesto'),
                                'cod3': openapi.Schema(type=openapi.TYPE_STRING, description='Código 3 del impuesto'),
                                'cod4': openapi.Schema(type=openapi.TYPE_STRING, description='Código 4 del impuesto'),
                                'afectacionIGV': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_INT32, description='Afectación del IGV')
                            }
                        )
                    }
                ),
                'items': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'unidadMedida': openapi.Schema(type=openapi.TYPE_STRING, description='Unidad de medida'),
                            'CantidadUnidadesItem': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Cantidad de unidades'),
                            'totalValorVenta': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Total valor de venta'),
                            'precioUnitarioConImpuestos': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Precio unitario con impuestos'),
                            'tipoPrecio': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de precio'),
                            'totalTax': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Total impuesto'),
                            'DescripcionItem': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del ítem'),
                            'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID del producto'),
                            'precioUnitario': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Precio unitario'),
                            'codProducto': openapi.Schema(type=openapi.TYPE_INTEGER, description='Código del producto'),
                            'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del producto'),
                            'tax': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'TaxName (Example: IGV)': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'operacionesGravadas': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Operaciones gravadas'),
                                            'MontoTotalImpuesto': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Monto total del impuesto'),
                                            'cod1': openapi.Schema(type=openapi.TYPE_STRING, description='Código 1 del impuesto'),
                                            'cod2': openapi.Schema(type=openapi.TYPE_STRING, description='Código 2 del impuesto'),
                                            'cod3': openapi.Schema(type=openapi.TYPE_STRING, description='Código 3 del impuesto'),
                                            'afectacionIGV': openapi.Schema(type=openapi.TYPE_INTEGER, description='Afectación del IGV')
                                        }
                                    )
                                }
                            )
                        }
                    ),
                    description='Items del comprobante'
                ),
                'payTerms': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'metodo': openapi.Schema(type=openapi.TYPE_STRING, description='Método de pago')
                        }
                    )
                ),
                'observaciones': openapi.Schema(type=openapi.TYPE_STRING, description='Observaciones'),
                'formaPago': openapi.Schema(type=openapi.TYPE_STRING, description='Forma de pago')
            }
        )
    )
    def post(self, request):
        return generateComprobantePDF(request)