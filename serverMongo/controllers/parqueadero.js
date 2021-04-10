/* de express utilizo response */
const { response } = require('express');

/* importo el modelo */

const Parqueadero = require('../models/parqueaderos');


/* get para parqueaderos */

const getParqueaderos = async(req, res = response) => {

    const parqueaderos = await Parqueadero.find({}, 'nombre ubicacion cantidadParqueaderos');

    res.json({
        ok: true,
        parqueaderos

    });
}

/* crear parqueadero */
const createParqueadero = async(req, res = response) => {

    /* voy a verifica si el parqueadero fue creado ya por tener la misma ubicacion */
    const { ubicacion } = req.body;

    try {
        const existeP = await Parqueadero.findOne({ ubicacion });

        if (existeP) {
            return res.status(400).json({
                ok: false,
                msg: 'Un parqueadero con esa ubicacion ya ha sido registrado'
            });
        }


        /* creo parqueadero */
        const parqueadero = new Parqueadero(req.body);


        /* guardo parqueadero*/
        await parqueadero.save();


        res.json({
            ok: true,
            parqueadero
        })

    } catch (error) {
        console.log(error);
        res.status(500).json({
            ok: false,
            mgs: 'error inesperado, hable con admi'
        });
    }


}


module.exports = {
    getParqueaderos,
    createParqueadero
}