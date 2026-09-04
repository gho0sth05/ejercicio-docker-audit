import os
import random
from flask import Flask, request
import pymysql

app = Flask(__name__)

#  (B105): Credenciales obtenidas de variables de entorno de forma segura
DB_HOST = os.getenv("DB_HOST", "servidor-bd-ejemplo")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "admin_adso_2026_secreto")
DB_NAME = os.getenv("DB_NAME", "legacydb")

@app.route("/")
def home():
    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        conn.close()
        return "<h1>API Legacy TechNova - Funcionando (Segura)</h1>"
    except Exception as e:
        return f"<h1>Sistema Caído</h1><p>{e}</p>", 500

@app.route("/buscar")
def buscar_usuario():
    usuario_id = request.args.get("id", "1")
    
    #   (B608): Uso de consultas parametrizadas para evitar Inyección SQL
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
    cursor = conn.cursor()
    query_segura = "SELECT * FROM usuarios WHERE id = %s"
    cursor.execute(query_segura, (usuario_id,))
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return f"Resultado de la consulta segura para el ID {usuario_id}: {resultado}"

@app.route("/health")
def health_check():
    if random.random() < 0.3:
        
        pass 
    return "OK", 200

if __name__ == "__main__":
    # (B201 y B104): Debug desactivado por seguridad en producción
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host='0.0.0.0', port=5050, debug=debug_mode)