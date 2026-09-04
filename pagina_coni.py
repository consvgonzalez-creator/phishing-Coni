from flask import Flask, render_template_string

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
            transition: width 0.2s;
        }

        .hidden {
            display: none;
        }

        h1 {
            color: #ef4444;
        }
    </style>
</head>
<body>

<div class="container">

    <div id="loading">
        <h2>Extrayendo datos...</h2>
        <p>Por favor espere mientras se recopila información del dispositivo.</p>

        <div class="progress-container">
            <div class="progress-bar" id="progress"></div>
        </div>

        <p id="percent">0%</p>
    </div>

    <div id="result" class="hidden">
        <h1>⚠️ Simulación de Phishing</h1>

        <p>
            Has hecho clic en un enlace potencialmente malicioso.
        </p>

        <p>
            En un ataque real un actor malicioso podría haber intentado obtener
            credenciales corporativas o información sensible.
        </p>

        <h3>¿Qué debes revisar antes de hacer clic?</h3>

        <ul style="text-align:left;">
            <li>Remitente del correo.</li>
            <li>Dominio del enlace.</li>
            <li>Solicitudes inesperadas.</li>
            <li>Mensajes con urgencia excesiva.</li>
        </ul>

        <p>
            Esta fue una simulación autorizada por el equipo de Seguridad de la Información.
        </p>
    </div>

</div>

<script>
let progress = 0;

const interval = setInterval(() => {
    progress += 2;

    document.getElementById("progress").style.width = progress + "%";
    document.getElementById("percent").innerText = progress + "%";

    if (progress >= 100) {
        clearInterval(interval);

        document.getElementById("loading").classList.add("hidden");
        document.getElementById("result").classList.remove("hidden");
    }
}, 100);
</script>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)