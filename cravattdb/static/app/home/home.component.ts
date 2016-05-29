import { Component } from '@angular/core';
import { HomeService } from './home.service';
import * as _ from 'lodash';

@Component({
    templateUrl: 'static/app/home/home.html',
    providers: [HomeService]
})

export class HomeComponent {
    data: any[];

    constructor(private service: HomeService) {}

    search(term) {
        this.service.getData(term).then(d => {
            this.data = d.dataset.map(o => {
                return _.values(o);
            });

            console.log(this.data);
        } );
        console.log(term, this.data);
    }
}