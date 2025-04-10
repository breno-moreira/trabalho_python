import pymysql
from db_config import connect_db
from flask import request, Blueprint, jsonify

musica_bp = Blueprint('musica')

@musica_bp.route('/musica')
def get_musicas():
    try:
        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM musica")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@musica_bp.route('/musica/<int:id>')
def get_musica_by_id(id):
    try:
        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM musica WHERE id=%s", (id,))
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@musica_bp.route('/musica/pesquisa/<string:pesquisa>')
def search_musica(pesquisa):
    try:
        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM musicas WHERE titulo LIKE %s", (f"%{pesquisa}%",))
        row = cursor.fetchall()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@musica_bp.route('/musica', methods=['POST'])
def add_musica():
    try:
        _json = request.json
        _titulo = _json['titulo']
        _ano = _json['ano']
        _artista = _json['artista']
        _genero = _json['genero']

        if _titulo and _ano and _artista and _genero:
            sql = "INSERT INTO musica(titulo, ano, artista, genero) VALUES(%s, %s, %s, %s)"
            data = (_titulo, _ano, _artista, _genero)
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Música adicionada com sucesso!')
            resp.status_code = 200
            return resp
        else:
            return jsonify({'error': 'Dados incompletos'}), 400
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@musica_bp.route('/musica/<int:id>', methods=['PUT'])
def update_musica(id):
    try:
        _json = request.json
        _titulo = _json['titulo']
        _ano = _json['ano']
        _artista = _json['artista']
        _genero = _json['genero']

        if _titulo and _ano and _artista and _genero:
            sql = """UPDATE musica SET titulo=%s, ano=%s, artista=%s, genero=%s WHERE id=%s"""
            data = (_titulo, _ano, _artista, _genero, id)
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Música atualizada com sucesso!')
            resp.status_code = 200
            return resp
        else:
            return jsonify({'error': 'Dados incompletos'}), 400
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@musica_bp.route('/musica/<int:id>', methods=['DELETE'])
def delete_musica(id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM musica WHERE id=%s", (id,))
        conn.commit()
        resp = jsonify('Música deletada com sucesso!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close