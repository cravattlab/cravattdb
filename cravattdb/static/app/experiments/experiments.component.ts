import { Component } from '@angular/core';
import { CanDeactivate, OnActivate, Router, RouteSegment, ROUTER_DIRECTIVES } from '@angular/router';
import { ExperimentsService } from './experiments.service'

@Component({
    templateUrl: 'static/app/experiments/experiments.html',
    providers: [ExperimentsService],
    directives: [ROUTER_DIRECTIVES]
})

export class ExperimentsComponent implements OnActivate {
    experiments: any[];

    constructor(
        private service: ExperimentsService,
        private router: Router
    ) {}

    routerOnActivate() {
        this.service.getExperiments().then(experiments => this.experiments = experiments);
    }
}