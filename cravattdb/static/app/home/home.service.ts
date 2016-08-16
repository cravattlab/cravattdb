import { Injectable } from '@angular/core';
import { UrlSegment } from '@angular/router';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class HomeService {
    constructor(private http: Http) { }

    search(params): Promise<any> {
        let url = new UrlSegment('/api/search', params);
        return this.http.get(url.toString())
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    }

    getFilters(): Promise<any> {
        return this.http.get('/api/filters')
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError);
    }

    getDetail(experiment_id, uniprot): Promise<any> {
        return this.http.get(`/api/dataset/${experiment_id}/protein/${uniprot}`)
            .toPromise()
            .then(this.extractData)
            .catch(this.handleError)
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