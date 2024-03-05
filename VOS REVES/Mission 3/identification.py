import tkinter as tk
import mysql.connector
import subprocess
# Connexion à la base de données MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="Caron",
    password="Vos_reves_fou",
    database="vos_reves"
)

mycursor = mydb.cursor()
def open_second_window():
    subprocess.run(["python", "Hotel.pyw"])


def show_create_account():
    create_account_button.pack()
    first_name_label.pack()
    first_name_entry.pack()
    last_name_label.pack()
    last_name_entry.pack()
    email_label.pack()
    email_entry.pack()
    password_label.pack()
    password_entry.pack()
    create_account_link.pack_forget()
    no_account_label.pack_forget()
    create_account_button.pack()

def create_account():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    identifier = first_name + '.' + last_name

    # Insérer les informations dans la base de données
    sql = "INSERT INTO users (first_name, last_name, email, identifier, password) VALUES (%s, %s, %s, %s, %s)"
    val = (first_name, last_name, email, identifier, password)
    mycursor.execute(sql, val)
    mydb.commit()

    result_label.config(text=f"Compte créé pour {first_name} {last_name}")


    result_label.config(text=f"Votre identifiant est {identifier}")

def login():
    identifier = login_entry.get()
    password = login_password_entry.get()

    # Rechercher l'utilisateur dans la base de données
    sql = "SELECT identifier, password FROM users WHERE identifier = %s"
    mycursor.execute(sql, (identifier,))
    result = mycursor.fetchone()

    if result and result[1] == password:
        result_label.config(text=f"Connexion réussie en tant que {result[0]}")
        open_second_window()  # Appel de la fonction pour ouvrir la deuxième fenêtre
    else:
        result_label.config(text="Mot de passe incorrect")

# Création de la fenêtre principale
window = tk.Tk()
window.title("Programme d'Identification")
window.geometry("400x400")

# Création des éléments d'interface
first_name_label = tk.Label(window, text="Prénom:")
first_name_entry = tk.Entry(window)
last_name_label = tk.Label(window, text="Nom:")
last_name_entry = tk.Entry(window)
email_label = tk.Label(window, text="Adresse E-mail:")
email_entry = tk.Entry(window)
password_label = tk.Label(window, text="Mot de passe:")
password_entry = tk.Entry(window, show='*')
create_account_button = tk.Button(window, text="Créer un Compte", command=create_account)
login_button = tk.Button(window, text="Se Connecter", command=login)

login_label = tk.Label(window, text="Identifiant:")
login_entry = tk.Entry(window)
login_password_label = tk.Label(window, text="Mot de passe:")
login_password_entry = tk.Entry(window, show='*')

create_account_link = tk.Label(window, text="Pas de compte? Créez-en un maintenant!", fg="blue", cursor="hand2")
create_account_link.bind("<Button-1>", lambda e: show_create_account())
no_account_label = tk.Label(window, text="Déjà un compte? Connectez-vous!")

result_label = tk.Label(window, text="")

# Placement des éléments dans la fenêtre
login_label.pack()
login_entry.pack()
login_password_label.pack()
login_password_entry.pack()
login_button.pack()
result_label.pack()
no_account_label.pack()
create_account_link.pack()

# Créer le dossier 'data' s'il n'existe pas

# Lancer la fenêtre principale
window.mainloop()
