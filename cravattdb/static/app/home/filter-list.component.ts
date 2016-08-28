import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
    selector: 'filter-list',
    templateUrl: 'filter-list.html',
    styleUrls: [ 'filter-list.css' ]
})

export class FilterListComponent {
    @Input() activeFilters: any[];
    @Output() remove: EventEmitter<any> = new EventEmitter();
    @Output() edit: EventEmitter<any> = new EventEmitter();

    constructor() {}
    
    removeFilter(e, filter, item) {
        e.stopPropagation();

        this.remove.emit({
            value: { filter: filter, item: item }
        });
    }
    
    editFilter(filter) {
        this.edit.emit({
            value: filter
        });
    }
}