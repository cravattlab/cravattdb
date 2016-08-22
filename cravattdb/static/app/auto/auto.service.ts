import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import { Observer } from 'rxjs/Observer';

@Injectable()
export class AutoService {

    progress$: Observable<any>;
    progressObserver: Observer<any>;

    constructor(private http: Http) {
        this.progress$ = new Observable(observer => {
            this.progressObserver = observer;
        }).share();
    }

    getData(): Observable<{}> {
        return this.http.get('/api/user_defined')
            .map(this.extractData)
            .catch(this.handleError);
    }

    submitForm(form, files: File[]): Observable<any> {
        return new Observable(observer => {
            const url = '/auto/search';
            let formData: FormData = new FormData();
            let xhr: XMLHttpRequest = new XMLHttpRequest();

            for (let key in form) {
                if (form[key]) {
                    formData.append(key, form[key]);
                }
            }

            for (let file of files) {
                formData.append('files', file, file.name);
            }

            xhr.onreadystatechange = () => {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        observer.next(JSON.parse(xhr.response));
                        observer.complete();
                    } else {
                        observer.error(xhr.response);
                    }
                }
            };

            xhr.upload.onprogress = (event) => {
                let progress = Math.round(event.loaded / event.total * 100);

                this.progressObserver.next(progress);

                if (progress === 100) {
                    this.progressObserver.complete();
                }
            };

            xhr.open('POST', url, true);
            xhr.send(formData);
        });
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