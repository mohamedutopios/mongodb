from pymongo import MongoClient

from datetime import datetime
 
if __name__ == "__main__":
 
    print("=== CONNEXION MONGODB ===")
 
    # Connexion à MongoDB

    client = MongoClient(

        "mongodb://admin:password@localhost:27017/?authSource=admin"

    )
 
    # Sélection de la base

    db = client["demo_crud"]
 
    # Sélection de la collection

    collection = db["utilisateurs"]
 
    # Nettoyage pour repartir de zéro

    collection.drop()

    print("Collection nettoyée\n")
 
    # ======================

    # CREATE

    # ======================

    print("=== INSERTION ===")
 
    collection.insert_many([

        {

            "nom": "Dupont",

            "prenom": "Jean",

            "age": 30,

            "ville": "Paris",

            "profession": "Développeur",

            "date_creation": datetime.now()

        },

        {

            "nom": "Martin",

            "prenom": "Marie",

            "age": 25,

            "ville": "Lyon",

            "profession": "Designer",

            "date_creation": datetime.now()

        },

        {

            "nom": "Dubois",

            "prenom": "Pierre",

            "age": 40,

            "ville": "Marseille",

            "profession": "Manager",

            "date_creation": datetime.now()

        }

    ])
 
    print("Documents insérés\n")
 
    # ======================

    # READ

    # ======================

    print("=== LECTURE ===")
 
    for user in collection.find():

        print(user)
 
    print()
 
    print("Utilisateurs de moins de 30 ans:")

    for user in collection.find({"age": {"$lt": 30}}):

        print(user["prenom"], user["nom"], "-", user["age"], "ans")
 
    print()
 
    # ======================

    # UPDATE

    # ======================

    print("=== MISE À JOUR ===")
 
    result = collection.update_one(

        {"nom": "Dupont", "prenom": "Jean"},

        {"$set": {"age": 31}}

    )
 
    print("Documents modifiés:", result.modified_count)
 
    print("Après mise à jour:")

    print(collection.find_one({"nom": "Dupont"}))

    print()
 
    # ======================

    # DELETE

    # ======================

    print("=== SUPPRESSION ===")
 
    result = collection.delete_many({"age": {"$gt": 35}})

    print("Documents supprimés:", result.deleted_count)
 
    print("\nÉtat final:")

    for user in collection.find():

        print(user)
 
    # ======================

    # FERMETURE

    # ======================

    client.close()

    print("\nConnexion fermée")

 