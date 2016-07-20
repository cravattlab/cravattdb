import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DataComponent } from './data.component'
import { MetaComponent } from './meta.component'

@Component({
    selector: 'experiment',
    templateUrl: 'static/app/experiment/experiment.html',
    styleUrls: [ 'static/app/experiment/experiment.css' ],
    directives: [ DataComponent, MetaComponent ]
})

export class ExperimentComponent implements OnInit {
    data: any[];
    minRatio: number;
    maxRatio: number;
    id: number;
    byPeptide: boolean;
    collapsed: boolean;

    constructor(private route: ActivatedRoute) {
        this.byPeptide = false;
        this.collapsed = false;
    }

    ngOnInit() {
        this.id = this.route.snapshot.params['id'];
    }
}