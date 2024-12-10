import hashlib
import time
from itertools import product
import string

# Definice funkcí pro crackování hashů

def brute_force_hash(hash_to_crack, charset, max_length):
    """
    Funkce pro brute-force útok na hash.
    :param hash_to_crack: Hash, který chceme prolomit.
    :param charset: Znaky použité pro generování kombinací.
    :param max_length: Maximální délka hesla.
    :return: Původní heslo, pokud je hash prolomen, jinak None.
    """
    start_time = time.time()
    attempts = 0

    for length in range(1, max_length + 1):
        for combination in product(charset, repeat=length):
            attempts += 1
            password = ''.join(combination)
            hashed = hashlib.md5(password.encode()).hexdigest()

            if hashed == hash_to_crack:
                end_time = time.time()
                print(f"Hash prolomen! Heslo: {password}")
                print(f"Počet pokusů: {attempts}")
                print(f"Čas: {end_time - start_time:.2f} sekund")
                return password

    print("Hash se nepodařilo prolomit.")
    return None


def dictionary_attack(hash_to_crack, dictionary_file):
    """
    Funkce pro útok pomocí slovníku.
    :param hash_to_crack: Hash, který chceme prolomit.
    :param dictionary_file: Soubor se seznamem slov.
    :return: Původní heslo, pokud je hash prolomen, jinak None.
    """
    start_time = time.time()
    attempts = 0

    with open(dictionary_file, 'r') as file:
        for line in file:
            attempts += 1
            password = line.strip()
            hashed = hashlib.md5(password.encode()).hexdigest()

            if hashed == hash_to_crack:
                end_time = time.time()
                print(f"Hash prolomen! Heslo: {password}")
                print(f"Počet pokusů: {attempts}")
                print(f"Čas: {end_time - start_time:.2f} sekund")
                return password

    print("Hash se nepodařilo prolomit pomocí slovníku.")
    return None


if __name__ == "__main__":
    print("Vyberte metodu crackování:")
    print("1 - Brute-force útok")
    print("2 - Útok pomocí slovníku")

    choice = int(input("Zadejte číslo metody: "))

    hash_to_crack = input("Zadejte hash (MD5): ").strip()

    if choice == 1:
        charset = string.ascii_lowercase + string.digits + string.punctuation
        max_length = int(input("Zadejte maximální délku hesla: "))
        brute_force_hash(hash_to_crack, charset, max_length)

    elif choice == 2:
        dictionary_file = input("Zadejte cestu k souboru se slovníkem: ").strip()
        dictionary_attack(hash_to_crack, dictionary_file)

    else:
        print("Neplatná volba. Ukončuji program.")
