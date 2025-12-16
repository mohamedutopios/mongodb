# Importation du client MongoDB pour se connecter à la base de données
from pymongo import MongoClient
# Importation de datetime pour gérer les dates et heures
from datetime import datetime

def afficher_separateur(titre):
    """Affiche un séparateur visuel"""
    # Affiche une ligne vide suivie d'une ligne de 60 caractères '='
    print("\n" + "="*60)
    # Affiche le titre centré avec des espaces
    print(f"  {titre}")
    # Affiche une autre ligne de 60 caractères '='
    print("="*60)

def afficher_tous_documents(collection):
    """Affiche tous les documents de la collection"""
    # Récupère tous les documents de la collection et les convertit en liste
    documents = list(collection.find())
    # Vérifie si la liste de documents n'est pas vide
    if documents:
        # Parcourt chaque document dans la liste
        for doc in documents:
            # Affiche l'ID unique du document (généré automatiquement par MongoDB)
            print(f"  ID: {doc['_id']}")
            # Affiche le nom et prénom, ou 'N/A' si ces champs n'existent pas
            print(f"  Nom: {doc.get('nom', 'N/A')} {doc.get('prenom', 'N/A')}")
            # Affiche l'âge, ou 'N/A' si ce champ n'existe pas
            print(f"  Age: {doc.get('age', 'N/A')} ans")
            # Affiche l'email, ou 'N/A' si ce champ n'existe pas
            print(f"  Email: {doc.get('email', 'N/A')}")
            # Affiche la ville, ou 'N/A' si ce champ n'existe pas
            print(f"  Ville: {doc.get('ville', 'N/A')}")
            # Affiche la profession, ou 'N/A' si ce champ n'existe pas
            print(f"  Profession: {doc.get('profession', 'N/A')}")
            # Affiche une ligne de séparation entre chaque document
            print("-" * 40)
    else:
        # Si aucun document n'est trouvé, affiche un message
        print("  Aucun document trouvé")
    # Affiche le nombre total de documents trouvés
    print(f"Total: {len(documents)} document(s)\n")

def connecter_mongodb():
    """
    Établit la connexion à MongoDB et retourne le client
    Retourne: client MongoDB ou None en cas d'erreur
    """
    # Affiche un titre de section pour la connexion
    afficher_separateur("CONNEXION À MONGODB")
    
    # Crée une connexion au serveur MongoDB local avec authentification
    # Format: mongodb://utilisateur:motdepasse@hôte:port/?authSource=baseDAuth
    client = MongoClient(
        'mongodb://admin:password@localhost:27017/?authSource=admin'
    )
    
    # Tente de se connecter et de vérifier que MongoDB répond
    try:
        # Récupère les informations du serveur (force la connexion)
        client.server_info()
        # Affiche un message de succès si la connexion fonctionne
        print("✓ Connecté à MongoDB avec succès!\n")
        # Retourne le client pour l'utiliser dans les autres fonctions
        return client
    except Exception as e:
        # En cas d'erreur, affiche le message d'erreur
        print(f"Erreur de connexion: {e}")
        # Retourne None pour indiquer l'échec de la connexion
        return None

def initialiser_collection(db):
    """
    Initialise et nettoie la collection utilisateurs
    Paramètres: db - la base de données MongoDB
    Retourne: la collection utilisateurs
    """
    # Sélectionne (ou crée si elle n'existe pas) la collection 'utilisateurs'
    collection = db['utilisateurs']
    # Supprime complètement la collection si elle existe (pour repartir de zéro)
    collection.drop()
    # Affiche un message confirmant le nettoyage
    print("Collection nettoyée pour commencer\n")
    # Retourne la collection pour l'utiliser dans les autres fonctions
    return collection

def fonction_create(collection):
    """
    Démontre les opérations CREATE (insertion de documents)
    Paramètres: collection - la collection MongoDB
    """
    # Affiche le titre de la section CREATE (création de documents)
    afficher_separateur("CREATE - Insertion de documents")
    
    # ===== Insertion d'un seul document =====
    # Affiche un sous-titre pour l'insertion d'un seul document
    print("1. Insertion d'un seul utilisateur:")
    # Crée un dictionnaire Python représentant un document utilisateur
    utilisateur1 = {
        "nom": "Dupont",              # Champ nom
        "prenom": "Jean",             # Champ prénom
        "age": 30,                    # Champ âge (nombre entier)
        "email": "jean.dupont@example.com",  # Champ email
        "ville": "Paris",             # Champ ville
        "profession": "Développeur"   # Champ profession
    }
    # Insère le document dans la collection et récupère le résultat
    resultat = collection.insert_one(utilisateur1)
    # Affiche l'ID généré automatiquement par MongoDB pour ce document
    print(f"   ✓ Document inséré avec l'ID: {resultat.inserted_id}\n")
    
    # ===== Insertion de plusieurs documents =====
    # Affiche un sous-titre pour l'insertion multiple
    print("2. Insertion de plusieurs utilisateurs:")
    # Crée une liste de dictionnaires (plusieurs documents)
    utilisateurs = [
        {
            "nom": "Martin",
            "prenom": "Marie",
            "age": 25,
            "email": "marie.martin@example.com",
            "ville": "Lyon",
            "profession": "Designer"
        },
        {
            "nom": "Dubois",
            "prenom": "Pierre",
            "age": 35,
            "email": "pierre.dubois@example.com",
            "ville": "Marseille",
            "profession": "Manager"
        },
        {
            "nom": "Laurent",
            "prenom": "Sophie",
            "age": 28,
            "email": "sophie.laurent@example.com",
            "ville": "Paris",
            "profession": "Analyste"
        },
        {
            "nom": "Moreau",
            "prenom": "Luc",
            "age": 42,
            "email": "luc.moreau@example.com",
            "ville": "Toulouse",
            "profession": "Architecte"
        }
    ]
    # Insère tous les documents en une seule opération
    resultat = collection.insert_many(utilisateurs)
    # Affiche le nombre de documents insérés en comptant les IDs générés
    print(f"   ✓ {len(resultat.inserted_ids)} documents insérés\n")
    
    # Affiche un message avant d'afficher tous les documents
    print("État actuel de la collection:")
    # Appelle la fonction pour afficher tous les documents de la collection
    afficher_tous_documents(collection)

def fonction_read(collection):
    """
    Démontre les opérations READ (lecture de documents)
    Paramètres: collection - la collection MongoDB
    """
    # Affiche le titre de la section READ (lecture de documents)
    afficher_separateur("READ - Lecture de documents")
    
    # ===== Recherche d'un seul document =====
    # Affiche un sous-titre pour la recherche d'un seul document
    print("1. Recherche d'un utilisateur spécifique (nom='Dupont'):")
    # Recherche le premier document où nom='Dupont' (retourne None si non trouvé)
    utilisateur = collection.find_one({"nom": "Dupont"})
    # Vérifie si un utilisateur a été trouvé
    if utilisateur:
        # Affiche les informations de l'utilisateur trouvé
        print(f"   ✓ Trouvé: {utilisateur['prenom']} {utilisateur['nom']}, {utilisateur['age']} ans\n")
    
    # ===== Recherche avec condition =====
    # Affiche un sous-titre pour la recherche avec condition
    print("2. Recherche des utilisateurs de moins de 30 ans:")
    # Recherche tous les documents où age < 30 (opérateur $lt = less than)
    jeunes = collection.find({"age": {"$lt": 30}})
    # Parcourt tous les résultats de la recherche
    for user in jeunes:
        # Affiche les informations de chaque utilisateur trouvé
        print(f"   - {user['prenom']} {user['nom']}: {user['age']} ans")
    # Affiche une ligne vide après les résultats
    print()
    
    # ===== Recherche par ville =====
    # Affiche un sous-titre pour la recherche par ville
    print("3. Recherche des utilisateurs à Paris:")
    # Recherche tous les documents où ville='Paris' (égalité exacte)
    parisiens = collection.find({"ville": "Paris"})
    # Parcourt tous les résultats
    for user in parisiens:
        # Affiche le nom et la profession de chaque parisien
        print(f"   - {user['prenom']} {user['nom']}: {user['profession']}")
    # Affiche une ligne vide
    print()
    
    # ===== Recherche avec projection =====
    # Affiche un sous-titre pour la recherche avec projection
    print("4. Liste des noms et emails uniquement:")
    # Recherche tous les documents mais retourne uniquement certains champs
    # 1 = inclure le champ, 0 = exclure le champ
    users_proj = collection.find({}, {"nom": 1, "prenom": 1, "email": 1, "_id": 0})
    # Parcourt les résultats (qui ne contiennent que nom, prenom, email)
    for user in users_proj:
        # Affiche uniquement les champs demandés
        print(f"   - {user['prenom']} {user['nom']}: {user['email']}")
    # Affiche une ligne vide
    print()
    
    # ===== Tri et limitation =====
    # Affiche un sous-titre pour le tri et la limitation
    print("5. Les 3 utilisateurs les plus âgés:")
    # Recherche tous les documents, les trie par âge décroissant (-1) et limite à 3
    ages = collection.find().sort("age", -1).limit(3)
    # Parcourt les 3 résultats
    for user in ages:
        # Affiche le nom et l'âge
        print(f"   - {user['prenom']} {user['nom']}: {user['age']} ans")
    # Affiche une ligne vide
    print()
    
    # ===== Comptage et statistiques =====
    # Affiche un sous-titre pour les statistiques
    print("6. Statistiques:")
    # Compte le nombre total de documents dans la collection
    total = collection.count_documents({})
    # Compte le nombre de documents où age < 30
    jeunes_count = collection.count_documents({"age": {"$lt": 30}})
    # Affiche le total
    print(f"   - Total d'utilisateurs: {total}")
    # Affiche le nombre de jeunes
    print(f"   - Utilisateurs de moins de 30 ans: {jeunes_count}\n")

def fonction_update(collection):
    """
    Démontre les opérations UPDATE (mise à jour de documents)
    Paramètres: collection - la collection MongoDB
    """
    # Affiche le titre de la section UPDATE (mise à jour)
    afficher_separateur("UPDATE - Mise à jour de documents")
    
    # ===== Mise à jour d'un seul document =====
    # Affiche un sous-titre pour la mise à jour d'un seul document
    print("1. Mise à jour de l'âge de Jean Dupont (30 → 31 ans):")
    # Met à jour le premier document correspondant aux critères
    resultat = collection.update_one(
        {"nom": "Dupont", "prenom": "Jean"},  # Critère de recherche
        {"$set": {"age": 31}}                 # Opération: définir age à 31
    )
    # Affiche le nombre de documents modifiés (0 ou 1)
    print(f"   ✓ {resultat.modified_count} document(s) modifié(s)\n")
    
    # ===== Vérification de la mise à jour =====
    # Affiche un message de vérification
    print("   Vérification: ", end="")
    # Recherche à nouveau le document pour vérifier la modification
    utilisateur = collection.find_one({"nom": "Dupont"})
    # Affiche le nouvel âge
    print(f"{utilisateur['prenom']} {utilisateur['nom']} a maintenant {utilisateur['age']} ans\n")
    
    # ===== Ajout de champs à tous les documents =====
    # Affiche un sous-titre pour la mise à jour de tous les documents
    print("2. Ajout du champ 'statut' = 'actif' à tous les utilisateurs:")
    # Met à jour tous les documents (filtre vide = tous)
    resultat = collection.update_many(
        {},  # Pas de filtre = sélectionne tous les documents
        {"$set": {"statut": "actif", "date_maj": datetime.now()}}  # Ajoute 2 champs
    )
    # Affiche le nombre de documents modifiés
    print(f"   ✓ {resultat.modified_count} document(s) modifié(s)\n")
    
    # ===== Incrémentation conditionnelle =====
    # Affiche un sous-titre pour la mise à jour conditionnelle multiple
    print("3. Augmentation de l'âge de +1 pour tous les utilisateurs de moins de 30 ans:")
    # Met à jour plusieurs documents correspondant aux critères
    resultat = collection.update_many(
        {"age": {"$lt": 30}},  # Seulement si age < 30
        {"$inc": {"age": 1}}   # Opération $inc: incrémente age de 1
    )
    # Affiche le nombre de documents modifiés
    print(f"   ✓ {resultat.modified_count} document(s) modifié(s)\n")
    
    # ===== Ajout conditionnel de champ =====
    # Affiche un sous-titre pour l'ajout conditionnel de champ
    print("4. Ajout de la catégorie 'senior' pour les utilisateurs de plus de 35 ans:")
    # Met à jour plusieurs documents avec condition
    resultat = collection.update_many(
        {"age": {"$gte": 35}},              # $gte = greater than or equal (>=)
        {"$set": {"categorie": "senior"}}   # Ajoute le champ categorie
    )
    # Affiche le nombre de documents modifiés
    print(f"   ✓ {resultat.modified_count} document(s) modifié(s)\n")
    
    # ===== Affichage de l'état après mises à jour =====
    # Affiche un message avant d'afficher l'état mis à jour
    print("État de la collection après les mises à jour:")
    # Appelle la fonction pour afficher tous les documents
    afficher_tous_documents(collection)

def fonction_delete(collection):
    """
    Démontre les opérations DELETE (suppression de documents)
    Paramètres: collection - la collection MongoDB
    """
    # Affiche le titre de la section DELETE (suppression)
    afficher_separateur("DELETE - Suppression de documents")
    
    # ===== Suppression d'un seul document =====
    # Affiche un sous-titre pour la suppression d'un seul document
    print("1. Suppression de Pierre Dubois:")
    # Supprime le premier document correspondant aux critères
    resultat = collection.delete_one({"nom": "Dubois", "prenom": "Pierre"})
    # Affiche le nombre de documents supprimés (0 ou 1)
    print(f"   ✓ {resultat.deleted_count} document(s) supprimé(s)\n")
    
    # ===== Suppression multiple avec condition =====
    # Affiche un sous-titre pour la suppression multiple
    print("2. Suppression de tous les utilisateurs de plus de 40 ans:")
    # Supprime tous les documents correspondant aux critères
    resultat = collection.delete_many({"age": {"$gt": 40}})  # $gt = greater than (>)
    # Affiche le nombre de documents supprimés
    print(f"   ✓ {resultat.deleted_count} document(s) supprimé(s)\n")
    
    # ===== Affichage de l'état final =====
    # Affiche un message avant d'afficher l'état final
    print("État final de la collection:")
    # Appelle la fonction pour afficher tous les documents restants
    afficher_tous_documents(collection)

def fonction_operations_avancees(collection):
    """
    Démontre les opérations avancées (opérateurs logiques)
    Paramètres: collection - la collection MongoDB
    """
    # Affiche le titre de la section des opérations avancées
    afficher_separateur("OPÉRATIONS AVANCÉES")
    
    # ===== Opérateur $and (ET logique) =====
    # Affiche un sous-titre pour l'opérateur $and
    print("1. Recherche avec opérateur $and (Paris ET moins de 30 ans):")
    # Recherche avec plusieurs conditions (toutes doivent être vraies)
    resultats = collection.find({
        "$and": [                    # Opérateur logique ET
            {"ville": "Paris"},      # Condition 1: ville = Paris
            {"age": {"$lt": 30}}     # Condition 2: age < 30
        ]
    })
    # Initialise un compteur pour savoir s'il y a des résultats
    count = 0
    # Parcourt les résultats
    for user in resultats:
        # Affiche les informations de chaque utilisateur trouvé
        print(f"   - {user['prenom']} {user['nom']}: {user['age']} ans, {user['ville']}")
        # Incrémente le compteur
        count += 1
    # Si aucun résultat n'a été trouvé
    if count == 0:
        # Affiche un message
        print("   Aucun résultat")
    # Affiche une ligne vide
    print()
    
    # ===== Opérateur $or (OU logique) =====
    # Affiche un sous-titre pour l'opérateur $or
    print("2. Recherche avec opérateur $or (Designer OU Analyste):")
    # Recherche avec plusieurs conditions (au moins une doit être vraie)
    resultats = collection.find({
        "$or": [                           # Opérateur logique OU
            {"profession": "Designer"},    # Condition 1: profession = Designer
            {"profession": "Analyste"}     # Condition 2: profession = Analyste
        ]
    })
    # Parcourt les résultats
    for user in resultats:
        # Affiche le nom et la profession
        print(f"   - {user['prenom']} {user['nom']}: {user['profession']}")
    # Affiche une ligne vide
    print()
    
    # ===== Opérateur $in (dans une liste) =====
    # Affiche un sous-titre pour l'opérateur $in
    print("3. Recherche avec $in (Paris, Lyon ou Marseille):")
    # Recherche les documents où le champ correspond à une valeur dans la liste
    resultats = collection.find({
        "ville": {"$in": ["Paris", "Lyon", "Marseille"]}  # $in = dans la liste
    })
    # Parcourt les résultats
    for user in resultats:
        # Affiche le nom et la ville
        print(f"   - {user['prenom']} {user['nom']}: {user['ville']}")
    # Affiche une ligne vide
    print()

def fermer_connexion(client):
    """
    Ferme proprement la connexion à MongoDB
    Paramètres: client - le client MongoDB à fermer
    """
    # Affiche le titre de la section nettoyage
    afficher_separateur("NETTOYAGE")
    
    # Affiche un message avant de fermer
    print("Fermeture de la connexion...")
    # Ferme proprement la connexion au serveur MongoDB
    client.close()
    # Affiche un message de confirmation
    print("   ✓ Connexion fermée\n")

def main():
    """
    Fonction principale qui orchestre toutes les opérations CRUD
    """
    # ===== Connexion à MongoDB =====
    # Établit la connexion à MongoDB
    client = connecter_mongodb()
    # Vérifie si la connexion a réussi
    if client is None:
        # Si la connexion a échoué, arrête le programme
        return
    
    # ===== Initialisation de la base de données =====
    # Sélectionne (ou crée si elle n'existe pas) la base de données 'demo_crud'
    db = client['demo_crud']
    # Initialise et nettoie la collection
    collection = initialiser_collection(db)
    
    # ===== Exécution des opérations CRUD =====
    # Appelle la fonction CREATE (insertion de documents)
    fonction_create(collection)
    # Appelle la fonction READ (lecture de documents)
    fonction_read(collection)
    # Appelle la fonction UPDATE (mise à jour de documents)
    fonction_update(collection)
    # Appelle la fonction DELETE (suppression de documents)
    fonction_delete(collection)
    # Appelle la fonction pour les opérations avancées
    fonction_operations_avancees(collection)
    
    # ===== Fermeture de la connexion =====
    # Ferme proprement la connexion à MongoDB
    fermer_connexion(client)
    
    # Affiche le titre final
    afficher_separateur("OPÉRATIONS TERMINÉES")

# Point d'entrée du programme Python
if __name__ == "__main__":
    # Exécute la fonction main() si le script est lancé directement
    main()