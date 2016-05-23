import { Component } from '@angular/core';
import { AutoService } from './auto.service'
import { FORM_DIRECTIVES } from '@angular/common';

@Component({
    templateUrl: 'static/app/auto/auto.html',
    directives: [FORM_DIRECTIVES],
    providers: [AutoService]
})

export class AutoComponent  {
    constructor(private service: AutoService) {}
}