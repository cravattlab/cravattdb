import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AutoComponent } from './auto.component';
import { TreatmentComponent } from './treatment.component';

import { InitializeDropdown, InitializeCheckbox } from '../directives/semantic-ui-init';

import { AutoService } from './auto.service'

import { routing } from './auto.routing';

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        ReactiveFormsModule,
        routing
    ],
    declarations: [
        AutoComponent,
        TreatmentComponent,
        InitializeDropdown,
        InitializeCheckbox
    ],
    providers: [
        AutoService
    ]
})
export class AutoModule {}