# Les fonction d'aggrégation dans MongoDB

### A quoi ça sert ? 

Dans le cadre d'une requête plus complexe, il est parfois nécessaire de pouvoir transformer les données récupérées. Pour ce faire, il faut en général, dans l'univers MongoDB, faire appel à ce que l'on appelle les **fonctions d'aggrégation**. L'aggrégation est en réalité un framework qui fonctionne en surcouche sur les requête que l'on effectue dans notre base de données. Il est possible de nous servir de plusieurs fonctions d'aggrégation que l'on peut enchainer dans le but d'obtenir le résultat escompté. Chaque fonction est ainsi appellée une **étape**, et l'ensemble du processus se trouve être ce que l'on nomme un **pipeline**.

---

### L'opérateur $group

Pour nous servir du framework d'aggerégation, il faut passer non pas par la fonction `find()` mais par `aggregate()` dans laquelle on passera un tableau des différentes fonction d'aggrégation que l'on veut utiliser, dans l'ordre prévu. Ici, nous allons utiliser la capacité du groupement du framework, pour obtenir par exemple le nombre de fruits par marque dans notre magasin, par ordre décroissant:

```js
db.products.aggregate([
    { $match: { category: "fruit" } }, 
    { $group: { _id: { brand: "brand.name" }, totalProducts: { $sum: 1 } } }, 
    { $sort: { totalProducts: -1 } }, 
])
```

Ici, nous utilisons l'opérateur `$group` pour regrouper les entités par champs. Ce regroupement peut ensuite être utilisé pour obtenir des valeurs spécifiques, comme ici la somme des produits, qui est un champ créé à la volée et qui se nommera `totalProducts` et dont la valeur sera le résultat de la somme de chaque produits disponible après le regroupement via l'utilisation de l'opérateur `$sum`. Bien entendu, il est possible d'avoir d'autres calculs, tels que la moyenne avec `$avg` ou la valeur minimale avec `$min`, etc...

---

### L'opérateur $project

A côté de la capacité de grouper les documents, il est aussi possible d'avoir recours à la projection dans le cadre du framework d'aggrégation dans le but de par exemple permettre l'affichage d'un nom complet pour les personnes, ce dernier pouvant également être mit en forme via l'utilisation d'opérateurs supplémentaires pour offrir un affichage plus élégant et un retour plus adapté à nos besoins d'application:

```js
db.people.aggregate([
    { $project: { _id: 0, gender: 1, fullname: { $concat: [ 
        { $toUpper: { $substrCP: [ "$firstname", 0, 1 ] } }, 
        { $toLower: { $substrCP: [ "$firstname", 1, { $substract: [ { $strLenCP: "$firstname" }, 1 ] } ] } } ,
        " " , 
        { $toUpper: "$lastname" } 
    ] } } }, 
])
```

Ici, nous avons besoin de manipuler les données pour les mettre en majuscule ou en minuscule via les opérateurs `$toUpper` et `$toLower`. Dans certains cas, il nous faut également traiter des sous-chaines, obtenues via l'opérateur `$substrCP`. Enfin, pour trouver la taille des chaines à convertir, il faut des fois avoir recours à la taille de la chaine de caractère initiale, obtenue via l'opérateur `$strLenCP`. A la fin, nous obtenons en sortie un nouveau champ, nommé `fullname` et donc la valeur est le résultat de nos nombreuses manipulation des deux champs initiaux `firstname` et `lastname` dans la collection de personnes.

Si l'on travaille avec des données géo-spatialles, il est bien entendu possible de nous servir du framework pour les transformer directement et ainsi apprécier des capacités de MongoDB à transformer les données de ce type. Une fois fait, il serra ainsi possible de potentiellement récupérer les éléments les plus proches les uns des autres:

```js
db.people.aggregate([
    { $project: { _id: 0, name: 1, email: 1, location: { type: "Point", coordinates: [ 
        { $convert: { input: "$address.coordinates.longitude", to: "double", onError: 0, onNull: 0 } }, 
        { $convert: { input: "$address.coordinates.latitude", to: "double", onError: 0, onNull: 0 } } 
        ] } } },
])
```

Pour ce faire, il va nous falloir transformer le type de retour de nos éléments via des opérateurs spécifiques. Par exemple, les coordonnées se voient être transformées en valeurs numériques ci-dessus. L'opérateur `$convert` demandera une **entrée**, un **type de sortie** ainsi que les **valeurs par défaut en cas d'erreur** ou une **valeur par défaut en cas d'entrée nulle**. 

Dans le cas où l'on n'a pas de besoin spécifique pour gérer une sortie en cas d'erreur ou de null, on peut utiliser la syntaxe ci-dessous: 

```js
db.people.aggregate([
    { $project: { _id: 0, name: 1, email: 1, location: { type: "Point", coordinates: [ 
        { $toDouble: "$address.coordinates.longitude" }, 
        { $toDouble: "$address.coordinates.latitude" } 
        ] } } },
])
```

Si l'on travaille avec des valeur de type data, il est également possible d'extraire si l'on le veut les valeurs telles que l'année, le mois, la semaine, etc via des opérateurs de type `$isoYear` tel que:

```js
db.collection.aggregate([
    { $group: { _id: birthDate: { $isoYear: { $isoWeekYear: "$birthDate" } }, numberPersons: { $sum: 1 } } },
    { $sort: { numberPersons: -1 } }
])
```

En résumé, l'opérateur `$group` a pour objectif de transformer une série de document en une entité exploitable par la suite, alors que l'opérateur `$project` a pour vocation de transformer une série de document en une nouvelle série de document avec leurs champs altérés.

---

### Travailler avec les tableaux

Dans le cadre du framework d'aggréagation, beaucoup de fonctionnalités sont possibles dans le cas de l'utilisation de champs de type tableau. Par exemple, imaginons que l'on veut ajouter des éléments à un tableau en se basant sous une série de documents, comme par exemple regrouper dans un tableau tous les loisirs d'une série de personnes:  

```js
db.people.aggregate([
    { $group: { _id: { age: "$age" }, allHobbies: { $push: "$hobbies" } } }
])
```

De la sorte, nous aurons cependant un tableau de tableaux, et non un tableau unique regroupant les différents loisris. Pour parvenir à ceci, il nous faut ajouter une étape supplémentaire dans l'aggrégation. Via l'opérateur `$unwind`, il est possible d'aplatir les données en créant à partir d'un document ayant plusieurs données dans un champ de type tableau, plusieurs documents ayant chacun une donnée dans un champ n'étant plus un tableau. Il ne nous restera plus qu'à éliminer les duplicats via l'utilisation d'autre chose qu'un opérateur `$push`. L'opérateur a utiliser est `$addToSet`:

```js
db.people.aggregate([
    { $unwind: "$hobbies" },
    { $group: { _id: { age: "$age" }, allHobbies: { $addToSet: "$hobbies" } } }
])
```

La projection est également possible dans le cadre des tableaux, avec par exemple l'opérateur `$slice` qui permet de n'obtenir qu'une portion du tableau, allant d'un index de départ à un index de fin. Ainsi, pour n'avoir que le premier élément, on peut utiliser une syntaxe telle que:

```js
db.students.aggregate([
    { $project: { _id: 0, examScore: { $slice: [ "$examScores", 1 ] } } }, // Pour n'avoir que le premier
    { $project: { _id: 0, examScore: { $slice: [ "$examScores", -2 ] } } }, // Pour avoir les deux derniers
    { $project: { _id: 0, examScore: { $slice: [ "$examScores", 3, 1 ] } } } // Pour n'avoir que le troisième
])
```

Si ce que l'on veut désormais est de savoir combien d'éléments sont présent dans un tableau, il est facile de le savoir via l'opérateur `$size` permettant d'obtenir cette valeur: 

```js
db.people.aggregate([
    { $group: { _id: { age: "$age" }, numberOfHobbies: { $size: "hobbies" } } }
])
```

Maintenant, imaginons que l'on veuille ne récupérer qu'une portion d'un tableau lors de la projection, en se basant sur un filtrage. Pour cela, l'opérateur `$filter` existe, et permettra de transformer chaque élément d'un tableau en une variable disponible dans une condition de filtrage via l'utilisation de la syntaxe `$$nomVariable`. Si la variable résultante se trouve être un document, il sera possible d'en chercher le champ voulu via `$$nomVariable.nomChamp`: 

```js
db.students.aggregate([
    { $project: { _id: 0, examScores: { $filter: { input: "$examScores", as: "score", cond: { $gt: [ "$$score", 60 ] } } } } }
])
```

---

### L'opérateur $bucket

L'opérateur `$bucket` de son côté est un opérateur plutôt utile dans le cadre de notre aggrégation, car il permet de regrouper par valeurs connues, par exemple pour créer des sous-groupes de personnes en se basant sur des écart d'âge allant d'une valeur X à Y, alors on peut procéder de la sorte, ceci permettant ensuite via les autres fonctions et opérateurs d'obtenir le nombre d'entités par catégories (avec `$sum`) ainsi que l'âge moyen pour chaque catégorie (`$avg`):

```js
db.collection.aggregate([
    { 
        $bucket: { 
            groupBy: "$dob.age" , 
            boundaries: [ 0, 18, 30, 50, 80, 120 ], 
            ouput: { 
                numPersons: { $sum: 1 },
                averageAge: { $avg: "dob.age" }
            }
        } 
    },
])
```

Il est également possible de laisser le choix à MongoDb de regrouper nos éléments par catégorie via l'utilisation de l'opérateur `$bucketAuto` en lui indiquant quel champ séparé en X groupements tel que:

```js
db.collection.aggregate([
    { 
        $bucketAuto: { 
            groupBy: "$dob.age" , 
            buckets: 5
            ouput: { 
                numPersons: { $sum: 1 },
                minAge: { $min: "dob.age" },
                maxAge: { $max: "dob.age" }
            }
        } 
    },
])
```

---

### Spécificités de l'aggrégation

Dans le cadre de l'utilisation des fonctions d'aggrégation, contrairement à l'utilisation de multiples opérations dans le cadre de la méthode `find()`, il faut ici faire attention à l'ordre des manipulations. Ainsi, pour obtenir les personnes 11e jusqu'à la 20ème dans le cadre de la récupération des hommes les plus vieux, il nous faut procéder dans cet ordre précis pour à la fois optimiser la chose et aussi être sur d'obtenir les valeurs voulues: 

```js
db.people.aggregate([
    { $match: { gender: "male" } },
    { 
        $project: {
            _id: 0,
            name: {
                $concat: [ "$name.firstName", " ", "$name.lastName" ]
            },
            birthDate: {
                $toDate: "$dob.date"
            }
        }
    },
    { $sort: { birthDate: 1 } },
    { $skip: 10 },
    { $limit: 10 }
])
```

Il est également possible par la suite, si l'on le veut, de stocker le résultat d'une aggrégation dans une collection. Pour cela, il suffit de procéder via l'utilisation d'une étape d'aggrégation supplémentaire usant de l'opérateur `$out` tel que: 

```js
db.people.aggregate([
    { 
        $project: {
            _id: 0,
            name: {
                $concat: [ "$name.firstName", " ", "$name.lastName" ]
            },
            birthDate: {
                $toDate: "$dob.date"
            }
        }
    },
    { $sort: { birthDate: 1 } },
    { $limit: 10 },
    { $out: "oldestPersons" }
])
```

Dans la cadre de l'aggrégation avec des données de type localités, il est possible d'utiliser le stage `$geoNear` (qui doit être le premier stage d'un pipeline d'aggrégation). Pour pouvoir filtrer les résultats, il est possible, de par l'impossibilité d'utiliser une étape de type `$match`, de nous servir du champ `query` pour placer une requête qui sera optimisée par MongoDB dans l'objectif de notre pipeline:

```js
db.persons.aggregate([
    {
        $geoNear: {
            near: {
                type: "Point", 
                coordinates: [ -18.4, -42.8 ]
            },
            maxDistance: 100000, // Valeur en mètres
            num: 10, // Pour n'obtenir que les 10 plus proches
            query: {
                age: { $gt: 20 }
            },
            distanceField: "distance"
        }
    }
])
```

---

[Retour](../README.md)