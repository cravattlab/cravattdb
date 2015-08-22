'use strict';

var app = angular.module('cravatt-ip2', ['ngRoute', 'ngResource', 'ngFileUpload']);

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
            if (data.status === 401) {
                var message = 'Incorrect username or password';
                this.showErrors = true;

                if (this.errors.indexOf(message) === -1) {
                    this.errors.push(message);
                }
            }
        }.bind(this));
    };
}]);

app.controller('StatusController', ['$scope', '$http', function($scope, $http) {

}]);

$(function() {
    $('.ui.dropdown').dropdown();
});