import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ExperimentService } from './experiment.service'

@Component({
    selector: 'experiment',
    templateUrl: 'static/app/experiment/experiment.html',
    styleUrls: [ 'static/app/experiment/experiment.css' ]
})

export class ExperimentComponent implements OnInit, OnDestroy {
    private sub: any;
    metadata: any[];
    minRatio: number;
    maxRatio: number;
    id: number;
    byPeptide: boolean;
    collapsed: boolean;
    lh_quant: boolean;

    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private service: ExperimentService
    ) {
        this.byPeptide = false;
        this.collapsed = false;
    }

    ngOnInit() {
        this.sub = this.route.params.subscribe(({id}) =>  {
            this.id = id;
            this.service.getData(id).then(d => {
                this.metadata = d;
                this.lh_quant = this.metadata['quantification_numerator'] === 'L';
            });
        });
    }

    ngOnDestroy() {
        this.sub.unsubscribe()
    }

    flipQuantification() {
        if (this.metadata['inverse_ratio_id']) {
            this.router.navigate(['/experiment', this.metadata['inverse_ratio_id']]);
        }
    }
}