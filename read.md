Parfait.
Je te fais **un cours COMPLET et structuré sur TOUTES les options de recherche (`find`)** applicables **à TA collection `boooks`**, **uniquement avec tes données**, **sans aggregation pour l’instant**, et **avec explication précise de ce que MongoDB fait**.

> 👉 On parle ici **exclusivement de RECHERCHE (`find`)**
> 👉 Chaque requête est **exécutable telle quelle dans `mongosh`**

---

# 📚 Collection cible

```js
use demo
db.boooks.findOne()
```

Structure observée (résumé réel) :

```js
{
  _id: Number,
  title: String,
  isbn: String,
  pageCount: Number,
  publishedDate: Date,
  shortDescription?: String,
  longDescription?: String,
  status: String,
  authors: [String],
  categories: [String]
}
```

---

# 1️⃣ RECHERCHE SIMPLE (égalité)

## 🔹 Tous les documents

```js
db.boooks.find()
```

👉 MongoDB parcourt **toute la collection**.

---

## 🔹 Recherche par égalité stricte

```js
db.boooks.find({ status: "PUBLISH" })
```

👉 MongoDB compare **exactement la valeur BSON** (`"PUBLISH"` ≠ `"publish"`).

---

## 🔹 Recherche par `_id`

```js
db.boooks.find({ _id: 1 })
```

👉 `_id` est **indexé par défaut**, donc recherche **O(log n)**.

---

# 2️⃣ PROJECTION (choisir les champs retournés)

## 🔹 Inclure certains champs

```js
db.boooks.find(
  { status: "PUBLISH" },
  { title: 1, authors: 1 }
)
```

👉 MongoDB :

* lit le document complet
* **ne retourne que les champs demandés**

---

## 🔹 Exclure des champs lourds

```js
db.boooks.find(
  {},
  { longDescription: 0 }
)
```

👉 Très utile pour éviter des payloads massifs.

---

# 3️⃣ COMPARAISONS NUMÉRIQUES (`$gt`, `$lt`, …)

## 🔹 Plus de 500 pages

```js
db.boooks.find({ pageCount: { $gt: 500 } })
```

---

## 🔹 Intervalle

```js
db.boooks.find({
  pageCount: { $gte: 300, $lte: 600 }
})
```

👉 MongoDB compare **les valeurs BSON numériques**, pas des strings.

---

## 🔹 Valeur exacte OU manquante

```js
db.boooks.find({
  pageCount: { $in: [0, null] }
})
```

---

# 4️⃣ RECHERCHE SUR DATES

## 🔹 Livres publiés après 2010

```js
db.boooks.find({
  publishedDate: { $gte: ISODate("2010-01-01") }
})
```

👉 MongoDB compare des **timestamps**, pas des chaînes.

---

## 🔹 Entre deux dates

```js
db.boooks.find({
  publishedDate: {
    $gte: ISODate("2008-01-01"),
    $lte: ISODate("2012-12-31")
  }
})
```

---

# 5️⃣ RECHERCHE SUR TABLEAUX (`authors`, `categories`)

## 🔹 Contient une valeur (le plus courant)

```js
db.boooks.find({ categories: "Java" })
```

👉 MongoDB :

* parcourt le tableau
* match **si UNE valeur correspond**

---

## 🔹 Auteur exact dans le tableau

```js
db.boooks.find({ authors: "Kyle Banker" })
```

---

## 🔹 Plusieurs valeurs possibles (`$in`)

```js
db.boooks.find({
  categories: { $in: ["Internet", "Java"] }
})
```

---

## 🔹 Toutes les valeurs requises (`$all`)

```js
db.boooks.find({
  categories: { $all: ["Internet", "Mobile"] }
})
```

---

# 6️⃣ CONDITIONS LOGIQUES (`$and`, `$or`, `$not`)

## 🔹 AND implicite (le plus courant)

```js
db.boooks.find({
  status: "PUBLISH",
  pageCount: { $gt: 400 }
})
```

---

## 🔹 OR explicite

```js
db.boooks.find({
  $or: [
    { categories: "Java" },
    { categories: "Web Development" }
  ]
})
```

---

## 🔹 NOT

```js
db.boooks.find({
  pageCount: { $not: { $gt: 500 } }
})
```

---

# 7️⃣ EXISTENCE DE CHAMPS (`$exists`)

## 🔹 Livres avec description longue

```js
db.boooks.find({
  longDescription: { $exists: true }
})
```

---

## 🔹 Livres SANS description courte

```js
db.boooks.find({
  shortDescription: { $exists: false }
})
```

---

# 8️⃣ EXPRESSIONS RÉGULIÈRES (TEXT SEARCH BASIQUE)

## 🔹 Titre contenant “Action”

```js
db.boooks.find({
  title: /Action/
})
```

---

## 🔹 Insensible à la casse

```js
db.boooks.find({
  title: /action/i
})
```

---

## 🔹 Description contenant “Android”

```js
db.boooks.find({
  longDescription: /Android/i
})
```

⚠️ Sans index → **scan complet**

---

# 9️⃣ RECHERCHE TEXTE (`$text`) – AVANCÉE

## 🔹 Créer un index texte

```js
db.boooks.createIndex({
  title: "text",
  shortDescription: "text",
  longDescription: "text"
})
```

---

## 🔹 Recherche plein texte

```js
db.boooks.find({
  $text: { $search: "Android Java" }
})
```

👉 MongoDB :

* tokenise
* score
* trie par pertinence

---

## 🔹 Exclure un mot

```js
db.boooks.find({
  $text: { $search: "Java -Flex" }
})
```

---

# 🔟 TRI (`sort`)

## 🔹 Par date (récent → ancien)

```js
db.boooks.find().sort({ publishedDate: -1 })
```

---

## 🔹 Par nombre de pages

```js
db.boooks.find().sort({ pageCount: 1 })
```

---

# 1️⃣1️⃣ PAGINATION (`limit`, `skip`)

## 🔹 Page 1 (10 résultats)

```js
db.boooks.find().limit(10)
```

---

## 🔹 Page 2

```js
db.boooks.find().skip(10).limit(10)
```

---

# 1️⃣2️⃣ COMPTER

## 🔹 Nombre total

```js
db.boooks.countDocuments()
```

---

## 🔹 Nombre filtré

```js
db.boooks.countDocuments({ categories: "Java" })
```

---

# 1️⃣3️⃣ REQUÊTES AVANCÉES SUR CHAÎNES

## 🔹 Commence par “Flex”

```js
db.boooks.find({
  title: /^Flex/
})
```

---

## 🔹 Se termine par “Action”

```js
db.boooks.find({
  title: /Action$/
})
```

---

# 1️⃣4️⃣ PERFORMANCE (IMPORTANT)

## 🔹 Créer les bons index

```js
db.boooks.createIndex({ categories: 1 })
db.boooks.createIndex({ authors: 1 })
db.boooks.createIndex({ publishedDate: -1 })
```

---

## 🔹 Vérifier le plan d’exécution

```js
db.boooks.find({ categories: "Java" }).explain("executionStats")
```

👉 Tu vois :

* `COLLSCAN` ❌
* `IXSCAN` ✅

---

# 🧠 RÉCAP GLOBAL — TOUT CE QUE TU PEUX FAIRE AVEC `find`

| Type de recherche | Outils                       |
| ----------------- | ---------------------------- |
| Égalité           | `{ field: value }`           |
| Comparaison       | `$gt`, `$lt`, `$gte`, `$lte` |
| Logique           | `$and`, `$or`, `$not`        |
| Tableaux          | `$in`, `$all`                |
| Texte simple      | regex                        |
| Texte avancé      | `$text`                      |
| Projection        | `{ field: 1/0 }`             |
| Tri               | `.sort()`                    |
| Pagination        | `.skip().limit()`            |
| Performance       | index + explain              |

---

👉 **Prochaine étape naturelle** (si tu veux) :

* mêmes recherches avec **Aggregation Framework**
* recherches géospatiales
* recherches avec **collation (accent / casse)**
* pièges classiques `find`

Dis-moi 👍
