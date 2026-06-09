/** @odoo-module **/

import WebsiteSaleDaterangePicker from "@website_sale_renting/js/website_sale_renting_daterangepicker";
const {DateTime} = luxon;
import {RentingMixinFix} from "@tg_website_sale_renting/js/renting_mixin";
import {_t} from "@web/core/l10n/translation";
import {session} from "@web/session";

luxon.Settings.defaultZone = "America/Panama";

WebsiteSaleDaterangePicker.include(RentingMixinFix);

WebsiteSaleDaterangePicker.include({
    async _loadRentingConstraints() {
        return this._super().then(() => {
            const $el = $(this.el).find("#rentingDates");
            const maxEndDateFromOptions = DateTime.fromSQL($el.data("max-end-date"));
            if (
                maxEndDateFromOptions.isValid &&
                DateTime.now() > maxEndDateFromOptions
            ) {
                session.denyRenting = _t(
                    "The product is not available for renting since %s",
                    maxEndDateFromOptions.toLocaleString(DateTime.DATE_FULL)
                );
            }
        });
    },

    _initSaleRentingDateRangePicker(el) {
        const hasDefaultDates = Boolean(this._hasDefaultDates());
        el.dataset.hasDefaultDates = hasDefaultDates;
        // <-- changes start
        const minStartDateFromOptions = DateTime.fromSQL(el.dataset.minStartDate);
        const maxEndDateFromOptions = DateTime.fromSQL(el.dataset.maxEndDate);

        let minStartDate = DateTime.min(DateTime.now(), this.startDate);
        if (minStartDateFromOptions.isValid) {
            minStartDate = DateTime.max(
                DateTime.now().set({
                    hour: 0,
                    minute: 0,
                    second: 0,
                    millisecond: 0,
                }),
                minStartDateFromOptions
            );
        }

        let maxEndDate = DateTime.max(DateTime.now().plus({years: 3}), this.endDate);

        if (maxEndDateFromOptions.isValid) {
            maxEndDate = maxEndDateFromOptions;
        }

        if (maxEndDate < minStartDate) {
            el.querySelector("input[name=renting_start_date]").disabled = true;
            el.querySelector("input[name=renting_end_date]").disabled = true;
            return;
        }

        // <-- changes end;

        const value =
            this.isShopDatePicker && !hasDefaultDates
                ? ["", ""]
                : [this.startDate, this.endDate];
        this.call(
            "datetime_picker",
            "create",
            {
                target: el,
                pickerProps: {
                    value,
                    range: true,
                    type: this._isDurationWithHours() ? "datetime" : "date",
                    minDate: minStartDate,
                    maxDate: maxEndDate,
                    isDateValid: this._isValidDate.bind(this),
                    dayCellClass: (date) => this._isCustomDate(date).join(" "),
                },
                onApply: ([start_date, end_date]) => {
                    this.startDate = start_date;
                    this.endDate = end_date;
                    this._verifyValidPeriod();
                    this.$("input[name=renting_start_date]").change();
                    this.$el.trigger("daterangepicker_apply", {
                        start_date,
                        end_date,
                    });
                },
            },
            () => [
                el.querySelector("input[name=renting_start_date]"),
                el.querySelector("input[name=renting_end_date]"),
            ]
        ).enable();

        // Removing the pointer event here to avoid updating templates in stable.
        const inputElement = el.querySelector("input[name=renting_start_date]");
        if (inputElement?.disabled) {
            inputElement.parentElement
                .querySelector("div .input-group-text.cursor-pointer")
                ?.classList.add("pe-none");
        }
    },
});
