'use strict';

var app = angular.module('cravattdb', ['ngRoute', 'ngResource', 'ngFileUpload']);

app.value('bootstrap', window.bootstrap || {});

app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    $locationProvider.html5Mode(true);
    $routeProvider.when('/', {
        templateUrl: '/static/partials/index.html',
        controller: 'MainController',
        controllerAs: 'main'
    }).when('/status', {
        templateUrl: '/static/partials/status.html',
        controller: 'StatusController',
        controllerAs: 'status'
    }).when('/sideload', {
       templateUrl: '/static/partials/sideload.html',
       controller: 'SideloadController',
       controllerAs: 'sideload' 
    });
}]);

app.controller('MainController', ['$scope', '$http', 'Upload', function($scope, $http, Upload) {
    this.data = {};
    this.progress = 0;
    this.showErrors = true;
    this.errors = [];

    this.submit = function() {
        var upload = Upload.upload({
            url: '/search/' + this.data.name,
            file: this.files,
            method: 'POST',
            sendFieldsAs: 'json-blob',
            fields: this.data
        }).success(function (data, status, headers, config) {
            console.log(data, status, headers, config)
        }).progress(function(e) {
            this.progress = parseInt(100.0 * e.loaded / e.total);
        }.bind(this));

        upload.catch(function(data) {
            console.log(data)
            if (data.data.hasOwnProperty('error')) {
                var message = data.data.error;
                this.showErrors = true;

                if (data.status === 401) {
                    message = 'Incorrect username or password';
                } else if (data.status === 409) {
                    message = 'Dataset already exists';
                }
                
                if (this.errors.indexOf(message) === -1) {
                    this.errors.push(message);
                }
            }


        }.bind(this));
    };
}]);

app.controller('StatusController', ['$scope', '$http', function($scope, $http) {

}]);

app.controller('SideloadController', ['$scope', '$http', 'bootstrap', function($scope, $http, bootstrap) {
    this.bootstrap = bootstrap || {};

    this.submit = function() {
        $http.put('/api/experiment', this.data);
    }.bind(this);
}]);

// http://ng.malsup.com/#!/titlecase-filter
app.filter('titlecase', function() {
    return function(s) {
        s = ( s === undefined || s === null ) ? '' : s;
        return s.toString().toLowerCase().replace( /\b([a-z])/g, function(ch) {
            return ch.toUpperCase();
        });
    };
});

$(function() {
    $('.ui.dropdown').dropdown();
});