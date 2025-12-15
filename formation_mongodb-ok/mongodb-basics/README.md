# Les bases de MongoDB

### La structure de MongoDB

Une base de données MongoDB, contrairement à une base de données séquentielle, a une structure plus libre car elle ne suit pas un shéma de construction figé. Malgré tout, les éléments sont regroupés dans des ensembles bien définis tels que:

- `Database`: Sur un serveur de base de données, il est bien entendu possible de créer plusieurs bases de données, en général chacune d'entre elle ayant pour objectif de fournir le stockage d'un besoin utilisateur en particulier (en général donc une application).
- `Collection`: Une collection comprendra plusieurs éléments de données qu'elle regroupera derrière un nom commun, de la sorte, il est possible d'avoir une collection de chiens, d'utilisateurs, de produits, etc...
- `Document`: Chaque entité de donnée se voit dans l'univers MongoDB stocké sous la forme d'un document, qui n'est au final qu'une entité au format **BSON** (un dérivé du JSON). Il est ainsi possible d'avoir plusieurs documents dans une même collection. Cependant, contrairement à une base de données séquentielle classique, un document et un autre ne sont pas forcé d'avoir la même structure pour co-éxister au sein de la même collection. De plus, il est possible qu'un document A et un document B dans deux collection différentes soient les mêmes. Il convient donc au développeur d'organiser lui-même cette structure et cet ensemble de données avec la rigueur nécessaire.

Tous ces éléments peuvent être créés de façon implicite par MongoDB. Il n'est par exemple pas forcément nécessaire de procéder à la création de la collection avant de s'en servir.

---

### Le BSON (Binary JSON)

Contrairement au format JSON, MongoDB se sert d'un élément de type **BSON**. Cette différence n'importe pas réellement dans le cadre de la syntaxe, car in fine les informations sont sous la forme d'un JSON. La raison réelle vient d'un objectif de performance et de taille, en plus de permettre l'ajout de types de données supplémentaires (comme par exemple ObjectId, qui n'est pas un type de valeur correcte dans le format JSON).

---

### Les différents types numériques

Dans le cadre du stockage de valeurs numériques, il est possible de fonctionner via plusieurs types de valeurs:
* `Int32`: Les entiers classiques encodés sur **32 bits**, utilisables via `NumberInt()`
* `Int64`: Les entiers longs  encodés sur **64 bits**, utilisables via `NumberLong()`
* `Double`: Les nombres à virgule flottante  encodés sur **64 bits**, utilisables par défaut dans le Shell de par son fonctionnement basé sur le Javascript
* `High Precision Double`: Les nombres à virgule flottante encodés sur **128 bits**, utilisables via `NumberDecimal()`

---

### Les bases du CRUD - Create

Le CRUD (Create, Read, Update, Delete) est un processus essentiel à maîtriser lorsque l'on travaille avec une base de données. Pour une implémentation correcte d'un système de stockage de données, il est nécessaire de respecter ces 4 fonctionnalités dans une application pour qu'elle respecte les conventions usuelles.

Pour insérer des informations dans la base de données il nous faut utiliser la fonctionnalité `insertOne(data, options)` qui prendra en paramètre un objet à la structure d'un JSON, et dont on peut ommettre les guillements de nom de propriétés si on le veut. Par exemple, pour insérer un client, on peut procéder de la sorte:  

```js
db.collectionName.insertOne({ propA: 'Value', propB: 12345, procC: { propA: true } })
```

Il est également possible de procéder à des insertions multiples via la fonction `insertMany(data, options)` qui se présente sous la forme de l'ajout d'un tableau d'éléments:

```js
db.collectionName.insertMany([
  { prop: 'Value' },
  { prop: 'Value' },
  { prop: 'Value' },
])
```

---

### Les bases du CRUD - Read

Suite à l'insertion de cet élément, il se verra affecté une clé primaire ayant pour type `ObjectId`. Il est possible cependant de donner nous même la valeur de la clé primaire via l'ajout de la propriété `_id` lors de l'insertion (attention aux duplicats cependant dans ce genre de cas). Ce type de donnée est utilisé dans l'univers MongoDB. Si l'on veut par la suite accéder à un élément, il est possible de nous servir de la fonction `find(filter, options)` pour afficher tous les éléments d'une collection. A cela, on peut ajouter `pretty()` pour améliorer l'affichage: 

```js
db.collectionName.find().pretty()
```

Si l'on le souhaite, on peut bien entendu rendre notre requête plus sélective via l'utilisation des filtres, où n'avoir qu'un seul élément via la commande `findOne(filter, options)`.

---

### Les bases du CRUD - Update

Si l'on souhaite éditer les valeurs d'un élément, il est possible d'utiliser les méthodes `updateOne(filter, data, options)` pour éditer un élément, `updateMany(filter, data, options)` pour éditer plusieurs éléments. Pour réaliser une modification, il nous faut utiliser ce que l'on appelle des opérateurs dans le but d'informer MongoDB de l'opération à effectuer. Les opérateurs commencent par le caractère `$` pour ceux fourni dans MongoDB. La syntaxe, dans le cadre de la modification du titre d'un produit, se présenterai de la sorte: 

```js
db.products.updateOne({ _id: "Value" }, { $set: { newField: "Value" } })
```

Pour un édit multiple, il suffit d'utiliser la méthode de modification multiple avec un filtre vide de la sorte: 

```js
db.products.updateMany({}, { $set: { newField: "Value" } })
```

Il existe aussi une autre méthode, `update(filter, data, options)` qui n'a pas pour rôle d'ajouter ou de modifier des champs, mais de simplement remplacer le document par les informations fournies en données. Il est alors important de faire attention lors de son utilisation sous peine de supprimer sans le vouloir toute une partie des infos de notre élément. La méthode `replaceOne(filter, data, options)` existe également et aura la même fonction mais son nom est plus explicite et il est donc préférable de la retenir.

---

### Les bases du CRUD - Delete

Pour supprimer des éléments, il existe deux méthodes qui se nomment `deleteOne(filter, options)` pour la suppression unitaire et `deleteMany(filter, options)` pour la suppression multiple. 

Si l'on veut supprimer d'un seul coup l'ensemble d'une collection, alors le plus simple est d'utiliser la méthode de supression multiple avec un filtre vide. De la sorte, on obtient une collections vide. Sans le cas où l'on veut supprimer un élément correspondant à un critère, la syntaxe se présente de la sorte:

Pour supprimer une base de données, on peut utiliser la commande:

```js
db.dropDatabase()
```

De même, si c'est la collection que l'on veut supprimer, il est possible de le faire via:

```js
db.collectionName.drop()
```

```js
db.collectionName.deleteOne({ _id_: "Value" })
```
---

### Aller plus loin dans la sélection

Pour pouvoir améliorer nos sélection, il est nécessaire de connaitre un peu plus de chose sur les filtres potentiels d'être utilisés dans MongoDB. Par exemple, si l'on veut sélectionner des posts basés sur un titre, alors on peut réaliser une sélection de la sorte: 

```js
db.collection.find({ title: "Value" })
```

Pour des sélection plus complexe, par exemple un prix supérieur à une valeur, alors on doit passer par l'opérateur `$gt` (Greater Than) de la sorte: 

```js
db.collection.find({ price: { $gt: 12345 } })
```

Lorsque l'on utilise une sélection, il est important de savoir que dans notre système de données se trouvera un curseur. Ce curseur indique au système que l'on est actuellement en train de visionner les 20 premières données relatives à notre requête et non pas toutes les données d'un coup. Pour pouvoir afficher la suite en cas d'un grand nombre de données, il nous faudra utiliser `it`. 

```js
// On aura les 20 premier éléments
db.collectionName.find()

it
```

Si l'on veut avoir l'entièreté de la liste d'élément et ne pas avoir à aller aux 20 suivants, alors on peut utiliser `.toArray()`:

```js
// On aura tous les éléments transformé en tableau puis affichés
db.collectionName.find().toArray()
```

Si l'on veut réaliser des opérations pour l'ensemble des données, on peut utiliser la méthode `.forEach()` en lui passant une fonction fléchée pour spécifier l'opération à effectuer. Cette méthode utilisera la méthode du curseur pour travailler, et effectuera l'opération groupement d'éléments par groupement d'éléments:

```js
// On aura tous les éléments transformé en tableau puis affichés
db.collectionName.find().forEach(x => { printjson(x) })
```

---

### La Projection

Dans la majorité des cas, au sein d'une application, nous n'aurons pas besoin de toutes les informations d'un document à chaque fois. Pour éviter d'avoir à faire une requête couteuse retournant tous les attributs des documents d'une collection, mais avoir seulement ceux qui nous intéresse, on a recourt à un mécanisme nommé **projection**. Pour la réaliser, on passe par les options dans les méthodes de sélection. Pour inclure un élément, on utilise la valeur `1`, les autres se voyant automatiquement exclus, mis à part l'Id qui doit être exclue manuellement via la valeur `0`:

```js
db.collectionName.find({}, { _id: 0, name: 1 })
```

---

### Les documents liées

Dans l'univers du NoSQL, il est possible de placer des documents dans des attributs de document, à hauteur de 100 niveaux de hierarchie maximaux et ne devant pas dépasser une taille de plus de 16 MB par document de niveau hierarchique N. Il est d'ailleurs possibles, dans les documents, d'avoir en valeur d'attributs des tableaux, pour lier des ensembles de données à un document d'un seul coup. 

Il est du coup possible d'avoir un document semblable au modèle ci-dessous: 

```json
{
  "firstName": "John",
  "lastName": "DOE",
  "job": {
    "name": "Gardener",
    "hireDate": "2007-05-18"
  },
  "favColors": [ "Red", "Green", "Blue" ],
  "dogs": [
    {
      "name": "Zoé",
      "breed": "German Shepard",
      "age": 10,
      "isMale": false
    },
    {
      "name": "Rex",
      "breed": "Doberman",
      "age": 3,
      "isMale": true
    }
  ]
}
```

Dans ce genre de structure, il devient parfois nécessaire de faire une recherche basée sur la valeur d'une propriété de document enfant. Pour cela, la notation avec l'usage du `.` est disponible. Elle se présente de la sorte: 

```js
db.collectionName.find({ "dogs.isMale": true })
```

---

[Retour](../README.md)