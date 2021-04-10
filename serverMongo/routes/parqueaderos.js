/* uso de rutas en express */
const { Router } = require('express');

/* validacion de datos en express */
const { check } = require('express-validator');

/* importo validar campos middleware personalizado */
const { validarCampos } = require('../middlewares/validar-campos');

/* importo crear y traer parqueaderos de los controllers */
const { createParqueadero, getParqueaderos } = require('../controllers/parqueadero');

/* uso rutas en express */

const router = Router();


/* rutar crear parqueadero */

router.post('/', [
    check('usuario', 'el usuario id debe ser valido').isMongoId(),
    check('nombre', 'El nombre es obligatorio').not().isEmpty(),
    check('ubicacion', 'La ubicacion es obligatorio').not().isEmpty(),
    check('cantidadParqueaderos', 'la cantidad es obligatoria').not().isEmpty(),
    validarCampos

], createParqueadero);


/* creo la ruta   del get*/
router.get('/', getParqueaderos);

/* ---------------------- */
module.exports = router;