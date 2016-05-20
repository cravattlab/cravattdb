declare var bootstrap: any;

import { Injectable, Inject } from '@angular/core';


@Injectable()
export class SideloadService {
    getData() { return Promise.resolve(bootstrap || {}); }

    submitForm(form) {
        let formData: FormData = new FormData();
        let xhr: XMLHttpRequest = new XMLHttpRequest();

        for (let key in form) {
            formData.append(key, form[key]);
        }

        xhr.onreadystatechange = () => {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    JSON.parse(xhr.response);
                } else {
                    // observer.error(xhr.response);
                }
            }
        };

        xhr.open('PUT', '/api/experiment', true);
        xhr.send(formData);
    }
}