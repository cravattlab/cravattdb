declare var bootstrap: any;

import { Injectable } from '@angular/core';

@Injectable()
export class SideloadService {
    getData() { return Promise.resolve(bootstrap || {}); }
}