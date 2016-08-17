import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DataComponent } from './data.component'
import { MetaComponent } from './meta.component'
import { ExperimentService } from './experiment.service'

@Component({
    selector: 'experiment',
    templateUrl: 'static/app/experiment/experiment.html',
    styleUrls: [ 'static/app/experiment/experiment.css' ],
    directives: [ DataComponent, MetaComponent ],
    providers: [ ExperimentService ]
})

export class ExperimentComponent implements OnInit {
    metadata: any[];
    minRatio: number;
    maxRatio: number;
    id: number;
    byPeptide: boolean;
    collapsed: boolean;

    constructor(
        private route: ActivatedRoute,
        private service: ExperimentService
    ) {
        this.byPeptide = false;
        this.collapsed = false;
    }

    ngOnInit() {
        this.id = this.route.snapshot.params['id'];
        this.service.getData(this.id).then(d => this.metadata = d);
    }
}