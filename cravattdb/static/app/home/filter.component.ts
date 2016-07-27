import { Component, ViewChild, Input, Output, EventEmitter } from '@angular/core';
import { FilterDetailComponent } from './filter-detail.component';
import { SidebarComponent } from './sidebar.component';

@Component({
    selector: 'filter',
    templateUrl: 'static/app/home/filter.html',
    styleUrls: ['static/app/home/filter.css'],
    directives: [ FilterDetailComponent, SidebarComponent ]
})

export class FilterComponent {
    @ViewChild(SidebarComponent) sidebar: SidebarComponent;
    @ViewChild(FilterDetailComponent) filterDetail: FilterDetailComponent;
    @Input() filters: any[];
    @Output() filtersChange: EventEmitter<any> = new EventEmitter();
    @Output() filterSelect: EventEmitter<any> = new EventEmitter();

    constructor() {}
    
    show() {
        this.sidebar.show();
    }

    toggle() {
        this.sidebar.toggle();
    }
    
    done() {
        this.sidebar.hide();
    }

    update() {
        // we save a reference to the index of the original filter
        // this will be useful later when editing or removing
        let activeFilters = this.filters.map((filter, index) => {
            // we use Object.assign to avoid mutating the original
            // objects in the filters array
            return Object.assign({ 'index': index }, filter );
        });

        // only keep filters that have at least one active item
        activeFilters = activeFilters.filter(filter => {
            return filter.options.some(item => item.active);
        });

        // only keep items that are set to active
        activeFilters = activeFilters.map(filter => {
            filter.options = filter.options.filter(item => item.active);
            return filter;
        });

        this.filtersChange.emit({
            value: activeFilters
        });
    }

    showFilterDetails(filter) {
        this.filterDetail.show(filter);
    }
}