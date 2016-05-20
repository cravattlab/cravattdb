declare var bootstrap: any;

import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class SideloadService {
    getData() { return Promise.resolve(bootstrap || {}); }

    submitForm(form) {
        // var formData = new FormData();

        // for (var key in this.data) {
        //     formData.append(key, this.data[key]);
        // }

        // // https://uncorkedstudios.com/blog/multipartformdata-file-upload-with-angularjs
        // $http.put(
        //     '/api/experiment',
        //     formData,
        //     {
        //         transformRequest: angular.identity,
        //         headers: { 'Content-Type': undefined }
        //     }
        // );
    }
}