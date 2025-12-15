use("restau");
//db.createCollection("restaurant");

//db.restaurant.find().limit(10);

//db.restaurant.find({outcode: "W6"})
//db.restaurant.find({postcode:{$exists: false}});
//db.restaurant.find({postcode: {$not :{$eq: "8NX" }}})

//db.restaurant.aggregate([{$match: {"rating": 5}}]);

//db.restaurant.aggregate({$match : {rating : 5}},{$count:"comptage"});

//db.restaurant.aggregate({$match : {rating : 5}},{$project:{URL : 1, name: 1}})

//db.restaurant.aggregate([{$group: {_id: "$type_of_food", count: {$sum: 1}}}])

//db.restaurant.aggregate([{$group: {_id: "$type_of_food", count: {$sum: 1}}},{$match:{count:{$gt:10}}}])

//db.restaurant.aggregate([{$group: {_id: "$type_of_food", count: {$sum: 1}}}, {$match: {count: {$gt: 10}}},{$sort: {count: -1}}]);

// Nombre de restaurants dans chaque code postal :
//db.restaurant.aggregate([{$group: {_id: "$postcode", nombre_de_restaurants: {$sum: 1}}}]);

// Liste des restaurants de type 'Thai' avec une note supérieure à 4 :
//db.restaurant.aggregate([{$match: {type_of_food: "Thai", rating: {$gt: 4}}}]);

//db.restaurant.aggregate([{$match : {rating : 6}}, {$project : {_id : 0, name : 1, type_of_food : 1, rating : 1}}, {$limit : 3}])

//db.restaurant.aggregate([{$match : {type_of_food : "Caribbean"}}, {$count : "no_of_restaurants_with_caribbean_food"}])

// Moyenne des notes par type de nourriture :
//db.restaurant.aggregate([{$group: {_id: "$type_of_food", note_moyenne: {$avg: "$rating"}}}]);


//db.restaurant.aggregate([{$match : {rating : {$ne : "Not yet rated"}}}, {$group : {_id : "$type_of_food", total_rating : {$sum : "$rating"} , avg_rating : {$avg : "$rating"}, max_rating : {$max : "$rating"},min_rating : {$min : "$rating"}}}])