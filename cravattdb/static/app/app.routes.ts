import { provideRouter, RouterConfig } from '@angular/router';
import { ExperimentsComponent } from './experiments/experiments.component';
import { HomeComponent } from './home/home.component';
import { ExperimentComponent } from './experiment/experiment.component';
import { ProbesComponent } from './probes/probes.component';
import { AutoComponent } from './auto/auto.component';

export const routes: RouterConfig = [
    { path: '', component: HomeComponent },
    { path: 'experiments', component: ExperimentsComponent },
    { path: 'experiment/:id', component: ExperimentComponent },
    { path: 'probes', component: ProbesComponent },
    { path: 'auto', component: AutoComponent }
];

export const APP_ROUTER_PROVIDERS = [
  provideRouter(routes)
];