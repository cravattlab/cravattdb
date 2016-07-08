import { Component, OnInit } from '@angular/core';
import { Router, ROUTER_DIRECTIVES } from '@angular/router';
import { ExperimentsService } from './experiments.service'

@Component({
    templateUrl: 'static/app/experiments/experiments.html',
    providers: [ExperimentsService],
    directives: [ROUTER_DIRECTIVES]
})

export class ExperimentsComponent implements OnInit {
    experiments: any[];

    constructor(private service: ExperimentsService, private router: Router) {}

    ngOnInit() {
        this.service.getExperiments().then(data => this.experiments = data.experiments);
    }
}