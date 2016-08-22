import { Component, ViewChild, EventEmitter, Output, Input, OnInit } from '@angular/core';
import { SidebarComponent } from './sidebar.component';

@Component({
    selector: 'filter-detail',
    templateUrl: 'static/app/home/filter-detail.html'
})

export class FilterDetailComponent {
    @ViewChild(SidebarComponent) sidebar: SidebarComponent;
    @Output() filterChange: EventEmitter<any> = new EventEmitter();
    activeFilter: {};
    term: string = '';

    show(filter) {
        this.activeFilter = filter;
        // clear the search term whenever we show the details panel
        this.term = '';

        this.sidebar.show();
    }

    toggleFilter(item) {
        item.active = !item.active;
        this.filterChange.emit({});
    }

    done() {
        this.sidebar.hide();
    }
}
