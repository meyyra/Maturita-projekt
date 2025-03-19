import bcrypt

USER_FILE = "users.txt"

def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    with open(USER_FILE, "a") as file:
        file.write(f"{username}:{hashed_password}\n")
    print(f"Uživatel '{username}' byl úspěšně zaregistrován.")

# Zadej uživatelské jméno a heslo
username = input("Zadej uživatelské jméno: ")
password = input("Zadej heslo: ")

register_user(username, password)