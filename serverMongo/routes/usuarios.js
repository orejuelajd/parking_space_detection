// Ruta: /api/usuarios
const { Router } = require('express');
/* voy a importar express validators */
const { check } = require('express-validator');

/* importo validar campos middleware personalizado */
const { validarCampos } = require('../middlewares/validar-campos');


const { crearUsuario, getUsuarios } = require('../controllers/usuarios');


const router = Router();


/* crear usuario */
router.post('/', [
    check('nombre', 'El nombre es obligatorio').not().isEmpty(),
    check('apellido', 'El apellido es obligatorio').not().isEmpty(),
    check('password', 'El password es obligatorio').not().isEmpty(),
    check('email', 'El Email es obligatorio').isEmail(),
    check('telefono', 'El telefono es obligatorio').not().isEmpty(),

    validarCampos,

], crearUsuario);

/* obtener usuarios */
router.get('/', getUsuarios);






module.exports = router;