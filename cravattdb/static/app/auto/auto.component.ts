import { Component, OnInit, NgZone } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { AutoService } from './auto.service'

import * as _ from 'lodash';

@Component({
    selector: 'auto',
    templateUrl: 'static/app/auto/auto.html',
    styleUrls: [ 'static/app/auto/auto.css' ]
})

export class AutoComponent implements OnInit {
    data: {} = {};
    showErrors: boolean = false;
    errors: any[] = [];
    files: any[] = [];
    progress: number = 0;

    constructor(private service: AutoService, private zone: NgZone) {
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