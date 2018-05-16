const path = require("path")
const webpack = require('webpack')
let config = require('./webpack.base.config.js')
const CleanWebpackPlugin = require('clean-webpack-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker')

const uglifyOptions = {
  minimize: true,
  // cache: false,
  parallel: true,
  mangle: false,
  sourcemap: true,
  output: {
    comments: false,
    beautify: false,
  },
};

let pathsToClean = [
  'dist',
];

// the clean options to use
let cleanOptions = {
  // root:     path.resolve('./static/'),
  exclude: [],
  verbose: true,
  dry: false,
  preview: true
};

config.output.path = path.resolve('./static/dist')


config.plugins = [new BundleTracker({ filename: './webpack-stats.json' })].concat(config.plugins)

config.plugins.concat([

  // removes a lot of debugging code
  new webpack.DefinePlugin({
    'process.env': {
      'NODE_ENV': JSON.stringify('production')
    }
  }),


  // new CleanWebpackPlugin(pathsToClean,cleanOptions),

  // keeps hashes consistent between compilations
  // new webpack.optimize.OccurenceOrderPlugin(),

  new webpack.optimize.UglifyJsPlugin(uglifyOptions)
  // new UglifyJsPlugin(uglifyOptions)


])

//use babel traspiler
config.module.rules.push({
  test: /\.js$/,
  // exclude: /(node_modules|bower_components)/,
  exclude: /(node_modules|bower_components|assets) /,
  use: {
    loader: 'babel-loader',
    options: {
      presets: ['es2015']
    }
  }
})

module.exports = config
