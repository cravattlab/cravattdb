import { Component, OnInit } from '@angular/core';
import { AutoService } from './auto.service'
import { FORM_DIRECTIVES } from '@angular/common';
import { InitializeDropdown } from '../directives/semantic-ui-init';
import * as _ from 'lodash';

@Component({
    templateUrl: 'static/app/auto/auto.html',
    directives: [FORM_DIRECTIVES, InitializeDropdown],
    providers: [AutoService]
})

export class AutoComponent implements OnInit {
    data: {} = {};
    showErrors: boolean = false;
    errors: any[] = [];
    files: any[] = [];

    constructor(private service: AutoService) {}

    ngOnInit(): void {
        this.service.getData().subscribe(d => this.data = d);
    }

    onFileChange(e): void {
        this.files = _.values(e.target.files);
    }

    onSubmit(form: any): void {
        this.service.submitForm(form, this.files);
    }
}