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

    constructor(
        private service: SideloadService
    ) {
        this.showErrors = false;
        this.errors = [];
    }

    onSubmit(form: any): void {
        console.log('you submitted value:', form); 
    }

    onFileChange(e) {
        console.log(e.target.files);
    }

    routerOnActivate() {
        this.service.getData().then(d => this.data = d);
    }
}