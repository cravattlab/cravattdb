import { Component, ViewChild, OnInit, OnDestroy } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HomeService } from './home.service';
import { FilterComponent } from './filter.component';

declare var chroma: any;

@Component({
    selector: 'home',
    templateUrl: 'home.html',
    styleUrls: [ 'home.css' ]
})

export class HomeComponent implements OnInit, OnDestroy {
    @ViewChild(FilterComponent) filter: FilterComponent;
    private _data: any[];
    private sub: any;
    term: string = '';
    filters: any[] = [];
    activeFilters: any[] = [];
    details: {} = {};
    scale: any = chroma.scale('YlOrRd');
    searching: boolean = false;

    constructor(
        private service: HomeService,
        private router: Router,
        private route: ActivatedRoute
    ) { }

    ngOnInit() {
        this.service.getFilters().then(d => {
            let params = this.route.snapshot.params;
            d.forEach(f => f.options.forEach(o =>
                o.active = params.hasOwnProperty(f.name + '_id') && 
                           (params[f.name + '_id'].split(',').map(parseInt).indexOf(o.id)) !== -1
            ));
            this.filters = d;
        });

        this.sub = this.route.params.subscribe(params =>  {
            this.term = params['term'] || '';
            this._search(params);
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
        this.searching = !!term;
        this.term = term;
        this.updateUrl();
    }

    _search(params) {
        if (!this.term) return;
        this.searching = true;
        this.service.search(params)
            .then(d => this.data = d)
            .catch(e => this.searching = false);
    }

    toggleDetail(experimentId, uniprot) {
        // not very happy with this, a lot of initialization because I chose a
        // nested object data structure. Could this be aleviated with an async
        // pipe perhaps? Or maybe just a different data structure. Alas, it works.
        if (!this.details.hasOwnProperty(experimentId)) {
            this.details[experimentId] = {};
        }

        if (!this.details[experimentId].hasOwnProperty(uniprot)) {
            this.details[experimentId][uniprot] = {};
        }

        let detail = (Object.keys(this.details[experimentId][uniprot]).length) ?
            this.details[experimentId][uniprot] :
            this.details[experimentId][uniprot] = { 'data': [], visible: false };

        if (detail.data.length) {
            detail.visible = !detail.visible;
        } else {
            this.service.getDetail(experimentId, uniprot)
                .then(d => {
                    detail.data = d;
                    detail.visible = true;
                });
        }
    }

    isDetailVisible(experimentId, uniprot) {
        if (!this.details.hasOwnProperty(experimentId)) return false;
        if (!this.details[experimentId].hasOwnProperty(uniprot)) return false;

        const detail = this.details[experimentId][uniprot];

        return !!detail.data.length && detail.visible;
    }

    onFiltersChange(filters) {
        this.activeFilters = filters;
    }

    onFiltersSelect(filters) {
        this.updateUrl(filters);
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
        this.updateUrl();
    }
    
    onFilterEdit(filter) {
        this.filter.show();
        this.filter.showFilterDetails(this.filters[filter.index]);
    }

    updateUrl(filters = this.activeFilters) {
        let params = Object.assign({ term: this.term }, this._flattenActiveFilters(filters));
        this.router.navigate(['/search', params]);
    }

    _flattenActiveFilters(filters = this.activeFilters) {
        // map active filter structure into url param structure
        return Object.assign({}, ...filters.map(filter => {
            return { [filter.name + '_id']: filter.options.map(o => o.id).join(',') }
        }));
    }
}