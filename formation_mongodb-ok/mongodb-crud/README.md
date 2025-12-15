# Le CRUD en détails

### Create - Ajouter des données dans notre Database

Historiquement, dans le monde de MongoDB, il y a eu la méthode `insert()` qui permettait de pouvoir insérer soit un élément ou tout un ensemble d'élément. Cependant, suite à des plaintes de la communauté sur la non lisibilité des lignes de code suite à l'utilisation d'une méthode unique pouvant causer des erreurs relative à un mauvais type d'entrée, il a été décidé de séparer cette fonctionnalité en deux méthodes distinctes qui sont `insertOne()` et `insertMany()`. La premier est encore utilisable, mais est généralement désormais non utilisée de part les problèmes qu'elle soulève. De plus, les nouvelles méthodes ont l'avantage de fournir les ID insérées en réponse à la requête.

Lors d'une insertion, il est possible d'ajouter des informations en plus de réaliser l'ajout à proprement parler, comme par exemple spécifier l'Id inséré en même temps que les informations. Si l'on réalise une insertion de clé en duplicat, alors les insertion prcédente réussirons, mais le processus s'arrêtera au moment où l'on atteindra la clé problématique. Ceci se voit confirmé dans le message d'erreur dans l'attribut `nInserted` de l'erreur `BulkWriteError`. Ce processus est possible de par le mode de fonctionnement de MongoDB. 

Il est possible de mettre des options sur notre insertion via un autre objet, par exemple l'attribut `ordered` qui par défaut est à `true`. Si l'on le change, alors il est possible de ne pas éliminer les insertion car l'arrivée d'une insertion infructueuse n'aura plus d'incidance sur les suivante de par l'absence d'ordre:

```js
db.collection.insertMany([ ... ], { ordered: false })
```

Une autre option qui pourrait être intéressante de modifier serait l'option `writeConcern`, qui a pour objectif de gérer le nombre d'instances sur lesquelles on veut que l'insertion ait lieu avec le paramètre `w` (il est possible de travailler avec plusieurs instances de BdD en même temps) et la journalisation via le paramètre `j` (il s'agit d'un fichier fonctionnant comme une todo-list pour la gestion de l'ordre des modifications à faire dans les fichiers de la BdD, ce fichier pouvant être lu en cas de crash). Enfin, il est possible de définir le temps d'attente possible pour les actions d'écriture via l'attribut `wtimeout`

```js
db.collection.insertOne( data, { writeConcern: { w: 1, j: true, wtimeout: 200 }})
```

Dans l'insertion, il est aussi intéressant de savoir ce qu'est l'**Atomicité**. Cette notion concerne le besoin de rendre les requêtes atomiques, c'est à dire qu'elle doivent soit réussir entièrement soit échouer entièrement au niveau du document. Ainsi, si l'on essaie d'insérer un nouvel élément, on est sur que s'il est inséré, tous ses champs auront été insérés. De même, en cas d'echec, nous n'aurons pas une partie du document mais l'absence de l'entièreté du document.

### Create - Importer des données

Si l'on veut importer des éléments directement dans notre base de données, avec par exemple un fichier JSON, il est possible de le faire via `mongoimport`. Cette commande est disponible en cas d'installation du binaire et son ajout à la variable d'environnement `PATH`:

```bash
mongoimport file.json -d databaseName -c collectionName --jsonArray --drop
```

Les options ont pour objectif les suivants: 
* `-d`: Permet d'informer de la database que l'on cherche à peupler
* `-c`: Permet d'informer de la collection que l'on cherche à peupler
* `--jsonArray`: Permet d'informer que l'on aura plusieurs éléments à insérer sous la forme d'un tableau
* `--drop`: Permet la suppression de la collection au préalable pour être sur de partir sur une ré-écriture et non un ajout

---

### Read - Récupérer les données de notre base de données

Pour la sélection dans la base de donnée, les méthodes à connaître sont `find()` pour la récupération multiple et `findOne()` pour la récupération unitaire de nos éléments. Nous allons désormais pousser un peu plus loin l'utilisation des filtres de sélection et les opérateurs fourni par MongoDB dans le cadre d'une récupération. 

Dans la partie Read du CRUD, il est possible de voir deux syntaxes de base:

```js
db.collectionName.find({ field: "value" }) // Possible en cas d'égalité(s)

db.collectionName.find({ field: { $operator: "value" } }) // Le cas le plus courant si l'on a besoin de sélectionner autrement que par égalité champs-valeurs
```

---

### Read - Les opérateurs de comparaison

Pour bien sélectionner les entités qui nous intéresse, il est donc important de connaître leso pérateurs majeurs de MongoDB. Dans un premier temps, nous allons nous intéresser aux opérateurs de comparaison: 

```js
db.products.findOne({ price: { $gte: 25 } })
```

- `$eq`: Egalité 
- `$ne`: Différence 
- `$lt`: Plus petit que
- `$gt`: Plus grand que
- `$lte`: Plus petit ou égal à
- `$gte`: Plus grand ou égal à

Dans le cadre de tableaux, il est également possible de procéder au requêtage sur une égalité d'ensemble de données, par exemple pour les couleurs préférées des enfants d'une personne: 

```js
db.people.find({ "people.children.favColors": ["Red", "Blue", "Green"] })
```

Pour les documents enfants et les arrays, il est également intéressant de connaitre les opérateurs suivants, qui s'avèrent être assez pratique pour sélectionner dans ces types de données: 

- `$in`: La valeur du champ doit être parmi les valeurs recherchées
- `$nin`: LA valeur du champ ne doit pas être parmi les valeurs recherchées

---

### Read - Les opérateurs logiques

D'autres types d'opérateurs sont intéressant dans le cadre du requêtage. Il s'agit des opérateurs logiques. Ces dernier permettent en effet de réaliser des opérations relatives aux tables de vérité, comme par exemple **AND**, **OR**, etc... Ils se présentent de la sorte: 

```js
db.movies.find({ $or: [ { "rating.average": { $lt: 10 }, { "rating.average": { $gt: 90 } ]}})

db.movies.find({ { "rating.average": { $not: { $eq: 90 } } }})
```

- `$or`: Pour chercher une valeur qui correspond à l'un des sélecteurs demandés
- `$nor`: Pour chercher une valeur qui ne correspond à aucun de l'un des sélecteurs demandés
- `$and`: Pour chercher une valeur qui correspond tous les sélecteurs demandés (La syntaxe classique en mettant des virgule entre nos filtres aurait le même effet)
- `$not`: Pour chercher une valeur qui ne correspond pas à la requête demandées

---

### Read - Les opérateurs d'élément

Dans les opérateurs, il existe aussi deux opérateurs d'éléments, dont l'objetif est:

- `$exists`: Le document possède ce champ dans sa structure
- `$type`: Le document possède un champ avec le bon type dans sa structure

```js
// Pour trouver les produits qui possèdent le champ 'sale', même si la valeur est 'null'
dc.product.find({ sale: { $exists: true } })

// Pour trouver tous les utilisateurs qui ont un numéro de téléphone sous forme de 'string' ou de 'double'
dc.users.find({ phone: { $type: [ 'double', 'string' ] } })
```

---

### Read - Les opérateurs d'évaluation

Il est possible d'utiliser des opérateurs un peu plus spécifique, comme par exemple celui des expressions régulières via l'utilisation de l'opérateur `$regex`:

```js
db.music.find({ genre: { $regex: /soundtrack/ } })
```

Un autre opérateur d'évaluation est celui permettant le calcul de valeurs via des expressions. Pour s'en servir, le nom de l'opérateur est `$expr` tel que:

```js
// Imaginons que l'on cherche à connaître les éléments dont le prix a baissé, en comparant l'ancien et le nouveau prix
db.products.find({ $expr: { $gt: [ "$oldPrice", "$newPrice" ]}})

// Pour avoir les produits dont le stock est soit inférieur à 150 tonnes, soit, au cas où c'est le cas, ce stock soustrait de 50 tonnes est supérieur à la valeur cible
db.products.find({ $expr: { 
    $gt: [ $cond: { if: { $gte: [ "$stock", 150 ] }, then: { $substract: [ "$stock", 50 ]} }, else:  "$stock",
    "$target" ]
  }})
```

---

### Read - Les opérateurs de tableaux

Pour le cas où l'on cherche à manipuler des requêtes se concentrant sur des champs de type tableau, il est peut être utile de connaître les opérateurs qui y sont dédiés: 

- `$size`: Permet de tester si le tableau dispose d'un certain nombre d'éléments

```js
db.users.find( { "hobbies": { $size: 2 } } )
```

- `$all`: Permet de tester si la valeur tableau contient toutes les valeurs demandées, peu importe l'ordre de ces éléments

```js
db.movies.find({ genre: { $all: ["action", "thriller" ] } } )
```

- `$elementMatch`: Permet de forcer la demande de plusieurs critères au sein d'un même document, et non au sein de la collection. Ainsi, les deux requêtes suivantes sont différentes: 

```js
// Recherche de document contenant à la fois un élément du tableau possédant un nom valant 'Tomatoe' et potentiellement un autre élément du tableau (ou le même) ayant une quantité inférieure à 3
db.recipes.find({ $and: [ "ingredients.name": "Tomatoe", "ingredients.quantity": { $lte: 3 } ] })

// Recherche de document contenant à la fois un élément du tableau possédant un nom valant 'Tomatoe' et une quantité inférieure à 3
db.recipes.find({ ingredients: { $elemMatch: { name: "Tomatoe", quantity: { $lte: 3 } } } })
```

---

### Read - La notion du curseur

Dans le monde de MongoDB, les requêtes de récupération de données fonctionne via le mécanisme du curseur. Cet élément permet d'envoyer non pas l'entièreté de la récupération d'un coup à d'autres requête ou au visionnage, mais des portions de la collection que l'on nomme des **Batch**. Dans le Shell, ces portions font la taille d'une **vingtaine** de documents. Si l'on travaille via un driver, c'est à nous de gérer la taille du curseur. Cette feature est très utile dans le cadre d'applications, car il est très rare que celles-ci montrent toutes les données d'un coup. Bien generalement, il y a un mécanisme de page présentant par exemple les 100 premièeres, puis les 100 suivantes données, page par page.

Dans le cas où l'on stocke la valeur de sortie d'une requête de type `find()`, n peut parl a suite appeller les élément un par un via le mécanisme du curseur. Pour ce faire, la méthode à utiliser est `next()`. Dans le cadre où l'on veut effectuer une série d'instruction pour chaque élément de notre flux, alors on peut utiliser la méthode `forEach()` rendue disponible par le shell de par son utilisation du Javascript (d'autres drivers auront une syntaxe et un fonctionnement potentiellement différent). Pour connaître s'il y a encore des données à visionner dans le flux, la méthode se nomme `hasNext()` et retourne un booléen.

---

### Read - Fonctions usuelles

Si l'on a envie, il est aussi possible, non pas de récupérer les valeurs des documents, mais par exemple le nombre de documents correspondant à notre requête. Pour ce faire, des fonctions sont disponibles dans l'univers MongoDB, comme par exemple `.count()`:

```js
db.movies.find(filter).count()
```

Si l'on le veut, il est possible de trier nos éléments selon des champs, via l'utilisation de la méthode `sort()`, dont on peut spécifier le sens via une valeur positive `1` ou négative `-1`. Il est possible de trier bien entendu par plusieurs champs, en les faisant se suivre dans les attributs de l'objet en paramètre de la requête.:

```js
db.movies.find(filter).sort({ fieldA: 1, fieldB: -1 })
```

Pour limiter ou passer des éléments dans les résultats du curseur, il est possible de nous servir de méthodes supplémentaire tel que:

```js
// Pour passer les 15 premiers
db.movies.find(filter).skip(15)

// Pour n'avoir que les 10 premiers
db.movies.find(filter).limit(10)
```

L'ordre des méthodes n'a pas d'incidence, l'ordre est imposé par MongoDB et correspond à commencer par le tri, puis les échappements et enfin on limite la sortie.

Via la projection, il est également possible de limiter les champs nous intéressant pour les fonctions dans le but de ne traiter qu'une portion de nos documents:

```js
db.movies.find({}, { title: 1, genre: 1 }).limit(50)

db.movies.find({}, { title: 1, genre: 1 }).limit(50)
```

Il est également possible de n'afficher que l'élément qui respecte notre filtre de projection via la syntaxe `"fieldName.$": 1`. En cas de possibilité de projection, l'élément va s'affiche, mais dans le cas où il n'est pas possible de projeter l'information, celle-ci sera omise dans la sortie: 

```js
db.movies.find({ genre: "Drama"}, { "genre.$": 1 })

db.movies.find({ genre: "Drama"}, { genre: { $elemMatch: { $eq: "Horror" } } })
```

Dans le cadre de la projection et des tableaux, il est possible d'utiliser l'opérateur `$slice` qui a pour objectif de projeter une tranche du tableau, par exemple seulement les éléments de l'indice X à Y.

```js
// On prend les 3 premiers éléments du tableau
db.movies.find({ rating: { $gte: 70 } }, { genres: { $slice: 3 }}})

// On passe les 2 premiers éléments du tableaux puis on prend les 4 suivants
db.movies.find({ rating: { $gte: 70 } }, { genres: { $slice: [ 2, 4 ] } })
```

---

### Update - Editer nos documents

Il est très fréquent dans la manipulation des données que l'on ait besoin de réaliser des modifications de nos éléments. Par exemple, changer le stock des produits au fur et à mesure de leur écoulement. Pour faire des modification, on passe par la récolte via un filtre et l'on se sert d'opérateurs pour modifier des champs du ou des éléments trouvés en fonction de si l'on se sert de la méthode `updateOne()` ou `updateMany()`. Par exemple:

```js
// On va ajouter ou modifier le champ title de l'élément pour qu'il corresponde à 'Scarlet Night'
db.collection.updateOne({ _id: ObjectId("Value") }, { $set: { title: "Scarlet Night" }})

// On peut également se servir de cet opérateur pour modifier plusieurs champs d'un coup
db.collection.updateOne({ _id: ObjectId("Value") }, { $set: { public: "pegi-16", price: 9.89 }})
```

On peut également incrémenter ou décrémenter des valeurs dans le cadre d'un update. Pour ce faire, il nous faut utiliser une syntaxe de la sorte (attention, il n'est pas possible de travailler et d'effectuer deux modifications sur le même champ d'un document sous peine de générer un conflit): 

```js
// On augmente le stock de 50 tonnes pour les éléments dont le prix est inférieur ou égal à 20
dc.collection.updateMany({ price: { $lte: 20 } }, { $inc: { stock: 50 } })

// Impossible car conflit sur le champ 'stock'
dc.collection.updateMany({ price: { $lte: 20 } }, { $inc: { stock: 5 }, $set: { stock: 25} })
```

Via les opérateurs `$min` et `$max`, il est possible de changer des valeurs numériques de façon conditionnelles, de sorte à avoir une valeur ne dépassant par un threshold saisi par le développeur: 

```js
// Les éléments de la collection verront leur prix être modifié à 19.89 si leur prix précédent était d'une valeur dépassant ce nombre
dc.collection.updateMany({}, { $max: { price: 19..89 } })
```

Dans les opérateurs mathématiques, il est également possible de procéder à des calculs simples via les opérateurs: 

- `$add`: Pour additioner la valeur actuelle à un certain nombre.
- `$sub`: Pour soustraire la valeur actuelle par un certain nombre.
- `$mul`: Pour multiplier la valeur actuelle par un certain nombre.
- `$div`: Pour diviser la valeur actuelle par un certain nombre.

Si l'on le veut, il est également possible de se débarasser de champs au sein de nos éléments via l'opérateur `$unset`, qui permet de retirer simplement l'ensemble clé-valeur de notre / nos documents trouvés.

```js
db.collectioon.updateMany({ filter }, { $unset: { phone: "" }})
```

Il est aussi possible de renommer nos champs via l'opérateur dédié, ce dernier étant `$rename` et son fonctionnement est le suivant. Il faut passer en valeur un objet avec un ensemble de clés-valeurs correspondant à l'ancien nom du champs et comme valeur son nouveau nom: 

```js
db.collection.updateMany({ ... }, { $rename: { oldName: "newName" } })
```

La méthode d'édition est compatible avec une insertion en cas d'utilisation de l'option `upsert` (qui par défaut a pour valeur false) de la sorte: 

```js
db.collection.updateOne({ ... }, { ... }, { upsert: true })
```

---

### Update - Travailler avec des tableaux

Dans le cadre de la modification de champs qui sont dans des tableaux faisant eux-même partie des champs d'un document, la méthodologie de la modification des valeur diffère légèrement et d'autres éléments dans nos opérateurs qu'il est alors utiles à connaître. Pour l'ajout d'un champ dans l'un des document contenu dans le tableau X des documents trouvés, il est possible de procéder de la sorte:

```js
// On ajoute ici le champ 'units' aux document imbriqués se trouvant dans le tableau des ingrédients de nos recettes.
db.recipes.updateMany({ ingredients: $elemMatch: { name: "Tomatoe", quantity: 3 } }, { $set: { "ingredients.$.units": "kilograms" })

// On remplace le premier élément imbriqué respectant les critères du filtre et on le remplace par un nouveau document imbriqué
db.recipes.updateMany({ ingredients: $elemMatch: { name: "Tomatoe", quantity: 3 } }, { $set: { "ingredients.$": { field: "Value"} })
```

Si l'on veut cette fois-ci changer tous les éléments imbriqués d'un tableau d'un coup, la syntaxe ressemblera à celle-ci:

```js
// Via cette requête, on va incrémenter de 5 tous les éléments imbriqués du champ 'ingredient' ayant un champ 'quantity' et d'une valeur de 5
db.recipes.updateMany({ ingredients: $elemMatch: { name: "Tomatoe", quantity: 3 } }, { $inc: { "ingredients.$[].quantity": 5 })
```

Si, au sein d'un tableau contenant des éléments imbriqués, nous souhaitons désormais filtrer et modifier seulement certains champs, et non le premier ou tous, il nous faut utiliser l'option `arrayFilter`, qui va donner un identifiant utilisable dans la syntaxe vue précédemment pour ne modifier qu'une portion des éléments imbriqués: 

```js
// Si l'on veut ajouter le champs 'isVegan' avec pour valeur 'true' pour tous les éléments imbriqués du champ ingrédient de nos documents, qui est un array
db.recipes.updateMany({ "ingredients.quantity": { $gte: 2} }, { $set: { "ingredients.$[el].isVegan": true }, { arrayFilters: [ { "el.quantity": { $gte: 2 } } ]})
```

Il est aussi possible d'avoir envie de pouvoir ajouter ou supprimer des éléments du tableau d'éléments imbriqués. Pour cela, on peut utiliser les opérateurs:

```js
// Pour ajouter un élément imbriqué
db.recipes.updateOne({ name: "Tarte" }, { $push: { ingredients: { title: "flour", quantity: 5}}})

// Pour ajouter plusieurs éléments imbriqués d'un coup
db.recipes.updateOne({ name: "Tarte" }, { $push: { ingredients: { $each: [ { title: "flour", quantity: 5}, { title: "egg", quantity: 3}]}}})

// Il est possible d'ajouter des fonctionnalités supplémentaire, comme par exemple trier les éléments imbriqués avant leur ajout au tableau
db.recipes.updateOne({ name: "Tarte" }, { $push: { ingredients: { $each: [ { title: "flour", quantity: 5}, { title: "egg", quantity: 3 } ], $sort: { title: 1 }}}})
```

Si l'on le veut, il est possible d'éviter les doublons en usant à la place de l'opérateur `$addToSet`.

Pour supprimer les éléments d'un tableau, il est possible de le faire via l'opérateur `$pull` ou `$pop` de la sorte: 

```js
// On va retirer, dans les documents et dans leurs champ ingrédients, les éléments correspondant à de la farine
db.recipes.updateOne({ name: "Tarte" }, { $pull: { ingredients: { title: "flour" } } })

// On supprime le premier élément du tableau
db.recipes.updateOne({ name: "Tarte" }, { $pop: { ingredients: 1 } })

// On supprime le dernier élément du tableau
db.recipes.updateOne({ name: "Tarte" }, { $pop: { ingredients: -1 } })

```

---

### Delete - Supprimer nos documents

La suppression des documents dans le cadre de MongoDB est assez simple à comprendre et peut se résumer rapidement. Par exemple, pour supprimer un document d'une collection, on va utiliser la fonction ci-dessous: 

```js
db.ingredients.deleteOne({ title: "Tomatoe" })
```

Si l'on souhaite supprimer tous les documents d'une collection, il est possible de le faire de plusieurs façon, la première étant d'utiliser `deleteMany()` avec un filtre vide. L'autre solution est d'utiliser la suppression de la collection via `drop()`:

```js
db.collectionName.deleteMany({})

db.collectionName.drop()
```

Si l'on veut désormais supprimer la base de donnée en soit, on peut utiliser la commande ci-dessous: 

```js
db.dropDatabase()
```

---

[Retour](../README.md)