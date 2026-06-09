/** @odoo-module **/
/* eslint-disable no-unused-vars, init-declarations */

import {_t} from "@web/core/l10n/translation";
import {msecPerUnit, unitMessages} from "@website_sale_renting/js/renting_mixin";
import {session} from "@web/session";
import {sprintf} from "@web/core/utils/strings";

export const RentingMixinFix = {
    _getInvalidMessage(startDate, endDate, productId = false) {
        let message;
        if (!this.rentingUnavailabilityDays || !this.rentingMinimalTime) {
            return message;
        }
        if (session.denyRenting) {
            return session.denyRenting;
        }
        if (startDate && endDate) {
            if (this.rentingUnavailabilityDays[startDate.weekday]) {
                message = _t("You cannot pick up your rental on that day of the week.");
            } else if (this.rentingUnavailabilityDays[endDate.weekday]) {
                message = _t("You cannot return your rental on that day of the week.");
            } else {
                // <--- changes start
                const endDateFixed = endDate.endOf("day").plus({seconds: 1});
                const rentingDuration = endDateFixed - startDate;
                // <!--- changes end
                if (rentingDuration < 0) {
                    message = _t("The return date should be after the pickup date.");
                } else if (
                    startDate.startOf("day") < luxon.DateTime.now().startOf("day")
                ) {
                    message = _t("The pickup date cannot be in the past.");
                } else if (
                    ["hour", "day", "week", "month"].includes(
                        this.rentingMinimalTime.unit
                    )
                ) {
                    const unit = this.rentingMinimalTime.unit;
                    if (
                        rentingDuration / msecPerUnit[unit] <
                        this.rentingMinimalTime.duration
                    ) {
                        message = _t(
                            "The rental lasts less than the minimal rental duration %s",
                            sprintf(
                                unitMessages[unit],
                                this.rentingMinimalTime.duration
                            )
                        );
                    }
                }
            }
        } else {
            message = _t("Please select a rental period.");
        }
        return message;
    },
};
