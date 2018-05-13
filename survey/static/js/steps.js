import Vue from 'vue';
import moment from 'moment';
import jQuery from 'jquery';
// import PNotify from 'pnotify';
import PNotify from '../vendor/pnotify/pnotify.custom.min.js';

require('../css/style.css');
//
require('../bower_components/bootstrap/js/dropdown');
require('../bower_components/bootstrap/js/modal');
require('../bower_components/bootstrap/js/tab');
window.PNotify = PNotify;
window.$ = jQuery;
const channels = require('../vendor/js/websocket.js')



window.Steps = new Vue({
  el: '#app',
  template:`
            <div> {{message}}</div>
                `,
  data: {
    message: 'Hello Vue!  Steps',
    template_data : template_data,
  }
})


// The routing fires all common scripts, followed by the page specific scripts.
// Add additional events for more control over timing e.g. a finalize event
