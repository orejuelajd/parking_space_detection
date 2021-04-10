/* MODELO DE LOS DATOS DE LOS PARQUEADEROS */

const { Schema, model } = require('mongoose');

const ParqueaderosSchema = Schema({
    usuario: {

        type: Schema.Types.ObjectId, // esto indica a moogoze que el parqueadero debe pertenecer  aun usuario
        ref: 'Usuario',
        required: true
    },

    nombre: {
        type: String,
        require: true
    },
    ubicacion: {
        type: String,
        require: true

    },
    cantidadParqueaderos: {
        type: Number,
        require: true

    },



});

/* creamos el objeto que contiene los datos del modelo junto con la version y el id */
ParqueaderosSchema.method('toJson', function() {
    const { _v, _id, ...object } = this.toObject();

    object.uid = _id;

    return object;
});

/* exportamos el modelo para crear el parqueadero */

module.exports = model('Parqueadero', ParqueaderosSchema);