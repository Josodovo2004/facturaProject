from django.urls import path
from .views import (
    EntidadListCreateView,
    EntidadRetrieveUpdateDestroyView,
    ItemListCreateView,
    ItemRetrieveUpdateDestroyView,
    ItemImpuestoListCreateView,
    ItemImpuestoRetrieveUpdateDestroyView,
    ComprobanteListCreateView,
    ComprobanteRetrieveUpdateDestroyView,
    ComprobanteItemListCreateView,
    ComprobanteItemRetrieveUpdateDestroyView,
    emitirComprobante,
)

urlpatterns = [
    # URLs for Entidad
    path('entidades/', EntidadListCreateView.as_view(), name='entidad-list-create'),
    path('entidades/<int:pk>/', EntidadRetrieveUpdateDestroyView.as_view(), name='entidad-retrieve-update-destroy'),

    # URLs for Item
    path('items/', ItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemRetrieveUpdateDestroyView.as_view(), name='item-retrieve-update-destroy'),

    # URLs for ItemImpuesto
    path('item-impuestos/', ItemImpuestoListCreateView.as_view(), name='item-impuesto-list-create'),
    path('item-impuestos/<int:pk>/', ItemImpuestoRetrieveUpdateDestroyView.as_view(), name='item-impuesto-retrieve-update-destroy'),

    # URLs for Comprobante
    path('comprobantes/', ComprobanteListCreateView.as_view(), name='comprobante-list-create'),
    path('comprobantes/<int:pk>/', ComprobanteRetrieveUpdateDestroyView.as_view(), name='comprobante-retrieve-update-destroy'),

    # URLs for ComprobanteItem
    path('comprobante-items/', ComprobanteItemListCreateView.as_view(), name='comprobante-item-list-create'),
    path('comprobante-items/<int:pk>/', ComprobanteItemRetrieveUpdateDestroyView.as_view(), name='comprobante-item-retrieve-update-destroy'),
    
    path('emitir_comprobante/', emitirComprobante, name='emitircomprobante')
]
