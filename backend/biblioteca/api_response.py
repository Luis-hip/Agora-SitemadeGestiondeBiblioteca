from rest_framework.response import Response


def respuesta_estandar(exito, codigo, datos=None, mensaje='', detalle=None):
    cuerpo = {'exito': exito, 'codigo': codigo, 'datos': datos, 'mensaje': mensaje}
    if detalle is not None:
        cuerpo['detalle'] = detalle
    return Response(cuerpo, status=codigo)
