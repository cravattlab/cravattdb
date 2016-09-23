import { Component, OnInit, NgZone } from '@angular/core';
import { FormBuilder, FormGroup, FormArray } from '@angular/forms';
import { Observable } from 'rxjs/Observable';
import { AutoService } from './auto.service';

import * as _ from 'lodash';

@Component({
    selector: 'auto',
    templateUrl: 'auto.html',
    styleUrls: [ 'auto.css' ]
})

export class AutoComponent implements OnInit {
    form: FormGroup;
    data: {} = {};
    showErrors: boolean = false;
    errors: any[] = [];
    files: any[] = [];
    progress: number = 0;

    get treatments(): FormArray { return this.form.get('treatments') as FormArray; }
    get diffMods(): FormArray { return this.form.get('diffMods') as FormArray; }

    constructor(
        private service: AutoService,
        private formBuilder : FormBuilder,
        private zone: NgZone
    ) {
        this.service.progress$.debounceTime(100).subscribe(progress => {
            // struggle bus report:
            // http://stackoverflow.com/a/37695136/383744
            this.zone.run(() => {
                this.progress = progress;
            });
        });
    }

    ngOnInit(): void {
        this.service.getData().subscribe(d => this.data = d);

        this.form = this.formBuilder.group({
            name: '',
            description: '',
            organism: '',
            type: '',
            instrument: '',
            proteomic_fraction: '',
            sample_type: '',
            cell_type: '',
            ip2_username: '',
            ip2_password: '',
            treatments: new FormArray([]),
            diffMods: new FormArray([])
        });
    }

    addTreatment(treatmentType): void {
        let treatment = this.formBuilder.group({
            type: treatmentType,
            id: null,
            fraction: this.formBuilder.group({
                light: false,
                heavy: false
            }),
            treatment_type: '',
            concentration: null,
            time: null,
            description: ''
        });

        this.treatments.push(treatment);
    }

    removeTreatment(i: number): void {
        this.treatments.removeAt(i);
    }

    addDiffMod(mass, residue): void {
        let diffMod = this.formBuilder.group({
            mass: null,
            residue: ''
        });

        this.diffMods.push(diffMod);
    }

    removeDiffMod(i: number): void {
        this.diffMods.removeAt(i);
    }

    onFileChange(e): void {
        this.files = _.values(e.target.files);
    }

    onSubmit(form: any): void {
        let req = this.service.submitForm(form, this.files).subscribe(() => {
            console.log('sent');
        }, () => {
            console.log('error');
        });
    }
}