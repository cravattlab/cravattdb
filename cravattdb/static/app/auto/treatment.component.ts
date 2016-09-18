import { Component, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
    selector: '[treatment]',
    templateUrl: 'treatment.html',
    styleUrls: [ 'treatment.css' ]
})
export class TreatmentComponent {
    @Input() data: {};
    @Input() type: string;
    @Input() removeTreatment: Function;
    info: {} = {
        heavy: false,
        light: false
    };

    toggleFraction(e, fraction): void {
        e.preventDefault();
        this.info[fraction] = !this.info[fraction];
    }
}