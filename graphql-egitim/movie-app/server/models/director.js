const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const directorSchema = new Schema({
    name: String,
    birth: Number,
});

module.exports = mongoose.model('Director', directorSchema);