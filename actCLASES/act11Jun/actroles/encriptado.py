from cryptography.fernet import Fernet

# Generar una clave de encriptacion
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encriptación de un mensaje
mensaje = b"Este es un mensaje clasificado!"
cipher_text = cipher_suite.encrypt(mensaje)
print(f"Mensaje encriptado {cipher_text}")

# Desencriptar mensaje
plain_text = cipher_suite.decrypt(cipher_text)
print(f"Mensaje desencriptado: {plain_text.decode()}")

