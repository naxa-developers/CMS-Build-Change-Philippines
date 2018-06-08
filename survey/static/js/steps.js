import Vue from 'vue';
import jQuery from 'jquery';
window.$ = jQuery;
window.jQuery = jQuery;
import 'bootstrap';
require('../assets/css/style.css');
require('../assets/js/vendor/jquery.nicescroll.min.js');
require('../assets/js/plugins.js');

import VueResource from 'vue-resource'
import VuejsDialog from "vuejs-dialog"
import PNotify from '../vendor/pnotify/pnotify.custom.min.js';
window.PNotify = PNotify;
window.VueMultiselect = require('../vendor/vue-multiselect/vue-multiselect.min.js')
// import printjs from 'print-js'
//require('../components/daterangepicker.component.js')
require('../css/style.css');
//
require('../bower_components/bootstrap/js/dropdown');
require('../bower_components/bootstrap/js/modal');
require('../bower_components/bootstrap/js/tab');
const channels = require('../vendor/js/websocket.js')

Vue.use(VueResource);
Vue.use(VuejsDialog);
//Vue.use(VueMultiselect);

	$(document).ready(function(){
        	console.log("hello");
                //Height Fix
                schoolWrapHeightFix();
                window.onresize = function(event) {
                    schoolWrapHeightFix();
                }

                function schoolWrapHeightFix() {
                   var  vph = $(window).height();
                    if($(document).width() > 479) {
                        vph = vph - ($("#header").height() + 16);
                        $(".school-wrap").height(vph);
                    }else{
                        vph = ( vph / 1.5 ) - ($("#header").height() + 16);
                        $(".school-wrap").height(vph);
                    }
                }
                //Make it scroll
        		if ($.fn.niceScroll) {
        		console.log("scroll");
                    $(".school-wrap").niceScroll({
                        cursorcolor: "#FFF",
                        cursorborderradius: "0px",
                        cursorborder:"",
                        cursorwidth: "8px"
                    });
                }
        	});


window.Steps = new Vue({
    el: '#app',
    template: `
<div>
    <div class="row no-gutters">
             <div class="col-md-12">
                <nav aria-label="breadcrumb">
                  <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="javascript:void(0)"  title="Dashboard" v-bind:href="template_data.dashboard_url">Dashboard</a></li>
                    <li class="breadcrumb-item active" aria-current="page">Steps</li>
                  </ol>
                </nav>
            </div>
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
                                    <a href="javascript:void(0)"  title="" @click="newChecklist()"  class="btn btn-sm btn-xs btn-primary"
                                    v-show="step.hasOwnProperty('id')"><i class="la la-plus"></i>New  Checklist</a>
                                    <a href="javascript:void(0)"  title="" @click="editStep()"  class="btn btn-sm btn-xs btn-primary"
                                    v-show="step.hasOwnProperty('id')"><i class="la la-edit"></i>Edit Step</a>
                                </div>
                                <div class="widget-body" >
                                            <form v-if="show_form && !show_checklist_form">
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
                                                   class="btn btn-sm btn-primary" @click="saveStep()" v-show="valid_step"><i class="la la-plus"></i> Save Step</a>
                                                   <a href="javascript:void(0)"  title=""
                                                   class="btn btn-sm btn-warning" @click="show_form=false" v-show="valid_step"><i class="la la-plus"></i> Close</a>
                                                     <a href="javascript:void(0)"  title=""
                                                   class="btn btn-sm btn-danger" @click="deleteStep()" v-show="step.hasOwnProperty('id')"><i class="la la-trash"></i> Delete</a>
                                                </form>
                                                 <form v-show="show_checklist_form && !show_form">
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
                                                <div class="form-group" v-show="checklists.length>0 && !show_checklist_form  && !show_form">
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
                                                                  <td>
                                                                  <a href="javascript:void(0)"  title=""
                                                                        class="btn btn-xs" @click="" v-show="c.material"><i class="la la-eye"></i> {{c.materials.title}} </a>
                                                                  </td>
                                                                  <td>
                                                                  <a href="javascript:void(0)"  title=""
                                                       class="btn btn-sm btn-primary" @click="editChecklist(c)"><i class="la la-edit"></i>  </a>
                                                        <a href="javascript:void(0)"  title=""
                                                       class="btn btn-sm btn-danger" @click="deleteChecklist(c.id)"><i class="la la-trash"></i>  </a>

                                                                  </td>
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

            self.$http.get('/core/api/step-list/' + self.template_data.pk + '/', {
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

            self.$http.get('/core/api/material-list/' + self.template_data.project + '/', {
                params: {}
            }).then(successCallback, errorCallback);

        },
        getChecklists: function () {

            var self = this;
            self.loading = true;
            function successCallback(response) {
                self.checklists = response.body;
                if (response.body.length <= 0) {
                    self.show_checklist_form = true;
                }
                self.loading = false;
            }

            function errorCallback() {
                console.log('failed');
                self.loading = false;
            }

            self.$http.get('/core/api/checklist-list/' + self.step.id + '/', {
                params: {}
            }).then(successCallback, errorCallback);

        },
        editStep: function () {
            var self = this;
            self.show_form = true;
            self.show_checklist = false;
            self.show_checklist_form = false;
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
            self.show_content = true;
            self.show_checklist = false;
            self.show_checklist_form = false;
        },
        newChecklist: function () {
            var self = this;
            self.checklist = {
                text: '',
                localtext: '',
            };
            self.show_checklist_form = true;
            self.show_form = false;
        },
         editChecklist: function (c) {
            var self = this;
            self.checklist = c;
            self.show_checklist_form = true;
            self.show_form = false;
            if(self.checklist.material){
                console.log(self.checklist);
                var material = self.materials.filter(x => x.id === self.checklist.material)[0];

                self.material = material;
            }else{
            self.material  = {};
            }
        },

        saveStep: function () {
            var self = this;
            var csrf = $('[name = "csrfmiddlewaretoken"]').val();
            var options = { headers: { 'X-CSRFToken': csrf } };
            console.log(self.step);
            if (!self.step.hasOwnProperty("id")) {

                if (self.template_data.is_project == 1) {
                    self.step.project = self.template_data.pk;
                }
                if (self.template_data.is_project == 0) {
                    self.step.site = self.template_data.pk;
                }
                self.step.order = self.steps.length + 1;
                function successCallback(response) {
                console.log(response.body, "sucess  ");

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
                console.log(response.body);
                    var index = self.steps.findIndex(x => x.id == response.body.id);
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
            var csrf = $('[name = "csrfmiddlewaretoken"]').val();
            var options = { headers: { 'X-CSRFToken': csrf } };
            self.checklist.step = self.step.id;
            if (self.material.hasOwnProperty('id')) {
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
                            console.log(self.checklist);
                self.$http.post('/core/api/checklist/', self.checklist, options).then(successCallback, errorCallback);
            }
            else {
                function successCallback(response) {
                    var index = self.checklists.findIndex(x => x.id == response.body.id);
                    Vue.set(self.checklists, index, response.body);

                    self.error = "";
                    new PNotify({
                        title: 'Updated',
                        text: 'checklist ' + response.body.text + ' Updated'
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
                self.$http.put('/core/api/checklist/' + self.checklist.id + '/', self.checklist, options).then(successCallback, errorCallback);

            }

        },
        deleteStep: function () {
            var self = this;
            var csrf = $('[name = "csrfmiddlewaretoken"]').val();
            var options = { headers: { 'X-CSRFToken': csrf } };
            var message = {
                'title': 'Please Confirm Deletion',
                'body': 'Deleting Steps will Delete All Checklist and its Submission'
            }
            var id = self.step.id;
            var url = "/core/api/step/" + id + "/";
            var data = options;

            function errorCallback(response) {
                console.log(response.body);
                new PNotify({
                    title: 'failed',
                    text: 'Failed to delete step',
                    type: 'error'
                });
            }

            function successCallback(response) {
                self.step = {};
                self.show_content = false;
                self.show_form = false;
                var index = self.steps.findIndex(x => x.id==id);
                self.steps.splice(index, 1);
                new PNotify({
                    title: 'deleted',
                    text: 'Step deleted',
                });

            }

            self.$dialog.confirm(message)
                .then(function () {
                    self.$http.delete(url, options).then(successCallback, errorCallback);
                })
                .catch(function () {
                    console.log('Clicked on cancel')
                });
        },
        deleteChecklist: function (id) {
            var self = this;
            var csrf = $('[name = "csrfmiddlewaretoken"]').val();
            var options = { headers: { 'X-CSRFToken': csrf } };
            var message = {
                'title': 'Please Confirm Deletion',
                'body': 'Deleting  checklist  deletes its  Submission'
            }
            var url = "/core/api/checklist/" + id + "/";
            var data = options;

            function errorCallback(response) {
                console.log(response.body);
                new PNotify({
                    title: 'failed',
                    text: 'Failed to delete checklist',
                    type: 'error'
                });
            }

            function successCallback(response) {
                self.step = {};
                var index = self.checklists.findIndex(x => x.id==id);
                self.checklists.splice(index, 1);
                new PNotify({
                    title: 'deleted',
                    text: 'checklist deleted',
                });

            }

            self.$dialog.confirm(message)
                .then(function () {
                    self.$http.delete(url, options).then(successCallback, errorCallback);
                })
                .catch(function () {
                    console.log('Clicked on cancel')
                });
        },


    },

    watch: {
        step: function (newVal, oldVal) {
            var self = this;
            if (newVal.hasOwnProperty("id")) {
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
            var valid = true;
            if (!self.checklist.hasOwnProperty('text')) {
                return false;
            }
            if (!self.checklist.hasOwnProperty('localtext')) {
                return false;
            }

            if (self.checklist.localtext.length == 0 || self.checklist.text.length == 0) {
                return false;
            }

            return valid;
        },
        valid_step: function () {
            var self = this;
            var valid = true;
            if (!self.step.hasOwnProperty('name')) {
                return false;
            }
            if (!self.step.hasOwnProperty('localname')) {
                return false;
            }

            if (self.step.localname.length == 0 || self.step.name.length == 0) {
                return false;
            }

            return valid;
        },
    },
})


// The routing fires all common scripts, followed by the page specific scripts.
// Add additional events for more control over timing e.g. a finalize event
