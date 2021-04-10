// Ruta: /api/rois
const { Router } = require('express');
/* voy a importar express validators */
const { check } = require('express-validator');

/* importo validar campos middleware personalizado */
const { validarCampos } = require('../middlewares/validar-campos');


const { getDatos, createData, updateRoi } = require('../controllers/rois');


const router = Router();



router.post('/', [
    check('parqueadero', 'el parqueadero debe ser valido').isMongoId(),


    validarCampos,

], createData);


router.get('/:busqueda', getDatos);

router.put('/:id', updateRoi);

/* ---------------------- */
module.exports = router;