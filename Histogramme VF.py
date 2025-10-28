# histogramme.py - À exécuter sur votre PC
import matplotlib.pyplot as plt

# Lecture du fichier journal
try:
    with open("journal.txt", "r") as f:
        temps = [float(line.strip()) for line in f if line.strip()]
    
    if not temps:
        print("Aucune donnée dans le fichier journal!")
        exit()
    
    # Création de l'histogramme
    plt.figure(figsize=(10, 6))
    plt.hist(temps, bins=15, edgecolor='black', alpha=0.7, color='skyblue')
    
    # Personnalisation du graphique
    plt.axvline(x=15, color='red', linestyle='--', linewidth=2, label='Temps cible (15s)')
    plt.xlabel('Temps mesuré (secondes)')
    plt.ylabel("Nombre d'essais")
    plt.title('Précision de la perception du temps')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Affichage des statistiques
    moyenne = sum(temps) / len(temps)
    print(f"Nombre d'essais: {len(temps)}")
    print(f"Moyenne: {moyenne:.2f} secondes")
    print(f"Écart moyen avec 15s: {abs(moyenne-15):.2f} secondes")
    
    plt.show()
    
except FileNotFoundError:
    print("Fichier 'journal.txt' non trouvé!")
except Exception as e:
    print("Erreur:", e)