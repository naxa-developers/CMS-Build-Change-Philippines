import Vue from 'vue';
import moment from 'moment';
import jQuery from 'jquery';
// import PNotify from 'pnotify';
import PNotify from '../vendor/pnotify/pnotify.custom.min.js';
import PopperJs from '../../node_modules/popper.js/dist/popper.js';

require('../assets/css/style.css');
//
//require('../assets/js/vendor/modernizr-2.8.3-respond-1.4.2.min.js');

//require('../../node_modules/popper.js/dist/popper.js');
//require('../assets/js/vendor/bootstrap.min.js');
import 'bootstrap';
require('../assets/js/vendor/jquery.nicescroll.min.js');
require('../assets/js/plugins.js');
window.PNotify = PNotify;
window.$ = jQuery;
const channels = require('../vendor/js/websocket.js')



//window.Survey = new Vue({
//  el: '#app',
//  template:`
//            <div> {{message}}</div>
//                `,
//  data: {
//    message: 'Hello Vue!'
//  }
//})


// The routing fires all common scripts, followed by the page specific scripts.
// Add additional events for more control over timing e.g. a finalize event
