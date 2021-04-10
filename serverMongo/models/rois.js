/* MODELO DE LOS DATOS A GUARDAR EN LA DB  */

const { Schema, model } = require('mongoose');

const RoisSchema = Schema({

    parqueadero: {
        type: Schema.Types.ObjectId,
        ref: 'Parqueadero',
        requiered: true
    },

    totalZonas: {
        type: Number,
        require: true
    },

    zonas: {
        type: Array,
        //require: true
    },
    totalPermitidos: {
        type: Array,
        require: true

    }
    /* 
    json_data = {"total_zonas": 2,"zonas": [[[700, 1050], [490, 220], [1450, 1050], [570, 210]],[[1920, 700], [1100, 350], [1920, 440], [1200, 250]]],"total_permitido": 6}
    */



});

/* creamos el objeto que contiene los datos del modelo junto con la version y el id */
RoisSchema.method('toJson', function() {
    const { _v, _id, ...object } = this.toObject();

    object.uid = _id;

    return object;
});

module.exports = model('Rois', RoisSchema);