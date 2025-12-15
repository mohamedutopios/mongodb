use("demo");
db.products.insertOne({name: "koko", price:12});
db.products.find();
db.notes.find().limit(20);
db.demo.insertMany([{_id: 100000, "title":"Livre 2", "pageCount":45, "status":"PUBLISH"},{"title":"livre de moi", "auteur":"marco polo", "status":"PUBLISH"}])
use("eleve");
db.createCollection("notes")
db.notes.insertOne({ "matiere": 45, "date": new Date(2015 - 12 - 25), "present": true });
db.notes.find();

// il faut que tout soit précis.
//db.demo.findOne({title:"Android in Action, Second Edition"});
//db.demo.findOneAndDelete({title:"livre1"});
//db.demo.find().limit(10);

//db.demo.find({ $and: [{ pageCount: { $gte: 100 } }, { pageCount: { $lte: 400 } }] });
//db.demo.find({pageCount:{$eq:416}},{_id:1})._id

