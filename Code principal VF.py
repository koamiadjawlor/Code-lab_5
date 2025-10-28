#Ce code a été rédigé avec l'aide de l'IA Deepseeke. Il est destiné à être exécuté sur une carte MicroPython équipéed'un module RTC DS3231 et d'un bouton poussoir. 
#Le programme permet de mesurer la perception du temps en demandant à l'utilisateur de compter 15 secondes entre deux appuis sur le bouton. 
#Les temps mesurés sont sauvegardés dans un fichier texte pour une analyse ultérieure.


from machine import I2C, Pin
import utime

# Configuration DS3231
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=100000)
# Bouton avec PULL_DOWN 
button = Pin(22, Pin.IN, Pin.PULL_DOWN)

def read_ds3231_time():
    """Lit l'heure actuelle depuis le DS3231 et retourne le total en secondes depuis minuit"""
    try:
        # Lecture des registres secondes, minutes, heures
        data = i2c.readfrom_mem(0x68, 0x00, 3)
        
        # Conversion BCD vers décimal
        seconds = ((data[0] >> 4) * 10) + (data[0] & 0x0F)
        minutes = ((data[1] >> 4) * 10) + (data[1] & 0x0F)
        hours = ((data[2] >> 4) * 10) + (data[2] & 0x0F)
        
        # Total en secondes depuis minuit
        return hours * 3600 + minutes * 60 + seconds
    except Exception as e:
        print("Erreur lecture RTC:", e)
        return 0

def wait_button_press():
    """Attend un appui propre sur le bouton (avec anti-rebond)"""
    # Attente que le bouton soit relâché d'abord (valeur = 0 avec PULL_DOWN)
    while button.value():  # Attente que le bouton soit relâché
        utime.sleep_ms(20)
    
    # Attente de l'appui (valeur = 1 avec PULL_DOWN)
    while not button.value():  # Attente que le bouton soit appuyé
        utime.sleep_ms(10)
    
    # Anti-rebond
    utime.sleep_ms(50)

# Liste pour stocker les temps mesurés
journal = []

print("=== Jeu de perception du temps ===")
print("Consigne: Appuyez pour demarrer, puis comptez 15 secondes dans votre tete")
print("et appuyez a nouveau quand vous pensez que 15 secondes sont ecoulees.")
print("Appuyez pour commencer chaque essai. CTRL+C pour terminer.\n")

try:
    essai_numero = 1
    
    while True:
        print(f"--- Essai #{essai_numero} ---")
        print("Appuyez sur le bouton pour COMMENCER a compter...")
        
        # Premier appui - début du comptage
        wait_button_press()
        temps_debut = read_ds3231_time()
        print("Comptez 15 secondes dans votre tete...")
        
        # Deuxième appui - fin du comptage  
        print("Appuyez quand vous pensez que 15 secondes sont ecoulees...")
        wait_button_press()
        temps_fin = read_ds3231_time()
        
        # Calcul de la durée mesurée
        if temps_fin >= temps_debut:
            duree_mesuree = temps_fin - temps_debut
        else:
            # Gestion du passage à minuit
            duree_mesuree = (temps_fin + 86400) - temps_debut
        
        # Affichage du résultat
        print(f"Temps mesure: {duree_mesuree} secondes")
        difference = duree_mesuree - 15
        if difference > 0:
            print(f"Vous etiez trop lent de {difference} secondes")
        elif difference < 0:
            print(f"Vous etiez trop rapide de {abs(difference)} secondes")
        else:
            print(f"Parfait! Exactement 15 secondes!")
        
        # Sauvegarde dans le journal
        journal.append(duree_mesuree)
        essai_numero += 1
        print()  # Ligne vide pour séparer les essais
        
except KeyboardInterrupt:
    # Sauvegarde finale dans la mémoire flash
    print("\n" + "="*50)
    print("Fin du programme - Sauvegarde du journal...")
    
    if journal:
        try:
            with open("journal.txt", "w") as fichier:
                for temps in journal:
                    fichier.write(str(temps) + "\n")
            
            print(f"Journal sauvegarde dans la memoire flash")
            print(f"{len(journal)} essai(s) enregistré(s) dans 'journal.txt'")
            print(f"Temps enregistres: {journal}")
            
        except Exception as e:
            print(" Erreur lors de la sauvegarde:", e)
    else:
        print(" Aucune donnee a sauvegarder!")