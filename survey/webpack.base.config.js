var path = require("path")
var webpack = require('webpack')
//const BundleBuddyWebpackPlugin = require("bundle-buddy-webpack-plugin");
var CommonsChunkPlugin = require("webpack/lib/optimize/CommonsChunkPlugin");
var CleanObsoleteChunks = require('webpack-clean-obsolete-chunks');
var WebpackMd5Hash = require('webpack-md5-hash');
const ExtractTextPlugin = require("extract-text-webpack-plugin");//to extract css into separate css files
module.exports = {
  context: __dirname,

  entry: {
    // rare: './static/css/style.css',
    vendor_stylesheets: ['./static/css/vendor.css'],
    main: ['./static/js/survey'], // entry point of our app. assets/js/index.js should require other js modules and dependencies it needs
//    dashboard: ['./static/js/dashboard-report.js'],

  },

  output: {
    path: path.resolve('./static/build/'),
    filename: '[name]-[chunkhash].js',

      // filename: "[name].js?v=[hash]",
  },

  plugins: [
  new webpack.ProvidePlugin({
    'window.Quill': 'quill'
  }),
    new webpack.IgnorePlugin(/^\.\/locale$/, /moment/),
    new webpack.ProvidePlugin({
      jQuery: 'jquery',
      $: 'jquery'
    }),
    new ExtractTextPlugin({
      // filename: '[name]-[contenthash].css?v=[chunkhash]-name',
      filename: '[name]-[contenthash].css',
      disable:false,
      allChunks: true
    }),
  //    new ExtractTextPlugin("styles.css"),
    // new webpack.optimize.ModuleConcatenationPlugin(),
    // new BundleBuddyWebpackPlugin({sam: true}),
    new CommonsChunkPlugin({
      name: 'main',
      chunks: ["main", "dashboard"],
      minChunks:2
    }),
    // new CommonsChunkPlugin({
    //   name: 'vendor',
    //   minChunks: 2,
    // }),
    new CleanObsoleteChunks({verbose: true, deep: true}),
    new WebpackMd5Hash()



  ],

  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js' // 'vue/dist/vue.common.js' for webpack 1
    },
    extensions: ['.ts', '.js']
  },

  module: {
    rules: [
    {
      test: /\.js$/,
      exclude: /node_modules(?!\/quill-image-drop-module|quill-image-resize-module)/,
      loader: 'babel-loader',
    },

      {
        test: /\.css$/,
        use: ExtractTextPlugin.extract({
          fallback: "style-loader",
          use: {
            loader: "css-loader",
            options: {
              sourceMap: true
            }
          },
          // publicPath: "./static/build/"
        })
      },
      {
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
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        loader: "file-loader"
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          extractCSS: true,
          loaders: {
            js: 'babel-loader!eslint-loader'
          }
        }
      }
    ]
  },
  resolveLoader: {
    alias: {
      'scss-loader': 'sass-loader'
    }
  }
}
