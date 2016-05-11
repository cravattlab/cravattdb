declare var bootstrap: any;

let dataset = bootstrap || [];
let datasetPromise = Promise.resolve(dataset);

import { Injectable } from '@angular/core';

@Injectable()
export class DatasetService {
    getExperiments() { return datasetPromise; }
}