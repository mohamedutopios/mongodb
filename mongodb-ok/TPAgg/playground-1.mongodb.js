// Demo pour un oneToOne :

use("oneTo")
//db.address.drop()
//db.users.drop()
//db.createCollection("users")
//db.createCollection("address")
//db.users.insertOne({name:"Jean", age : 40})
//db.address.insertOne({street : "rue des fleurs", number : 46, city : "Croix", user_id : ObjectId("65a6e813ed066bd4908bdd92")})
//db.address.find();
//db.users.find();
//db.users.aggregate({$lookup:{from : "address", localField : "_id", foreignField : "user_id",as: "address"}},{$project: {"address.user_id":0}}) 
//db.users.insertOne({name:"Pierre", age : 34})
//db.address.insertOne({street : "rue de la lys", number : 89, city : "Roubaix", user_id : ObjectId("65a6e92d19092bb0a8de32a3")})
db.users.aggregate({$lookup:{from : "address", localField : "_id", foreignField : "user_id",as: "address"}},{$match : {_id : ObjectId("65a6e92d19092bb0a8de32a3")}},{$project: {"address.user_id":0}})


//use("manyTo")
// Demo pour un one ton many :
// use oneToMany
// db.createCollection("authors")
// db.createCollection("books")
// db.books.insertOne({name:"La nuit c'est beau"})
// db.books.insertOne({name:"Le jour c'est vraiment cool"})
// db.authors.insertOne({name : "Corentin", books : [ObjectId("637e7692251d499fa4a82b0c"), ObjectId("637e76a4251d499fa4a82b0d")]})
// db.authors.aggregate({$lookup : {from : "books", localField : "books", foreignField : "_id", as: "books"}})


// Demo pour un many to many :
//use("many")
// use manyToMany
// db.createCollection("orders")
// db.createCollection("products")
// db.products.insertMany([{name : "Clavier", orders : []},{name : "souris",orders : []}])
// db.orders.insertMany([{company : "Apple", products : []},{compagny : "Sony", products : []}])
// db.orders.updateOne({_id : ObjectId("637e865a251d499fa4a82b11")}, {$push : {products : ObjectId("637e85df251d499fa4a82b0f")}})
// db.orders.updateOne({_id : ObjectId("637e865a251d499fa4a82b11")}, {$push : {products : ObjectId("637e85df251d499fa4a82b10")}})
// db.orders.updateOne({_id : ObjectId("637e865a251d499fa4a82b12")}, {$push : {products : ObjectId("637e85df251d499fa4a82b10")}})
// db.orders.updateOne({_id : ObjectId("637e865a251d499fa4a82b12")}, {$push : {products : ObjectId("637e85df251d499fa4a82b0f")}})
// db.products.update({_id : ObjectId("637e85df251d499fa4a82b0f")},{$push :{orders : ObjectId("637e865a251d499fa4a82b12")}})
// db.products.update({_id : ObjectId("637e85df251d499fa4a82b0f")},{$push :{orders : ObjectId("637e865a251d499fa4a82b11")}})
// db.products.update({_id : ObjectId("637e85df251d499fa4a82b10")},{$push :{orders : ObjectId("637e865a251d499fa4a82b12")} })
// db.products.update({_id : ObjectId("637e85df251d499fa4a82b10")},{$push :{orders : ObjectId("637e865a251d499fa4a82b11")} })
// db.products.aggregate({$lookup : {from: "orders",localField : "orders", foreignField : "_id", as: "orders"}})
