# coding=utf-8

import json
from django.utils.timezone import localtime
from operator import attrgetter
from datetime import datetime

from django.core import serializers
from django.http.response import JsonResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict
from django.db.models import Q

from laboratorio.modelos_vista import Convertidor,  RecursoBusquedaVista, RecursoBusquedaDetalleVista
from laboratorio.models import Usuario, Bodega
from laboratorio.models import TransaccionInventario, Producto, ProductosEnBodega
from laboratorio.models import Tipo, ConteoInventario, DetalleProductos
from laboratorio.utils.utils import utils


# HU: LCINV-5
# FB.
# Hace una búsqueda para saber en qué bodega está y cuál fue su última fecha de transacción.
# request: Petición desde el form de usuario.
# return: Página html con la plantilla y los resultados de la búsqueda asociada.
@csrf_exempt
def ver_producto_busqueda(request):
    global bproducto
    global bBodega
    global bFechaTransaccion

    bproducto = ""
    bBodega = ""
    bFechaTransaccion = ""

    # Capturar el valor de los campos
    if request.method == 'POST':
        bproducto = request.POST.get('producto', "")
        bBodega = request.POST.get('bodega', "")
        bFechaTransaccion = request.POST.get('fechatransaccion', "")

    busqueda_producto(request)
    return render(request, "laboratorio/busquedaproducto.html")


# HU: LCINV-5
# FB.
# Hace una búsqueda para saber en qué bodega está y cuál fue su última fecha de transacción.
# Aquí puntualmente es donde se hace el filtro.
# request: Petición desde el form de usuario.
# return: json con los datos encontrados
@csrf_exempt
def busqueda_producto(request):
    # Filtra por la expresion; si no hay nada, muestra todos los productos
    if bproducto == "" and bBodega == "":  # Sin filtro
        qs = ProductosEnBodega.objects.all()
    else:  # Filtro
        if bproducto != "" and bBodega == "":  # Si solo se filtra por producto
            qs = ProductosEnBodega.objects.filter(producto__codigo=bproducto)
        elif bproducto == "" and bBodega != "":  # Si solo se filtra por bodega
            qs = ProductosEnBodega.objects.filter(bodega__serial=bBodega)
        else:  # Filtro por producto y bodega
            qs = ProductosEnBodega.objects.filter(producto__codigo=bproducto, bodega__serial=bBodega)

    # Quitar los productos en las bodegas que no deben salir (desperdicio, ...)
    qs = qs.filter(~Q(bodega__nombre="Desperdicios"))
    qs = qs.filter(~Q(bodega__nombre="Proveedor"))

    lista_recurso = []

    for peb in qs:
        req = RecursoBusquedaVista()
        req.id = peb.id
        req.nombre = peb.producto.nombre
        req.unidadesExistentes = peb.cantidad
        req.unidad_medida = peb.producto.unidad_medida.nombre
        req.fechaTransaccion = obtener_bodega_actualxpebxtransaccion(peb, 2)
        # Convertir a unidades de preferencia
        req.cantidad_convertida = str(utils.convertir(req.unidadesExistentes, peb.unidad_medida.nombre,
                                                      peb.bodega.unidad_medida.nombre))

        localizacion = ""
        if str(peb.nivel) != "":
            localizacion = ", Nivel " + str(peb.nivel)
        if str(peb.seccion) != "":
            localizacion = localizacion + ", Seccion " + str(peb.seccion)

        req.bodegaActual = peb.bodega.nombre + localizacion
        # Variable oculta para debug en html
        req.hidden1 = "bFechaTransaccion:" + bFechaTransaccion + " req.fechaTransaccion:" + req.fechaTransaccion + " pebbodega:" + str(peb.bodega.unidad_medida)

        if bFechaTransaccion == "":
            lista_recurso.append(req)
        else:
            if bFechaTransaccion in req.fechaTransaccion:
                lista_recurso.append(req)

    lista_recurso.sort(key=attrgetter('fechaTransaccion'), reverse=True)
    json_string = json.dumps(lista_recurso, cls=Convertidor)
    return JsonResponse(json_string, safe=False)


# HU: LCINV-5
# FB.
# Obtiene la última transacción ordenada por fecha de ejecucuón (la más reciente).
# peb: Petición desde el form de usuario.
# campo: El campo que se requiere retornar.
# return: El dato puntual solicitado.
def obtener_bodega_actualxpebxtransaccion(peb, campo):
    qs = TransaccionInventario.objects.filter(producto_bodega_destino=peb).order_by('-fecha_ejecucion')[:1]
    retorno = "N/A"
    if qs.exists():
        if campo == 1:
            retorno = qs[0].bodega_destino.nombre
        if campo == 2:
            fecha = localtime(qs[0].fecha_ejecucion)
            retorno = fecha.strftime('%Y-%m-%d %H:%M:%S')
        if campo == 3:
            retorno = localtime(qs[0].fecha_ejecucion)
    return retorno


# HU: LCINV-5
# FB.
# Obtiene el nombre completo del usuario consultado.
# usuario: Id de usuario.
# return: Nombre de usuario compuesto por Nombre y Apellido.
def obtener_nombre_usuarioxid(usuario):
    qs = Usuario.objects.filter(id=usuario)[:1]

    retorno = "N/A"

    retorno = qs[0].first_name + " " + qs[0].last_name

    return retorno


# HU: LCINV-5
# FB.
# Muestra el detalle de transacciones para un Producto dado.
# request: Petición desde el form de usuario.
# return: Página html con la plantilla y los resultados de la búsqueda asociada.
@csrf_exempt
def ver_producto_busqueda_detalle(request):
    global globvar
    globvar = request.GET.get('id')
    busqueda_producto_detalle(request)
    return render(request, "laboratorio/busquedaproductodetalle.html")


# HU: LCINV-5
# FB.
# Muestra el detalle de transacciones para un Producto dado. Esta es la búsqueda como tal.
# request: Petición desde el form de usuario.
# globvar: El Id de ProductosEnBodega (Producto).
# return: json con los datos encontrados
def busqueda_producto_detalle(request):
    idpeb = int(globvar)
    qs = TransaccionInventario.objects.filter(producto_bodega_destino_id=idpeb).order_by('-fecha_creacion')

    lista_trans = []

    for transaccion in qs:
        req = RecursoBusquedaDetalleVista()
        req.id = transaccion.id
        req.recurso = transaccion.producto.nombre
        fecha = localtime(transaccion.fecha_ejecucion)
        req.fecha = fecha.strftime('%Y-%m-%d %H:%M:%S')
        req.tipoTransaccion = transaccion.tipo.nombre  # TIPOTRX
        req.estadoTrans = transaccion.estado.nombre  # STATUSTRX

        localizacion1 = ""
        if str(transaccion.nivel_origen) != "":
            localizacion1 = localizacion1 + ", Nivel " + str(transaccion.nivel_origen)
        if str(transaccion.seccion_origen) != "":
            localizacion1 = localizacion1 + ", Seccion " + str(transaccion.seccion_origen)

        req.bodegaOrigen = transaccion.producto_bodega_origen.bodega.nombre + localizacion1
        req.nivel_origen = ""  # n/a
        req.seccion_origen = ""  # n/a

        localizacion2 = ""
        if str(transaccion.nivel_destino) != "":
            localizacion2 = localizacion2 + ", Nivel " + str(transaccion.nivel_destino)
        if str(transaccion.seccion_destino) != "":
            localizacion2 = localizacion2 + ", Seccion " + str(transaccion.seccion_destino)

        req.bodegaDestino = transaccion.producto_bodega_destino.bodega.nombre + localizacion2
        req.nivel_destino = ""  # n/a
        req.seccion_destino = ""  # n/a
        req.cantidad = str(transaccion.cantidad)
        req.unidad_medida = transaccion.unidad_medida.nombre
        req.comentarios = transaccion.comentarios
        lista_trans.append(req)

    json_string = json.dumps(lista_trans, cls=Convertidor)
    return JsonResponse(json_string, safe=False)


# HU: LCINV-5
# FB.
# Lista los productos, esto se utiliza para mostrar el listado en el html para la búsqueda.
# request: Petición desde el form de usuario.
# return: json con los datos encontrados
@csrf_exempt
def llenar_listado_productos_busqueda(request):
    qs = Producto.objects.all().order_by('nombre')
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False)


# HU: LCINV-5
# FB.
# Lista las bodegas, esto se utiliza para mostrar el listado en el html para la búsqueda.
# request: Petición desde el form de usuario.
# return: json con los datos encontrados
@csrf_exempt
def llenar_listado_bodegas_busqueda(request):
    qs = Bodega.objects.all().order_by('nombre')
    qs = qs.filter(~Q(nombre="Desperdicios"))
    qs = qs.filter(~Q(nombre="Proveedor"))
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False)

# ------------------------------------------

# HU: LCINV-21
# FB.
# Hace una búsqueda para saber en qué bodega está y cuál fue su última fecha de transacción.
# request: Petición desde el form de usuario.
# return: Página html con la plantilla y los resultados de la búsqueda asociada.
@csrf_exempt
def ver_conteoabc_busqueda(request):
    global tipoinventario
    tipoinventario = ""
    generar = ""
    opciones = ["A", "B", "C"]

    # valida si es el botón de filtro o de generar conteo
    # Capturar el valor de los campos
    if request.method == 'POST':
        tipoinventario = request.POST.get('tipoproductoinventario', "")
        generar=request.GET.get('btngenerar', "")

    if generar != "":
        id_conteo = generar_conteo(request)
        mensaje = "Se_genera_exitosamente_el_conteo_desde_el_sistema"
        return HttpResponseRedirect('/obtenerconteoabc/?id_conteo='+str(id_conteo)+'&mensaje='+mensaje)
    else:
        busqueda_conteoabc(request)

    context = {'tipoproductoinventario': tipoinventario, 'opciones': opciones}

    return render(request, "laboratorio/conteoabc.html", context)


def generar_conteo(request):
    # Aqui ya se supone que se validó que el request fuera POST y que proviniera del btngenerar.

    # Insertar registro en ConteoInventario
    estado = Tipo.objects.get(pk=Tipo.objects.filter(nombre='Ejecutada', grupo='STATUSCONTEO').first().id)

    conteo = ConteoInventario(fecha_creacion=datetime.now(),
                               usuario_creacion=Usuario.objects.get(pk=1),
                               estado=estado,
                               fecha_cambio_estado=datetime.now())
    conteo.save()

    # Capturar la información del formulario e insertar N registros en DetalleProductos
    qd = QueryDict(request.body)
    for values in qd.lists():
        for value in values:
            if value == "id":
                for valor in values[1]:
                    # Insercion
                    guardar_DetalleProductos_Estado_Inicial(conteo, valor)

    return conteo.id


def guardar_DetalleProductos_Estado_Inicial(conteo, peb_id):
    # Insertar registro en ConteoInventario
    producto_en_bodega = ProductosEnBodega.objects.get(pk=ProductosEnBodega.objects.filter(id=int(peb_id)))

    detalle = DetalleProductos(conteoinventario=conteo, productosenbodega=producto_en_bodega,
                               bodega=producto_en_bodega.bodega,
                               producto=producto_en_bodega.producto,
                               nivel=producto_en_bodega.nivel,
                               seccion=producto_en_bodega.seccion,
                               cantidad_contada=producto_en_bodega.cantidad,
                               unidad_medida=producto_en_bodega.unidad_medida,
                               usuario_conteo=Usuario.objects.get(pk=1)
                               )

    detalle.save()
    return True

# HU: LCINV-21
# FB.
# Hace una búsqueda para saber en qué bodega está y cuál fue su última fecha de transacción.
# Aquí puntualmente es donde se hace el filtro.
# request: Petición desde el form de usuario.
# return: json con los datos encontrados
@csrf_exempt
def busqueda_conteoabc(request):
    if tipoinventario == "A" or tipoinventario == "B" or tipoinventario == "C":
        qs = ProductosEnBodega.objects.all()
        qs = qs.filter(producto__tipo_producto_conteo='' + tipoinventario + '')
        # todo: quitar los productos en las bodegas que no deben salir (desperdicio, ...)
        qs = qs.filter(~Q(bodega__nombre="Desperdicios"))
        qs = qs.filter(~Q(bodega__nombre="Proveedor"))
    else:
        qs = ""

    lista_recurso = []

    for peb in qs:
        req = RecursoBusquedaVista()
        req.id = peb.id
        req.tipo_producto_conteo = peb.producto.tipo_producto_conteo
        req.nombre = peb.producto.nombre
        req.unidadesExistentes = peb.cantidad
        req.unidad_medida = peb.producto.unidad_medida.nombre
        req.cantidad_convertida = str(utils.convertir(req.unidadesExistentes, peb.unidad_medida.nombre,
                                                      peb.bodega.unidad_medida.nombre))

        localizacion = ""
        if str(peb.nivel) != "":
            localizacion = ", Nivel " + str(peb.nivel)
        if str(peb.seccion) != "":
            localizacion = localizacion + ", Seccion " + str(peb.seccion)

        req.bodegaActual = peb.bodega.nombre + localizacion

        lista_recurso.append(req)

    lista_recurso.sort(key=attrgetter('nombre', 'bodegaActual'), reverse=False)

    json_string = json.dumps(lista_recurso, cls=Convertidor)
    return JsonResponse(json_string, safe=False)
