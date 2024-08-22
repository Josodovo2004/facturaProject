from rest_framework import generics
from django.http import response
from .models import (
    Entidad,
    Item,
    ItemImpuesto,
    Comprobante,
    ComprobanteItem
)
from .serializers import (
    EntidadSerializer,
    ItemSerializer,
    ItemImpuestoSerializer,
    ComprobanteSerializer,
    ComprobanteItemSerializer
)

from .api.comprobantes.emitirComprobante import emitirComprobanteAPI
from .api.comunicadoBajas.anulacionFactura import emitirComunicadoAnulacion
from .api.notaCredito.emitirNotaCredito import emitirNotaCredito
from .api.resumenComprobantes.emitirResumenComprobante import emitirResumenComprobante
# CRUD views for Entidad
class EntidadListCreateView(generics.ListCreateAPIView):
    queryset = Entidad.objects.all()
    serializer_class = EntidadSerializer

class EntidadRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Entidad.objects.all()
    serializer_class = EntidadSerializer

# CRUD views for Item
class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# CRUD views for ItemImpuesto
class ItemImpuestoListCreateView(generics.ListCreateAPIView):
    queryset = ItemImpuesto.objects.all()
    serializer_class = ItemImpuestoSerializer

class ItemImpuestoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ItemImpuesto.objects.all()
    serializer_class = ItemImpuestoSerializer

# CRUD views for Comprobante
class ComprobanteListCreateView(generics.ListCreateAPIView):
    queryset = Comprobante.objects.all()
    serializer_class = ComprobanteSerializer

class ComprobanteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comprobante.objects.all()
    serializer_class = ComprobanteSerializer

# CRUD views for ComprobanteItem
class ComprobanteItemListCreateView(generics.ListCreateAPIView):
    queryset = ComprobanteItem.objects.all()
    serializer_class = ComprobanteItemSerializer

class ComprobanteItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ComprobanteItem.objects.all()
    serializer_class = ComprobanteItemSerializer


def emitirComprobante(request):
    return emitirComprobanteAPI(request)

def anular_factura(request):
    return emitirNotaCredito(request)

def comunicadoBaja(request):
    return emitirComunicadoAnulacion(request)

def resumen_diario(request):
    return emitirResumenComprobante(request)