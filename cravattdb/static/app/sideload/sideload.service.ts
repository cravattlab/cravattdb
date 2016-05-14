declare var bootstrap:any;

let sideload = bootstrap || {};
let sideloadPromise = Promise.resolve(sideload);

import { Injectable } from '@angular/core';

@Injectable()
export class SideloadService {
    getSideload() { return sideloadPromise; }
}