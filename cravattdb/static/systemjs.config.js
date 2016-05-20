(function(global) {

  // map tells the System loader where to look for things
  var map = {
    'app':                        'static/app', // 'dist',
    'lodash':                     'static/node_modules/lodash',
    // 'rxjs':                       'static/node_modules/rxjs',
    // 'angular2-in-memory-web-api': 'static/node_modules/angular2-in-memory-web-api',
    '@angular':                   'static/node_modules/@angular'
  };

  // packages tells the System loader how to load when no filename and/or no extension
  var packages = {
    'app':                        { main: 'main.js',  defaultExtension: 'js' },
    // 'rxjs':                       { defaultExtension: 'js' },
    'angular2-in-memory-web-api': { defaultExtension: 'js' },
    'lodash':                     { main: 'lodash.js', defaultExtension: 'js' }
  };

  var packageNames = [
    '@angular/common',
    '@angular/compiler',
    '@angular/core',
    '@angular/http',
    '@angular/platform-browser',
    '@angular/platform-browser-dynamic',
    '@angular/router',
    '@angular/testing'
  ];

  // add package entries for angular packages in the form '@angular/common': { main: 'index.js', defaultExtension: 'js' }
  // packageNames.forEach(function(pkgName) {
  //   packages[pkgName] = { main: 'index.js', defaultExtension: 'js' };
  // });

  packageNames.forEach(function(pkgName) {
    var name = pkgName.indexOf('/')>0 ? pkgName.split('/')[1] : pkgName; 
    packages[pkgName] = { main: name + '.umd.js', defaultExtension: 'js' };
  });

  var config = {
    map: map,
    packages: packages
  }

  // filterSystemConfig - index.html's chance to modify config before we register it.
  if (global.filterSystemConfig) { global.filterSystemConfig(config); }

  System.config(config);

})(this);