import { provideRouter, RouterConfig } from '@angular/router';
import { ExperimentsComponent } from './experiments/experiments.component';
import { HomeComponent } from './home/home.component';
import { ExperimentComponent } from './experiment/experiment.component';
import { ProbesComponent } from './probes/probes.component';
import { AutoComponent } from './auto/auto.component';

export const routes: RouterConfig = [
    // redirects are the recommended way to do this in 2.0rc4
    // I'd prefer to be able to redirect to the same component to avoid reloads
    // but keep the empty url until we add a param (can't have params on 
    // empty route either)
    { path: '', redirectTo: '/search', pathMatch: 'full' },
    // if we do the below route instead, we end up reloading the component 
    // unnecessarily in some cases
    // { path: '', component: HomeComponent },
    { path: 'search', component: HomeComponent },
    { path: 'experiments', component: ExperimentsComponent },
    { path: 'experiment/:id', component: ExperimentComponent },
    { path: 'probes', component: ProbesComponent },
    { path: 'auto', component: AutoComponent }
];

export const APP_ROUTER_PROVIDERS = [
  provideRouter(routes)
];