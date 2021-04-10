/* de express utilizo response */
const { response } = require('express');

/* importo el modelo */

const Rois = require('../models/rois');




const getDatos = async(req, res = response) => {

    /* lo que voy a buscar */
    const busqueda = req.params.busqueda;


    /* envio el id como una busqueda y encuentro los datos de ese parqueadero, con populate los datos del mismo a mi consulta de data */
    const Data = await (await Rois.findOne({ parqueadero: busqueda })).populate('parqueadero', 'nombre ubicacion cantidadParqueaderos');

    /* res.json({
        ok: true,
        Data


    }); */

    var free = [
        { zona: 'zona 1', number: Data.totalPermitidos[0] },
        { zona: 'zona 2', number: Data.totalPermitidos[1] },
        { zona: 'zona 3', number: Data.totalPermitidos[2] },

    ];

    console.log(free);
    res.render('pages/index', {
        free: free,

    });





}

/* crear data */
const createData = async(req, res = response) => {



        try {



            /* creo roi */
            const rois = new Rois(req.body);


            /* guardo roi*/
            await rois.save();


            res.json({
                ok: true,
                rois
            })

        } catch (error) {
            console.log(error);
            res.status(500).json({
                ok: false,
                mgs: 'error inesperado, hable con admi'
            });
        }


    }
    /* par actualizacion  */
const updateRoi = async(req, res = response) => {

    /* obtengo el id del parqueadero */
    const uid = req.params.id;

    try {

        const roiDB = await Rois.findById(uid);
        /* si no existe! */
        if (!roiDB) {
            return res.status(404).json({
                ok: false,
                msg: 'No existe el Roi seleccionado para ese parquedero'
            });
        }
        /* si existe! */
        const {...campos } = req.body;

        const roiActualizado = await Rois.findByIdAndUpdate(uid, campos, { new: true });

        res.json({
            ok: true,
            rois: roiActualizado

        });




    } catch (error) {

        console.log(error);
        res.status(500).json({
            ok: false,
            msg: 'Error inesperado'
        });

    }

};


module.exports = {
    getDatos,
    createData,
    updateRoi
}