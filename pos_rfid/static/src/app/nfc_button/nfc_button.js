/** @odoo-module **/

import {Component, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class NFCButton extends Component {
    static template = "pos_rfid.NFCButton";

    setup() {
        this.barcodeReader = useService("barcode_reader");
        this.state = useState({
            isRunning: false,
        });
        if (this.isVisible) {
            setTimeout(() => this.startScanning(false), 500);
        }
    }

    get isVisible() {
        return "NDEFReader" in window;
    }

    async startScanning(onErrorRaise) {
        const ndef = new window.NDEFReader();

        ndef.addEventListener("reading", ({serialNumber}) => {
            this.barcodeReader.scan(String(serialNumber.split(":").reverse().join("")));
        });

        try {
            await ndef.scan();
        } catch (e) {
            if (onErrorRaise) throw e;
            return;
        }

        this.state.isRunning = true;
    }

    async click() {
        if (this.state.isRunning) return;
        await this.startScanning(true);
    }
}
