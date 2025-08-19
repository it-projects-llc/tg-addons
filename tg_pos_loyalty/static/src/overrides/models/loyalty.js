/** @odoo-module **/

import {Order} from "@point_of_sale/app/store/models";
import {formatFloatTime} from "@web/views/fields/formatters";

import {patch} from "@web/core/utils/patch";
const {DateTime} = luxon;

patch(Order.prototype, {
    _programIsApplicable(program) {
        const res = super._programIsApplicable(...arguments);
        if (!res) return res;

        const now = DateTime.now();
        const weekday = now.weekday;

        if (program.are_happy_hours_enabled) {
            if (!program.happy_hours_weekdays.includes(weekday)) {
                return false;
            }

            const happyHoursFrom = DateTime.fromFormat(
                formatFloatTime(program.happy_hours_from),
                "h:m"
            );
            const happyHoursTo = DateTime.fromFormat(
                formatFloatTime(program.happy_hours_to),
                "h:m"
            );

            if (now < happyHoursFrom) {
                return false;
            }

            if (now > happyHoursTo) {
                return false;
            }
        }

        return true;
    },
});
