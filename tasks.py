from celery import shared_task, Celery # type: ignore
from facturacion.api.resumenComprobantes.emitirResumenComprobante import emitirResumenComprobante
from django.http.request import HttpRequest
from django.http import JsonResponse


@shared_task
def emisionDeResumenProgramada(data) -> bool:
    req = HttpRequest()
    req.body = data
    response: JsonResponse =  emitirResumenComprobante(req)

    if response.status_code == 200:
        return True
    else:
        return False 