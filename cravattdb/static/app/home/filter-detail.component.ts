import { Component, ViewChild } from '@angular/core';
import { SidebarComponent } from './sidebar.component';

@Component({
    selector: 'filter-detail',
    templateUrl: 'static/app/home/filter-detail.html',
    directives: [ SidebarComponent ]
})

export class FilterDetailComponent {
    @ViewChild(SidebarComponent) sidebar: SidebarComponent;
    filter: {};
    term: string = '';
    
    show(filter) {
        this.filter = filter;
        // clear the search term whenever we show the details panel
        this.term = '';

        this.sidebar.show();
    }

    done() {
        this.sidebar.hide();
    }
    
    cancel() {
        this.sidebar.hide();
    }
}
