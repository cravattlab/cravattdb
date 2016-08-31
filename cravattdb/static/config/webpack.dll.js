var webpack = require('webpack');

module.exports = {
  entry: {
    'polyfills': [ './config/polyfills.ts' ],
    'vendor': [ './config/vendor.ts' ]
  },

  resolve: {
    alias: {
        'semantic-ui-css': 'semantic-ui-css/semantic.js'
    }
  },

  output: {
    filename: '[name].dll.js',
    path: 'dist/',

    // The name of the global variable which the library's
    // require() function will be assigned to
    library: '[name]',
  },

  plugins: [
    new webpack.DllPlugin({
      // The path to the manifest file which maps between
      // modules included in a bundle and the internal IDs
      // within that bundle
      path: 'dist/[name]-manifest.json',
      // The name of the global variable which the library's
      // require function has been assigned to. This must match the
      // output.library option above
      name: '[name]'
    }),
    new webpack.ProvidePlugin({
      chroma: 'chroma-js',
      jQuery: 'jquery',
      jquery: 'jquery',
      $: 'jquery'
    })
  ]
};
