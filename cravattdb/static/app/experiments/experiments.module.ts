import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpModule } from '@angular/http';

import { ExperimentsComponent } from './experiments.component';

import { ExperimentsService } from './experiments.service';

import { routing } from './experiments.routing';

@NgModule({
    imports: [
        CommonModule,
        HttpModule,
        RouterModule,
        routing
    ],
    declarations: [
        ExperimentsComponent
    ],
    providers: [
        ExperimentsService
    ]
})
export class ExperimentsModule {}