import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { HomeModule } from './home/home.module';
import { ExperimentsModule } from './experiments/experiments.module';
import { ExperimentModule } from './experiment/experiment.module';
import { AutoModule } from './auto/auto.module';
import { ProbesModule } from './probes/probes.module';

import { routing } from './app.routing';


@NgModule({
    imports: [
        BrowserModule,
        routing,
        ReactiveFormsModule,
        FormsModule,
        HttpModule,
        HomeModule,
        ExperimentsModule,
        ProbesModule,
        AutoModule,
        ExperimentModule
    ],
    declarations: [
        AppComponent
    ],
    bootstrap: [ AppComponent ]
})
export class AppModule {}