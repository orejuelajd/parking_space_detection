/* mongoose libreria para conexion entre mongoDB y Nodejs */

const mongoose = require('mongoose');

/* creo una funcion para establecer la conexion con db */

const dbConnection = async() => {

    try {

        await mongoose.connect(process.env.DB, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
            useCreateIndex: true,
            useFindAndModify: false

        });

        console.log('Base de datos ready');
    } catch (error) {
        console.log(error);
        throw new Error('Error de inicio en base de datos');
    }
}

module.exports = {
    dbConnection
}