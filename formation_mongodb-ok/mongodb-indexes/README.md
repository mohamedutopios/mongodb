# Les Index dans MongDB

### A quoi ça sert ? 

Dans l'univers de la manipulation de données, l'indexage est une méthode permettant de retrouver nos informations à une vitesse supérieure. Dans l'univers des base de données, il est possible d'indéxer les attributs d'un document pour permettre à la requête de travailler via une méthodologie différente qui a pour but d'accélerer le retour via une recherche dans une liste des champs qui sont indéxés. Ainsi, si l'on indexe les prenoms des documents de personnes, la base de données gardera dans un espace de stockage particulier les prénoms sous la forme d'une liste des prénoms triés de la bonne façon pour ensuite récupérer les éléments qui y sont liés (l'ensemble du document).

Attention cependant, l'indéxage à outrance n'est pas forcément une bonne solution, de part la nécessité de mettre à jour les listes d'index à chaque entrée nouvelle dans la collection. Il est donc important de trouver le bon équilibre pour permettre des performances améliorées à la fois en ajout et en récupération des données.


Il est également intéressant de noter que l'utilisation d'un index peut s'avérer utile dans le cadre de la récupération de millions de données triées. De par la fait qu'un index est de base trié, alors MongoDB n'aura pas besoin de placer toutes les données en mémoire avant le tri, ce qui pourrait être trop demandé pour le paramètre par défaut dû à la limite de documents potentiels en mémoire.

---

### Ajouter un index

Pour créer et afixer un index sur une collection, il faut déjà choisir quel champ va être indéxé (le champ du document se verra mit dans une liste ordonnée ne contenant que le champ choisi pour tous les documents de la collection). Une fois fait, il nous faudra le paramétrer via la commande ci-dessous: 

```js
db.collectionName.createIndex({ fieldName: 1 }) // Si la valeur est négative ( -1 ) alors la liste générée le sera via un tri descendant
```

Si l'on utilise la méthodologie d'explication, on observe qu'en cas de requêtage avec un index, la requête se fait via deux stages, le premier étant la récupération dans la liste de l'index visée et l'autre de son utilisation pour atteindre directement l'élément trouvé.

Dans le cas où l'on souhaiterai retirer l'indexage, il est également possible de le faire via la commande suivante: 

```js
db.collectionName.dropIndex("embedded.fieldName") // Par le nom
db.collectionName.dropIndex({ "embedded.fieldName": 1 }) // Par la description
```

Si l'on le veut, il est aussi possible de visionner les indexages disponibles sur une collection via la méthode ci-dessous: 

```js
db.collection.getIndexes()
```

---

### Index lié

Il est également possible, dans le monde de MongoDB, de créer des index composés se basant sur plusieurs champs triés d'une certaine façon. Un index de ce genre va pouvoir être utilisé soit pour chercher rapidement dans le premier champs demande, soit dans les deux d'un coup, mais pas dans le deuxième uniquement. Pour pouvoir se servir d'une recherche par index dans le second champs, il faudra créer un autre index. Pour créer un index lié de ce type, il faut se servir de la syntaxe suivante:

```js
db.collectionName.createIndex({fieldNameA: 1, fieldNameB: -1})
```

---

### Unicité

Il est possible d'utiliser des index de type unique dans le but d'éviter les duplicats de données, comme par exemple dans le cadre d'un email. Pour pouvoir nous servir de ce type d'index, il nous faut procéder par ajout d'un argument supplémentaire dans le cadre de l création d'un index: 

```js
db.collection.createIndex({ field: 1 }, { unique: true })
```

En cas de duplicat lors de l'ajout de cet index, le système va nous avertir via une erreur qu'il n'est pas possible de placer cette contraire car les données ne le permettent pas. De même, par la suite, lors d'un ajout, le contrôle via cet index pourrait empêcher l'insertion.
---

### Filtres partiels

Il est également intéressant d'utiliser ce que l'on appelle des filtres partiels. Les filtres de ce type vont permettre la création d'un index pour une partie de nos éléments pour les documents de sorte à éviter l'indexage d'éléments n'étant pas essentiels lors des requêtes. 

```js
db.collection.createIndex( { field: 1 }, { partialFilterExpression: { "embadded.field": "value", field: { $gte: 60 } } })
```

Dans le cadre d'un requête, ce genre d'index ne sera utilisé par MongoDB uniquement en cas de recherche d'éléments respectant le filtre que l'on a utilisé. Contrairement à notre index composé, seule l'une des clé sera stockée, de sorte à éviter l'impact en cas d'écriture, contrairement à la méthodologie de l'index lié.

Dans le cadre d'un index d'unicité, il est intéressant de savoir que le système de MongoDB va traiter la présence d'une valeur nulle comme étant une valeur particulière. Celle-ci se verrait alors être unique. 

Pour éviter ceci, il est possible d'utiliser un filtre partiel de sorte à ce que cette unicité d'indexage ne se fasse que sur une potion des éléments, celle-ci étant les documents présentant une valeur pour leur champ.

```js
db.collection.createIndex({ email: 1 }, { unique: true, partialFilterExpression: { email: { $exists: true } } })
```

---

### Time-to-Live indexes

Dans le cadre où l'on aurait des données qui aurait pour objectif d'être auto-détruites, comme par exemple une session utilisation ayant un delais d'expiration, alors il peut être intéressant d'utiliser un autre type d'index, les index possédant un temps de vie, qui n'est possible que sur les valeurs de type date.

```js
db.collection.createIndex({ createAt: 1}, { expireAfterSeconds: 60 })
```

Une fois ce genre d'indexage ajouté, alors notre document va être supprimé une fois le temps voulu expiré. Ce genre d'indexage n'est pas possible sur les données liées.

---

### Le Monitoring des requêtes

Si l'on veut, dans un soucis de monitoring, il est possible de voir la façon dont MongoDB fonctionne lors de notre requête via la méthode `explain()` que l'on peut attacher à notre requête: 

```js
db.collection.explain().find() // Fonctionne également pour les requêtes de type Update ou Delete

db.collection.explain("executionStats").find() // Si l'on veut voir les statistiques de notre requête
```

De la sorte, il est possible de suivre la méthodologie de récupération du système de base de donnée, et ainsi de voir de comment il s'organise en cas de présence / absence d'un index sur le filtre de notre requête. 

Plusieurs valeurs sont possible pour la méthode d'explication, dont:
* `queryPlanner`: Donne un résumé de la requête exécutée et du résultat (wining plan)
* `executionStats`: Donne un résumé détaillé de la requête exécutée, du résultat et potentiellement des rejets
* `allPlansExecution`: Donne un résumé détaillé de la requête exécutée, du résultat et des décision prises durant le processus

La plupart du temps, les résultats à analyser lors du monitoring est le **temps** pris pour l'exécution, le **nombre de clés examinées**, de **documents examinées** et enfin de **documents retournés**.

---

### Le Wining Plan

Le rejet des plans se passe dans l'univers de MongoDB lors de certaines requêtes. Imaginons maintenant une collection d'éléments de type personnes dont les champs âge et nom ont été indéxés via un index imbriqué.Dans le cadre de la recherche de personnes ayant un certain nom et un certain âge, l'index imbriqué sera utilisé en lieu et place d'un index basé uniquement sur les noms. MongoDB se base sur une approche basée sur l'indexage le plus proche possible de l'objectif de notre requête. C'est ce qu'il appelle le **Wining Plan**. 

En se basant sur ce principe, il va faire en sorte de comparer les résultats potentiels des deux approches, et va se baser sur celle qui a le meilleur score de performances pour réaliser la requête finale. Ce mécanisme passe par le caching et sera utilisé en cas de demande d'un utilisateur correspondant au wining plan rejeté dans le cadre de la premiere requête. Le caching se voit être automatiquement vidé au bout d'un certain nombre d'insertions en cas de reconstruction de l'index, d'ajout d'autres indexs ou lors de la relance du serveur MongoDB.

---

### L'index multi-clés

Dans le cas de l'indexage d'éléments de type Array, il est nécessaire à MongoDb de se servir du mécanisme de l'indexage multi-clés. Ils serront plus grands que les indexs de base de par le besoin de stocker dans la liste des éléments de l'index plusieurs sous-éléments d'un coup. Il est important de se demander s'il est bon de s'en servir, mais bien souvent la réponse dépend simplement de nos habitudes de requêtage. 

Si l'on veut d'un autre côté travailler dans le cadre de documents imbriqués, alors il est possible de nous servir d'un index multi-clés dans le cas où l'on se sert d'un indexage basé sur les champs imbriqués de documents se plaçant dans un tableau de documents imbriqués, et non si l'on veut indéxer le tableau en soit.

Il existe une restiction dans le cadre des indexs multi-clés, qui se trouve être l'incompatibilité de ce type d'indexage avec les index imbriqués. Ceci est impossible de par la taille grandissante non maitrisable par MongoDB. Chaque document pourrait en effet avoir dans ses champs de type tableau une série d'élément plus ou moins grand, et la taille de l'indexage pourrait s'en voir être exponetiellement grandissante.

---

### Les indexs textuels

Dans le cas où l'on aurait besoin d'indéxer des phrases, alors il est possible, dans l'univers MongoDB, de gérer ces champs sous la forme de tableaux de mots qui se verront être indéxés. De la sorte, il sera ensuite possible de faire une recherche accelerée non pas sur la présence ou non d'une phrase en valeur d'un document mais de mots présents dans le champs d'un document. Pour créer ce genre d'index, la syntaxe est la suivante:

```js
db.collection.createIndex({ field: "text" })
```

La recherche dans le cadre d'un `find()`passera par une requête de ce type:

```js
db.collection.find({ $text: {$search: "wordA wordB"}})
```

La chaine envoyée en paramètre sera ensuite traitée comme plusieurs mots ne devant pas forcément suivre l'ordre précis des paramètres. De plus, si l'on demande en paramètre plusieurs mots, alors de base les éléments possédant ne serait-ce qu'une partie des mots recherchés seront inclus dans les résultats et il n'y aura pas forcément d'ordre de priorité en cas de présence de X mots recherchés dans les résultats proposés. Pour éviter ce soucis, il est possible d'ajouter du paramétrage et d'user du mécanisme de la projection pour observer le scoring des résultats avant de les trier: 

```js
db.collection.find({ $text: {$search: "wordA wordB", $caseSensitivity: true }, { $meta: "textSearch" } }).sort({ score: { $meta: "textScore" } })
```

Si l'on tente de nous servir d'index combinés dans le cadre d'indexs textuels, MongoDB permettra la création de ces indexages qui pourraient être utilisés pour la recherche de mots. Il est également possible de chercher par exclusion de mots. Pour ce faire, la syntaxe utilise le caractère `-` et se présente de la sorte: 

```js
db.collection.find({ $text: {$search: "wordA -wordB"}})
```

Il est également possible d'utiliser des features tels que la langue (dans le but d'optimiser la gestion des coupures entre les mots durant l'indexage) ou le poids des mots recherchés. Ces features sont disponibles lors de la création de notre index, et se présente via la syntaxe ci-dessous: 

```js
db.collection.createIndex({ fieldA: "text", fieldB: "text" }, { default_language: "french", weights: { fieldA: 5, fieldB: 10 } })
```

---

### Ajouter des index en arrière-plan

Si l'on le veut, il est possible de réaliser l'indexage de nos documents en tâche de fond. L'objectif de cette méthodologie d'indexage est déviter le blocage de notre collection durant la création de l'index, qui peut être problématique dans le cas où ceci prendrait un temps important et bloquerait potentiellement nos applications basées sur cette base de données.


Pour ce faire, il suffit, lors de l'ajout d'un index, de procéder de la sorte: 

```js
db.collection.createIndex({ field: 1 }, { background: true })
```

---

[Retour](../README.md)