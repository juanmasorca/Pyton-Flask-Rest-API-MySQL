from flask import Flask, jsonify
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
        return jsonify({'Mensaje': "Error"})


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
        return jsonify({'Mensaje': "Curso No Encontrado"})


def pagina_no_encontrada(error):
    return '<h1>F en el chat :v ...</h1>', 404


if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
