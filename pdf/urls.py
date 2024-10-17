from django.urls import path, include
from .views import PDFGenerator

urlpatterns = [
    path('generar_comprobante/', PDFGenerator.as_view(), name='generar_comprobante')
]