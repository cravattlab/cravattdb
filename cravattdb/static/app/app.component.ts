import { Component, OnInit } from '@angular/core';
import { Routes, Router, ROUTER_DIRECTIVES } from '@angular/router';
import { ExperimentsComponent } from './experiments/experiments.component';
import { HomeComponent } from './home/home.component';
import { ExperimentComponent } from './experiment/experiment.component';
import { SideloadComponent } from './sideload/sideload.component';
import { ProbesComponent } from './probes/probes.component';
import { AutoComponent } from './auto/auto.component';

@Component({
    selector: 'app',
    templateUrl: 'static/app/app.html',
    directives: [ ROUTER_DIRECTIVES ]
})

@Routes([
    { path: '/', component: HomeComponent },
    { path: '/sideload', component: SideloadComponent },
    { path: '/experiments', component: ExperimentsComponent },
    { path: '/experiment/:id', component: ExperimentComponent },
    { path: '/probes', component: ProbesComponent },
    { path: '/auto', component: AutoComponent }
])

export class AppComponent {}