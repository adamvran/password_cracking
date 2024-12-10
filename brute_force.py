import requests
import itertools
import string
import time

# URL serveru
url = "http://127.0.0.1:5000/check-password"

# Funkce pro brute-force útok
def brute_force(complexity_level):
    # Definice znakových sad podle složitosti
    charsets = {
        0: string.digits,  # 4 čísla
        1: string.digits,  # 5 čísel
        2: string.ascii_lowercase,  # 4 písmena
        3: string.ascii_lowercase + string.digits,  # 4 písmena a čísla
        4: string.ascii_lowercase + string.digits + "!@#$%^&*()"  # 4 písmena, čísla a speciální znaky
    }

    max_lengths = {0: 4, 1: 5, 2: 4, 3: 4, 4: 4}
    charset = charsets[complexity_level]
    max_length = max_lengths[complexity_level]

    attempts = 0
    start_time = time.time()

    # Generování kombinací a pokus o prolomení hesla
    for length in range(1, max_length + 1):
        for combination in itertools.product(charset, repeat=length):
            password = "".join(combination)
            attempts += 1

            # Odesílání požadavku na server
            response = requests.post(url, json={"password": password, "complexity": complexity_level})
            if response.status_code == 200 and response.text == "OK":
                end_time = time.time()
                print(f"Heslo prolomeno: {password}")
                print(f"Počet pokusů: {attempts}")
                print(f"Čas: {end_time - start_time:.2f} sekund")
                return

    print("Heslo nebylo prolomeno.")

# Spuštění brute-force útoku
if __name__ == "__main__":
    print("Vyberte úroveň složitosti hesla:")
    print("0 - 4 čísla")
    print("1 - 5 čísel")
    print("2 - 4 písmena")
    print("3 - 4 písmena a čísla")
    print("4 - 4 písmena, čísla a speciální znaky")

    complexity = int(input("Zadejte složitost (0-4): "))
    brute_force(complexity)
