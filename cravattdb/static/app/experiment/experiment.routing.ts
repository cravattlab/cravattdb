import { RouterModule } from '@angular/router';
import { ExperimentComponent } from './experiment.component';

export const routing = RouterModule.forChild([
    { path: 'experiment/:id', component: ExperimentComponent }
]);