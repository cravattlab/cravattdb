import { Component } from '@angular/core';
import { CanDeactivate, OnActivate, Router, RouteSegment } from '@angular/router';
import { SideloadService } from './sideload.service'
import { FORM_DIRECTIVES } from '@angular/common';
import { Experiment } from '../experiments/experiment'

@Component({
    templateUrl: 'static/app/sideload/sideload.html',
    directives: [FORM_DIRECTIVES],
    providers: [SideloadService]
})

export class SideloadComponent implements OnActivate {
    bootstrap: {};
    showErrors: boolean;
    errors: any[];
    // model = new Experiment();

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
        this.service.getSideload().then(sideload => this.bootstrap = sideload);
    }
}