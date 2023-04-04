from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL
app = Flask(__name__)

conexion = MySQL(app)


@app.route('/cursos', methods=['GET'])
def listar_cursos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM curso"
        cursor.execute(sql)
        datos = cursor.fetchall()
        cursos = []
        for fila in datos:
            curso = {'Codigo': fila[0], 'Nombre': fila[1], 'Creditos': fila[2]}
            cursos.append(curso)
        return jsonify({'Cursos': cursos, 'Mensaje': "Cursos Listados"})
    except Exception as ex:
        return jsonify({'Mensaje': "Error GET"})


@app.route('/cursos/<codigo>', methods=['GET'])
def leer_curso(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM curso WHERE codigo ='{0}'".format(codigo)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            curso = {'Codigo': datos[0],
                     'Nombre': datos[1], 'Creditos': datos[2]}
            return jsonify({'Cursos': curso, 'Mensaje': "Curso Encontrado"})
    except Exception as ex:
        return jsonify({'Mensaje': "Curso No Encontrado, GET"})


@app.route('/cursos', methods=['POST'])
def registrar_curso():
    try:
        # print(request.json)
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO curso (Codigo, Nombre, Creditos) 
        VALUES ('{0}', '{1}', '{2}')""".format(request.json['Codigo'],
                                               request.json['Nombre'], request.json['Creditos'])
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la accion de inserción
        return jsonify({'Mensaje': "Curso Registrado"})
    except Exception as ex:
        return jsonify({'Mensaje': "Error POST"})


@app.route('/cursos/<codigo>', methods=['DELETE'])
def eliminar_registros(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT Codigo FROM curso WHERE codigo ='{0}'".format(codigo)
        cursor.execute(sql)
        dato = cursor.fetchone()
        print(dato)
        if dato != None:
            sql = "DELETE From curso WHERE codigo ='{0}'".format(codigo)
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la accion de inserción
            return jsonify({'Mensaje': "Curso Eliminado"})
        else:
            return jsonify({'Mensaje': "No se encontro curso con codigo "+codigo})
    except Exception as ex:
        return jsonify({'Mensaje': "Error DELETE"})


@app.route('/cursos/<codigo>', methods=['PUT'])
def actualizar_registros(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "UPDATE curso SET Nombre = '{0}', Creditos ='{1}' WHERE Codigo = '{2}'".format(
            request.json['Nombre'], request.json['Creditos'], codigo)
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la accion de inserción
        return jsonify({'Mensaje': "Curso Actualizado"})
    except Exception as ex:
        return jsonify({'Mensaje': "Error PUT"})


def pagina_no_encontrada(error):
    return '<h1>F en el chat :v ...</h1>', 404


if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
