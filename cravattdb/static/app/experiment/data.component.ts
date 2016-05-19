import { Component, Input, OnInit } from '@angular/core';
import { DataService } from './data.service';
import { GroupByProteinPipe } from './groupByProtein.pipe';
import { GroupByPeptidePipe } from './groupByPeptide.pipe';

@Component({
    selector: 'experiment-data',
    templateUrl: 'static/app/experiment/data.html',
    providers: [DataService],
    pipes: [GroupByProteinPipe, GroupByPeptidePipe]
})

export class DataComponent implements OnInit {
    @Input() id: Number
    @Input() byPeptide: Boolean

    data: any[];
    minRatio: Number;
    maxRatio: Number;

    constructor(private service: DataService) { }

    ngOnInit(): void {
        this.service.getData(this.id).then(d => this.data = d);
    }

    toggleGroup(): void {
        this.byPeptide = !this.byPeptide;
    }
}