import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { HomeComponent } from './home.component';
import { SidebarComponent } from './sidebar.component';
import { FilterDetailComponent } from './filter-detail.component';
import { FilterComponent } from './filter.component';
import { FilterListComponent } from './filter-list.component';

import { HomeService } from './home.service';
import { routing } from './home.routing';

@NgModule({
    imports: [
        CommonModule,
        routing
    ],
    declarations: [
        HomeComponent,
        SidebarComponent,
        FilterComponent,
        FilterDetailComponent,
        FilterListComponent
    ],
    providers: [
        HomeService
    ]
})
export class HomeModule {}