# Introduction au NoSQL

### Qu’est-ce que le NoSQL ?

Le terme **NoSQL** signifie historiquement *“Not Only SQL”* et non *“No SQL du tout”*.
Il désigne une **famille de systèmes de gestion de bases de données** qui ne reposent pas sur le modèle relationnel classique (tables, lignes, colonnes, jointures strictes).

Contrairement aux SGBD relationnels comme **MySQL**, **PostgreSQL** ou **Oracle**, les bases NoSQL :

* ne reposent pas nécessairement sur des tables
* n’imposent pas toujours un schéma strict
* sont conçues dès l’origine pour **la scalabilité horizontale**
* privilégient souvent la **performance**, la **disponibilité** et la **souplesse**

Le NoSQL est apparu pour répondre à des besoins que les bases relationnelles géraient mal :

* très gros volumes de données
* données hétérogènes
* systèmes distribués
* applications web à fort trafic

---

# Rappel des grands types de SGBD

Il existe **plusieurs grandes familles de bases de données**, chacune répondant à des besoins précis.

---

## 1️⃣ Bases de données relationnelles (SQL)

### Exemples

* MySQL
* PostgreSQL
* Oracle
* SQL Server
* MariaDB

### Modèle

* Tables
* Lignes
* Colonnes
* Clés primaires / étrangères
* Jointures

### Points forts

* Modèle **rigoureux**
* Intégrité référentielle
* Transactions ACID fortes
* Langage SQL standardisé
* Très adapté aux données **structurées**

### Limites

* Schéma rigide
* Jointures coûteuses à grande échelle
* Scalabilité horizontale complexe
* Peu adapté aux données très hétérogènes

👉 Excellent pour :

* gestion financière
* ERP
* données fortement structurées
* systèmes transactionnels classiques

---

## 2️⃣ Bases NoSQL orientées documents

### Exemples

* MongoDB
* CouchDB
* Cosmos DB (API Mongo)

### Modèle

* Database
* Collections
* Documents (JSON/BSON)
* Pas de jointures obligatoires

### Points forts

* Schéma flexible
* Données imbriquées
* Lecture rapide
* Très bon compromis structure / souplesse
* Scalabilité native

### Limites

* Discipline requise côté développeur
* Jointures possibles mais non naturelles
* Modélisation différente du relationnel

👉 Idéal pour :

* API REST
* microservices
* catalogues
* données semi-structurées

---

## 3️⃣ Bases clé-valeur

### Exemples

* Redis
* DynamoDB
* Riak

### Modèle

```text
clé → valeur
```

### Points forts

* Extrêmement rapide
* Simple
* Très scalable

### Limites

* Pas de requêtes complexes
* Pas de structure
* Logique applicative très forte

👉 Idéal pour :

* cache
* sessions
* tokens
* compteurs

---

## 4️⃣ Bases orientées colonnes (Wide-column)

### Exemples

* Cassandra
* HBase
* ScyllaDB

### Modèle

* Colonnes groupées
* Accès par clé primaire
* Très orienté performance

### Points forts

* Scalabilité massive
* Tolérance aux pannes
* Très performant en écriture

### Limites

* Modélisation complexe
* Peu flexible
* Requêtes limitées

👉 Idéal pour :

* IoT
* logs
* big data
* séries temporelles

---

## 5️⃣ Bases orientées graphes

### Exemples

* Neo4j
* ArangoDB
* JanusGraph

### Modèle

* Nœuds
* Relations
* Propriétés

### Points forts

* Relations complexes naturelles
* Très performant pour les graphes
* Modélisation intuitive des liens

### Limites

* Peu adapté aux données tabulaires
* Cas d’usage spécifiques

👉 Idéal pour :

* réseaux sociaux
* moteurs de recommandation
* graphes de dépendances

---

# Le triangle de CAP

### Définition

Le **théorème CAP** stipule qu’un système distribué ne peut garantir **au maximum que deux des trois propriétés suivantes** :

* **C – Consistency (Cohérence)**
  Tous les nœuds voient la même donnée au même moment.

* **A – Availability (Disponibilité)**
  Chaque requête reçoit une réponse.

* **P – Partition Tolerance (Tolérance aux partitions)**
  Le système continue à fonctionner malgré des coupures réseau.

---

### Est-il encore d’actualité ?

👉 **Oui, mais avec des nuances importantes.**

À l’époque :

* SQL = **CP**
* NoSQL = **AP**

Aujourd’hui :

* Les SGBD modernes (MongoDB inclus) offrent :

  * des niveaux de cohérence configurables
  * des écritures majoritaires
  * des lectures causales
  * des compromis dynamiques

👉 CAP n’est plus un **choix binaire**, mais un **curseur configurable**.

---

# L’intérêt réel du NoSQL aujourd’hui

Le NoSQL n’est **pas un remplacement du SQL**, mais un **complément**.

Il permet :

* d’absorber la croissance
* de gérer des données hétérogènes
* de réduire la complexité applicative
* d’améliorer les performances en lecture
* de simplifier les architectures distribuées

---

# Pourquoi MongoDB en particulier ?

MongoDB est souvent choisi car il propose :

* un modèle **documentaire lisible**
* un langage de requête riche
* des index avancés
* des transactions
* des validations de schéma
* une réplication native
* un sharding intégré

👉 MongoDB **combine la souplesse du NoSQL**
👉 avec **des garanties proches du relationnel**

---

# Conclusion

MongoDB et le NoSQL en général ne sont pas là pour remplacer les bases relationnelles, mais pour répondre à des **problèmes modernes** :

* applications distribuées
* volumes importants
* schémas évolutifs
* besoins de performance

👉 Le bon choix n’est jamais *SQL ou NoSQL*, mais **SQL et NoSQL**, chacun à sa place.