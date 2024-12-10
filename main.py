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

# Ochrana proti brute force - pokusy za minutu
attempts = {}


@app.route("/")
def index():
    # Načtení HTML stránky s formulářem
    return render_template("index.html")


@app.route("/check-password", methods=["POST"])
def check_password():
    from time import time

    # Získání IP adresy klienta
    ip = request.remote_addr
    current_time = time()

    # Ochrana: sledujeme pokusy za poslední minutu
    if ip not in attempts:
        attempts[ip] = []
    else:
        # Uchováme jen pokusy z poslední minuty
        attempts[ip] = [t for t in attempts[ip] if current_time - t < 60]

    # Pokud je pokusů víc než 10 za poslední minutu, vrátíme chybu
    if len(attempts[ip]) >= 100000:
        return jsonify({"result": "Too many attempts. Try later."}), 429

    # Přidání aktuálního pokusu
    attempts[ip].append(current_time)

    # Zpracování dat z formuláře
    data = request.json
    password = data.get("password", "")
    complexity = int(data.get("complexity", 0))

    # Ověření hesla podle složitosti
    if complexity in passwords and password == passwords[complexity]:
        return jsonify({"result": "OK"})
    else:
        return jsonify({"result": "KO"})


if __name__ == "__main__":
    app.run(debug=True)
