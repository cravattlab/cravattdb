import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import * as _ from 'lodash';

declare var $: any

@Injectable()
export class AutoService {
    constructor(private http: Http) { }

    getData(): Observable<{}> {
        let observableBatch = [];

        const urls: string[] = [
            '/api/probe',
            '/api/organism',
            '/api/inhibitor',
            '/api/experiment_type'
        ];

        urls.forEach(url => {
            observableBatch.push(
                this.http.get(url).map(this.extractData).catch(this.handleError)
            )
        });

        return Observable.forkJoin(observableBatch, (...args) => {
            return _.merge({}, ...args);
        });
    }

    submitForm(form, files:File[]) {
        // Yes, I'm using fucking jQuery because the Http module blows right now.
        // And fuck XMLHttpRequest too. Couldn't they make a nice abstraction?
        let formData: FormData = new FormData();

        for (let key in form) {
            if (form[key]) {
                formData.append(key, form[key]);
            }
        }

        for (let file of files) {
            formData.append('files', file, file.name);
        }

        $.ajax({
            url: '/auto/search',
            method: 'POST',
            data: formData,
            async: false,
            cache: false,
            processData: false,
            contentType: false
        }).done(d => console.log(d));
    }

    private extractData(res: Response) {
        let body = res.json();
        return body || {};
    }

    private handleError(error: any) {
        // In a real world app, we might use a remote logging infrastructure
        // We'd also dig deeper into the error to get a better message
        let errMsg = error.message || error.statusText || 'Server error';
        console.error(errMsg); // log to console instead
        return Observable.throw(errMsg);
    }
}