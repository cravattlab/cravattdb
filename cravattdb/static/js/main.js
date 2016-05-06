'use strict';

var app = angular.module('cravattdb', ['ngRoute', 'ngResource', 'ngFileUpload', 'file-model']);

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
    }).when('/experiments', {
        templateUrl: '/static/partials/experiments.html',
        controller: 'ExperimentsController',
        controllerAs: 'experiments'
    }).when('/dataset/:experimentId', {
        templateUrl: '/static/partials/dataset.html',
        controller: 'DatasetController',
        controllerAs: 'dataset'
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

app.controller('DatasetController', [
    '$scope',
    'bootstrap',
    '$http',
    '$routeParams',
    'DTOptionsBuilder',
    'DTColumnBuilder',
    '$resource',
function($scope, bootstrap, $http, $routeParams, DTOptionsBuilder, DTColumnBuilder, $resource) {

    this.ratioMin = 0;
    this.ratioMax = 20;

    this.dtOptions = DTOptionsBuilder
        .fromSource('/api/dataset/' + $routeParams.id)
        .withFnServerData(function (sSource, aoData, fnCallback, oSettings) {
            oSettings.jqXHR = $.ajax({
                'dataType': 'json',
                'url': sSource,
                'data': aoData,
                'success': function(data) {
                    data = orderData(data.dataset.data);
                    // le monkey patch
                    fnCallback.call(this, data);
                }
            });
        })
        .withBootstrap();

    function orderData(data) {
        var lastId,
            lastIndex = 0,
            ratios = [];

        function mean(arr) {
            var sum = 0;
            for (var i = 0, n = arr.length; i < n; i++) {
                sum += arr[i];
            }
            return sum/arr.length;
        }

        // sort data based on UniprotKB identifier
        // for grouping by protein
        data.sort(function(a, b) {
            if (a[1] > b[1]) return 1;
            else if (a[1] < b[1]) return -1;
            else return 0;
        }).forEach(function(item, i, arr) {
            // new group
            if (lastId !== item[1]) {
                // add mean ratio to each row of previous group
                for (; lastIndex < i; lastIndex++) {
                    arr[lastIndex].push(mean(ratios));
                }

                // reset ratios
                ratios = [ item[7] ];
                // implicit lastIndex = i;
            // same group so keep adding to ratios
            } else {
                ratios.push(item[7]);
            }

            lastId = item[1];
        });

        for (; lastIndex < data.length; lastIndex++) {
            data[lastIndex].push(mean(ratios));
        }

        return data;
    }

    setDefaults(this.dtOptions);

    this.dtOptions.aoColumns = extractColumns(["peptide_index", "ipi", "symbol", "sequence", "mass", "charge", "segment", "ratio", "meanRatio"]);

    function setDefaults(options) {
        options.pageLength = 25;
        // options.paging = false;
        options.autoWidth = true;
        options.lengthMenu = [ [10, 25, 50, -1], [10, 25, 50, "All"] ];
        options.deferRender = true;
        options.order = [[ 8, 'desc' ]],
        options.columnDefs = [{
            'visible': false,
            'targets': [1, 2, 8]
        }];

        options.fnDrawCallback = function (settings) {
            var api = this.api();
            var rows = api.rows( {page:'current'} );
            var rowsNodes = rows.nodes();
            var rowsData = rows.data();
            var last = null;

            // if (api.order() !== 2) return;

            api.column(1, {page:'current'} ).data().each( function ( group, i ) {
                var row = rowsData[i],
                    symbol = row[2],
                    meanRatio = row[8];

                // starting a new group
                if ( last !== group ) {
                    $(['<tr class="group">',
                        '<td colspan="1">', group, '</td>',
                        '<td colspan="4">', symbol, '</td>',
                        '<td colspan="1">', meanRatio.toFixed(2), '</td>',
                    '</tr>'].join('')).insertBefore($(rowsNodes).eq(i));

                    last = group;
                }
            });
        }
    }

    function extractColumns(headers) {
        var columns = [];
        for (var i = 0, n = headers.length; i < n; i++) {
            columns.push({ sTitle: headers[i] });
        }
        return columns;
    }

    var self = this;


    $scope.$on('event:dataTableLoaded', function(event, loadedDT) {
        // loadedDT.DataTable is the DataTable API instance
        // loadedDT.dataTable is the jQuery Object
        // See http://datatables.net/manual/api#Accessing-the-API
        self.loadedDT = loadedDT;

        $scope.$watch('dataset.ratioMin', _.debounce(function(newValue, oldValue) {
            self.loadedDT.DataTable.draw();
        }, 200));

        $scope.$watch('dataset.ratioMax', _.debounce(function(newValue, oldValue) {
            self.loadedDT.DataTable.draw();
        }, 200));
    });

    $.fn.dataTable.ext.search.push(
        function( settings, data, dataIndex ) {
            var min = self.ratioMin;
            var max = self.ratioMax;
            console.log(min, max);
            var ratio = parseFloat( data[8] ) || 0; // use data for the ratio column

            if ( ( isNaN( min ) && isNaN( max ) ) ||
                 ( isNaN( min ) && ratio <= max ) ||
                 ( min <= ratio   && isNaN( max ) ) ||
                 ( min <= ratio   && ratio <= max ) )
            {
                return true;
            }
            return false;
        }
    );
}]);

app.controller('ExperimentsController', ['$scope', 'bootstrap', '$location', '$http', function($scope, bootstrap, $location, $http) {
    this.bootstrap = bootstrap || {};
    this.predicate = '';

    this.sorter = function(item) {
        return item[this.predicate];
    }.bind(this);

    this.showDataset = function(id) {
        $location.path('/dataset/' + id);
    };
}]);

app.controller('SideloadController', ['$scope', '$http', 'bootstrap', function($scope, $http, bootstrap) {
    this.bootstrap = bootstrap || {};

    this.submit = function() {
        var formData = new FormData();

        for (var key in this.data) {
            formData.append(key, this.data[key]);
        }

        // https://uncorkedstudios.com/blog/multipartformdata-file-upload-with-angularjs
        $http.put(
            '/api/experiment',
            formData,
            {
                transformRequest: angular.identity,
                headers: { 'Content-Type': undefined }
            }
        );
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