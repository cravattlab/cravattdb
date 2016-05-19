import { Component, Input, OnInit } from '@angular/core';
import { MetaService } from './meta.service'

@Component({
    selector: 'experiment-meta',
    templateUrl: 'static/app/experiment/meta.html',
    providers: [MetaService]
})

export class MetaComponent implements OnInit {
    @Input() id: Number

    data: any[];

    constructor(private service: MetaService) { }

    ngOnInit(): void {
        this.service.getData(this.id).then(d => this.data = d);
    }
}