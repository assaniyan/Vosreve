import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import mysql.connector

# Connexion à la base de données MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="Caron",
    password="Vos_reves_fou",
    database="vos_reves"
)

mycursor = mydb.cursor()

# Liste pour stocker les pièces jointes avec les heures
attachments = {"Repas Midi": {}, "Repas Soir": {}}

def import_justificatif(category):
    file_path = filedialog.askopenfilename(filetypes=[("Fichiers PDF et images", "*.pdf *.png *.jpg")])
    if file_path:
        heure = datetime.now().strftime("%H:%M:%S")
        attachments[category] = {"file": file_path, "heure": heure}
        messagebox.showinfo("Succès", "Justificatif importé avec succès.")

def save_to_database(nom_prenom, repas_midi, repas_soir, nuits_hotel, carburant, frais_autoroute, remboursement_repas_midi, remboursement_repas_soir, remboursement_nuits_hotel, remboursement_carburant, remboursement_frais_autoroute, total_depense, total_remboursement, difference):
    sql = "INSERT INTO remboursements (nom_prenom, repas_midi, repas_soir, nuits_hotel, carburant, frais_autoroute, justificatif_repas_midi, justificatif_repas_soir, justificatif_nuits_hotel, justificatif_carburant, justificatif_frais_autoroute, total_depense, total_remboursement, difference) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (nom_prenom, repas_midi, repas_soir, nuits_hotel, carburant, frais_autoroute,
           bool(attachments.get("Repas Midi")), bool(attachments.get("Repas Soir")),
           bool(attachments.get("Nuits d'hôtel")), bool(attachments.get("Carburant")),
           bool(attachments.get("Frais d'autoroute")), total_depense, total_remboursement, difference)
    mycursor.execute(sql, val)
    mydb.commit()

def check_justificatifs():
    justificatifs_requis = ["Repas Midi", "Repas Soir", "Nuits d'hôtel", "Carburant", "Frais d'autoroute"]
    for justificatif in justificatifs_requis:
        if justificatif not in attachments:
            return False
    return True

def calcul_remboursement():
    try:
        repas_midi = float(repas_midi_entry.get())
        repas_soir = float(repas_soir_entry.get())
        nuits_hotel = float(nuits_hotel_entry.get())
        carburant = float(carburant_entry.get())
        frais_autoroute = float(frais_autoroute_entry.get())
        nom_prenom = nom_prenom_entry.get()

        if repas_midi > 0:
            import_justificatif("Repas Midi")
        if repas_soir > 0:
            import_justificatif("Repas Soir")
        if nuits_hotel > 0:
            import_justificatif("Nuits d'hôtel")
        if carburant > 0:
            import_justificatif("Carburant")
        if frais_autoroute > 0:
            import_justificatif("Frais d'autoroute")

        remboursement_repas_midi = min(repas_midi, 30.0)
        remboursement_repas_soir = min(repas_soir, 30.0)
        remboursement_nuits_hotel = min(nuits_hotel, 110.0)
        remboursement_carburant = carburant
        remboursement_frais_autoroute = frais_autoroute
        total_depense = repas_midi + repas_soir + nuits_hotel + carburant + frais_autoroute
        total_remboursement = remboursement_repas_midi + remboursement_repas_soir + remboursement_nuits_hotel + remboursement_carburant + remboursement_frais_autoroute
        difference = total_depense - total_remboursement

        result_text.set(f"Remboursement détaillé :\n"
                        f"Nom et Prénom : {nom_prenom}\n"
                        f"Repsas Midi : {remboursement_repas_midi} € ({attachment.get('Repas Midi', {}).get('heure', '')})\n"
                        f"Repas Soir : {remboursement_repas_soir} € ({attachments.get('Repas Soir', {}).get('heure', '')})\n"
                        f"Nuits d'hôtel : {remboursement_nuits_hotel} € ({attachments.get('Nuits d hôtel', {}).get('heure', '')})\n"
                        f"Carburant : {remboursement_carburant} € ({attachments.get('Carburant', {}).get('heure', '')})\n"
                        f"Frais d'autoroute : {remboursement_frais_autoroute} € ({attachments.get('Frais d autoroute', {}).get('heure', '')})\n"
                        f"Total dépensé : {total_depense} €\n"
                        f"Total remboursé : {total_remboursement} €\n"
                        f"Différence : {difference} €")

        repas_midi_attachment_label.grid(row=10, column=0, columnspan=4)
        repas_soir_attachment_label.grid(row=11, column=0, columnspan=4)
        nuits_hotel_attachment_label.grid(row=12, column=0, columnspan=4)
        carburant_attachment_label.grid(row=13, column=0, columnspan=4)
        frais_autoroute_attachment_label.grid(row=14, column=0, columnspan=4)
        repas_midi_attachment_button.grid(row=10, column=4)
        repas_soir_attachment_button.grid(row=11, column=4)
        nuits_hotel_attachment_button.grid(row=12, column=4)
        carburant_attachment_button.grid(row=13, column=4)
        frais_autoroute_attachment_button.grid(row=14, column=4)
        export_pdf_button.config(state="active")

        # Enregistrement des informations dans la base de données
        save_to_database(nom_prenom, repas_midi, repas_soir, nuits_hotel, carburant, frais_autoroute)

    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")

def exporter_pdf():
    if check_justificatifs():
        c = canvas.Canvas("rapport_remboursement.pdf", pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 770, "Note de Service")
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, "La société Vos Rêves")
        c.setFont("Helvetica", 12)
        c.setFillColorRGB(0, 0, 0)
        text = result_text.get()
        text_lines = text.split('\n')
        line_height = 15
        y_position = 710

        for line in text_lines:
            c.drawString(100, y_position, line)
            y_position -= line_height

        # Ajoutez les pièces jointes au PDF avec les heures
        for category, attachment_info in attachments.items():
            c.showPage()
            c.drawString(100, 770, f"Justificatif pour {category} ({attachment_info['heure']}):")
            c.drawImage(attachment_info['file'], 100, 100, width=400, height=400)

        c.save()
    else:
        messagebox.showwarning("Justificatifs manquants", "Veuillez ajouter tous les justificatifs avant d'exporter le PDF.")

root = tk.Tk()
root.geometry("550x700")
root.title("Gestion des Remboursements AP")

root.configure(bg="#F2F2F2")

repas_midi_attachment_label = tk.Label(root, text="Justificatif pour repas midi:")
repas_soir_attachment_label = tk.Label(root, text="Justificatif pour repas soir:")
nuits_hotel_attachment_label = tk.Label(root, text="Justificatif pour nuits d'hôtel:")
carburant_attachment_label = tk.Label(root, text="Justificatif pour carburant:")
frais_autoroute_attachment_label = tk.Label(root, text="Justificatif pour frais d'autoroute:")
repas_midi_attachment_label.grid(row=10, column=0, columnspan=4)
repas_soir_attachment_label.grid(row=11, column=0, columnspan=4)
nuits_hotel_attachment_label.grid(row=12, column=0, columnspan=4)
carburant_attachment_label.grid(row=13, column=0, columnspan=4)
frais_autoroute_attachment_label.grid(row=14, column=0, columnspan=4)

repas_midi_attachment_button = tk.Button(root, text="Ajouter", command=lambda: import_justificatif("Repas Midi"))
repas_soir_attachment_button = tk.Button(root, text="Ajouter", command=lambda: import_justificatif("Repas Soir"))
nuits_hotel_attachment_button = tk.Button(root, text="Ajouter", command=lambda: import_justificatif("Nuits d'hôtel"))
carburant_attachment_button = tk.Button(root, text="Ajouter", command=lambda: import_justificatif("Carburant"))
frais_autoroute_attachment_button = tk.Button(root, text="Ajouter", command=lambda: import_justificatif("Frais d'autoroute"))
repas_midi_attachment_button.grid(row=10, column=4)
repas_soir_attachment_button.grid(row=11, column=4)
nuits_hotel_attachment_button.grid(row=12, column=4)
carburant_attachment_button.grid(row=13, column=4)
frais_autoroute_attachment_button.grid(row=14, column=4)

repas_midi_label = tk.Label(root, text="Montant des repas midi (€):", bg="#F2F2F2")
repas_midi_label.grid(row=0, column=0)
repas_midi_entry = tk.Entry(root)
repas_midi_entry.grid(row=0, column=1)

repas_soir_label = tk.Label(root, text="Montant des repas soir (€):", bg="#F2F2F2")
repas_soir_label.grid(row=1, column=0)
repas_soir_entry = tk.Entry(root)
repas_soir_entry.grid(row=1, column=1)

nuits_hotel_label = tk.Label(root, text="Montant des nuits d'hôtel (€):", bg="#F2F2F2")
nuits_hotel_label.grid(row=2, column=0)
nuits_hotel_entry = tk.Entry(root)
nuits_hotel_entry.grid(row=2, column=1)

carburant_label = tk.Label(root, text="Montant du carburant (€):", bg="#F2F2F2")
carburant_label.grid(row=3, column=0)
carburant_entry = tk.Entry(root)
carburant_entry.grid(row=3, column=1)

frais_autoroute_label = tk.Label(root, text="Montant des frais d'autoroute (€):", bg="#F2F2F2")
frais_autoroute_label.grid(row=4, column=0)
frais_autoroute_entry = tk.Entry(root)
frais_autoroute_entry.grid(row=4, column=1)

nom_prenom_label = tk.Label(root, text="Nom et Prénom:", bg="#F2F2F2")
nom_prenom_label.grid(row=5, column=0)
nom_prenom_entry = tk.Entry(root)
nom_prenom_entry.grid(row=5, column=1)

calcul_button = tk.Button(root, text="Calculer Remboursement", command=calcul_remboursement, bg="#4CAF50", fg="white")
calcul_button.grid(row=6, column=0, columnspan=2)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, bg="#F2F2F2", font=("Helvetica", 12))
result_label.grid(row=15, column=0, columnspan=4)

export_pdf_button = tk.Button(root, text="Exporter en PDF", command=exporter_pdf, bg="#4CAF50", fg="white", state="disabled")
export_pdf_button.grid(row=16, column=0, columnspan=4)

root.mainloop()
