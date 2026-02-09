/** @odoo-module **/

import WebsiteSaleDaterangePicker from "@website_sale_renting/js/website_sale_renting_daterangepicker";
const {DateTime} = luxon;

luxon.Settings.defaultZone = "America/Panama";

WebsiteSaleDaterangePicker.include({
    _initSaleRentingDateRangePicker(el) {
        const hasDefaultDates = Boolean(this._hasDefaultDates());
        el.dataset.hasDefaultDates = hasDefaultDates;
        // <-- changes start
        const minStartDate = DateTime.fromSQL(el.dataset.minStartDate);
        const maxEndDate = DateTime.fromSQL(el.dataset.maxEndDate);
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
                    minDate: minStartDate.isValid
                        ? minStartDate
                        : DateTime.min(DateTime.now(), this.startDate),
                    maxDate: maxEndDate.isValid
                        ? maxEndDate
                        : DateTime.max(DateTime.now().plus({years: 3}), this.endDate),
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
