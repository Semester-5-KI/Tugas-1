import socket

from des import encrypt_text, decrypt_text


HOST = "127.0.0.1"
PORT = 5000


print("=" * 50)
print("              DES SENDER")
print("=" * 50)

key = input("Masukkan key (8 karakter): ")

if len(key) != 8:
    print("ERROR: Key harus tepat 8 karakter.")
    exit()


# ------------------------------------------------------------
# CONNECT TO RECEIVER
# ------------------------------------------------------------

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

print(f"\nMenghubungkan ke {HOST}:{PORT}...")

client.connect((HOST, PORT))

print("Terhubung ke receiver.\n")


# File wrapper agar kita bisa menggunakan readline()
connection = client.makefile(
    "rwb"
)


# ------------------------------------------------------------
# COMMUNICATION LOOP
# ------------------------------------------------------------

while True:

    # =========================
    # SEND
    # =========================

    plaintext = input("Pesan untuk receiver: ")

    try:

        ciphertext = encrypt_text(
            plaintext,
            key
        )

    except Exception as e:
        print("Encryption error:", e)
        continue


    print("\n[ENCRYPT]")
    print("Plaintext :", plaintext)
    print("Ciphertext:", ciphertext)

    # Kirim ciphertext
    connection.write(
        (ciphertext + "\n").encode()
    )

    connection.flush()


    # Kalau user mengirim EXIT
    if plaintext == "/exit":
        break


    # =========================
    # RECEIVE
    # =========================

    data = connection.readline()

    if not data:
        print("Receiver menutup koneksi.")
        break


    received_ciphertext = data.decode().strip()

    print("\n[RECEIVE]")
    print("Ciphertext:", received_ciphertext)


    try:

        received_plaintext = decrypt_text(
            received_ciphertext,
            key
        )

    except Exception as e:
        print("Decryption error:", e)
        continue


    print("Plaintext :", received_plaintext)


    if received_plaintext == "/exit":
        break


print("\nKoneksi ditutup.")

connection.close()
client.close()