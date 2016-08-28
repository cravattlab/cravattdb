import { Component, OnInit } from '@angular/core'
import { ProbesService } from './probes.service'

@Component({
    templateUrl: 'probes.html'
})
export class ProbesComponent implements OnInit {
    data: any[];

    constructor(private service: ProbesService) {}

    ngOnInit(): void {
        this.service.getData().then(d => this.data = d);
    }

    getStructure(inchi): string {
        return `https://cactus.nci.nih.gov/chemical/structure/${inchi}/image?format=png&width=500&height=500&csymbol=none&hsymbol=special&border`;
    }
}