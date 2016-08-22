import { RouterModule } from '@angular/router';
import { ExperimentsComponent } from './experiments.component';

export const routing = RouterModule.forChild([
    { path: 'experiments', component: ExperimentsComponent }
]);