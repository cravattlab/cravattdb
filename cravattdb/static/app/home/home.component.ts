import { Component } from '@angular/core';
import { HomeService } from './home.service';

@Component({
    templateUrl: 'static/app/home/home.html',
    providers: [HomeService]
})

export class HomeComponent {
    constructor(private service: HomeService) {}
}