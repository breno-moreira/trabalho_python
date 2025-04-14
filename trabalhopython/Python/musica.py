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
        sql = "INSERT INTO musica1 (titulo, ano, genero, artista) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (data['titulo'], data['ano'], data['genero'], data['artista']))
        conn.commit()
        return jsonify({"message": "Música inserida com sucesso!", "success": True}), 201
    except Exception as e:
        return jsonify({"messagle": str(e), "success": False}), 500
    finally:
        cursor.close()
        conn.close()

# Atualizar música
@musica_bp.route("/musica/<id>/", methods=["PUT"])
def editar(id):
    try:
        conn = connect_db()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        musica = request.json
        titulo = musica["titulo"]
        artista = musica["artista"]
        ano = musica["ano"]
        genero = musica["genero"]

        cur.execute("""
            UPDATE musica 
            SET titulo = %s, artista = %s, ano = %s, genero = %s 
            WHERE idmusica = %s
        """, (titulo, artista, ano, genero, id))
        
        conn.commit()
        resp = jsonify({"message": "Música alterada com sucesso!"})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Deletar música
@musica_bp.route('/musica/<int:id>', methods=['DELETE'])
def deletar_musica(id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = "DELETE FROM musica1 WHERE idmusica = %s"
        cursor.execute(sql, (id,))
        conn.commit()
        return jsonify({"message": "Música excluída com sucesso!", "success": True}), 200
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500
    finally:
        cursor.close()
        conn.close()

# Listar músicas
@musica_bp.route('/musica', methods=['GET'])
def listar():
    try:
        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM musica1")
        rows = cursor.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        print("Erro ao listar músicas:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# Buscar por ID
@musica_bp.route('/musica/<int:id>', methods=['GET'])
def buscar_musica_por_id(id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = "SELECT * FROM musica1 WHERE idmusica = %s"
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
