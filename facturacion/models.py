from django.db import models
from django.db import models
import django.utils.timezone as tm

# Create your models here.

class Catalogo01TipoDocumento(models.Model):
    codigo = models.CharField(db_column='Codigo', max_length=2, primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True, null=True)  # Field name made lowercase.
    un_1001 = models.CharField(db_column='UN_1001', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'CATALOGO_01_TIPO_DOCUMENTO'
    def __str__(self):
        return self.descripcion

class Catalogo06DocumentoIdentidad(models.Model):
    codigo = models.CharField(db_column='Codigo', max_length=1, primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True, null=True)  # Field name made lowercase.
    abrev= models.CharField(db_column='ABREV', max_length=10, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        db_table = 'CATALOGO_06_DOCUMENTO_IDENTIDAD'
    def __str__(self):
        return self.descripcion
    
class UnidadMedida(models.Model):
    codigo = models.CharField(max_length=4, primary_key=True)  # Unique code for the unit of measure
    descripcion = models.CharField(max_length=200, blank=True, null=True)  # Description of the unit

    class Meta:
        db_table = 'unidad_medida'
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class EstadoDocumento(models.Model):
    id= models.CharField(db_column='id',  max_length=2,primary_key=True)  # Field name made lowercase.
    nombre= models.CharField(db_column='nombre',  max_length=50,null=True,blank=True)
    class Meta:
        db_table = 'ESTADO_DOCUMENTO'
    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    numDocUsuario = models.CharField(primary_key=True,max_length=15)
    rznSocialUsuario = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()

    def __str__(self):
        return self.rznSocialUsuario

class Cliente(models.Model):
    cfcodcli = models.CharField(db_column='CFCODCLI', max_length=11, primary_key=True)  # Field name made lowercase.
    cfnombre = models.CharField(db_column='CFNOMBRE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    direccion_receptor = models.CharField(db_column='DIRECCION_RECEPTOR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    correo = models.EmailField(db_column='CORREO', max_length=200, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = True
        db_table = 'CLIENTE'


class Catalogo05TiposTributos(models.Model):
    codigo = models.CharField(db_column='Codigo', max_length=4, primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Name', max_length=6, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True, null=True)  # Field name made lowercase.
    un_ece_5153 = models.CharField(db_column='UN_ECE_5153', max_length=3, blank=True, null=True)  # Field name made lowercase.
    un_ece_5305 = models.CharField(db_column='UN_ECE_5305', max_length=1, blank=True, null=True)



    class Meta:
        db_table = 'CATALOGO_05_TIPOS_TRIBUTOS'

    def __str__(self) -> str:
        return self.nombre



class Catalogo07TiposDeAfectacionDelIGV(models.Model):
    codigo = models.CharField(db_column='Codigo', max_length=2, primary_key=True)
    descripcion = models.CharField(db_column='Descripcion', max_length=200, null = False)

class Catalogo15ElementosAdicionales(models.Model):
    codigo = models.CharField(db_column='Codigo', max_length=4,primary_key =True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'CATALOGO_15_ELEMENTOS_ADICIONALES'

class Catalogo51Choices(models.TextChoices):
    A = 'a', 'Option A'
    B = 'b', 'Option B'

class Catalogo51TipoDeOperacion(models.Model):
    codigo = models.CharField(db_column='codigo', max_length=4, primary_key=True)
    descripcion = models.CharField(max_length=200)
    comprobantes = models.CharField(
        max_length=1,  # Adjust the max_length to fit the longest choice value
        choices=Catalogo51Choices.choices
    )

class Ubigeo(models.Model):
    codigo = models.CharField(max_length=10, null=False)
    distrito = models.CharField(max_length=32, null=False)
    provincia = models.CharField(max_length=32, null=False)
    departamento = models.CharField(max_length=32, null=False)
    def __str__(self) -> str:
        return f'{self.distrito} {self.provincia} {self.departamento}'

class CodigoPais(models.Model):
    codigo = models.CharField(max_length=5, null=False)
    pais = models.CharField(max_length=20, null=False)

    def __str__(self) -> str:
        return f'{self.pais}'

class CodigoMoneda(models.Model):
    codigo = models.CharField(max_length=4, null=False)
    moneda = models.CharField(max_length=50, null=False)
    
    def __str__(self) -> str:
        return self.moneda

from django.db import models

class TipoPrecio(models.Model):
    codigo = models.CharField(max_length=2, primary_key=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'tipo_precio'
    
    def __str__(self):
        return self.descripcion


class SegmentoProducto(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'segmento_producto'
    
    def __str__(self):
        return self.descripcion
    
class FamiliaProducto(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    segmento = models.ForeignKey(SegmentoProducto, on_delete=models.DO_NOTHING)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'familia_producto'
    
    def __str__(self):
        return self.descripcion
    
class ClaseProducto(models.Model):
    codigo = models.CharField(max_length=15, primary_key=True)
    familia = models.ForeignKey(FamiliaProducto, on_delete=models.DO_NOTHING)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'clase_producto'
    
    def __str__(self):
        return self.descripcion
    
class Producto(models.Model):
    codigo = models.CharField(max_length=20, primary_key=True)
    clase = models.ForeignKey(ClaseProducto, on_delete=models.DO_NOTHING)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'producto'
    
    def __str__(self):
        return self.descripcion
    


class Entidad(models.Model):
    numeroDocumento = models.CharField(max_length=11, null=False)
    tipoDocumento = models.ForeignKey(Catalogo06DocumentoIdentidad, on_delete=models.CASCADE, null=False)
    razonSocial = models.CharField(max_length=150, null=False)
    nombreComercial = models.CharField(max_length=150, null=False)
    ubigeo = models.ForeignKey(Ubigeo, on_delete=models.CASCADE, null=False)
    direccion = models.CharField(max_length=50, null=False)
    codigoPais = models.ForeignKey(CodigoPais, on_delete=models.CASCADE, null=False)
    usuarioSol = models.CharField(max_length=50, null=True)
    claveSol = models.CharField(max_length=50, null=True)

    def __str__(self) -> str:
        return self.nombreComercial

class Item(models.Model):
    unidadMedida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    tipoPrecio = models.ForeignKey(TipoPrecio, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30, null=False)
    descripcion = models.TextField(max_length=200, null=True)
    valorUnitario = models.IntegerField(null=False)
    codigoProducto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING, null=True)

    def __str__(self) -> str:
        return self.nombre


class ItemImpuesto(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=False)
    impuesto = models.ForeignKey(Catalogo05TiposTributos, on_delete=models.CASCADE, null=False)
    porcentaje = models.IntegerField(null=False)
    valorGravado = models.IntegerField(null=False)


class Comprobante(models.Model):
    emisor = models.ForeignKey(Entidad, on_delete=models.DO_NOTHING, null=False, related_name='comprobantes_emitidos')
    adquiriente = models.ForeignKey(Entidad, on_delete=models.DO_NOTHING, null=False, related_name='comprobantes_recibidos')
    tipoComprobante = models.ForeignKey(Catalogo01TipoDocumento, on_delete= models.DO_NOTHING, null=False)
    tipoOperacion = ''
    tipoPago = ''
    serie = models.CharField(max_length=4, null=False)
    numeroComprobante = models.CharField(max_length=8, null=False)
    fechaEmision = models.DateField(default=tm.now, null=False)
    codigoMoneda = models.ForeignKey(CodigoMoneda, on_delete=models.DO_NOTHING, null=True)


class ComprobanteItem(models.Model):
    comprobante = models.ForeignKey(Comprobante, on_delete=models.CASCADE ,null=False)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, null=False)
    cantidad = models.IntegerField(null=False)
