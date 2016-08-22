import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ProbesComponent } from './probes.component';

import { ProbesService } from './probes.service';
import { routing } from './probes.routing';

@NgModule({
    imports: [
        CommonModule,
        routing
    ],
    declarations: [
        ProbesComponent
    ],
    providers: [
        ProbesService
    ]
})
export class ProbesModule {}