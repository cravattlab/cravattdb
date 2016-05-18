import { Component, OnInit } from '@angular/core';
import { CanDeactivate, OnActivate, Router, RouteSegment } from '@angular/router';
import { DatasetService } from './dataset.service'

@Component({
    templateUrl: 'static/app/dataset/dataset.html',
    providers: [DatasetService]
})

export class DatasetComponent implements OnActivate {
    data: any[];
    minRatio: Number;
    maxRatio: Number;

    constructor(
        private service: DatasetService
    ) {
        this.minRatio = 0;
        this.maxRatio = 20;
    }

    routerOnActivate(curr: RouteSegment): void {
        let id = +curr.getParam('id')
        this.getData(id);
    }

    getData(id) {
        this.service.getData(id).then(d => this.data = d);
    }
}