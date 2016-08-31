import { Component, OnInit, NgZone } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Observable } from 'rxjs/Observable';
import { AutoService } from './auto.service';

import * as _ from 'lodash';

@Component({
    selector: 'auto',
    templateUrl: 'auto.html',
    styleUrls: [ 'auto.css' ]
})

export class AutoComponent implements OnInit {
    autoForm: FormGroup;
    data: {} = {};
    showErrors: boolean = false;
    errors: any[] = [];
    files: any[] = [];
    progress: number = 0;

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

        this.autoForm = this.formBuilder.group({
            name: '',
            organism: '',
            type: '',
            instrument: '',
            treatment_type: '',
            proteomic_fraction: '',
            probe: this.formBuilder.group({
                id: 0,
                concentration: '',
                time: 0,
            }),
            inhibitor: this.formBuilder.group({
                id: 0,
                concentration: '',
                time: 0,
            }),
            sample_type: '',
            cell_type: '',
            ip2_username: '',
            ip2_password: ''
        });
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