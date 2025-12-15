use("demo");
// //db.products.insertOne({
//     id: 1,
//     name: "Smartphone Alpha",
//     description: "Smartphone haut de gamme avec écran OLED 6.1 pouces",
//     price: 799.99,
//     category: "Electronics",
//     available: true
// });
db.products.find();

// Opération de création : 

// insertMany : 
// db.products.insertMany([
//     {
//         id: 2,
//         name: "Montre Connectée Solar",
//         description: "Montre connectée avec suivi d'activité et panneau solaire",
//         price: 199.99,
//         category: "Wearables",
//         available: true
//     },
//     {
//         id: 3,
//         name: "Casque Audio Pro",
//         description: "Casque audio sans fil avec réduction de bruit",
//         price: 299.99,
//         category: "Audio",
//         available: false
//     },
//     {
//         id: 4,
//         name: "Tablette Pro 12",
//         description: "Tablette 12 pouces avec stylet et clavier détachable",
//         price: 899.99,
//         category: "Computers",
//         available: true
//     }
// ]);


// Avec moins de champs : 
db.products.insertOne({
    id: 5,
    name: "Caméra de Sécurité Home",
    price: 99.99,
    category: "Home Security"
});


// Avec plus de champs : 

db.products.insertOne({
    id: 8,
    name: "Lampe de Bureau Lumo",
    description: "Lampe de bureau LED avec réglage d'intensité",
    price: 45.99,
    category: "Office Supplies",
    available: true,
    color: "White",
    warrantyYears: 2
});

// Avec un date : 

db.products.insertOne({
    id: 9,
    name: "Sac à Dos Voyage Pro",
    description: "Sac à dos de voyage robuste avec compartiments multiples",
    price: 74.99,
    category: "Travel",
    available: true,
    releaseDate: new Date("2024-01-01")
});

// Avec un tableau :

db.products.insertOne({
    id: 10,
    name: "Drone Explorer Air",
    description: "Drone avec caméra 4K et fonctionnalités avancées",
    price: 1199.99,
    category: "Electronics",
    available: false,
    tags: ["drone", "4K", "high-tech"]
});

// Avec tableau d'objet :

db.products.insertOne({
    id: 11,
    name: "Cafetière Expresso QuickBrew",
    description: "Cafetière expresso automatique avec options de personnalisation",
    price: 249.99,
    category: "Kitchen Appliances",
    available: true,
    comments: [
        { user: "Alice", comment: "Excellente cafetière, très rapide." },
        { user: "Bob", comment: "Facile à utiliser et à nettoyer." }
    ]
});

