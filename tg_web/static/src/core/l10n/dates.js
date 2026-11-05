/** @odoo-module **/

import * as dates from "@web/core/l10n/dates";

const originalFormatDateTime = dates.formatDateTime;

dates.formatDateTime = function () {
    let res = originalFormatDateTime(...arguments);
    if (res) {
        res += " (" + Intl.DateTimeFormat().resolvedOptions().timeZone + ")";
    }
    return res;
};
