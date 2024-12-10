from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Definice hesel podle složitosti
passwords = {
    0: "5612",  # 4 čísla
    1: "32276",  # 5 čísel
    2: "bzcd",  # 4 písmena
    3: "h4b2",  # 4 písmena a čísla
    4: "z+1c"  # 4 písmena, čísla a speciální znaky
}

# Ochrana proti brute force - sledujeme pokusy na IP adresu
attempts = {}

@app.route("/")
def index():
    """Nahrání HTML stránky s formulářem"""
    return render_template("index.html")


@app.route("/check-password", methods=["POST"])
def check_password():
    """Endpoint pro ověřování hesla"""
    from time import time

    # Získání IP adresy klienta
    ip = request.remote_addr
    current_time = time()

    # Ochrana: sledujeme pokusy za poslední minutu
    if ip not in attempts:
        attempts[ip] = []
    else:
        # Uchováváme pouze pokusy za poslední minutu
        attempts[ip] = [t for t in attempts[ip] if current_time - t < 60]

    # Pokud je pokusů více než 10, vrátíme chybu
    if len(attempts[ip]) >= 10:
        return jsonify({"result": "Too many attempts. Try again later."}), 429

    # Zaznamenání aktuálního pokusu
    attempts[ip].append(current_time)

    # Zpracování dat z POST požadavku
    data = request.json
    password = data.get("password", "")
    complexity = int(data.get("complexity", 0))

    # Kontrola hesla podle složitosti
    if complexity in passwords and password == passwords[complexity]:
        return jsonify({"result": "OK"})
    else:
        return jsonify({"result": "KO"})


if __name__ == "__main__":
    app.run(debug=True)
