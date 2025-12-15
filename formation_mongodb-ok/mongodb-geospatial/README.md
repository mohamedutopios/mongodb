# Les données Géospatiales dans MongoDB

### Késako ?

Dans MongoDB, il est possible de réaliser des requêtes sur un emplacement, par exemple trouver toutes les données situées à proximité d'un élément en particulier. Pour fonctionner, les données se verront stockées sous la forme d'un `GeoJSON`, qui est un format respectant les possibilités du JSON pour le stockage de localités. Ce standard n'a pas été invrenté par MongoDB mais est utilisé dans le cadre de ses systèmes avec quelques ajouts. 

Imaginons que l'on veuille travailler via des informations concernant San Francisco, comme par exemple stocker des restaurants qui nous intéressent. Pour cela, il est important de connaître le fonctionnement de la longitude et de la latitude, car ces infos seront utilisées dans le cadre du stockage de nos données.

--- 

### Manipuler les données de localisation

Pour insérer un restaurant dans notre BdD, on devra respecter des noms et une structure de notre champs (ici nommé `location`) de la sorte: 

```js
db.collection.insertOne({ name: "My Restaurant", location: { type: "Point", coordinates: [ 1234, 5678 ] } })
```

Pour par la suite récupérer les informations de notre restaurant, il est possible, dans une requête de type Read:

```js
db.collection.find({ location: { $near: { $geometry: { type: "Point", coordinates: [ 01474, 25589 ] }, $maxDistance: 30, $minDistance: 10 } } })
```

Pour que la requête fonctionne, elle aura besoin que les données géospatialles soient indexées. Pour ajouter un tel index, la méthodologie n'est pas différente des autres types de données:

```js
db.collection.createIndex({ location: "2dsphere" })
```

Via des données de ce type, il est également très simple de récupérer un ensemble d'éléments se trouvant dans une zone précise, en excluant les autres qui pourraient se trouver en dehors de la ville voulu par exemple. Pour ce faire, une requête usant de l'opération `geoWithin` de ce type est possible: 

```js
// Pour le faire via une zone rectangulaire
dc.collection.find({ location: { $geoWithin: { type: "Polygon", coordinates: [ [1456, 2369], [1456, 2369], [1456, 2369], [1456, 2369] ] } } })

// Pour une recherche basée sur une sphère et un rayon
dc.collection.find({ location: { $geoWithin: { $centerSphere: [[12345, 67890], 1 / 482452 ] } } })
```

Si l'on cherche à savoir si oui ou non un élément se situe dans une zone geographique particulière, il est possible de faire usure de l'opérateur `geoIntersects`: 

```js
db.collection.find({ area: { $geoIntersects: { $geometry: { type: "Point", coordinates: [ 1452, 2365 ] } } } })
```

---

[Retour](../README.md)