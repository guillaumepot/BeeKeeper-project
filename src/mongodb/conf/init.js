// init.js


db = db.getSiblingDB("data_user_beegis");



// Créer une collection
db.createCollection("locations");
db.createCollection("hives");

// Afficher un message de confirmation
print("Database and initial data have been set up successfully!");