import socket

from des import encrypt_text, decrypt_text


HOST = "0.0.0.0"
PORT = 5000


print("=" * 50)
print("DES RECEIVER")
print("=" * 50)

key = input("Masukkan key (8 karakter): ")

if len(key) != 8:
    print("ERROR: Key harus tepat 8 karakter.")
    exit()


# ------------------------------------------------------------
# CREATE SERVER
# ------------------------------------------------------------

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server.bind(
    (HOST, PORT)
)

server.listen(1)


print(f"\nReceiver aktif pada port {PORT}.")
print("Menunggu sender...")


# ------------------------------------------------------------
# ACCEPT CONNECTION
# ------------------------------------------------------------

connection, address = server.accept()

print(f"Sender terhubung dari {address}\n")


connection_file = connection.makefile(
    "rwb"
)


# ------------------------------------------------------------
# COMMUNICATION LOOP
# ------------------------------------------------------------

while True:

    # =========================
    # RECEIVE
    # =========================

    data = connection_file.readline()

    if not data:
        print("Sender menutup koneksi.")
        break


    received_ciphertext = data.decode().strip()

    print("[RECEIVE]")
    print("Ciphertext:", received_ciphertext)


    try:

        plaintext = decrypt_text(
            received_ciphertext,
            key
        )

    except Exception as e:
        print("Decryption error:", e)
        continue


    print("Plaintext :", plaintext)


    # EXIT
    if plaintext == "/exit":
        break


    # =========================
    # SEND RESPONSE
    # =========================

    reply = input("\nBalasan: ")


    try:

        ciphertext = encrypt_text(
            reply,
            key
        )

    except Exception as e:
        print("Encryption error:", e)
        continue


    print("\n[ENCRYPT]")
    print("Plaintext :", reply)
    print("Ciphertext:", ciphertext)


    connection_file.write(
        (ciphertext + "\n").encode()
    )

    connection_file.flush()


    if reply == "/exit":
        break


print("\nKoneksi ditutup.")

connection_file.close()
connection.close()
server.close()