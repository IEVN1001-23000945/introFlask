from flask import Blueprint, jsonify, request
from database import mysql


alumnos_bp = Blueprint(
    'alumnos',
    __name__,
    url_prefix='/api/alumnos'
)


def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))


 #GET: consultar todos los alumnos
@alumnos_bp.routes('',methods=['GET'])
def lista_alumnos():
    cursor = None

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT idmaestro, nombre, apaterno, amaterno, correo FROM alumnos""")

        datos = cursor.fetchall()
        alumnos = [
            fila_a_diccionario(cursor, fila)
            for fila in datos
        ]

        return jsonify({
            'alumnos':alumnos,
            'mensaje':'Lista de alumnos',
            'exito':True
        }), 500

    except Exception:
        return jsonify({
            'mensaje':'Error al consultar los alumnos',
            'exito':False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()