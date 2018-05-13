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
<div>
    <a href="javascript:void(0)"  title="" class="btn btn-sm btn-primary" @click="show_form=true"><i class="la la-plus"></i> New Step</a>
    <div v-for="s  in steps" v-if="!loading">
        {{s.name}}
    </div>

    <div v-if="!loading && steps.length<1">
        Currently No steps.
    </div>
     <div v-if="loading">
        loading steps ....
    </div>

    <div v-if="show_form">
        <form>
              <div class="form-group">
                <label for="name">Step Name</label>
                <input type="text" v-model="step.name" class="form-control" id="name" aria-describedby="nameHelp" placeholder="Enter Step Name">
                <small id="nameHelp" class="form-text text-muted"> Enter Step Name</small>
              </div>
              <div class="form-group">
              <label> Checklists</label>
                <li v-for ="ci in step.checklist">{{ci}}</li>
              </div>
              <div class="form-group">
                <label for="checklist">New Checklist Item</label>
                <input type="text" v-model="checklist_item" class="form-control" id="checklist" placeholder="Checklist Item">
                <a href="javascript:void(0)"  title="" class="btn btn-sm btn-primary" @click="adChecklist()"><i class="la la-plus"></i> Add  to Checklist</a>
              </div>
               <a href="javascript:void(0)"  title="" class="btn btn-sm btn-primary" @click="saveStep()" v-show="step.name.length>0"><i class="la la-plus"></i> Save Step</a>
            </form>
    </div>

</div>
                `,
  data: {
    message: 'Hello Vue!  Steps',
    template_data : template_data,
    steps:[],
    step:{'name':'', checklist:[]},
    checklist_item: '',
    isButtonDisabled: true,
    show_form:false,
    loading: false,
  },
  methods: {
    loadSteps: function () {

       var self = this;
       self.loading =  true;
        function successCallback(response) {
          self.steps = response.body;
          self.loading =  false;
        }

        function errorCallback() {
          console.log('failed');
          self.loading = false;
        }

        self.$http.get('/core/api/list-steps/' +
        self.template_data.is_project + '/' +
        self.template_data.pk+'/', {
          params: {}
        }).then(successCallback, errorCallback);

    },

    saveStep: function () {
        var self = this;
        let csrf = $('[name = "csrfmiddlewaretoken"]').val();
        let options = {headers: {'X-CSRFToken':csrf}};
        if (self.template_data.is_project == 1){
            self.step.project = self.template_data.pk;
        }
        if (self.template_data.is_project == 0){
            self.step.sites = self.template_data.pk;
        }
        self.step.order = self.steps.length +1;
        function successCallback (response){

        self.error = "";
            new PNotify({
          title: 'Saved',
          text: 'Step '+ response.body.name + ' Saved'
        });
        console.log(response.body);
        self.steps.push(response.body);
        self.show_form = false;
        self.step = {'name':'', checklist:[]};
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
        console.log(self.step);
        console.log(options);
       self.$http.post('/core/api/steps/', self.step, options).then(successCallback, errorCallback);


    },
    updateStep: function(step){
        var self = this;
    },
    deleteStep: function(pk){
        var self = this;
    },
    adChecklist: function(){
        var self = this;
        if(self.checklist_item.length>0){
            self.step.checklist.push(self.checklist_item);
            self.checklist_item = "";

        }
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
