import { Component, Input, OnInit } from '@angular/core';
import { DataService } from './data.service'

@Component({
    selector: 'experiment-data',
    templateUrl: 'static/app/experiment/data.html',
    providers: [DataService]
})

export class DataComponent implements OnInit {
    @Input() id: Number

    data: any[];
    minRatio: Number;
    maxRatio: Number;

    constructor(private service: DataService) {}

    ngOnInit(): void {
        this.service.getData(this.id).then(d => this.data = d);
    }
}