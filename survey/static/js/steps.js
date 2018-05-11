import Vue from 'vue';
import moment from 'moment';
import VueResource from 'vue-resource'
import jQuery from 'jquery';
// import PNotify from 'pnotify';
import PNotify from '../vendor/pnotify/pnotify.custom.min.js';
//window.VueMultiselect = require('../../vendor/vue-multiselect/vue-multiselect.min.js')
// import printjs from 'print-js'
//require('../components/daterangepicker.component.js')
require('../css/style.css');
//
require('../bower_components/bootstrap/js/dropdown');
require('../bower_components/bootstrap/js/modal');
require('../bower_components/bootstrap/js/tab');
window.PNotify = PNotify;
window.$ = jQuery;
const channels = require('../vendor/js/websocket.js')

Vue.use(VueResource);
//Vue.use(VueMultiselect);



window.Steps = new Vue({
  el: '#app',
  template:`
            <div> {{message}}
                <button v-bind:disabled="isButtonDisabled">Button</button>
            </div>
                `,
  data: {
    message: 'Hello Vue!  Steps',
    template_data : template_data,
    steps:[],
    step:{},
    isButtonDisabled: true,
    show_form:false,
  },
  methods: {
    loadSteps: function () {
      // `this` loads steps from server

       var self = this;
        function successCallback(response) {
          self.steps = response.body;
        }

        function errorCallback() {
          console.log('failed');
        }
        self.$http.get('/core/api/steps/' +
        self.template_data.is_project + '/' +
        self.template_data.pk+'/', {
          params: {}
        }).then(successCallback, errorCallback);

    },

    saveStep: function () {
        var self = this;
        let csrf = $('[name = "csrfmiddlewaretoken"]').val();
        let options = {headers: {'X-CSRFToken':csrf}};

        function successCallback (response){

        self.error = "";
            new PNotify({
          title: 'Saved',
          text: 'Step '+ response.body.name + ' Saved'
        });
        console.log(response.body);
        self.steps.push(response.body);
        self.show_form = false;
//        self.heightLevel();
        }

        function errorCallback (response){
        console.log(response.body);
          new PNotify({
          title: 'failed',
          text: 'Failed to Save Step',
          type: 'error'
        });

        }
       self.$http.post('/api/steps/', self.step, options).then(successCallback, errorCallback);


    },

    },

    watch: {
        step: function (newVal, oldVal) {
            var self = this;
        },
        },

    mixins: [],

    created: function () {
        var self = this;
        self.loadSteps();
        }
})


// The routing fires all common scripts, followed by the page specific scripts.
// Add additional events for more control over timing e.g. a finalize event
