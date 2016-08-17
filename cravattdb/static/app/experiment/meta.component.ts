import { Component, Input } from '@angular/core';

@Component({
    selector: 'experiment-meta',
    templateUrl: 'static/app/experiment/meta.html',
    styleUrls: [ 'static/app/experiment/meta.css' ],
})

export class MetaComponent {
    @Input() data: any[];
}