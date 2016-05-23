import { Component } from '@angular/core'
import { ProbesService } from './probes.service'


@Component({
    templateUrl: 'static/app/probes/probes.html',
    providers: [ProbesService]
})

export class ProbesComponent {
    data: any[];

    constructor(private service: ProbesService) {}

    ngOnInit(): void {
        this.service.getData().then(d => this.data = d);
    }
}