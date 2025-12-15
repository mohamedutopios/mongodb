# La modélisation des données

### Qu'est-ce qu'un schéma de données ?

Quand bien même MongoDB ne nous force pas à utiliser des structure précises pour nos données, il peut être intéressant d'en respecter une pour avoir une certaine cohérence dans notre collection et éviter ainsi que chaque document soit complètement différent l'un de l'autre, empêchant une projecton efficace. 

La structure d'un document, ses attributs, leurs types et leur nom se trouve être nommé le **schéma**. Ce schéma a pour but d'être partagé pour informer les utilisateurs de notre BdD des entités qu'il est possible d'y trouver. D'un côté, on peut avoir une approche chaotique de nos collection, de l'autre, une approche de type SQL. 

Bien entendu, la bonne solution est celle qui convient le mieux à nos besoins, mais bien souvent, il se trouve qu'elle se trouve à mi-chemin entre les deux ou du côté du respect d'un shéma de structure. Pour respecter la structure mais ne pas entrer de données pour certains champs, il est possible de mettre leur valeur à `null`. De la sorte, on a une structure de notre schéma de type SQL. Dans l'idéal, on peut également simplement ommettre le champs, et on a alors un schéma flexible à la MongoDB.

---

### Les types de données

Il est important de connaître les types de données que l'on peut placer dans un document pour avoir un contrôle des plus précis sur la structure de nos éléments. Dans la majorité des cas, on utilise ces types de données:
* `Textuel`: Les données de type texte se voient avoir une valeur entourée de doubles guillemets.
* `Nombre`: Les données de type nombre se voient être écrites telles qu'elles, avec la virgule à l'anglaise via le point. Les valeurs numériques peuvent être des Integer (Int32), des NumberLong (Int64), des Float ou des NumberDecimal. Dans MongoSH, les valeurs de voient être traitées comme des Float de par le fait que le shell est basé sur le Javascript et que ce langage ne fait pas de différence entre les types numériques.
* `Booléen`: Les données de type vrai / faux se voient avoir comme valeur `false` ou `true`.
* `Clé primaire`: Les données de la clé primaire sont encodée d'une certaine façon dans MongoDB qui utilise un système de tri basé sur la date d'ajout via l'objet `ObjectId`
* `Date`: Les données de temporalité peuvent être stockées sous la forme d'un `ISODate()` ou d'un `Timestamp()` dans l'objectif d'avoir un temps en millisecondes adjoint d'une valeur ordinale.
* `Documents enfants`: Les documents peuvent contenir d'autres documents en valeur d'un de leurs champs.
* `Tableaux`: Les documents peuvent contenir une série de valeur en valeur d'un de leurs champs.

Il est possible d'analyser notre base de données et ses informations via la commande:

```js
db.stats()
```

On peut aini apprécier la taille qu'occupe nos éléments dans la base de donnée, en particulier via l'attribut `avgObjSize`. Si l'on veut réduire un peu cette valeur, il convient de forcer le type de stockage de nos valeurs, comme par exemple les valeurs numérique. Par exemple, pour forcer le stockage d'un chiffre en tant qu'Integer, on peut se servir du constructeur `NumberInt()`:

```js
db.collection.insertOne({ stock: NumberInt(150) })
```

Pour connaître le type d'un attribut en particulier, il est possible d'utiliser `typeof` de la sorte: 

```js
typeof db.collection.findOne().attributeName
```
---

### Réaliser une structuration de nos données

Si l'on se sert d'un schéma et de types de données, il est important de bien structurer nos données. Pour cela, il est important de se poser les bonnes questions lors de la planification de notre base de donnéeS. Par exemple, ces questions peuvent nous guider dans cette planification: 
* **Quelles seront les données dont notre application aura besoin ?**: Dans le but de définir les champs dont nous avons besoin et quels seront les rapports entre ces champs
* **Où est-ce que ces données seront nécessaire ?**: Pour définir les collections et les groupements d'entités nécessaire à notre besoin.
* **Quel genre de données j'aurai besoin d'y afficher ?**: Pour définir les requêtes dont nous aurons besoin.
* **A quelle fréquence aura-t-on besoin de ces données ?**: Pour définir le niveau d'optimisation de ces entités dans un but de récolte fréquente ou non.
* **A quelle fréquence aura-t-on besoin  modifier de ces données ?**: Pour définir le niveau d'optimisation de ces entités dans un but d'écriture fréquente ou non.

---

### Les relations via les options

Si l'on a plusieurs collections liées entre elles, il est parfois nécessaire de réfléchir au stockage des liaisons. Si l'on le veut, on peut utiliser des **documents enfants** ou des **référencements de valeurs**. La différence entre ces deux méthodes va vanir de la capacité ou non des éléments autres à notre collection de récupérer la référence. Si cette référence n'a lieu que dans cette collection et dans un seul document alors il n'est pas nécessaire de procéder à la méthode usant des références. Si au contraire plusieurs documents peuvent être liées au même autre document, alors le référencement est préférable dans le cas où l'on souhaite minimiser la place que prendre notre collection et ainsi éviter les soucis d'édition de la référence.

- Dans le cas d'une relation de type **One to One** ou **One to Many**, on peut optimiser la chose via un document enfant dans l'élément que l'on souhaite lier. De la sorte, il n'est pas nécessaire, pour chaque élément d'une collection, d'aller rechercher une jointure à la volée durant la requête, ce qui aurait un coût certain niveau performances pour la requête finale.
- Dans le cas d'une relation de type **Many to One**, ou **Many to Many**, l'utilisation d'une référence permet d'éviter qu'en cas de modification de l'élément lié, tous les éléments qui y sont liés se trouvent obligés de devoir modifier des champs. Pour la réaliser, il suffit d'avoir un champs dans notre document dont la valeur serait la clé de notre document référencé.

Dans le monde de MongoDB, ces choix sont cependant laissés au développeur et dépendent majoritairement du type et de la taille des données que l'on va liéer. C'est en partie important dans le cas où l'on utilise des listes de valeurs enfants très longues ou si les objets enfant sont très détaillées. En effet, on peut facilement atteindre dans ce genre de cas la taille d'un document de plus de 16MB, ce qui est la limite permise par MongoDB. Dans ce genre de cas, la structure des données sera à revoir dans le but d'atteindre notre objectif.

---

### $lookup

Si l'on veut rassembler nos éléments lors d'une requête sans avoir à faire plusieurs requêtes et stocker les valeurs récupérées par la référence entre temps, alors il est possible d'utiliser l'opérateur `$lookup` dont l'utilisation passe par une fonction aggrégation. Sa syntaxe se présenterait de la sorte: 

```js
db.collectionA.aggregate([
  {
    $lookup: {
      from: "collectionB", // Le nom de la collection à lier
      localField: "fieldName", // Le nom de l'attribut dans notre collection de base contenant les références
      foreignField: "_id", // Le nom du champs dans la collection externe qui est référencé
      as: "newAliasName", // Un nom de champs qui servira à stocker les références
    }
  }
])
```

---

### La validation de nos données

Il est possible d'avoir une validation de nos schémas dans l'univers de MongoDB. Par exemple, si l'on veut forcer le respect de certaines contraites sur un champs ou sur un document, il est possible d'avoir ces validations dans l'univers de MongoDB, quand bien même de base il n'y en a aucune de part la forte liberté laissée par le système de base de données. 

Il est possible de définir les règles en gérant le niveau de validation, par exemple en empêchant les ajout ou les modifications, en permettant les modifications de documents préalablement ajouté correctement, etc... La validation peut également provoquer des actions spécifiques en cas d'echec ou de réussite. 

L'ajout d'une validation est faisable quand on ajoute une collection. Pour cela, il est possible de le faire dans le cadre d'une création explicite en usant de `db.createCollection(name, options)`et non via l'ajout d'un document dans une collection non existante (création implicite). Les validations se trouveront dans un attribut `validator` et les actions à effectuer suite à celle-ci dans un attribut `validationAction`. 

```js
db.createCollection("collectionName", { 
  validator: {
    $jsonSchema: {
      bsonType: "object", // Tout sera traité comme un objet
      required: [ // Les noms de champs qu'il faudra alimenter dans une requête d'ajout
        "fieldNameA",
        "fieldNameB",
        "fieldNameC",
      ],
      properties: { // Pour ajouter des détails sur le type des attributs
        fieldNameA: {
          bsonType: "array"; // string, objectId, array, etc...
          description: "Description of the field",
          items: { // Pour définir la structure des éléments d'un array
            bsonType: "object",
            properties: {
              ...
            }
          }
        }
      }
    }
  },
  validationAction: 'error' // error | warn  | ...
})
```

Si l'on veut par exemple altérer notre collection pour modifier nos validations, il va falloir exécuter une commande via `db.runCommand()`. Cette commande prend en paramètre un objet avec ici comme attribut `collMod` pour informer que l'on veut modifier la collection: 

```js
db.runCommand({ collMod: "collectionName", validator: { ... }, validationAction: "Value" })
```

---

[Retour](../README.md)