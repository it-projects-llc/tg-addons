/** @odoo-module **/

import {Order} from "@point_of_sale/app/store/models";
import {patch} from "@web/core/utils/patch";
const {DateTime} = luxon;

patch(Order.prototype, {
    _programIsApplicable(program) {
        const res = super._programIsApplicable(...arguments);
        if (!res) return res;

        const weekday = DateTime.now().weekday;

        if (
            program.are_happy_hours_enabled &&
            !program.happy_hours_weekdays.includes(weekday)
        ) {
            return false;
        }

        console.log(program.happy_hours_from);
        console.log(program.happy_hours_to);

        return true;
    },
});
