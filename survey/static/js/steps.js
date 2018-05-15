import Vue from 'vue';
import moment from 'moment';
import VueResource from 'vue-resource'
import jQuery from 'jquery';
// import PNotify from 'pnotify';
import PNotify from '../vendor/pnotify/pnotify.custom.min.js';
window.VueMultiselect = require('../vendor/vue-multiselect/vue-multiselect.min.js')
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
    template: `
<div>
    <div class="row no-gutters">
            <div class="col-md-4 col-lg-3">
                <div class="module-school-list">
                    <div class="school-wrap">
                        <ul class="school-list">
                        <li>
                                <a href="#" title="">
                                     <img src="assets/img/img-school.png" class="school-logo" alt="">
                                    <a href="javascript:void(0)"  title="" @click="newStep()"  class="btn btn-sm btn-xs btn-primary" ><i class="la la-plus"></i> Add New Step </a>
                                </a>
                            </li>
                            <li v-for="s in steps">
                                <a href="javascript:void(0)"  title="" @click="step=s">
                                     <img  :src= 'img_url' class="school-logo" alt="">
                                    <h6>{{s.name}}</h6>
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-md-8 col-lg-9">
                <div class="dash-right" v-show="show_content">
                    <div class="row" >
                        <div class="col-md-12">
                            <div class="widget-info margin-top-large">
                                <div class="widget-head">
                                    <h4><a href="#" title="" >
                                    <span v-show="step.hasOwnProperty('id')"> {{step.name}}</span>
                                    <span v-show="!step.hasOwnProperty('id')"> New Step</span>
                                    </a></h4>
                                    <a href="javascript:void(0)"  title="" @click="newChecklist()"  class="btn btn-sm btn-xs btn-primary" ><i class="la la-plus"></i>New  Checklist</a>
                                    <a href="javascript:void(0)"  title="" @click="editStep()"  class="btn btn-sm btn-xs btn-primary"
                                    v-show="step.hasOwnProperty('id')"><i class="la la-plus"></i>Edit Step</a>
                                </div>
                                <div class="widget-body" >
                                            <form v-if="show_form">
                                            <legend>Step Form</legend>
                                                  <div class="form-group">
                                                    <label for="name">Name(English)</label>
                                                    <input type="text" v-model="step.name" class="form-control" id="name" aria-describedby="nameHelp" placeholder="Enter Step Name">
                                                    <small id="nameHelp" class="form-text text-muted"> Enter step name in english.</small>
                                                  </div>
                                                  <div class="form-group">
                                                    <label for="lname">Name(local)</label>
                                                    <input type="text" v-model="step.localname" class="form-control" id="lname"
                                                        aria-describedby="nameHelp" placeholder=" local Language step name">
                                                    <small id="nameHelp" class="form-text text-muted"> Enter step name in local Language</small>
                                                  </div>
                                                   <a href="javascript:void(0)"  title=""
                                                   class="btn btn-sm btn-primary" @click="saveStep()" v-show="step.name.length>0"><i class="la la-plus"></i> Save Step</a>
                                                   <a href="javascript:void(0)"  title=""
                                                   class="btn btn-sm btn-warning" @click="show_form=false" v-show="step.name.length>0"><i class="la la-plus"></i> Close</a>
                                                </form>
                                                 <form v-show="show_checklist_form">
                                                 <legend>Checklist Form</legend>
                                                      <div class="form-group">
                                                        <label for="name">Text(English)</label>
                                                        <input type="text" v-model="checklist.text" class="form-control" id="name" aria-describedby="nameHelp"
                                                        placeholder="Enter Checklist Text">
                                                        <small id="nameHelp" class="form-text text-muted"> Enter step name in english.</small>
                                                      </div>
                                                      <div class="form-group">
                                                        <label for="lname">Text(local)</label>
                                                        <input type="text" v-model="checklist.localtext" class="form-control" id="lname"
                                                            aria-describedby="nameHelp" placeholder=" local Language Checklist Text">
                                                        <small id="nameHelp" class="form-text text-muted"> Enter Checklist Text in local Language</small>
                                                      </div>
                                                      <div class="form-group">
                                                                <label>Material:</label>
                                                                <vselect :options="materials" label="title" :value="''" v-model="material" :allow-empty="true"
                                                                 :select-label="''" :show-labels="false" :internal-search="true"  :placeholder="'Select Material'">
                                                                <template slot="noResult">No such Material</template>
                                                                </vselect>
                                                      </div>
                                                       <a href="javascript:void(0)"  title=""
                                                       class="btn btn-sm btn-primary" @click="saveChecklist()" v-show="valid_checklist"><i class="la la-plus"></i> Save Checklist</a>
                                                       <a href="javascript:void(0)"  title=""
                                                       class="btn btn-sm btn-warning" @click="show_checklist_form=false"><i class="la la-plus"></i> Close</a>
                                                    </form>
                                                <div class="form-group" v-show="checklists.length>0 && !show_checklist_form ">
                                                    <table class="table">
                                                              <thead>
                                                                <tr>
                                                                  <th scope="col">Checklist</th>
                                                                  <th scope="col">Name</th>
                                                                  <th scope="col">Local Name</th>
                                                                  <th scope="col">Material</th>
                                                                  <th scope="col">Actions</th>
                                                                </tr>
                                                              </thead>
                                                              <tbody>
                                                                <tr v-for="c, index in checklists">
                                                                  <th scope="row">{{index+1}}</th>
                                                                  <td>{{c.text}}</td>
                                                                  <td>{{c.localtext}}</td>
                                                                  <td>{{c.material}}</td>
                                                                  <td></td>
                                                                  </tr>

                                                              </tbody>
                                                            </table>
                                                </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    <div v-if="!loading && steps.length<1">
        Currently No steps.
    </div>
     <div v-if="loading">
        loading steps ....
    </div>



</div>
                `,
    data: {
        template_data: template_data,
        steps: [],
        step: {},

        checklists: [],
        checklist: {},
        materials: [],
        material: {},

        show_form: false,
        show_content: false,
        show_checklist: false,
        show_checklist_form: false,

        loading: false,
        error: '',
        img_url: '/static/assets/img/img-school.png',
    },
    methods: {
        getSteps: function () {

            var self = this;
            self.loading = true;
            function successCallback(response) {
                self.steps = response.body;
                self.loading = false;
            }

            function errorCallback() {
                console.log('failed');
                self.loading = false;
            }

            self.$http.get('/core/api/step-list/'+ self.template_data.pk+'/' , {
                    params: {}
                }).then(successCallback, errorCallback);

        },
        getMaterials: function () {

            var self = this;
            self.loading = true;
            function successCallback(response) {
                self.materials = response.body;
                self.loading = false;
            }

            function errorCallback() {
                console.log('failed');
                self.loading = false;
            }

            self.$http.get('/core/api/material-list/'+ self.template_data.project+'/' , {
                    params: {}
                }).then(successCallback, errorCallback);

        },
        getChecklists: function () {

            var self = this;
            self.loading = true;
            function successCallback(response) {
                self.checklists = response.body;
                if(response.body.length <= 0){
                    self.show_checklist_form = true;
                }
                self.loading = false;
            }

            function errorCallback() {
                console.log('failed');
                self.loading = false;
            }

            self.$http.get('/core/api/checklist-list/'+ self.step.id+'/' , {
                    params: {}
                }).then(successCallback, errorCallback);

        },
        editStep: function(){
            var self = this;
            self.show_form = true;
            self.show_checklist = false;
        },
        getStep: function (step) {

            var self = this;
            self.loading = true;
            function successCallback(response) {
                self.step = response.body;
                self.show_content = true;
                self.show_checklist = true;
                self.show_form = false;
                self.loading = false;
            }

            function errorCallback() {
                console.log('failed');
                self.loading = false;
            }

            self.$http.get('/core/api/step/' +
                step.id + '/', {
                    params: {}
                }).then(successCallback, errorCallback);

        },
        newStep: function () {
            var self = this;
            self.step = {
                name: '',
                localname: '',
            },
            self.show_form = true;
           self. show_content= true;
            self.show_checklist= false;
        },
        newChecklist: function () {
            var self = this;
            self.checklist = {
                text: '',
                localtext: '',
            };
            self.show_checklist_form = true;
        },

        saveStep: function () {
            var self = this;
            let csrf = $('[name = "csrfmiddlewaretoken"]').val();
            let options = { headers: { 'X-CSRFToken': csrf } };
            if (!self.step.hasOwnProperty("id")) {

                if (self.template_data.is_project == 1) {
                    self.step.project = self.template_data.pk;
                }
                if (self.template_data.is_project == 0) {
                    self.step.site = self.template_data.pk;
                }
                self.step.order = self.steps.length + 1;
                function successCallback(response) {

                    self.error = "";
                    new PNotify({
                        title: 'Saved',
                        text: 'Step ' + response.body.name + ' Saved'
                    });
                    console.log(response.body);
                    self.steps.push(response.body);
                    self.step = response.body;
                    self.show_form = false;
                    self.show_checklist = true;
                    //        self.heightLevel();
                }

                function errorCallback(response) {
                    console.log(response.body);
                    new PNotify({
                        title: 'failed',
                        text: 'Failed to Save Step',
                        type: 'error'
                    });

                }
                //            console.log(self.step);
                self.$http.post('/core/api/step/', self.step, options).then(successCallback, errorCallback);
            }
            else {
                function successCallback(response) {
                    let index = self.steps.findIndex(x => x.id == response.body.id);
                    Vue.set(self.steps, index, response.body);

                    self.error = "";
                    new PNotify({
                        title: 'Updated',
                        text: 'Step ' + response.body.name + ' Updated'
                    });
                    self.show_form = false;
                    self.step = response.body;
                    self.show_checklist = true;
                    //        self.heightLevel();
                }

                function errorCallback(response) {
                    console.log(response.body);
                    new PNotify({
                        title: 'failed',
                        text: 'Failed to Update Step',
                        type: 'error'
                    });

                }
                self.$http.put('/core/api/step/' + self.step.id + '/', self.step, options).then(successCallback, errorCallback);

            }

        },
        saveChecklist: function () {
            var self = this;
            let csrf = $('[name = "csrfmiddlewaretoken"]').val();
            let options = { headers: { 'X-CSRFToken': csrf } };
            self.checklist.step = self.step.id;
            if(self.material.hasOwnProperty('id')){
                self.checklist.material = self.material.id;
            }
            if (!self.checklist.hasOwnProperty("id")) {


                self.checklist.order = self.checklists.length + 1;
                function successCallback(response) {

                    self.error = "";
                    new PNotify({
                        title: 'Saved',
                        text: 'Checklist ' + response.body.text + ' Saved'
                    });
                    self.checklists.push(response.body);
                    self.checklist = response.body;
                    self.show_checklist_form = false;
                    self.show_checklist = true;
                    //        self.heightLevel();
                }

                function errorCallback(response) {
                    console.log(response.body);
                    new PNotify({
                        title: 'failed',
                        text: 'Failed to Save Checklist',
                        type: 'error'
                    });

                }
                //            console.log(self.step);
                self.$http.post('/core/api/checklist/', self.checklist, options).then(successCallback, errorCallback);
            }
            else {
                function successCallback(response) {
                    let index = self.checklists.findIndex(x => x.id == response.body.id);
                    Vue.set(self.checklists, index, response.body);

                    self.error = "";
                    new PNotify({
                        title: 'Updated',
                        text: 'checklist ' + response.body.title + ' Updated'
                    });
                    self.show_checklist_form = false;
                    self.checklist = response.body;
                    self.show_checklist = true;
                    //        self.heightLevel();
                }

                function errorCallback(response) {
                    console.log(response.body);
                    new PNotify({
                        title: 'failed',
                        text: 'Failed to Update Checklist',
                        type: 'error'
                    });

                }
                self.$http.put('/core/api/checklist/' + self.checklist.id + '/', self.step, options).then(successCallback, errorCallback);

            }

        },
        deleteStep: function (pk) {
            var self = this;
        },


    },

    watch: {
        step: function (newVal, oldVal) {
            var self = this;
            if(newVal.hasOwnProperty("id")){
                self.checklists = [];
                self.checklist = {};
                self.getChecklists();
                self.show_content = true;
                self.show_checklist_form = false;

            }
        },
    },

    mixins: [],
    components: {
        'vselect': VueMultiselect.default,
    },

    created: function () {
        var self = this;
        self.getSteps();
        self.getMaterials();
    },
    computed: {
        valid_checklist: function () {
            var self = this;
            let valid = true;
            if(!self.checklist.hasOwnProperty('text')){
                return false;
            }
            if(!self.checklist.hasOwnProperty('localtext')){
                return false;
            }

            if(self.checklist.localtext.length ==0 || self.checklist.text.length ==0){
                return false;
            }

            return valid;
    },
  },
})


// The routing fires all common scripts, followed by the page specific scripts.
// Add additional events for more control over timing e.g. a finalize event
