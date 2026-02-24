/** @odoo-module **/

export function unhex(code) {
    let unhexed_code = parseInt(code, 16).toString();
    if (unhexed_code.length % 2) {
        unhexed_code = "0" + unhexed_code;
    }
    return unhexed_code;
}

export function unhexForOdoo(session, code) {
    if (code && session.pos_hex_barcode) {
        return unhex(code);
    }
    return code;
}
