from django.urls import path
from .views import (
    emitirComprobante,
    emitirNota_Credito,
    emitirNota_Debito,
    emitir_resumen_diario,
    emitirGuiaRemision,
    emitir_comunicado_de_bajas,
)

urlpatterns = [
    path('emitir_comprobante/', emitirComprobante, name='emitir_comprobante'),
    path('nota_credito/', emitirNota_Credito, name='nota_credito'),
    path('nota_debito/', emitirNota_Debito, name='nota_debito'),
    path('resumen_diario/', emitir_resumen_diario, name='resumen_diario' ),
    path('guia_remision/', emitirGuiaRemision, name='guia_remision' ),
    path('comunicado_bajas/', emitir_comunicado_de_bajas, name='comunicado_bajas' ),
]
