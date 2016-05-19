import { Component, Input, OnInit } from '@angular/core';

@Component({
    selector: 'experiment-meta',
    templateUrl: 'static/app/experiment/meta.html',
})

export class MetaComponent implements OnInit {
    @Input() id: Number

    ngOnInit(): void {
        console.log(this.id);
    }
}