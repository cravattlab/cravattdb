import { Component } from '@angular/core';
import { CanDeactivate, OnActivate, Router, RouteSegment } from '@angular/router';
import { ExperimentsService } from './experiments.service'

@Component({
    templateUrl: 'static/app/experiments/experiments.html',
    providers: [ExperimentsService]
})

export class ExperimentsComponent implements OnActivate {
    experiments: any[];

    constructor(
        private service: ExperimentsService
    ) {}

    routerOnActivate() {
        this.service.getExperiments().then(experiments => this.experiments = experiments);
    }
}