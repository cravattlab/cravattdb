import { Component } from '@angular/core';
import { CanDeactivate, OnActivate, Router, RouteSegment } from '@angular/router';
import { DatasetService } from './dataset.service'

@Component({
    templateUrl: 'static/app/dataset/dataset.html',
    providers: [DatasetService]
})

export class DatasetComponent implements OnActivate {
    dataset: any[];

    constructor(
        private service: DatasetService
    ) { }

    routerOnActivate() {
        this.service.getExperiments().then(dataset => this.dataset = dataset);
    }
}