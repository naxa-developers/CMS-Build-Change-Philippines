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
                                <a href="#" title="">
                                     <img  :src= 'img_url' class="school-logo" alt="">
                                    <h6>{{s.name}}</h6>
                                    <span @click="getStep(s)">Detail</span>
                                    <span @click="getStep(s)">Checklists</span>
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
                                    <a href="javascript:void(0)"  title="" @click="newStep()"  class="btn btn-sm btn-xs btn-primary" ><i class="la la-plus"></i>New  Checklist</a>
                                    <a href="javascript:void(0)"  title="" @click="editStep()"  class="btn btn-sm btn-xs btn-primary"
                                    v-show="step.hasOwnProperty('id')"><i class="la la-plus"></i>Edit Step</a>
                                </div>
                                <div class="widget-body" >
                                            <form v-if="show_form">
                                                  <div class="form-group">
                                                    <label for="name">Name(English)</label>
                                                    <input type="text" v-model="step.name" class="form-control" id="name" aria-describedby="nameHelp" placeholder="Enter Step Name">
                                                    <small id="nameHelp" class="form-text text-muted"> Enter step name in english.</small>
                                                  </div>
                                                  <div class="form-group">
                                                    <label for="lname">Name(local)</label>
                                                    <input type="text" v-model="step.localName" class="form-control" id="lname"
                                                        aria-describedby="nameHelp" placeholder=" local Language step name">
                                                    <small id="nameHelp" class="form-text text-muted"> Enter step name in local Language</small>
                                                  </div>
                                                  <div class="form-group" v-show="false">
                                                  <label> Checklists</label>
                                                    <li v-for ="ci in step.checklist">{{ci}}</li>
                                                  </div>
                                                  <div class="form-group" v-show="false">
                                                    <label for="checklist">New Checklist Item</label>
                                                    <input type="text" v-model="checklist_item" class="form-control" id="checklist" placeholder="Checklist Item">
                                                    <a href="javascript:void(0)"  title="" class="btn btn-sm btn-primary" @click="adChecklist()" v-show="checklist_item.length>0">
                                                    <i class="la la-plus"></i> Add  to Checklist</a>
                                                  </div>
                                                   <a href="javascript:void(0)"  title="" class="btn btn-sm btn-primary" @click="saveStep()" v-show="step.name.length>0"><i class="la la-plus"></i> Save Step</a>
                                                   <a href="javascript:void(0)"  title="" class="btn btn-sm btn-warning" @click="show_form=false" v-show="step.name.length>0"><i class="la la-plus"></i> Close</a>
                                                </form>
                                                <div class="form-group" v-show="show_checklist">
                                                    <table class="table">
                                                              <thead>
                                                                <tr>
                                                                  <th scope="col">Checklist</th>
                                                                  <th scope="col">Name</th>
                                                                  <th scope="col">Local Name</th>
                                                                  <th scope="col">Material</th>
                                                                </tr>
                                                              </thead>
                                                              <tbody>
                                                                <tr>
                                                                  <th scope="row">1</th>
                                                                  <td>Mark</td>
                                                                  <td>Otto</td>
                                                                  <td>@mdo</td>
                                                                </tr>
                                                                <tr>
                                                                  <th scope="row">2</th>
                                                                  <td>Jacob</td>
                                                                  <td>Thornton</td>
                                                                  <td>@fat</td>
                                                                </tr>
                                                                <tr>
                                                                  <th scope="row">3</th>
                                                                  <td>Larry</td>
                                                                  <td>the Bird</td>
                                                                  <td>@twitter</td>
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
        message: 'Hello Vue!  Steps',
        template_data: template_data,
        steps: [],
        step: {},
        checklist_item: {},
        isButtonDisabled: true,
        show_form: false,
        show_content: false,
        show_checklist: false,
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

            self.$http.get('/core/api/list-steps/' +
                self.template_data.is_project + '/' +
                self.template_data.pk + '/', {
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

            self.$http.get('/core/api/steps/' +
                step.id + '/', {
                    params: {}
                }).then(successCallback, errorCallback);

        },
        newStep: function () {
            var self = this;
            self.step = {
                name: '',
                localName: '',
                checklist: []
            },
                self.checklist_item = {};
            self.show_form = true;
           self. show_content= true;
            self.show_checklist= false;
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
                    self.step.sites = self.template_data.pk;
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
                console.log(options);
                self.$http.post('/core/api/steps/', self.step, options).then(successCallback, errorCallback);
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
                self.$http.put('/core/api/steps/' + self.step.id + '/', self.step, options).then(successCallback, errorCallback);

            }

        },
        deleteStep: function (pk) {
            var self = this;
        },
        adChecklist: function () {
            var self = this;
            if (self.checklist_item.length > 0) {
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
        self.getSteps();
    }
})


// The routing fires all common scripts, followed by the page specific scripts.
// Add additional events for more control over timing e.g. a finalize event
