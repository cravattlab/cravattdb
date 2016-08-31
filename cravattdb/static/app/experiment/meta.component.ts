import { Component, Input } from '@angular/core';

@Component({
    selector: 'experiment-meta',
    templateUrl: 'meta.html',
    styleUrls: [ 'meta.css' ],
})

export class MetaComponent {
    @Input() data: any[];
}