import { Component, ViewChild, EventEmitter, Output } from '@angular/core';
import { SidebarComponent } from './sidebar.component';

@Component({
    selector: 'filter-detail',
    templateUrl: 'static/app/home/filter-detail.html',
    directives: [ SidebarComponent ]
})

export class FilterDetailComponent {
    @ViewChild(SidebarComponent) sidebar: SidebarComponent;
    @Output() filterChange: EventEmitter<any> = new EventEmitter();
    filter: {};
    term: string = '';
    
    show(filter) {
        this.filter = filter;
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
