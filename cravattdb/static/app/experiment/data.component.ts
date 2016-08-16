import {
    Component,
    Input,
    OnInit,
    OnChanges,
    ChangeDetectionStrategy,
    ChangeDetectorRef,
    SimpleChange
} from '@angular/core';
import * as _ from 'lodash';
import Utils from '../shared/utils';
import Constants from '../shared/constants';
import { DataService } from './data.service';

declare var chroma: Chroma.ChromaStatic;

enum Sort {
    Ascending = 1,
    Descending = -1
}

// We're going to handle a lot of things manually inside this component.
// Lots of data passing through which we want to avoid re-rendering
// except when we know it is strictly necessary
@Component({
    selector: 'experiment-data',
    templateUrl: 'static/app/experiment/data.html',
    styleUrls: ['static/app/experiment/data.css'],
    changeDetection: ChangeDetectionStrategy.OnPush,
    providers: [DataService]
})

export class DataComponent implements OnInit, OnChanges {
    @Input() id: number
    @Input() byPeptide: boolean
    @Input() collapsed: boolean;

    loading: boolean = true;

    // original data from server
    _data: { data: any[], headers: string[] };
    // grouped and sorted data
    data: any[];
    scale: any = chroma.scale('YlOrRd');

    Sort = Sort;

    sortDirection: { [ propName: string]: Sort } = {
        'median': Sort.Descending
    };

    constructor(
        private service: DataService,
        private cd: ChangeDetectorRef
    ) { }

    ngOnInit(): void {
        this.service.getData(this.id).then(d => {
            d.headers.push('median');
            // save reference to pristine copy of data
            this._data = d;
            this.data = this.groupBy(this.byPeptide);
            this.sort('median', Sort.Descending);
        });
    }

    ngOnChanges(changes: { [propName: string]: SimpleChange }): void {
        let change = changes['byPeptide'];

        if (change && !change.isFirstChange()) {
            this.groupBy(change.currentValue)
        }
    }

    getHeaderIndex(header: string): number {
        return this._data.headers.indexOf(header);
    }

    sort(header: string, direction: Sort): void {
        const sortByIndex = this.getHeaderIndex(header);
        this.data = _.sortBy(this.data, item => item[0][sortByIndex] * direction);
        this.cd.markForCheck();
    }

    groupBy(byPeptide: boolean): any[] {
        let groupBy = byPeptide ? 'sequence' : 'uniprot';
        return this.group(groupBy);
    }

    group(header: string): any[] {
        const groupByIndex = this.getHeaderIndex(header);
        const ratioIndex = this.getHeaderIndex('ratio');
        const rsquaredIndex = this.getHeaderIndex('rsquared');
        let grouped: any = _.values(_.groupBy(this._data.data, groupByIndex));

        grouped = grouped.map(group => {
            // median by the ratio column
            let ratios = group.filter(x => x[rsquaredIndex] >= Constants.RSQUARED_CUTOFF).map(x => x[ratioIndex]);
            let median = Utils.specialMedian(ratios);
            // add median ratio as final element of first group member
            // I know this would be nicer on an object, but... we have to
            // juggle around tens of thousands of these sometimes
            //
            // also this is not formatted using toFixed since we want it
            // to stay a number, for details see:
            // http://stackoverflow.com/a/29494612/383744 
            group[0].push(Math.round(median * 1e2) / 1e2);
            return group;
        });

        this.cd.markForCheck();
        // processing data is finished, we can turn off progress spinner
        this.loading = false;

        return grouped;
    }
}
