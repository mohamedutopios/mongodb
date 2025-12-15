# Aller plus loin avec MongoDB

### La sécurité 

Dans le cas où l'on se retrouve à devoir administrer une base de données, il est essentiel de pouvoir gérer les notions clés que sont l'**authentification** et l'**autorisation** des utilisateurs. De la sorte, il est possible de restreindre des features de nos bases de données en fonction de qui est en train de l'utiliser.

Une autre notion essentielle à connaitre est la capacité de **crypter** les informations stockées dans une base de données, que cela soit lors des envois d'informations ou au sein du système de stockage de la base de données. 

Enfin, il est également bon de connaitre, pour une administration optimale, de permettre l'**audit** de notre base de donnée pour être au courant de ses dernières modifications. Il est aussi bon d'être capable de réaliser des **backups** fréquents de nos donnéesp our éviter les pertes éventuelles de grande ampleur.

---

### Comprendre les rôles

Dans le monde de l'authentification et de l'autorisation des utilisateurs, il est bon de savoir que ce processus passe par l'accès à des rôles pour les utilisateurs enregistrés, et qu'un rôle permet généralement l'accès à un certain nombre de droits. 

Ainsi, une fois l'accès confirmé au moyen de l'authentification, on offre à l'utilisateur ses droits qui seront utilisés par la suite dans le cadre de l'autorisation de ce même utilisateur de manipuler la base de données. 

Dans MongoDB, l'autorisation est essentiellement basée sur l'absence ou la présence de rôle chez l'utilisateur qui lui offrent des privilèges, comme par exemple l'accès à certaines ressources ainsi que les actions qu'il peut faire sur ces ressources. Il est de par ce fait possible de permettre uniquement la récolte des données sur une collection particulière ou de ne permettre d'un autre côté que l'insertion sur une série de collection. 

Pour attribuer des rôles, il faut déjà créer des utilisateurs. Pour cela, il faut utiliser la méthode `createUser()`. Pour par la suite le modifier, la fonction `updateUser()` est également disponible. Leur fonctionnement se présente tel que:

```js
db.createUser({ 
    user:"Username", 
    pwd: "Password",
    roles: [ 
        "userAdminAnyDatabase", // Pour avoir un rôle de superAdmin
        "readWrite", // Pour avoir la capacité de réaliser un CRUD complet
        { role: "readWrite", db: "databaseName" } // Pour spécifier la base de donnée associée à ce rôle, la syntaxe est différente
    ]
})
```

Il est par la suite possible d'éditer l'utilisateur voulu via des commandes telles que: 

```js
db.updateUser({
    user: "Username", 
    roles: [
        "roleA", 
        { role: "roleB", db: "databaseName" }
    ]
})
```

Pour nous connecter, il est ensuite possible d'avoir recourt à:

```js
db.auth("Username", "Password")
```

Enfin, pour nous déconnecter, on peut utiliser: 

```js
db.logout()
```

---

### Gérer l'encryption ( Théorie )

Pour sécuriser désormais les transferts de données entre le serveur et le client, il peut être intéressant d'utiliser le mécanisme des formulaires SSL dans le but d'encrypter de bout en bout la requête HTTP. Pour activer ceci, il est nécessaire d'utiliser une clé publique et une clé privée après avoir installé un binaire dans le but de gérer un serveur SSL sur notre machine.

Dans le cadre de l'encryption de nos données au repos, il faut pour cela généralement utiliser des applicatifs / modules supplémentaires dans le cadre de notre application, comme par exemple Identity dans le monde du .NET ou le package bcryptjs dans l'univers Javascript.

---

### Les transactions

Les transactions sont apparues suite à la mise à jour 4.0 et sont utiles dans le cadre de l'utilisation de multiples instances de MongoDB (dans un environnement Kubernetes par exemple). 

Pour un cas pratique, imaginons que l'on veuille modifier le stock des produits de notre collections de fruits uniquement dans le cas où l'achat de l'utilisateur est concluent. Pour ce faire, il nous faudra généralement deux étapes dans notre application, celle de gestion de l'achat, puis celle de modification des stocks. En cas de non reliement des deux requêtes, il y a possibilité que la seconde requête (celle de modification des stocks) s'effectue alors que celle de confirmation de l'achat échoue (suite à une erreur réseau par exemple). 

Pour éviter ce genre de soucis, nous avons la possibilité d'utiliser le mécanisme des transactions, qui va relier ensemble les deux requêtes et n'appliquer les changements dans la base de donnée qu'en cas de succès des deux requêtes. En cas d'echec de l'une d'entre elle, alors l'état précédent de la base de donnée sera récupéré via un Rollback pour la requête ayant de son côté réussi.

Pour nous en servir, il nous faut utiliser le mécanisme de la session: 

```js
const session = db.getMongo().startSession()

// On débute notre transaction
session.startTransaction()

// On récupère les collections
const productsCollection = session.getDatabase("shop").products
const salesCollection = session.getDatabase("shop").sales

// On effectue nos commandes de CRUD
salesCollection.insertOne( ... )
productsCollection.updateMany( ... )

// En cas de réussite, on peut confirmer les changements
session.commitTransaction()

// En cas d'échec de l'une des requête, on peut annuler les changements
session.abortTransaction()
```

[Retour](../README.md)