Parfait.
Je repars **depuis zéro**, **sans raccourci**, **sans slogan**, **sans confusion**, et **en expliquant exactement ce que MongoDB fait à chaque étape**, **ligne par ligne**, **option par option**.

👉 Ce qui suit est **une démo pédagogique complète**, exécutable **telle quelle dans `mongosh`**, avec **un seul fil conducteur**, et **des explications factuelles** (ce que le moteur fait / ne fait pas).

---

# 🧪 DÉMO COMPLÈTE — CREATE DANS MONGODB

## (du plus simple → au plus contrôlé)

## 🎯 Contexte métier (important pour comprendre)

On construit un **catalogue de produits e-commerce**.

Au début :

* on veut **juste stocker des produits**

Ensuite :

* on veut **éviter les erreurs**
* on veut **des règles**
* on veut **des garanties techniques**

MongoDB permet **tout ça**, mais **uniquement si on lui demande explicitement**.

---

# 🔹 ÉTAPE 0 — ÉTAT INITIAL (aucune règle)

```js
use("demo")
db.products.drop()
```

### Ce que MongoDB fait

* `use("demo")` : change de contexte **sans créer la base**
* `drop()` : supprime la collection **et toutes ses métadonnées**

  * documents
  * index
  * validation

👉 On repart **comme si rien n’avait jamais existé**

---

# 🔹 ÉTAPE 1 — CREATE MINIMAL (`insertOne`)

```js
db.products.insertOne({
  id: 1,
  name: "Smartphone Alpha",
  description: "Smartphone haut de gamme avec écran OLED 6.1 pouces",
  price: 799.99,
  category: "Electronics",
  available: true
})
```

### Ce que MongoDB fait **exactement**

1. Vérifie que le document est du **BSON valide**
2. Ajoute automatiquement :

   ```js
   _id: ObjectId(...)
   ```
3. Crée la collection `products` (elle n’existait pas)
4. Écrit le document sur disque

### Ce que MongoDB **NE FAIT PAS**

* ❌ ne vérifie pas que `id` est unique
* ❌ ne vérifie pas le type de `price`
* ❌ ne vérifie pas la cohérence métier

👉 MongoDB **stocke**, il ne **juge pas**

---

# 🔹 ÉTAPE 2 — CREATE MULTIPLE (`insertMany`)

```js
db.products.insertMany([
  {
    id: 2,
    name: "Montre Connectée Solar",
    description: "Montre connectée avec suivi d'activité et panneau solaire",
    price: 199.99,
    category: "Wearables",
    available: true
  },
  {
    id: 3,
    name: "Casque Audio Pro",
    description: "Casque audio sans fil avec réduction de bruit",
    price: 299.99,
    category: "Audio",
    available: false
  },
  {
    id: 4,
    name: "Tablette Pro 12",
    description: "Tablette 12 pouces avec stylet et clavier détachable",
    price: 899.99,
    category: "Computers",
    available: true
  }
])
```

### Ce que MongoDB fait

* Traite **chaque document indépendamment**
* N’impose **aucune structure commune**
* Insère tout ce qui est valide BSON

👉 Contrairement à SQL :

* pas de table
* pas de schéma
* pas de contrainte implicite

---

# 🔹 ÉTAPE 3 — CREATE AVEC CHAMPS MANQUANTS

```js
db.products.insertOne({
  id: 5,
  name: "Caméra de Sécurité Home",
  price: 99.99,
  category: "Home Security"
})
```

### Ce que MongoDB fait

* Accepte le document
* N’ajoute **aucun champ manquant**
* Ne remplit rien automatiquement

### Pourquoi c’est autorisé

MongoDB est **document-centric** :

* chaque document est **autonome**
* il n’existe **aucune obligation globale**

👉 Avantage : flexibilité
👉 Inconvénient : incohérence possible

---

# 🔹 ÉTAPE 4 — CREATE AVEC CHAMPS SUPPLÉMENTAIRES

```js
db.products.insertOne({
  id: 8,
  name: "Lampe de Bureau Lumo",
  description: "Lampe de bureau LED avec réglage d'intensité",
  price: 45.99,
  category: "Office Supplies",
  available: true,
  color: "White",
  warrantyYears: 2
})
```

### Ce que MongoDB fait

* Stocke **tous les champs**
* Ne modifie **aucun autre document**

👉 En SQL, cela nécessiterait un `ALTER TABLE`
👉 En MongoDB, c’est **natif**

---

# 🔹 ÉTAPE 5 — CREATE AVEC DATE

```js
db.products.insertOne({
  id: 9,
  name: "Sac à Dos Voyage Pro",
  description: "Sac à dos robuste",
  price: 74.99,
  category: "Travel",
  available: true,
  releaseDate: new Date("2024-01-01")
})
```

### Ce que MongoDB fait

* Stocke un **BSON Date**
* Valeur interne : timestamp UTC
* Indexable / triable / comparable

👉 Une date **n’est pas une string**

---

# 🔹 ÉTAPE 6 — CREATE AVEC TABLEAU

```js
db.products.insertOne({
  id: 10,
  name: "Drone Explorer Air",
  description: "Drone avec caméra 4K",
  price: 1199.99,
  category: "Electronics",
  available: false,
  tags: ["drone", "4K", "high-tech"]
})
```

### Ce que MongoDB fait

* Stocke un **array BSON**
* Autorise des requêtes directes :

  ```js
  { tags: "drone" }
  ```

👉 Pas de table intermédiaire
👉 Pas de jointure

---

# 🔹 ÉTAPE 7 — CREATE AVEC DOCUMENTS IMBRIQUÉS

```js
db.products.insertOne({
  id: 11,
  name: "Cafetière Expresso QuickBrew",
  description: "Cafetière automatique",
  price: 249.99,
  category: "Kitchen Appliances",
  available: true,
  comments: [
    { user: "Alice", comment: "Très rapide." },
    { user: "Bob", comment: "Facile à nettoyer." }
  ]
})
```

### Ce que MongoDB fait

* Stocke **des objets imbriqués**
* Tout est lu en **une seule opération disque**

👉 C’est le **cœur du modèle MongoDB**

---

# 🔵 AJOUT PROGRESSIF DES RÈGLES ET OPTIONS

---

# 🔹 ÉTAPE 8 — INDEX UNIQUE (RÈGLE MÉTIER)

```js
db.products.createIndex(
  { id: 1 },
  { unique: true }
)
```

### Ce que MongoDB fait

* Crée une structure d’index interne
* Toute future insertion :

  * vérifie l’unicité de `id`
  * rejette en cas de doublon

👉 MongoDB **ne protège rien sans index**

---

# 🔹 ÉTAPE 9 — `insertMany` + `ordered:false`

```js
db.products.insertMany(
  [
    { id: 12, name: "Produit A", price: 10 },
    { id: 12, name: "Produit A bis", price: 12 },
    { id: 13, name: "Produit B", price: 15 }
  ],
  { ordered: false }
)
```

### Ce que MongoDB fait

* Insère le 1er document
* Le 2e viole l’index → rejet
* **Continue** avec le 3e

👉 `ordered:false` = stratégie d’exécution
👉 Pas une règle métier

---

# 🔹 ÉTAPE 10 — CREATE IDÉMPOTENT (`upsert` + `$setOnInsert`)

```js
db.products.updateOne(
  { id: 14 },
  {
    $setOnInsert: {
      name: "Produit Unique",
      price: 59.99,
      category: "Misc",
      createdAt: new Date()
    }
  },
  { upsert: true }
)
```

### Ce que MongoDB fait

1. Cherche `id:14`
2. S’il **n’existe pas** :

   * crée le document
   * applique `$setOnInsert`
3. S’il **existe déjà** :

   * **n’écrit rien**
   * ignore `$setOnInsert`

👉 Résultat : **0 ou 1 document**, jamais plus

---

# 🔹 ÉTAPE 11 — GARANTIE D’ÉCRITURE (`writeConcern`)

```js
db.products.insertOne(
  {
    id: 15,
    name: "Produit Critique",
    price: 999.99,
    category: "Premium"
  },
  {
    writeConcern: {
      w: "majority",
      j: true
    }
  }
)
```

### Ce que MongoDB fait

* Écrit sur le primary
* Attend la réplication majorité
* Attend l’écriture dans le journal disque
* **Puis seulement** répond OK

👉 Ce n’est pas de la logique métier
👉 C’est une **garantie de durabilité**

---

# 🔹 ÉTAPE 12 — VALIDATION DE SCHÉMA

```js
db.runCommand({
  collMod: "products",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["id", "name", "price", "category"],
      properties: {
        id: { bsonType: "int" },
        name: { bsonType: "string" },
        price: { bsonType: "double", minimum: 0 },
        category: { bsonType: "string" },
        available: { bsonType: "bool" }
      }
    }
  },
  validationAction: "error"
})


db.products.insertOne({
  id: 100,
  name: "Clavier Mécanique Pro",
  price: 129.99,
  category: "Computers",
  available: true
})



db.products.insertOne({
  id: "101",          // ❌ string au lieu de int
  name: "Souris Pro",
  price: -25,         // ❌ prix négatif
  // category manquante ❌
  available: "yes"    // ❌ string au lieu de bool
})

```

### Ce que MongoDB fait maintenant

* À chaque INSERT / UPDATE :

  * compare le document au schéma
  * bloque si non conforme
* **Aucune écriture** si invalide

---

# 🔹 ÉTAPE 13 — BYPASS DE VALIDATION

```js
db.products.insertOne(
  { id: 21, name: "Ancien produit", price: "N/A" },
  { bypassDocumentValidation: true }
)


db.products.insertOne(
  {
    id: "101",
    name: "Souris Pro",
    price: -25,
    available: "yes"
  },
  { bypassDocumentValidation: true }
)

```

### Ce que MongoDB fait (important)

* **Ignore totalement le validator**
* Continue normalement :

  * `_id`
  * index
  * écriture disque

👉 Seule la validation est sautée
👉 Rien d’autre n’est désactivé

---

# 🧠 CONCLUSION FINALE (à retenir)

CREATE dans MongoDB, ce n’est pas :

> “insérer un document”

C’est :

> **choisir exactement quelles responsabilités tu donnes au moteur**

MongoDB :

* **ne devine rien**
* **n’impose rien**
* **exécute exactement ce que tu configures**

---

Si tu veux la suite (même niveau de rigueur) :

* UPDATE expliqué de la même manière
* READ + index + explain
* Anti-patterns MongoDB
* Comparaison SQL ↔ MongoDB

Dis-moi.
