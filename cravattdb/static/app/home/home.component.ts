import { Component, ViewChild, OnInit, OnDestroy } from '@angular/core';
import { Router, ActivatedRoute, ROUTER_DIRECTIVES } from '@angular/router';
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

export class HomeComponent implements OnInit, OnDestroy {
    @ViewChild(FilterComponent) filter: FilterComponent;
    private _data: any[];
    private sub: any;
    term: string = '';
    filters: any[];
    activeFilters: any[];
    scale: any = chroma.scale('YlOrRd');
    searching: boolean = false;

    constructor(
        private service: HomeService,
        private router: Router,
        private route: ActivatedRoute
    ) { }

    ngOnInit() {
        this.service.getFilters().then(d => {
            d.forEach(f => f.options.forEach(o => o.active = false));
            this.filters = d;
        });

        this.sub = this.route.params.subscribe(({term}) =>  {
            this.term = term || '';
            this._search(this.term);
        });
    }

    ngOnDestroy() {
        this.sub.unsubscribe()
    }

    set data(data: any[]) {
        this.searching = false;
        this._data = data;
    }

    get data(): any[] {
        return this._data;
    }

    search(term) {
        let routeOptions: any[] = ['/search'];

        if (term) {
            routeOptions.push({ term: term });
        }

        this.searching = !!term;
        this.term = term;
        this.router.navigate(routeOptions);
    }

    _search(term) {
        if (!term) return;
        this.service.search(term)
            .then(d => this.data = d)
            .catch(e => this.searching = false);
    }

    onFiltersChange(filters) {
        this.activeFilters = filters;
    }
    
    onFilterRemove({filter, item}) {
        let index = filter.index;

        this.filters[index].options = this.filters[index].options.map(i => {
            if (i.id === item.id) {
                i.active = false;
            }
            return i;
        });
        
        this.filter.update();
    }
    
    onFilterEdit(filter) {
        this.filter.show();
        this.filter.showFilterDetails(this.filters[filter.index]);
    }
}