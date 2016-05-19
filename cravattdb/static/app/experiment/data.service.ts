declare var bootstrap: any;

import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class DataService {
    constructor(private http: Http) { }

    getData(id): Promise<any> {
        if (bootstrap.hasOwnProperty('experiment') && bootstrap.experiment.id === id) {
            return Promise.resolve(bootstrap.experiment.data);
        } else {
            return this.http.get('/api/dataset/' + id)
                .toPromise()
                .then(this.extractData)
                .catch(this.handleError);
        }
    }

    private extractData(res: Response) {
        let body = res.json();
        return body.data || {};
    }

    private handleError(error: any) {
        // In a real world app, we might use a remote logging infrastructure
        // We'd also dig deeper into the error to get a better message
        let errMsg = error.message || error.statusText || 'Server error';
        console.error(errMsg); // log to console instead
        return Observable.throw(errMsg);
    }
}