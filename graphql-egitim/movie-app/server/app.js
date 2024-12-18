const express = require('express');
const cors = require('cors');
const { graphqlHTTP } = require('express-graphql');

const schema = require('./schema/schema');
const { graphql } = require('graphql');
const app = express();

// dotenv
require('dotenv').config()

// db
const db = require('./helpers/db.js')();
app.use(cors());
app.use('/graphql', graphqlHTTP({

    schema,
    graphiql: true
}));
app.listen(5050, () => {
    console.log('server is running...');
});