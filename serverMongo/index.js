/* cluster compass */
//franciscojpf
//iP9cDRy1KIa5xVjh
// DB=mongodb+srv://franciscopedroza0305:w7ujNw5rjg4CgmK@cluster0.qfzww.mongodb.net/parking
// DB=mongodb://127.0.0.1:27017/parking
/*  ---------------  */

/* importo express */
const express = require('express');

/* import body parser, manejo de informacion */
const bodyParser = require('body-parser');

/* variables de entorno .env*/

require('dotenv').config();

/* para los paths de la peticiones */

const path = require('path');

/* import Cors (permisos) */

const cors = require('cors');


/* importo la base de datos mongo */

const { dbConnection } = require('./database/config');

/* crear el servidor express */
const app = express();

/* say epres we are using EJS template engine */
app.set('view engine', 'ejs')

app.use(cors());

/* para leer los datos  */
app.use(bodyParser.json({ limit: "10mb" }));

/* uso de base de datos */
dbConnection();



/*usar rutas para CRUD */



app.use('/api/parqueaderos', require('./routes/parqueaderos'));

app.use('/api/usuarios', require('./routes/usuarios'));

app.use('/api/rois', require('./routes/rois'));

/* visualizar un front */
// Lo último
/* app.get('*', (req, res) => {
    res.sendFile(path.resolve(__dirname, 'public/index.html'));
}); */

/* const dispo = require('./api/rois/60706f253d7d85482c32fc87'); */


app.get('/api/rois/:60706f423d7d85482c32fc88');



// index page
/* app.get('/', function(req, res) {


    var free = [
        { zona: 'zona 1', number: 0 },
        { zona: 'zona 2', number: 0 },
        { zona: 'zona 3', number: 0 },

    ];


    res.render('pages/index', {
        free: free,

    });
}); */




/* correr el servidor */

app.listen(process.env.PORT, () => {
    console.log('Servidor corriendo en puerto ' + process.env.PORT);
});