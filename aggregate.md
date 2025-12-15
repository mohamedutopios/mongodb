Parfait 👍
Je vais **reprendre TOUTES tes requêtes**, **les corriger si nécessaire**, **les compléter** et surtout **les enrichir avec des options avancées** (notamment `$project`, `$sort`, `$limit`, `$addFields`, `$count`, `$group`, `$match`), **sans changer le sens pédagogique**.

👉 Objectif : que tu puisses les utiliser **comme TP MongoDB / Aggregation**, pas juste comme recettes.

---

# 📍 Contexte

```js
use("restau")
// collection : restaurant
```

Structure observée (d’après tes données) :

```js
{
  URL: String,
  name: String,
  address: String,
  outcode: String,
  postcode: String,
  rating: Number | "Not yet rated",
  type_of_food: String
}
```

⚠️ Attention importante :
`rating` peut être **un nombre OU une chaîne** → impact direct sur les requêtes.

---

# 1️⃣ Requêtes simples (`find`)

## 🔹 Afficher 10 restaurants

```js
db.restaurant.find().limit(10)
```

➡️ Scan simple + limite côté serveur.

---

## 🔹 Restaurants dans un `outcode` précis

```js
db.restaurant.find(
  { outcode: "W6" },
  { name: 1, type_of_food: 1, rating: 1, _id: 0 }
)
```

👉 Projection ajoutée :

* réduit la taille des documents retournés
* améliore la lisibilité

---

## 🔹 Restaurants sans code postal

```js
db.restaurant.find({
  postcode: { $exists: false }
})
```

👉 `$exists` vérifie **la présence du champ**, pas sa valeur.

---

## 🔹 Restaurants dont le postcode ≠ "8NX"

```js
db.restaurant.find({
  postcode: { $ne: "8NX" }
})
```

⚠️ Version plus simple et plus lisible que `$not + $eq`.

---

# 2️⃣ Aggregation – filtrage (`$match`)

## 🔹 Restaurants avec une note EXACTE de 5

```js
db.restaurant.aggregate([
  { $match: { rating: 5 } }
])
```

👉 `$match` ≈ `WHERE` en SQL.

---

## 🔹 Compter les restaurants notés 5

```js
db.restaurant.aggregate([
  { $match: { rating: 5 } },
  { $count: "comptage" }
])
```

➡️ `$count` remplace :

```js
$group + $sum
```

---

## 🔹 Restaurants notés 5 (champs utiles uniquement)

```js
db.restaurant.aggregate([
  { $match: { rating: 5 } },
  {
    $project: {
      _id: 0,
      name: 1,
      URL: 1,
      type_of_food: 1,
      rating: 1
    }
  }
])
```

👉 `$project` :

* sélectionne les champs
* peut aussi les renommer ou en calculer

---

# 3️⃣ Aggregation – groupements (`$group`)

## 🔹 Nombre de restaurants par type de nourriture

```js
db.restaurant.aggregate([
  {
    $group: {
      _id: "$type_of_food",
      count: { $sum: 1 }
    }
  }
])
```

👉 `_id` = clé de regroupement.

---

## 🔹 Types de nourriture avec plus de 10 restaurants

```js
db.restaurant.aggregate([
  {
    $group: {
      _id: "$type_of_food",
      count: { $sum: 1 }
    }
  },
  {
    $match: { count: { $gt: 10 } }
  }
])
```

---

## 🔹 Même requête + tri décroissant

```js
db.restaurant.aggregate([
  {
    $group: {
      _id: "$type_of_food",
      count: { $sum: 1 }
    }
  },
  { $match: { count: { $gt: 10 } } },
  { $sort: { count: -1 } }
])
```

---

# 4️⃣ Groupement par code postal

## 🔹 Nombre de restaurants par `postcode`

```js
db.restaurant.aggregate([
  {
    $group: {
      _id: "$postcode",
      nombre_de_restaurants: { $sum: 1 }
    }
  },
  { $sort: { nombre_de_restaurants: -1 } }
])
```

---

# 5️⃣ Filtres combinés

## 🔹 Restaurants Thai avec note > 4

```js
db.restaurant.aggregate([
  {
    $match: {
      type_of_food: "Thai",
      rating: { $gt: 4 }
    }
  },
  {
    $project: {
      _id: 0,
      name: 1,
      rating: 1,
      outcode: 1
    }
  }
])
```

---

# 6️⃣ Projection + limite

## 🔹 Top 3 restaurants notés 6

```js
db.restaurant.aggregate([
  { $match: { rating: 6 } },
  {
    $project: {
      _id: 0,
      name: 1,
      type_of_food: 1,
      rating: 1
    }
  },
  { $limit: 3 }
])
```

---

# 7️⃣ Comptage ciblé

## 🔹 Nombre de restaurants Caribbean

```js
db.restaurant.aggregate([
  { $match: { type_of_food: "Caribbean" } },
  { $count: "no_of_restaurants_with_caribbean_food" }
])
```

---

# 8️⃣ Statistiques sur les notes (IMPORTANT)

## 🔹 Moyenne des notes par type de nourriture

⚠️ Il faut **exclure les notes non numériques**.

```js
db.restaurant.aggregate([
  {
    $match: {
      rating: { $type: "number" }
    }
  },
  {
    $group: {
      _id: "$type_of_food",
      note_moyenne: { $avg: "$rating" }
    }
  },
  { $sort: { note_moyenne: -1 } }
])
```

---

## 🔹 Statistiques complètes par type

```js
db.restaurant.aggregate([
  {
    $match: {
      rating: { $type: "number" }
    }
  },
  {
    $group: {
      _id: "$type_of_food",
      total_rating: { $sum: "$rating" },
      avg_rating: { $avg: "$rating" },
      max_rating: { $max: "$rating" },
      min_rating: { $min: "$rating" },
      count: { $sum: 1 }
    }
  },
  {
    $project: {
      type_of_food: "$_id",
      _id: 0,
      count: 1,
      avg_rating: { $round: ["$avg_rating", 2] },
      max_rating: 1,
      min_rating: 1
    }
  }
])
```

👉 `$round` améliore la lisibilité.

---

# 9️⃣ Option avancée BONUS – champ calculé

## 🔹 Ajouter un champ “bien_noté”

```js
db.restaurant.aggregate([
  {
    $addFields: {
      bien_note: {
        $cond: [
          { $gte: ["$rating", 5] },
          true,
          false
        ]
      }
    }
  },
  {
    $project: {
      name: 1,
      rating: 1,
      bien_note: 1,
      _id: 0
    }
  }
])
```

---

# 🧠 RÉCAP DES OPÉRATEURS UTILISÉS

| Opérateur    | Rôle                       |
| ------------ | -------------------------- |
| `$match`     | Filtrer                    |
| `$project`   | Sélectionner / transformer |
| `$group`     | Regrouper                  |
| `$count`     | Compter                    |
| `$sort`      | Trier                      |
| `$limit`     | Limiter                    |
| `$addFields` | Ajouter un champ calculé   |
| `$type`      | Vérifier le type           |
| `$round`     | Arrondir                   |

---

Si tu veux la suite logique :

* même TP avec **index + explain**
* optimisation des requêtes lentes
* transformer ces requêtes en **API REST**
* version SQL équivalente

👉 Dis-moi 👍
