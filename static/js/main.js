'use strict';

var app = angular.module('cravatt-ip2', ['ngRoute', 'ngResource', 'angularFileUpload']);

app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    $locationProvider.html5Mode(true);
    $routeProvider.when('/', {
        templateUrl: '/static/partials/index.html',
        controller: 'MainController',
        controllerAs: 'main'
    });
}]);

app.controller('MainController', ['$scope', '$http', 'FileUploader', function($scope, $http, FileUploader) {
    console.log('hello world');
    this.data = {
    	files: []
    };

    this.submit = function() {
        $http.post('/search/' + this.data.name, this.data).success(function(data) {
            console.log(data);
        }.bind(this));
    };

    var uploader = $scope.uploader = new FileUploader();
    this.uploadCompleted = false;
    // mix in ng-file-upload queue with files thave have already been uploaded
    this.flatQueue = function() {
        return this.data.files.concat(uploader.queue);
    }

    uploader.onCompleteAll = function() {
        this.uploadCompleted = true;
    }.bind(this);
}]);

$(function() {
	$('.ui.dropdown').dropdown();
});