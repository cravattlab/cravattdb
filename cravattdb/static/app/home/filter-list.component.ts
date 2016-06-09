import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
    selector: 'filter-list',
    templateUrl: 'static/app/home/filter-list.html',
    styleUrls: [ 'static/app/home/filter-list.css' ],
})

export class FilterListComponent {
    @Input() activeFilters: any[];
    @Output() remove: EventEmitter<any> = new EventEmitter();
    @Output() edit: EventEmitter<any> = new EventEmitter();

    constructor() {}
    
    removeFilter(e, filter) {
        e.stopPropagation();

        this.remove.emit({
            value: filter
        });
    }
    
    editFilter(filter) {
        this.edit.emit({
            value: filter
        });
    }
}