const { response } = require('express');
/* importo validation result */
const { validationResult } = require('express-validator');

const validarCampos = (req, res, next) => {

    /* aqui valido con validatios result */
    const errores = validationResult(req);

    if (!errores.isEmpty()) {
        return res.status(400).json({
            ok: false,
            errors: errores.mapped()
        });
    }

    next();

}

module.exports = {
    validarCampos
}