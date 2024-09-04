from django.urls import path
from .views import (
    emitirComprobante,
    anular_factura,
    resumen_diario,
    emitirGuiaRemision
)

urlpatterns = [
    path('emitir_comprobante/', emitirComprobante, name='emitir_comprobante'),
    path('anular_factura/', anular_factura, name='anular_factura'),
    path('resumen_diario/', resumen_diario, name='resumen_diario' ),
    path('emitir_guia_remision/', emitirGuiaRemision, name='emitir_guia_remision' ),
]
