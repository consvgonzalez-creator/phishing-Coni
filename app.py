from flask import Flask, render_template_string, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Validando información...</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #111827;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .container {
            width: 700px;
            text-align: center;
        }

        .progress-container {
            width: 100%;
            background-color: #374151;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 20px;
        }

        .progress-bar {
            height: 30px;
            width: 0%;
            background-color: #ef4444;
        }

        .hidden {
            display: none;
        }

        table {
            border-collapse: collapse;
            width: 100%;
        }

        td, th {
            border: 1px solid #ccc;
            padding: 8px;
        }
    </style>
</head>
<body>

<div class="container">

    <div id="loading">
        <h2 id="mensaje">Extrayendo datos...</h2>

        <div class="progress-container">
            <div id="progress" class="progress-bar"></div>
        </div>

        <p id="percent">0%</p>
    </div>

    <div id="result" class="hidden">

        <h1>⚠️ Simulación de Phishing</h1>

        <p>
            Has interactuado con un enlace que podría haber sido utilizado
            para comprometer información corporativa.
        </p>

        <p>
            Esta actividad forma parte de una campaña de concientización de seguridad.
        </p>

    </div>

</div>

<script>

let progress = 0;
const totalTime = 40000;
const stepTime = totalTime / 100;

const interval = setInterval(() => {

    progress++;

    document.getElementById("progress").style.width = progress + "%";
    document.getElementById("percent").innerText = progress + "%";

    const mensaje = document.getElementById("mensaje");

    if(progress < 25){
        mensaje.innerText = "Analizando dispositivo...";
    }
    else if(progress < 50){
        mensaje.innerText = "Extrayendo datos...";
    }
    else if(progress < 75){
        mensaje.innerText = "Validando credenciales...";
    }
    else{
        mensaje.innerText = "Generando reporte...";
    }

    if(progress >= 100){
        clearInterval(interval);

        document.getElementById("loading").classList.add("hidden");
        document.getElementById("result").classList.remove("hidden");
    }

}, stepTime);

</script>

</body>
</html>
"""


def init_db():
    conn = sqlite3.connect("estadisticas.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS visitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            ip TEXT,
            user_agent TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def index():

    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("estadisticas.db")
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO visitas (fecha, ip, user_agent)
        VALUES (?, ?, ?)
        """,
        (fecha, ip, user_agent)
    )

    conn.commit()
    conn.close()

    return render_template_string(HTML)


@app.route("/stats")
def stats():

    conn = sqlite3.connect("estadisticas.db")
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM visitas")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT ip) FROM visitas")
    unicos = cur.fetchone()[0]

    cur.execute("""
        SELECT fecha, ip
        FROM visitas
        ORDER BY id DESC
        LIMIT 100
    """)

    registros = cur.fetchall()

    conn.close()

    html = f"""
    <h1>Estadísticas</h1>

    <h3>Total Accesos: {total}</h3>
    <h3>IPs Únicas: {unicos}</h3>

    <table>
        <tr>
            <th>Fecha</th>
            <th>IP</th>
        </tr>
    """

    for fecha, ip in registros:
        html += f"<tr><td>{fecha}</td><td>{ip}</td></tr>"

    html += "</table>"

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)