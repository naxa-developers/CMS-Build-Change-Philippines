const path = require("path")
const webpack = require('webpack')
// const CleanWebpackPlugin = require('clean-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker')
let config = require('./webpack.base.config.js')

// const ExtractTextPlugin = require("extract-text-webpack-plugin");//to extract css into separate css files
/*
let envConfig = {
  cleanOptions: {
    root: path.resolve('./static/'),
    exclude: [],
    verbose: true,
    dry: true,
    preview: true
  },
  pathsToClean : [
    'build'
  ]
};
*/
// the clean options to use
// console.log(config.output)
Object.keys(config.entry).forEach(key => {
  config.entry[key].push('webpack/hot/only-dev-server')
  config.entry[key].push('webpack-dev-server/client?http://0.0.0.0:8080' )
})
/*
vendor_stylesheets: ['./static/css/vendor.css', 'webpack/hot/only-dev-server', 'webpack-dev-server/client?http://0.0.0.0:8080'],
    main: ['./static/js/rare', 'webpack/hot/only-dev-server', 'webpack-dev-server/client?http://0.0.0.0:8080'], // entry point of our app. assets/js/index.js should require other js modules and dependencies it needs
    dashboard:['./static/js/dashboard-report.js', 'webpack/hot/only-dev-server', 'webpack-dev-server/client?http://0.0.0.0:8080'],
    report:['./static/js/matches/ad_reports.js', 'webpack/hot/only-dev-server', 'webpack-dev-server/client?http://0.0.0.0:8080'],
    channel_detail:['./static/js/channel_detail.js', 'webpack/hot/only-dev-server', 'webpack-dev-server/client?http://0.0.0.0:8080'],
    channel_schedule:['./static/js/channel_schedule.js', 'webpack/hot/only-dev-server', 'webpack-dev-server/client?http://0.0.0.0:8080'],
    notification_history:['./static/js/notification.js', 'webpack/hot/only-dev-server', 'webpack-dev-server/client?http://0.0.0.0:8080'],
 */

config.output.path = path.resolve('./static/build')
config.output.filename = '[name]-[hash].js'
// config.output['publicPath'] = "/static/build/"
config.output.publicPath = 'http://localhost:8080/' // need to run npm run devserver first

// const BundleBuddyWebpackPlugin = require("bundle-buddy-webpack-plugin");

config.devServer = {
  headers: {
    "Access-Control-Allow-Origin": "*" 
  },
  hot: true,
  // inline: true,
  contentBase: config.output.path
}
config.plugins = [new BundleTracker({ filename: './webpack-stats-local.json' })].concat(config.plugins)

config.plugins.concat([
  new BundleTracker({ filename: './webpack-stats-local.json' }),
  // new BundleBuddyWebpackPlugin({sam: true}),
  new webpack.HotModuleReplacementPlugin(),
  new webpack.NoErrorsPlugin(), // don't reload if there is an error
  // new ExtractTextPlugin({
  //     // filename: 'css/rare-[name].css?[chunkhash]-[contenthash]-name',
  //     filename: 'css/rare.css',
  //     disable:false,
  //     allChunks: true
  //   }),
  // new CleanWebpackPlugin(pathsToClean,cleanOptions),

  /*
  new webpack.optimize.UglifyJsPlugin({
    // minimize: true,
    // cache: false,
    parallel: true,
    mangle:false,
    sourcemap: true,
    output: {
      comments: true,
      beautify: true,
    },
  })
  */

])

config.resolve['alias'] = config.resolve.alias || {}
config.resolve['alias']['vue$'] = 'vue/dist/vue.esm.js' // 'vue/dist/vue.common.js' for webpack 1
config.resolve['extensions'] = ['.ts', '.js']

// config.module.rules.push(
// {
//         test: /\.css$/,
//         use: ExtractTextPlugin.extract({
//           fallback: "style-loader",
//           use: {
//             loader: "css-loader",
//             options: {
//               sourceMap: true
//             }
//           },
//           publicPath: "../"
//         })
//       }
// )


config.module.rules.push({
    test: /\.(gif|png|jpe?g|svg)$/i,
    use: [
      'file-loader',
      {
        loader: 'image-webpack-loader',
        options: {
          bypassOnDebug: true,
        },
      },
    ],
  })

module.exports = config
