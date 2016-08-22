var webpack = require('webpack');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var helpers = require('./helpers');

module.exports = {
  entry: {
    'polyfills': './config/polyfills.ts',
    'vendor': './config/vendor.ts',
    'app': './app/main.ts'
  },

  resolve: {
    extensions: ['', '.js', '.ts'],
    alias: {
        'semantic-ui-css': 'semantic-ui-css/semantic.js'
    }
  },

  module: {
    loaders: [
      {
        test: /\.ts$/,
        loaders: ['ts', 'angular2-template-loader']
      }, {
        test: /\.html$/,
        loader: 'html'
      }, {
        test: /\.(png|jpe?g|gif|svg|woff|woff2|ttf|eot|ico)$/,
        loader: 'file?name=assets/[name].[hash].[ext]'
      }, {
        test: /\.css$/,
        include: helpers.root('app'),
        loader: 'raw'
      }
    ]
  },

  plugins: [
    new webpack.optimize.CommonsChunkPlugin({
      name: ['app', 'vendor', 'polyfills']
    }),

    new HtmlWebpackPlugin({
      inject: true,
      template: 'templates/index.html',
      filename: '../../templates/index.html'
    }),

    new webpack.ProvidePlugin({
        chroma: 'chroma-js',
        jQuery: 'jquery',
        jquery: 'jquery',
        $: 'jquery'
    })
  ]
};