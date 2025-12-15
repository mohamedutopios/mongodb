use('book');


// ***1*** Create :

//db.books.find();

db.books.find({_id:45});

//db.books.find().limit(5);

// -- Book avec 2 auteurs:
//db.books.find({authors: {$size: 2}});
// db.boooks.countDocuments({ authors: { $size: 2 } })

//db.books.find().forEach(x => print(x._id));

// -- Compte le nombre de livre qui ont plus de 400 pages.
//db.books.find({pageCount: {$gte: 400}}).count();
// db.boooks.find({pageCount: {$gte: 400}}).count();

//db.books.find({_id: {$in:[55,75]}});

// -- Cette commande recherche dans la collection books tous les documents où il y a exactement deux auteurs, et elle les trie par titre dans l'ordre alphabétique. Si plusieurs livres ont le même titre, ils seront ensuite triés par leur ID MongoDB dans l'ordre décroissant. Le résultat de cette commande sera une liste de documents (livres) de la collection books qui correspondent à ces critères.
//db.books.find({authors: {$size: 2}}).sort({title: 1, _id: -1});


// -- Cette commande MongoDB recherche dans la collection books les documents ayant exactement deux auteurs, ignore les deux premiers résultats, puis trie les documents restants par titre dans l'ordre croissant et par ID MongoDB dans l'ordre décroissant.
//db.books.find({authors: {$size: 2}}).skip(2).sort({title: 1, _id: -1});

//-- Cette commande MongoDB recherche dans la collection books les documents dont l'ID est supérieur à 25 et inférieur à 28, en utilisant un filtre AND pour combiner les deux conditions.
//db.books.find({$and: [ {_id: { $gt: 25 }},{_id: { $lt:28 }}]});


// -- Cette commande MongoDB recherche dans la collection books les documents dont l'ID est supérieur à 25 et ne retourne que les champs _id et authors de ces documents.
//db.books.find( {_id: { $gt: 25 }}, {_id: 1, authors:1});

// -- Cette commande MongoDB recherche dans la collection books les documents dont l'ID est supérieur ou égal à 5 et retourne seulement le premier auteur de chaque document trouvé.
//db.books.find({_id: {$lte:5}},{authors: {$slice: 1}},{title:1});

// -- cette requête recherche les livres avec un ID jusqu'à 5 inclus et, pour ces livres, elle retourne leur titre et le premier auteur listé.
//db.books.find({_id: {$lte:5}}, {authors: {$slice: 1}, title:1});

// -- cette commande trouve et supprime le premier livre intitulé "Unlocking Android" dans la collection books, et retourne les détails de ce livre supprimé.
//db.books.findOneAndDelete({title: "Unlocking Android"});

// -- cette commande trouve tous les livres de la collection books ayant plus de 500 pages et renvoie les résultats dans un format lisible et bien structuré.
//db.books.find({pageCount: {$gt: 500}}).pretty();

// -- L'un ou l'autre
//db.books.find({categories: {$in: ['Java', 'Web Development']}});

// -- Tous
//db.books.find({categories: {$all: ['Java', 'Web Development']}});

// OU l'un ou l'autre
//db.books.find({$or: [{_id: 19}, {_id:98745}]});

// -- cette requête recherche dans la collection books tous les documents dont le champ longDescription contient le mot 'Distributed', quelle que soit la casse.
//db.books.find({longDescription: {$regex: 'Distributed', $options: "i"}});

// -- cette requête recherche les documents dans la collection books où le champ longDescription commence par 'ext', sans tenir compte de la casse.
//db.books.find({longDescription: {$regex: '^ext', $options: "i"}});

// -- cette requête recherche dans la collection books tous les documents où le titre se termine par 'Perl', indépendamment de la casse des caractères.
//db.books.find({title: {$regex: 'Perl$', $options: "i"}});

// ***2*** command update 

//db.books.updateOne({_id: 45}, {$set: {status: "CANDELED", pageCount: 250}});

//db.books.updateOne({_id: 45}, {$inc:{ pageCount: 1000}});

// -- Cette commande supprime le champ authors du document dans la collection books où _id est égal à 45.
//db.books.updateOne({_id: 45},{$unset: {authors: []}})

// -- Elle renomme le champ status en position dans le document de la collection demo où _id est égal à 45.
// db.demo.updateOne({_id: 45},{$rename: {status: "position"}})

// -- Met à jour (ou ajoute si non existant) le champ publishedDate avec la valeur "2012-12-01" dans le document de demo avec _id 45.
//db.demo.updateOne({_id: 45}, {$set: {publishedDate: "2012-12-01"}})

// -- Met à jour le titre du document dans books avec _id 55 pour qu'il devienne "Object Oriented Cassandre".
//db.books.updateOne({_id: 55}, {$set: {title: "Object Oriented Cassandre"}});

//db.books.findOne({_id: 55});

// -- Met à jour tous les documents dans la collection books dont les identifiants sont soit 55, soit 75, en définissant leur champ status à "CANCELED".
//db.books.updateMany({_id:{$in:[55,75]}},{$set: {status: "CANCELED"}})

