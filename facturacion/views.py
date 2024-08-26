from rest_framework import generics
from django.http import response
from django.views.decorators.csrf import csrf_exempt

from .api.comprobantes.emitirComprobante import emitirComprobanteAPI
from .api.notaCredito.emitirNotaCredito import emitirNotaCredito
from .api.resumenComprobantes.emitirResumenComprobante import emitirResumenComprobante
# CRUD views for Entidad


@csrf_exempt
def emitirComprobante(request):
    return emitirComprobanteAPI(request)

def anular_factura(request):
    return emitirNotaCredito(request)

def resumen_diario(request):
    return emitirResumenComprobante(request)