var webpack = require('webpack');
var HtmlWebpackPlugin = require('html-webpack-plugin')
var AddAssetHtmlPlugin = require('add-asset-html-webpack-plugin');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var ForkCheckerPlugin = require('awesome-typescript-loader').ForkCheckerPlugin;
var HappyPack = require('happypack');
var helpers = require('./helpers');

module.exports = {
  entry: [
    './config/polyfills.ts',
    './config/vendor.ts',
    './app/main.ts'
  ],

  output: {
    path: helpers.root('dist'),
    publicPath: 'http://localhost:3000/',
    filename: 'bundle.js'
  },

  resolve: {
    // resolve module file requests by looking for explicit extensions
    // or look for matching files with .js or .ts extensions
    extensions: ['', '.js', '.ts']
  },

  module: {
    loaders: [
      {
        test: /\.ts$/,
        loaders: ['awesome-typescript-loader', '@angularclass/hmr-loader','angular2-template-loader'],
      },
      {
        test: /\.html$/,
        loader: 'raw',
        happy: { id: 'raw' }
      },
      // handle component-scoped styles specified with styleUrls
      {
        test: /\.css$/,
        include: helpers.root('app'),
        loader: 'raw',
        happy: { id: 'raw' }
      }
    ]
  },

  plugins: [
    new ExtractTextPlugin('[name].css'),
    new webpack.DllReferencePlugin({
      context: '.',
      manifest: require(helpers.root('dist', 'vendor-manifest.json'))
    }),
    new webpack.DllReferencePlugin({
      context: '.',
      manifest: require(helpers.root('dist', 'polyfills-manifest.json'))
    }),
    new HtmlWebpackPlugin({
      inject: true,
      template: 'app/index.html',
      filename: '../../templates/index.html'
    }),
    new AddAssetHtmlPlugin([
      { filepath: 'dist/polyfills.dll.js', includeSourcemap: false },
      { filepath: 'dist/vendor.dll.js', includeSourcemap: false }
    ]),
    new ForkCheckerPlugin(),
    new webpack.ProvidePlugin({
      chroma: 'chroma-js',
      jQuery: 'jquery',
      jquery: 'jquery',
      $: 'jquery'
    }),
    new HappyPack({ id: 'raw' })
  ],

  devServer: {
    host: '0.0.0.0',
    port: 3000,
    profile: true,
    progress: true
  },
  // needed for dev work in a network share from a VM
  watchOptions: {
    poll: true
  }
};
