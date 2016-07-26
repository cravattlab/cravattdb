import { Component, ViewChild, OnInit } from '@angular/core';
import { Router, ROUTER_DIRECTIVES } from '@angular/router';
import { HomeService } from './home.service';
import { FilterComponent } from './filter.component';
import { FilterListComponent } from './filter-list.component';
import * as _ from 'lodash';

declare var chroma: any;

@Component({
    selector: 'home',
    templateUrl: 'static/app/home/home.html',
    styleUrls: [ 'static/app/home/home.css' ],
    directives: [ FilterComponent, FilterListComponent ],
    providers: [ HomeService ]
})

export class HomeComponent implements OnInit {
    @ViewChild(FilterComponent) filter: FilterComponent;
    private _data: any[];
    filters: any[];
    activeFilters: any[];
    scale: any = chroma.scale('YlOrRd');
    searching: boolean = false;

    constructor(private service: HomeService, private router: Router) { }

    ngOnInit() {
        this.service.getFilters().then(d => {
            d.forEach(f => f.options.forEach(o => o.active = false));
            this.filters = d;
        });
    }

    set data(data: any[]) {
        this.searching = false;
        this._data = data;
    }

    get data(): any[] {
        return this._data;
    }

    search(term) {
        this.searching = true;
        this.service.search(term)
            .then(d => this.data = d)
            .catch(e => this.searching = false);
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