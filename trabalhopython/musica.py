import pymysql
from db_config import connect_db
from flask import jsonify
from flask import Flask, request, Blueprint

musica_bp = Blueprint('musica_bp',__name__)

# Inserir música
@musica_bp.route('/musica', methods=['POST'])
def inserir_musica():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        data = request.json
        sql = "INSERT INTO musica (titulo, ano, genero, artista) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (data['titulo'], data['ano'], data['genero'], data['artista']))
        conn.commit()
        return jsonify({"message": "Música inserida com sucesso!", "success": True}), 201
    except Exception as e:
        return jsonify({"messagle": str(e), "success": False}), 500
    finally:
        cursor.close()
        conn.close()

# Atualizar música
@musica_bp.route('/musica/<int:id>', methods=['PUT'])
def atualizar_musica(id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        data = request.json
        sql = "UPDATE musica SET titulo = %s, ano = %s, genero = %s, artista = %s WHERE idmusica = %s"
        cursor.execute(sql, (data['titulo'], data['ano'], data['genero'], data['artista'], id))
        conn.commit()
        return jsonify({"message": "Música atualizada com sucesso!", "success": True}), 200
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500
    finally:
        cursor.close()
        conn.close()

# Deletar música
@musica_bp.route('/musica/<int:id>', methods=['DELETE'])
def deletar_musica(id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = "DELETE FROM musica WHERE idmusica = %s"
        cursor.execute(sql, (id,))
        conn.commit()
        return jsonify({"message": "Música excluída com sucesso!", "success": True}), 200
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500
    finally:
        cursor.close()
        conn.close()

# Listar músicas (com filtro opcional por título)
@musica_bp.route("/musica", methods=["POST"])
def listar():
    try:
        conn = connect_db()
        cur = conn.cursor(pymysql.cursors.DictCursor)

        # Obtendo dados do JSON
        musica = request.json
        titulo = musica["titulo"]
        artista = musica["artista"]
        ano = musica["ano"]
        genero = musica["genero"]

        # Inserindo no banco
        cur.execute(
            "INSERT INTO musica (titulo, artista, ano, genero) VALUES (%s, %s, %s, %s)",
            (titulo, artista, ano, genero)
        )
        conn.commit()

        resp = jsonify({"message": "Música inserida com sucesso!"})
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()

# Buscar por ID
@musica_bp.route('/musica/<int:id>', methods=['GET'])
def buscar_musica_por_id(id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = "SELECT * FROM musica WHERE idmusica = %s"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if row:
            return jsonify(row), 200
        else:
            return jsonify({"message": "Não encontrada", "success": False}), 404
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500
    finally:
        cursor.close()
        conn.close()
