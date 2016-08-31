import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ExperimentsService } from './experiments.service';

@Component({
    templateUrl: 'experiments.html'
})

export class ExperimentsComponent implements OnInit {
    experiments: any[];

    constructor(private service: ExperimentsService, private router: Router) {}

    ngOnInit() {
        this.service.getExperiments().then(data => this.experiments = data.experiments);
    }
}