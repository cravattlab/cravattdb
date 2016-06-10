import { Component, Input, OnInit } from '@angular/core';
import { DataService } from './data.service';
import { GroupByProteinPipe } from './groupByProtein.pipe';
import { GroupByPeptidePipe } from './groupByPeptide.pipe';

declare var chroma: any;

@Component({
    selector: 'experiment-data',
    templateUrl: 'static/app/experiment/data.html',
    styleUrls: [ 'static/app/experiment/data.css' ],
    providers: [DataService],
    pipes: [GroupByProteinPipe, GroupByPeptidePipe]
})

export class DataComponent implements OnInit {
    @Input() id: number
    @Input() byPeptide: boolean
    @Input() collapsed: boolean;

    data: any[];
    minRatio: number;
    maxRatio: number;
    scale: any = chroma.scale('YlOrRd');

    constructor(private service: DataService) { }

    ngOnInit(): void {
        this.service.getData(this.id).then(d => this.data = d);
    }
}