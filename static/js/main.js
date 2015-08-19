'use strict';

var app = angular.module('cravatt-ip2', ['ngRoute', 'ngResource', 'ngFileUpload']);

app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    $locationProvider.html5Mode(true);
    $routeProvider.when('/', {
        templateUrl: '/static/partials/index.html',
        controller: 'MainController',
        controllerAs: 'main'
    });
}]);

app.controller('MainController', ['$scope', '$http', 'Upload', function($scope, $http, Upload) {
    this.data = {};
    this.progress = 0;

    this.submit = function() {
        var upload = Upload.upload({
            url: '/search/' + this.data.name,
            file: this.files,
            method: 'POST',
            sendFieldsAs: 'json-blob',
            fields: this.data
        }).success(function (data, status, headers, config) {
            console.log(data, status, headers, config)
        }).error(function (data, status, headers, config) {
            console.log('error status: ' + status);
        }).progress(function(e) {
            this.progress = parseInt(100.0 * e.loaded / e.total);
        }.bind(this));
    };
}]);

$(function() {
    $('.ui.dropdown').dropdown();
});