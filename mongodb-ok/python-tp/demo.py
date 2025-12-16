# solutions_tp_mongodb.py
from pymongo import MongoClient
import json

def connexion():
    """Établit la connexion à MongoDB"""
    client = MongoClient('mongodb://admin:password@localhost:27017/?authSource=admin')
    db = client['tp_mongodb']
    collection = db['students']
    return client, collection

def afficher_separateur(titre):
    """Affiche un séparateur visuel"""
    print("\n" + "="*70)
    print(f"  {titre}")
    print("="*70)

# ============================================================
# PARTIE 1 - REQUÊTES SIMPLES (4 points)
# ============================================================

def question_1():
    """Q1: Affichez le premier document de la collection"""
    afficher_separateur("Question 1 - Premier document")
    
    # Connexion à la base
    client, collection = connexion()
    
    # Récupère le premier document
    premier = collection.find_one()
    
    # Affichage
    print(f"ID: {premier['_id']}")
    print(f"Nom: {premier['name']}")
    print(f"Scores:")
    for score in premier['scores']:
        print(f"  - {score['type']}: {score['score']:.2f}")
    
    # Fermeture
    client.close()

def question_2():
    """Q2: Comptez le nombre total d'étudiants"""
    afficher_separateur("Question 2 - Nombre total d'étudiants")
    
    client, collection = connexion()
    
    # Compte tous les documents
    total = collection.count_documents({})
    
    print(f"Nombre total d'étudiants: {total}")
    
    client.close()

def question_3():
    """Q3: Trouvez et affichez l'étudiant nommé 'Aurelia Menendez'"""
    afficher_separateur("Question 3 - Recherche par nom")
    
    client, collection = connexion()
    
    # Recherche par nom exact
    etudiant = collection.find_one({"name": "Aurelia Menendez"})
    
    if etudiant:
        print(f"ID: {etudiant['_id']}")
        print(f"Nom: {etudiant['name']}")
        print(f"Scores:")
        for score in etudiant['scores']:
            print(f"  - {score['type']}: {score['score']:.2f}")
    else:
        print("Étudiant non trouvé")
    
    client.close()

def question_4():
    """Q4: Trouvez l'étudiant avec _id = 50"""
    afficher_separateur("Question 4 - Recherche par ID")
    
    client, collection = connexion()
    
    # Recherche par _id
    etudiant = collection.find_one({"_id": 50})
    
    if etudiant:
        print(f"ID: {etudiant['_id']}")
        print(f"Nom: {etudiant['name']}")
        print(f"Scores:")
        for score in etudiant['scores']:
            print(f"  - {score['type']}: {score['score']:.2f}")
    
    client.close()

def question_5():
    """Q5: Trouvez tous les étudiants qui n'ont pas de nom"""
    afficher_separateur("Question 5 - Étudiants sans nom")
    
    client, collection = connexion()
    
    # Recherche avec name vide
    etudiants_sans_nom = collection.find({"name": ""})
    
    print("Étudiants sans nom:")
    count = 0
    for etudiant in etudiants_sans_nom:
        print(f"  - ID: {etudiant['_id']}")
        count += 1
    
    print(f"\nTotal: {count} étudiant(s) sans nom")
    
    client.close()

def question_6():
    """Q6: Affichez uniquement les noms des 10 premiers étudiants"""
    afficher_separateur("Question 6 - Noms des 10 premiers")
    
    client, collection = connexion()
    
    # Projection pour ne récupérer que le nom, sans l'_id
    etudiants = collection.find({}, {"name": 1, "_id": 0}).limit(10)
    
    print("Les 10 premiers noms:")
    for i, etudiant in enumerate(etudiants, 1):
        print(f"  {i}. {etudiant['name']}")
    
    client.close()

def question_7():
    """Q7: Affichez les 5 premiers étudiants triés par ordre alphabétique"""
    afficher_separateur("Question 7 - Tri alphabétique")
    
    client, collection = connexion()
    
    # Tri par nom (ordre croissant) et limite à 5
    # On exclut les noms vides du tri
    etudiants = collection.find({"name": {"$ne": ""}}).sort("name", 1).limit(5)
    
    print("Les 5 premiers noms (ordre alphabétique):")
    for i, etudiant in enumerate(etudiants, 1):
        print(f"  {i}. {etudiant['name']} (ID: {etudiant['_id']})")
    
    client.close()

# ============================================================
# PARTIE 2 - MANIPULATION DES TABLEAUX (3 points)
# ============================================================

def question_8():
    """Q8: Extrayez la note d'examen de l'étudiant _id=0"""
    afficher_separateur("Question 8 - Note d'examen d'un étudiant")
    
    client, collection = connexion()
    
    # Récupère l'étudiant
    etudiant = collection.find_one({"_id": 0})
    
    # Parcourt le tableau scores pour trouver l'exam
    if etudiant:
        for score in etudiant['scores']:
            if score['type'] == 'exam':
                print(f"Étudiant: {etudiant['name']}")
                print(f"Note d'examen: {score['score']:.2f}")
                break
    
    client.close()

def question_9():
    """Q9: Calculez la moyenne des 3 notes de l'étudiant _id=1"""
    afficher_separateur("Question 9 - Moyenne d'un étudiant")
    
    client, collection = connexion()
    
    # Récupère l'étudiant
    etudiant = collection.find_one({"_id": 1})
    
    if etudiant:
        # Calcule la somme de toutes les notes
        total = sum(score['score'] for score in etudiant['scores'])
        moyenne = total / len(etudiant['scores'])
        
        print(f"Étudiant: {etudiant['name']}")
        print(f"Notes:")
        for score in etudiant['scores']:
            print(f"  - {score['type']}: {score['score']:.2f}")
        print(f"\nMoyenne: {moyenne:.2f}")
    
    client.close()

def question_10():
    """Q10: Utilisez $unwind pour déplier le tableau scores"""
    afficher_separateur("Question 10 - Utilisation de $unwind")
    
    client, collection = connexion()
    
    # Pipeline d'agrégation avec $unwind
    pipeline = [
        {"$unwind": "$scores"},  # Déplie le tableau scores
        {"$limit": 5}            # Limite à 5 résultats
    ]
    
    resultats = collection.aggregate(pipeline)
    
    print("5 premiers résultats après $unwind:")
    for i, doc in enumerate(resultats, 1):
        print(f"\n{i}. ID: {doc['_id']} - {doc['name']}")
        print(f"   Type: {doc['scores']['type']}")
        print(f"   Score: {doc['scores']['score']:.2f}")
    
    client.close()

# ============================================================
# PARTIE 3 - AGRÉGATIONS (5 points)
# ============================================================

def question_11():
    """Q11: Calculez la moyenne générale de chaque étudiant (top 10)"""
    afficher_separateur("Question 11 - Top 10 des moyennes")
    
    client, collection = connexion()
    
    # Pipeline d'agrégation
    pipeline = [
        {"$unwind": "$scores"},                    # Déplie les scores
        {"$group": {                               # Groupe par étudiant
            "_id": "$_id",
            "name": {"$first": "$name"},
            "moyenne": {"$avg": "$scores.score"}   # Calcule la moyenne
        }},
        {"$sort": {"moyenne": -1}},                # Tri décroissant
        {"$limit": 10}                             # Top 10
    ]
    
    resultats = collection.aggregate(pipeline)
    
    print("Top 10 des meilleures moyennes:")
    for i, etudiant in enumerate(resultats, 1):
        print(f"  {i}. {etudiant['name']} (ID: {etudiant['_id']}): {etudiant['moyenne']:.2f}")
    
    client.close()

def question_12():
    """Q12: Moyenne par type d'évaluation"""
    afficher_separateur("Question 12 - Moyenne par type")
    
    client, collection = connexion()
    
    # Pipeline d'agrégation
    pipeline = [
        {"$unwind": "$scores"},                    # Déplie les scores
        {"$group": {                               # Groupe par type
            "_id": "$scores.type",
            "moyenne": {"$avg": "$scores.score"}   # Calcule la moyenne
        }},
        {"$sort": {"_id": 1}}                      # Tri alphabétique
    ]
    
    resultats = collection.aggregate(pipeline)
    
    print("Moyenne par type d'évaluation:")
    for resultat in resultats:
        print(f"  {resultat['_id']}: {resultat['moyenne']:.2f}")
    
    client.close()

def question_13():
    """Q13: Meilleure note par type d'évaluation"""
    afficher_separateur("Question 13 - Meilleure note par type")
    
    client, collection = connexion()
    
    # Pipeline d'agrégation
    pipeline = [
        {"$unwind": "$scores"},                    # Déplie les scores
        {"$sort": {"scores.score": -1}},           # Tri décroissant par score
        {"$group": {                               # Groupe par type
            "_id": "$scores.type",
            "meilleur_etudiant": {"$first": "$name"},
            "meilleur_score": {"$first": "$scores.score"}
        }},
        {"$sort": {"_id": 1}}                      # Tri alphabétique
    ]
    
    resultats = collection.aggregate(pipeline)
    
    print("Meilleure note par type:")
    for resultat in resultats:
        print(f"  {resultat['_id']}: {resultat['meilleur_score']:.2f} par {resultat['meilleur_etudiant']}")
    
    client.close()

def question_14():
    """Q14: Min, max, moyenne pour chaque étudiant"""
    afficher_separateur("Question 14 - Statistiques par étudiant")
    
    client, collection = connexion()
    
    # Pipeline d'agrégation
    pipeline = [
        {"$unwind": "$scores"},
        {"$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "minimum": {"$min": "$scores.score"},
            "maximum": {"$max": "$scores.score"},
            "moyenne": {"$avg": "$scores.score"}
        }},
        {"$sort": {"moyenne": -1}},
        {"$limit": 10}  # On affiche les 10 premiers
    ]
    
    resultats = collection.aggregate(pipeline)
    
    print("Statistiques des 10 meilleurs étudiants:")
    for i, etudiant in enumerate(resultats, 1):
        print(f"\n{i}. {etudiant['name']} (ID: {etudiant['_id']})")
        print(f"   Min: {etudiant['minimum']:.2f}")
        print(f"   Max: {etudiant['maximum']:.2f}")
        print(f"   Moyenne: {etudiant['moyenne']:.2f}")
    
    client.close()

def question_15():
    """Q15: Nombre d'étudiants avec moyenne > 70"""
    afficher_separateur("Question 15 - Étudiants avec moyenne > 70")
    
    client, collection = connexion()
    
    # Pipeline d'agrégation
    pipeline = [
        {"$unwind": "$scores"},
        {"$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "moyenne": {"$avg": "$scores.score"}
        }},
        {"$match": {"moyenne": {"$gt": 70}}},  # Filtre moyenne > 70
        {"$count": "nombre"}                    # Compte les résultats
    ]
    
    resultats = list(collection.aggregate(pipeline))
    
    if resultats:
        print(f"Nombre d'étudiants avec moyenne > 70: {resultats[0]['nombre']}")
    else:
        print("Aucun étudiant avec moyenne > 70")
    
    client.close()

# ============================================================
# PARTIE 4 - MISES À JOUR (4 points)
# ============================================================

def question_16():
    """Q16: Ajoutez un champ moyenne à tous les documents"""
    afficher_separateur("Question 16 - Ajout champ moyenne")
    
    client, collection = connexion()
    
    # Récupère tous les étudiants
    etudiants = collection.find()
    
    count = 0
    for etudiant in etudiants:
        # Calcule la moyenne
        total = sum(score['score'] for score in etudiant['scores'])
        moyenne = total / len(etudiant['scores'])
        
        # Met à jour le document
        collection.update_one(
            {"_id": etudiant['_id']},
            {"$set": {"moyenne": moyenne}}
        )
        count += 1
    
    print(f"✓ Champ 'moyenne' ajouté à {count} étudiants")
    
    # Vérification : affiche quelques exemples
    print("\nExemples:")
    exemples = collection.find().limit(3)
    for etudiant in exemples:
        print(f"  {etudiant['name']}: moyenne = {etudiant.get('moyenne', 'N/A'):.2f}")
    
    client.close()

def question_17():
    """Q17: Ajoutez un champ niveau selon la moyenne"""
    afficher_separateur("Question 17 - Ajout champ niveau")
    
    client, collection = connexion()
    
    # S'assure que la moyenne existe (exécute Q16 si nécessaire)
    if collection.find_one({"moyenne": {"$exists": False}}):
        print("Calcul des moyennes d'abord...")
        question_16()
        client, collection = connexion()
    
    # Récupère tous les étudiants
    etudiants = collection.find()
    
    count = 0
    for etudiant in etudiants:
        moyenne = etudiant.get('moyenne', 0)
        
        # Détermine le niveau
        if moyenne >= 80:
            niveau = "Excellent"
        elif moyenne >= 60:
            niveau = "Bien"
        elif moyenne >= 40:
            niveau = "Passable"
        else:
            niveau = "Insuffisant"
        
        # Met à jour le document
        collection.update_one(
            {"_id": etudiant['_id']},
            {"$set": {"niveau": niveau}}
        )
        count += 1
    
    print(f"✓ Champ 'niveau' ajouté à {count} étudiants")
    
    # Statistiques par niveau
    pipeline = [
        {"$group": {
            "_id": "$niveau",
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    
    stats = collection.aggregate(pipeline)
    print("\nRépartition par niveau:")
    for stat in stats:
        print(f"  {stat['_id']}: {stat['count']} étudiant(s)")
    
    client.close()

def question_18():
    """Q18: Supprimez la note de homework la plus faible"""
    afficher_separateur("Question 18 - Suppression homework le plus faible")
    
    client, collection = connexion()
    
    # Récupère tous les étudiants
    etudiants = collection.find()
    
    count = 0
    for etudiant in etudiants:
        # Trouve tous les homeworks
        homeworks = [score for score in etudiant['scores'] if score['type'] == 'homework']
        
        if homeworks:
            # Trouve le plus faible
            min_homework = min(homeworks, key=lambda x: x['score'])
            
            # Supprime ce score du tableau
            collection.update_one(
                {"_id": etudiant['_id']},
                {"$pull": {"scores": {"type": "homework", "score": min_homework['score']}}}
            )
            count += 1
    
    print(f"✓ Homework le plus faible supprimé pour {count} étudiants")
    
    # Vérification
    exemple = collection.find_one({"_id": 0})
    print(f"\nExemple - Étudiant ID 0:")
    print(f"Nombre de scores restants: {len(exemple['scores'])}")
    
    client.close()

def question_19():
    """Q19: Mettez à jour le nom de l'étudiant _id=113"""
    afficher_separateur("Question 19 - Mise à jour nom étudiant 113")
    
    client, collection = connexion()
    
    # Avant modification
    avant = collection.find_one({"_id": 113})
    print(f"Avant: ID 113, nom = '{avant['name']}'")
    
    # Mise à jour
    resultat = collection.update_one(
        {"_id": 113},
        {"$set": {"name": "Nom Inconnu"}}
    )
    
    # Après modification
    apres = collection.find_one({"_id": 113})
    print(f"Après: ID 113, nom = '{apres['name']}'")
    print(f"\n✓ {resultat.modified_count} document modifié")
    
    client.close()

# ============================================================
# PARTIE 5 - ANALYSES AVANCÉES (4 points)
# ============================================================

def question_20():
    """Q20: Top 5 des différences exam vs homework"""
    afficher_separateur("Question 20 - Plus grande différence exam/homework")
    
    client, collection = connexion()
    
    # Pipeline d'agrégation
    pipeline = [
        {"$unwind": "$scores"},
        {"$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "exam": {
                "$max": {
                    "$cond": [{"$eq": ["$scores.type", "exam"]}, "$scores.score", 0]
                }
            },
            "homework": {
                "$max": {
                    "$cond": [{"$eq": ["$scores.type", "homework"]}, "$scores.score", 0]
                }
            }
        }},
        {"$project": {
            "name": 1,
            "exam": 1,
            "homework": 1,
            "difference": {"$subtract": ["$exam", "$homework"]}
        }},
        {"$sort": {"difference": -1}},
        {"$limit": 5}
    ]
    
    resultats = collection.aggregate(pipeline)
    
    print("Top 5 - Plus grande différence (exam - homework):")
    for i, etudiant in enumerate(resultats, 1):
        print(f"\n{i}. {etudiant['name']} (ID: {etudiant['_id']})")
        print(f"   Exam: {etudiant['exam']:.2f}")
        print(f"   Homework: {etudiant['homework']:.2f}")
        print(f"   Différence: {etudiant['difference']:.2f}")
    
    client.close()

def question_21():
    """Q21: Étudiants ayant échoué (< 50) à au moins une évaluation"""
    afficher_separateur("Question 21 - Étudiants avec au moins un échec")
    
    client, collection = connexion()
    
    # Pipeline d'agrégation
    pipeline = [
        {"$unwind": "$scores"},
        {"$match": {"scores.score": {"$lt": 50}}},  # Filtre notes < 50
        {"$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "echecs": {
                "$push": {
                    "type": "$scores.type",
                    "score": "$scores.score"
                }
            }
        }},
        {"$sort": {"name": 1}},
        {"$limit": 10}  # On limite l'affichage
    ]
    
    resultats = collection.aggregate(pipeline)
    
    print("Étudiants ayant échoué (< 50) à au moins une évaluation (10 premiers):")
    for i, etudiant in enumerate(resultats, 1):
        print(f"\n{i}. {etudiant['name']} (ID: {etudiant['_id']})")
        print(f"   Échecs:")
        for echec in etudiant['echecs']:
            print(f"     - {echec['type']}: {echec['score']:.2f}")
    
    # Compte total
    total_pipeline = [
        {"$unwind": "$scores"},
        {"$match": {"scores.score": {"$lt": 50}}},
        {"$group": {"_id": "$_id"}},
        {"$count": "total"}
    ]
    
    total = list(collection.aggregate(total_pipeline))
    if total:
        print(f"\nTotal: {total[0]['total']} étudiants ont échoué à au moins une évaluation")
    
    client.close()

def question_22():
    """Q22: Écart-type des notes par type d'évaluation"""
    afficher_separateur("Question 22 - Écart-type par type")
    
    client, collection = connexion()
    
    # Pipeline d'agrégation avec stdDevPop (écart-type de population)
    pipeline = [
        {"$unwind": "$scores"},
        {"$group": {
            "_id": "$scores.type",
            "moyenne": {"$avg": "$scores.score"},
            "ecart_type": {"$stdDevPop": "$scores.score"},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    
    resultats = collection.aggregate(pipeline)
    
    print("Statistiques par type d'évaluation:")
    for resultat in resultats:
        print(f"\n{resultat['_id'].upper()}:")
        print(f"  Moyenne: {resultat['moyenne']:.2f}")
        print(f"  Écart-type: {resultat['ecart_type']:.2f}")
        print(f"  Nombre de notes: {resultat['count']}")
    
    client.close()

def question_23():
    """Q23: Étudiants avec toutes les notes > 60"""
    afficher_separateur("Question 23 - Toutes notes > 60")
    
    client, collection = connexion()
    
    # Pipeline d'agrégation
    pipeline = [
        {"$unwind": "$scores"},
        {"$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "note_min": {"$min": "$scores.score"}  # Plus petite note
        }},
        {"$match": {"note_min": {"$gt": 60}}},     # Filtre min > 60
        {"$sort": {"note_min": -1}}
    ]
    
    resultats = collection.aggregate(pipeline)
    
    print("Étudiants dont toutes les notes sont > 60:")
    count = 0
    for etudiant in resultats:
        count += 1
        print(f"  {count}. {etudiant['name']} (ID: {etudiant['_id']}) - Note min: {etudiant['note_min']:.2f}")
    
    print(f"\nTotal: {count} étudiant(s)")
    
    client.close()

# ============================================================
# BONUS - RAPPORT DÉTAILLÉ (+2 points)
# ============================================================

def question_24_rapport_etudiant(student_id):
    """Q24 BONUS: Rapport complet d'un étudiant"""
    afficher_separateur(f"RAPPORT ÉTUDIANT - ID {student_id}")
    
    client, collection = connexion()
    
    # Récupère l'étudiant
    etudiant = collection.find_one({"_id": student_id})
    
    if not etudiant:
        print(f"Étudiant avec ID {student_id} non trouvé")
        client.close()
        return
    
    # 1. Informations de base
    print(f"NOM: {etudiant['name']}")
    print(f"ID: {etudiant['_id']}")
    
    # 2. Toutes ses notes
    print(f"\n--- NOTES ---")
    total = 0
    for score in etudiant['scores']:
        print(f"{score['type'].capitalize()}: {score['score']:.2f}")
        total += score['score']
    
    # 3. Moyenne générale
    moyenne = total / len(etudiant['scores'])
    print(f"\nMoyenne générale: {moyenne:.2f}")
    
    # 4. Classement
    pipeline = [
        {"$unwind": "$scores"},
        {"$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "moyenne": {"$avg": "$scores.score"}
        }},
        {"$sort": {"moyenne": -1}}
    ]
    
    classement = list(collection.aggregate(pipeline))
    rang = next((i+1 for i, e in enumerate(classement) if e['_id'] == student_id), None)
    
    print(f"\n--- CLASSEMENT ---")
    print(f"Rang: {rang}/{len(classement)}")
    pourcentile = (1 - rang/len(classement)) * 100
    print(f"Meilleur que {pourcentile:.1f}% des étudiants")
    
    # 5. Comparaison avec les moyennes de classe
    print(f"\n--- COMPARAISON AVEC LA CLASSE ---")
    
    moyennes_classe = {}
    for score in etudiant['scores']:
        type_eval = score['type']
        
        # Moyenne de la classe pour ce type
        pipeline_moy = [
            {"$unwind": "$scores"},
            {"$match": {"scores.type": type_eval}},
            {"$group": {"_id": None, "moyenne": {"$avg": "$scores.score"}}}
        ]
        
        result = list(collection.aggregate(pipeline_moy))
        moy_classe = result[0]['moyenne'] if result else 0
        moyennes_classe[type_eval] = moy_classe
        
        ecart = score['score'] - moy_classe
        symbole = "+" if ecart >= 0 else ""
        print(f"{type_eval.capitalize()}: {score['score']:.2f} (classe: {moy_classe:.2f}, écart: {symbole}{ecart:.2f})")
    
    # 6. Points forts et faibles
    print(f"\n--- ANALYSE ---")
    
    scores_etudiant = {s['type']: s['score'] for s in etudiant['scores']}
    ecarts = {type_e: scores_etudiant[type_e] - moyennes_classe[type_e] 
              for type_e in scores_etudiant}
    
    meilleur = max(ecarts, key=ecarts.get)
    pire = min(ecarts, key=ecarts.get)
    
    print(f"Point fort: {meilleur.capitalize()} ({symbole_ecart(ecarts[meilleur])}{ecarts[meilleur]:.2f} vs classe)")
    print(f"Point faible: {pire.capitalize()} ({symbole_ecart(ecarts[pire])}{ecarts[pire]:.2f} vs classe)")
    
    # 7. Commentaire global
    print(f"\n--- COMMENTAIRE ---")
    
    if moyenne >= 80:
        print("🌟 Excellent niveau ! Continue comme ça !")
    elif moyenne >= 60:
        print("👍 Bon travail, continue tes efforts !")
    elif moyenne >= 40:
        print("⚠️  Performance passable, il faut travailler davantage.")
    else:
        print("❌ Niveau insuffisant, un soutien est nécessaire.")
    
    if ecarts[pire] < -10:
        print(f"💡 Concentre-toi particulièrement sur le {pire}.")
    
    if rang <= len(classement) * 0.1:
        print("🏆 Tu fais partie du top 10% de la classe !")
    
    client.close()

def symbole_ecart(ecart):
    """Retourne + si positif, sinon rien"""
    return "+" if ecart >= 0 else ""

# ============================================================
# FONCTION PRINCIPALE
# ============================================================

def main():
    """Fonction principale pour exécuter toutes les questions"""
    
    print("\n" + "="*70)
    print("  SOLUTIONS TP MONGODB - ANALYSE DES NOTES D'ÉTUDIANTS")
    print("="*70)
    
    # Menu interactif
    while True:
        print("\n--- MENU ---")
        print("1-7: Partie 1 (Requêtes simples)")
        print("8-10: Partie 2 (Manipulation tableaux)")
        print("11-15: Partie 3 (Agrégations)")
        print("16-19: Partie 4 (Mises à jour)")
        print("20-23: Partie 5 (Analyses avancées)")
        print("24: BONUS - Rapport étudiant")
        print("ALL: Exécuter toutes les questions")
        print("0: Quitter")
        
        choix = input("\nChoix: ").strip().upper()
        
        if choix == "0":
            print("\nAu revoir !")
            break
        elif choix == "1":
            question_1()
        elif choix == "2":
            question_2()
        elif choix == "3":
            question_3()
        elif choix == "4":
            question_4()
        elif choix == "5":
            question_5()
        elif choix == "6":
            question_6()
        elif choix == "7":
            question_7()
        elif choix == "8":
            question_8()
        elif choix == "9":
            question_9()
        elif choix == "10":
            question_10()
        elif choix == "11":
            question_11()
        elif choix == "12":
            question_12()
        elif choix == "13":
            question_13()
        elif choix == "14":
            question_14()
        elif choix == "15":
            question_15()
        elif choix == "16":
            question_16()
        elif choix == "17":
            question_17()
        elif choix == "18":
            question_18()
        elif choix == "19":
            question_19()
        elif choix == "20":
            question_20()
        elif choix == "21":
            question_21()
        elif choix == "22":
            question_22()
        elif choix == "23":
            question_23()
        elif choix == "24":
            student_id = int(input("ID de l'étudiant (0-199): "))
            question_24_rapport_etudiant(student_id)
        elif choix == "ALL":
            # Exécute toutes les questions
            for i in range(1, 24):
                fonction_nom = f"question_{i}"
                if fonction_nom in globals():
                    globals()[fonction_nom]()
            
            # Question bonus
            print("\nExemple de rapport pour l'étudiant ID 50:")
            question_24_rapport_etudiant(50)
        else:
            print("Choix invalide !")
        
        input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()