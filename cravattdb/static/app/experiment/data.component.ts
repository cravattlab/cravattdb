import {
    Component,
    Input,
    OnInit,
    OnChanges,
    ChangeDetectionStrategy,
    ChangeDetectorRef,
    SimpleChange
} from '@angular/core';
import * as imagesLoaded from 'imagesloaded';
import * as _ from 'lodash';
import { DataService } from './data.service';

declare var chroma: Chroma.ChromaStatic;

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

    constructor(
        private service: DataService,
        private cd: ChangeDetectorRef
    ) { }

    ngOnInit(): void {
        this.service.getData(this.id).then(d => {
            // save reference to pristine copy of data
            this._data = d;
            this.data = this.groupBy(this.byPeptide);
        });
    }

    ngOnChanges(changes: { [propName: string]: SimpleChange }): void {
        let change = changes['byPeptide'];

        if (change && !change.isFirstChange) {
            this.groupBy(change.currentValue)
        }
    }

    getHeaderIndex(header: string): number {
        return this._data.headers.indexOf(header);
    }

    groupBy(byPeptide: boolean): any[] {
        let groupBy = byPeptide ? 'sequence' : 'uniprot';
        return this.group(groupBy);
    }

    group(header: string): any[] {
        const groupByIndex = this.getHeaderIndex(header);
        const ratioIndex = this.getHeaderIndex('ratio');
        let grouped: any = _.values(_.groupBy(this._data.data, groupByIndex));

        grouped = grouped.map(group => {
            // mean by the ratio column
            let mean = _.meanBy(group, ratioIndex);
            // add mean ratio as final element of first group member
            // I know this would be nicer on an object, but... we have to
            // juggle around tens of thousands of these sometimes    
            group[0].push(mean.toFixed(1));
            return group;
        });

        // processing data is finished, we can turn off progress spinner
        this.loading = false;

        return grouped;
    }
}