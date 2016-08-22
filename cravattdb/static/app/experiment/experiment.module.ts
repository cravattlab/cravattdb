import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ExperimentComponent } from './experiment.component';
import { DataComponent } from './data.component';
import { MetaComponent } from './meta.component';

import { DataService } from './data.service';
import { ExperimentService } from './experiment.service'

import { routing } from './experiment.routing';

@NgModule({
    imports: [
        CommonModule,
        routing
    ],
    declarations: [
        ExperimentComponent,
        DataComponent,
        MetaComponent
    ],
    providers: [
        DataService,
        ExperimentService
    ]
})
export class ExperimentModule {}