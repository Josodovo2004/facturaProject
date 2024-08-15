from django.contrib import admin
from .models import (
    Catalogo01TipoDocumento,
    Catalogo06DocumentoIdentidad,
    EstadoDocumento,
    Usuario,
    Cliente,
    Catalogo05TiposTributos,
    Catalogo07TiposDeAfectacionDelIGV,
    Catalogo15ElementosAdicionales,
    Ubigeo,
    CodigoPais,
    CodigoMoneda,
    Entidad,
    Item,
    ItemImpuesto,
    Comprobante
)

# Register all the models
admin.site.register(Catalogo01TipoDocumento)
admin.site.register(Catalogo06DocumentoIdentidad)
admin.site.register(EstadoDocumento)
admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Catalogo05TiposTributos)
admin.site.register(Catalogo07TiposDeAfectacionDelIGV)
admin.site.register(Catalogo15ElementosAdicionales)
admin.site.register(Ubigeo)
admin.site.register(CodigoPais)
admin.site.register(CodigoMoneda)
admin.site.register(Entidad)
admin.site.register(Item)
admin.site.register(ItemImpuesto)
admin.site.register(Comprobante)
