declare var bootstrap:any;

let experiments = bootstrap || [];
let experimentsPromise = Promise.resolve(experiments);

import { Injectable } from '@angular/core';

@Injectable()
export class ExperimentsService {
    getExperiments() { return experimentsPromise; }
}