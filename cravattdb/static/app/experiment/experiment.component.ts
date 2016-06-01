import { Component} from '@angular/core';
import { OnActivate, RouteSegment } from '@angular/router';
import { DataComponent } from './data.component'
import { MetaComponent } from './meta.component'

@Component({
    selector: 'experiment',
    templateUrl: 'static/app/experiment/experiment.html',
    directives: [DataComponent, MetaComponent]
})

export class ExperimentComponent implements OnActivate {
    data: any[];
    minRatio: number;
    maxRatio: number;
    id: number;
    byPeptide: boolean;
    collapsed: boolean;

    constructor() {
        this.byPeptide = false;
        this.collapsed = false;
    }

    routerOnActivate(curr: RouteSegment): void {
        this.id = +curr.getParam('id');
    }
}