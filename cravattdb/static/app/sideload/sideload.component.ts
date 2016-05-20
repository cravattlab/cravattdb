import { Component } from '@angular/core';
import { OnActivate } from '@angular/router';
import { SideloadService } from './sideload.service'
import { FORM_DIRECTIVES } from '@angular/common';
import { InitializeDropdown } from '../directives/semantic-ui-init';

@Component({
    templateUrl: 'static/app/sideload/sideload.html',
    directives: [FORM_DIRECTIVES, InitializeDropdown],
    providers: [SideloadService]
})

export class SideloadComponent implements OnActivate {
    data: {};
    showErrors: boolean;
    errors: any[];
    file: File;

    constructor(
        private service: SideloadService
    ) {
        this.showErrors = false;
        this.errors = [];
    }

    onSubmit(form: any): void {
        form.file = this.file;
        this.service.submitForm(form);
    }

    onFileChange(e) {
        this.file = e.target.files[0];
    }

    routerOnActivate() {
        this.service.getData().then(d => this.data = d);
    }
}