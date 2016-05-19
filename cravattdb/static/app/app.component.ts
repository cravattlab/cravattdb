import { Component, OnInit } from '@angular/core'
import { Routes, Router, ROUTER_DIRECTIVES } from '@angular/router'
import { ExperimentsComponent } from './experiments/experiments.component'
import { MainComponent } from './home/home.component'
import { ExperimentComponent } from './experiment/experiment.component'
import { SideloadComponent } from './sideload/sideload.component'

@Component({
    selector: 'app',
    templateUrl: 'static/app/app.html',
    directives: [ROUTER_DIRECTIVES]
})

@Routes([
    { path: '/', component: MainComponent },
    { path: '/sideload', component: SideloadComponent },
    { path: '/experiments', component: ExperimentsComponent },
    { path: '/experiment/:id', component: ExperimentComponent }
])

export class AppComponent {}