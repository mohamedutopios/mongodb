# TP MongoDB avec Python - Analyse des Notes d'Étudiants

## 📋 Données
Base de données : `tp_mongodb`  
Collection : `students`  
200 étudiants avec leurs notes (exam, quiz, homework)

## 📝 Questions

### Partie 1 - Requêtes simples

1. Affichez le premier document de la collection
2. Comptez le nombre total d'étudiants
3. Trouvez et affichez l'étudiant nommé "Aurelia Menendez"
4. Trouvez l'étudiant avec `_id = 50`
5. Trouvez tous les étudiants qui n'ont pas de nom (name vide)
6. Affichez uniquement les noms des 10 premiers étudiants (sans les _id)
7. Affichez les 5 premiers étudiants triés par ordre alphabétique

### Partie 2 - Manipulation des tableaux

8. Pour l'étudiant avec `_id = 0`, extrayez et affichez sa note d'examen
9. Calculez la moyenne des 3 notes de l'étudiant avec `_id = 1`
10. Utilisez `$unwind` pour déplier le tableau scores et afficher les 5 premiers résultats

### Partie 3 - Agrégations

11. Calculez la moyenne générale de chaque étudiant et affichez le top 10
12. Calculez la moyenne de tous les étudiants pour chaque type d'évaluation (exam, quiz, homework)
13. Pour chaque type d'évaluation, trouvez qui a eu la meilleure note
14. Pour chaque étudiant, calculez le minimum, maximum et moyenne de ses notes
15. Comptez combien d'étudiants ont une moyenne générale supérieure à 70

### Partie 4 - Mises à jour

16. Ajoutez un champ `moyenne` à tous les documents contenant la moyenne des 3 notes
17. Ajoutez un champ `niveau` selon la moyenne : "Excellent" (≥80), "Bien" (≥60), "Passable" (≥40), "Insuffisant" (<40)
18. Supprimez la note de homework la plus faible de chaque étudiant
19. Mettez à jour le nom de l'étudiant avec `_id = 113` (qui est vide) en "Nom Inconnu"

---

