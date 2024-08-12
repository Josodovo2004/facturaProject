from rest_framework import serializers
from .models import (
    Catalogo01TipoDocumento,
    Catalogo06DocumentoIdentidad,
    EstadoDocumento,
    Usuario,
    TipoComprobante,
    Cliente,
    Catalogo05TiposTributos,
    Catalogo15ElementosAdicionales,
    Ubigeo,
    CodigoPais,
    CodigoMoneda,
    Entidad,
    Item,
    ItemImpuesto,
    Comprobante,
    ComprobanteItem,
)

class Catalogo01TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo01TipoDocumento
        fields = '__all__'

class Catalogo06DocumentoIdentidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo06DocumentoIdentidad
        fields = '__all__'

class EstadoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoDocumento
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class TipoComprobanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoComprobante
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class Catalogo05TiposTributosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo05TiposTributos
        fields = '__all__'

class Catalogo15ElementosAdicionalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo15ElementosAdicionales
        fields = '__all__'

class UbigeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubigeo
        fields = '__all__'

class CodigoPaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodigoPais
        fields = '__all__'

class CodigoMonedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodigoMoneda
        fields = '__all__'

class EntidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entidad
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ItemImpuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImpuesto
        fields = '__all__'

class ComprobanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comprobante
        fields = '__all__'

class ComprobanteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComprobanteItem
        fields = '__all__'
