import { Component, ViewChild, OnInit } from '@angular/core';
import { HomeService } from './home.service';
import { FilterComponent } from './filter.component';
import { FilterListComponent } from './filter-list.component';
import * as _ from 'lodash';
import * as chroma from 'chroma-js';

@Component({
    templateUrl: 'static/app/home/home.html',
    selector: 'home',
    directives: [ FilterComponent, FilterListComponent ],
    providers: [ HomeService ]
})

export class HomeComponent implements OnInit {
    @ViewChild(FilterComponent) filter: FilterComponent;
    data: {};
    filters: any[];
    activeFilters: any[];
    scale: any;

    constructor(private service: HomeService) {
        this.scale = chroma.scale('YlOrRd');
    }

    ngOnInit() {
        this.service.getFilters().then(d => this.filters = d);
    }

    search(term) {
        this.service.search(term).then(d => this.data = d);
    }

    onFiltersChange(filters) {
        this.activeFilters = filters;
    }
    
    onFilterRemove(filter) {
        let index = filter.index;

        this.filters[index].options = this.filters[index].options.map(item => {
            item.active = false;
            return item;
        })
        
        this.filter.update();
    }
    
    onFilterEdit(filter) {
        this.filter.show();
        this.filter.showFilterDetails(this.filters[filter.index]);
    }
}