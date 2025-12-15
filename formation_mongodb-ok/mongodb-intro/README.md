# Introduction à MongoDB

### Qu'est-ce que MongoDB ?

**MongoDB** est un système de gestion de données. La compagnie qui a créé ce système se nomme également MongoDB, ce qui peut causer une certaine confusion. Dans les deux cas, via l'utilisation de MongoDB, il est possible, contrairement à **MySQL** et les autres systèmes de données séquentielles, de gérer des informations sans utiliser de tables. 

Les données, au sein d'un système de données non séquentielles, se trouvent gérées via des ensembles de types **Database**, **Collections**, **Documents**, etc... Contrairement à l'univers des tables, ici, il est possible de gérer des valeurs dans une même collections mais ayant une structure complètement différentes au besoin (avec des informations en plus ou en moins pour certaines entitées). Pour stocker les documents, c'est à dire les entitées, ces dernières sont stockées sous la forme d'un BSON (équivalent du JSON classique) avec des ensembles de **clés** et de **valeurs**.

---
  
### Le format BSON

Ainsi, une entité pourrait se présenter de la sorte: 

```json
{
  "name": "Bernie",
  "breed": "German Shepard",
  "age": 4,
  "owner": {
    "firstname": "John",
    "lastname": "DOE",
    "hobbies": [
      { "name": "Tennis" },
      { "name": "Swimming" },
    ]
  }
}
```
De la sorte, il n'est pas nécessaire, dans l'univers d'un système MongoDB, d'utiliser des jointures pour obtenir les informations liées à une entité. Il suffit d'étendre son shéma en ajoutant une propriété alimentée par des sous-objets telles qu'ici la propriété `owner` ou `hoobies`. On peut également, de la sorte, récolter les informations au format qui nous convient.

Pour conserver une certaine rigueur dans les entitées de données que l'on conserve dans une collection en particulier, il convient donc au développeur de faire plus attention à la structure des données qui se voient ajoutées.

---

### Installer MongoDB

 - Sur la machine : https://www.mongodb.com/try/download/community-edition (Intégrer Compass)
 - Avec Docker, on peut utiliser docker-compose.

---

### Installer MongoDB Shell

 - Avec Tools : https://www.mongodb.com/try/download/shell
 - Accéssible aussi au travers de Compass

---

### Installer mongoimport

 - https://www.mongodb.com/try/download/database-tools

---

### Les lignes de commande

Dans l'univers de MongoSH (Mongo Shell), il est utile de connaitre les commandes de base pour la manipulation des entités et de notre base de données. Par défaut, trois bases de données sont présentes sur le serveur. Pour pouvoir les visionner, il est possible d'utiliser la commande: 

```bash
show dbs
```

Dans le but de nous connecter à une Database, il est possible de le faire via une commande:

```bash
use nom-database
```

Si la base de données n'est pas pré-éxistante, alors elle sera créée sur le moment, et les commandes suivantes partirons du principe que l'on travaille avec cette dernière. 

Dans le but de créer une collection, c'est à dire un ensemble d'entités de données, on peut utiliser la commande suivante, qui a de base pour vocation d'insérer un élément dans la collection, mais causera la création de cette dernière si elle n'existe pas en amont: 

```bash
db.products.insertOne({ name: "Book", price: 12.89 })
```

Pour vérifier ensuite la présence du nouvel élément dans notre collection, il suffit d'utiliser une commande, qui, sans paramètre, va nous amener tous les éléments présents dans la collection: 

```bash
db.products.find()
```

Via cette commande, on aura un affichage de la sorte: 

```bash
[
  {
    _id: ObjectId("645b8ac15e79403ae2823f60"),
    name: 'Book',
    price: 12.89
  }
]
```

On remarque que MongoDB aura automatiquement alimenté une clé unique pour notre élément, de sorte à permettre sa récupération de façon unique, il s'agit de sa **clé primaire**. Cette clé est encodée via un format particulier, qui se trouve être un `ObjectId` et porte comme nom de propriété `_id`. Ces paramètres sont essentiels à connaître lorsque l'on veut travailler avec MongoDB.

---

### Les drivers

Bien entendu, la plupart du temps, nous n'allons pas manipuler des données de la sorte, et notre base de données servira simplement de support de stockage pour une application réalisée dans un langage de programmation particulier. Pour fonctionner, notre code aura besoin d'un moyen d'intéragir avec la base de donnée. Ce moyen se trouve être ce que l'on appelle un **driver**. Un driver servira de lien entre notre code réalisée par exemple en Java et le code d'instruction compatible avec MongoDB. Il se chargera de transformer nos instructions en des requêtes dans le but de nous faciliter le travail.

Pour plonger un peu plus dans la théorie, une application va posséder généralement deux couches majeures qui sont la couche **Frontend** et la couche **Backend**. La seconde couche va pouvoir, via les **drivers**, intéragir avec le **serveur MongoDB**. Le serveur MongoDB va de son côté communiquer avec un moteur de stockage (Généralement `WiredTiger`), qui va de son côté manipuler les données stockées sur le serveur. Le fonctionnement du moteur est à la fois en partie en RAM, et en stockage dur. Les requêtes vont atteindre dans un premier temps une sorte de cache (qui concerne les données en court de traitement) et les manipulations seront par la suite fixées dans les fichiers après coup.

---

[Retour](../README.md)