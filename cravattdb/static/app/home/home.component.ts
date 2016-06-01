import { Component, ViewChild, OnInit } from '@angular/core';
import { HomeService } from './home.service';
import { FilterComponent } from './filter.component';
import { FilterListComponent } from './filter-list.component';
import * as _ from 'lodash';

@Component({
    templateUrl: 'static/app/home/home.html',
    selector: 'home',
    directives: [ FilterComponent, FilterListComponent ],
    providers: [ HomeService ]
})

export class HomeComponent implements OnInit {
    @ViewChild(FilterComponent) filter: FilterComponent;
    data: any[];
    filters: any[];
    activeFilters: any[];

    constructor(private service: HomeService) {}

    ngOnInit() {
        this.service.getFilters().then(d => this.filters = d);
    }

    search(term) {
        this.service.search(term).then(d => {
            this.data = d.dataset.map(o => {
                return _.values(o);
            });

            console.log(this.data);
        } );
        console.log(term, this.data);
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