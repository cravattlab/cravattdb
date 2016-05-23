import { Component, OnInit } from '@angular/core';
import { AutoService } from './auto.service'
import { FORM_DIRECTIVES } from '@angular/common';
import { InitializeDropdown } from '../directives/semantic-ui-init';

@Component({
    templateUrl: 'static/app/auto/auto.html',
    directives: [FORM_DIRECTIVES, InitializeDropdown],
    providers: [AutoService]
})

export class AutoComponent implements OnInit {
    data: {};
    showErrors: boolean = false;
    errors: any[] = [];
    files: File[];

    constructor(private service: AutoService) {}

    ngOnInit(): void {
        this.service.getData().subscribe(d => this.data = d);
    }

    onFileChange(e): void {
        this.files = e.target.files;
    }
}