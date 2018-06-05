import Vue from 'vue';
import moment from 'moment';
import VueResource from 'vue-resource'
import jQuery from 'jquery';
import VuejsDialog from "vuejs-dialog"
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
Vue.use(VuejsDialog);
//Vue.use(VueMultiselect);




window.Survey = new Vue({
    el: '#app',
    template: `
                <div>
                    <div class="row no-gutters">
                    {{steps}}
                    <br>
                    </div>
                    <br>
                    {{reports}}
                    <br>
<div>
                    <br>
                    {{documents}}
                    <br>
                    <br>
                    {{materials}}
                    <br>
                    </div>

                            <div class="col-md-12">
                    <nav aria-label="breadcrumb">
                      <ol class="breadcrumb">
                        <li class="breadcrumb-item"><a href="#">Dashboard</a></li>
                        <li class="breadcrumb-item active" aria-current="page">Site-Details</li>
                      </ol>
                    </nav>
                </div>
                     <div class="col-md-8 col-lg-9">
            <div class="dash-right">
                <div class="row">
                    <div class="col-md-6">
                        <div class="widget-info margin-top-large">
                            <div class="widget-head">
                                <h4><a href="#" title="">Steps</a></h4>
                                <a href="#" title="" class="btn btn-sm btn-xs btn-primary" target="_blank"><i
                                        class="la la-caret-right"></i> Manage</a>
                            </div>
                            <div class="widget-body overflow-show" data-mh="sd-widget">
                                <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
                                    <div v-for="step in steps">
                                        
                                            <li class="nav-item">
                                                <a class="nav-link active" id="tab-{{ forloop.counter0 }}"
                                                   data-toggle="pill" href="" role="tab"
                                                    aria-selected="true"><i
                                                        class="la la-exclamation"></i>{{ step.name }}</a>
                                            </li>

                                        <li v-else>
                                            <li class="nav-item">
                                            <a class="nav-link" id="tab-{{ forloop.counter0 }}" data-toggle="pill"
                                               href="" role="tab" aria-controls="step-{{ forloop.counter0 }}"
                                               aria-selected="false">{{ steps.name }}</a>
                                            </li>
                                        <endif>
                                    <div v-if="v-empty"<p>No Steps Found.</p>
                                    
                                </ul>
                                <div class="tab-content" id="pills-tabContent">
                                    <div v-for step in step_list>
                                        <div v-if forloop.counter0 == 0>
                                            <div class="tab-pane fade show active" id="step-{{ forloop.counter0 }}"
                                                 role="tabpanel" aria-labelledby="tab-{{ forloop.counter0 }}">
                                                <a href="" title="" class="btn btn-primary btn-xs pull-right"><i
                                                        class="la la-edit"></i> Edit</a>
                                                <div class="clearfix"></div>
                                                <ul class="steps-checklist margin-top">
                                                    <li>
                                                        <i class="la la-check-circle"></i>
                                                        <strong>{{ step.name }}</strong>
                                                        <span class="check-info">
                                                        <i class="la la-user" aria-hidden="true"></i>Order: {{ step.order }}
                                                        <i class="la la-clock-o" aria-hidden="true"></i>{{ step.site }}
                                                    </span>
                                                    </li>
                                                </ul>
                                            </div>
                                        <else>
                                            <div class="tab-pane fade" id="step-{{ forloop.counter0 }}" role="tabpanel"
                                                 aria-labelledby="tab-{{ forloop.counter0 }}">{{ step.name }}
                                                <a href="" title="" class="btn btn-primary btn-xs pull-right"><i
                                                        class="la la-edit"></i> Edit</a>
                                                <div class="clearfix"></div>
                                                <ul class="steps-checklist margin-top">
                                                    <li>
                                                        <i class="la la-check-circle"></i>
                                                        <strong>Name: {{ step.name }}</strong>
                                                        <span class="check-info">
                                                        <i class="la la-user" aria-hidden="true"></i>{{ step.order }}
                                                        <i class="la la-clock-o" aria-hidden="true"></i>{{ step.site }}
                                                    </span>
                                                    </li>
                                                </ul>
                                            </div>
                                        
                                    
                                </div>
                            </div>
                        </div>
                    </div>
                        <div class="col-md-6">
                        <div class="widget-info margin-top-large">
                            <div class="widget-head">
                                <h4><a href="#" title="">Reports</a></h4>
                                <a href="#" title="" class="btn btn-sm btn-xs btn-primary" target="_blank"><i
                                        class="la la-caret-right"></i> More</a>
                            </div>
                            <div class="widget-body" data-mh="sd-widget">
                                <ul class="submission-list">
                                     <li v-for="report in reports">
                                     <li>
                                            <img src="{{ MEDIA_URL }}{{ report.id }}" alt="">
                                            <a title="View submission detail"
                                               href="#"><strong>{{ report.id }}</strong></a>
                                            <br>
                                            <a href="#" title="View details of user">
                                                <small><i class="la la-user"></i>{{ report.step_id }}</small>
                                            </a>
                                            <small class="site_icon_float" style=""><i class="la la-clock-o"
                                                                                       aria-hidden="true"></i>{{ report.date }}
                                            </small>
                                        </li>
                                        </li>
                                    <div v-empty >
                                        No Reports Found.

                                     
                                </ul>
                            </div>
                        </div>











                </div>
                `,
    data: {
        steps: [],
        reports:[],
        documents:[],
        materials:[],

        step: {},
        report:{},
        document:{},
        material:{},
        loading: false,
        error: '',
        template_data: template_data,
    },
    methods: {

        getStep: function () {

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

            self.$http.get('/core/api/step-list/' + 1 + '/', {
                params: {}
            }).then(successCallback, errorCallback);
            console.log(steps);
        },

        getReport: function() {

            var self=this;
            self.loading=true;

            function successCallback(response) {
                self.reports= response.body;
                self.loading= false;

            }

            function errorCallback() {
                console.log('failed');
                self.loading= false;
            }
            self.$http.get('/core/api/report/' + 1 + '/',{
                params:{}
            }).then(successCallback, errorCallback);
        },
        getDocument: function() {

            var self=this;
            self.loading=true;

            function successCallback(response) {
                self.documents= response.body;
                self.loading= false;

            }

            function errorCallback() {
                console.log('failed');
                self.loading= false;
            }
            self.$http.get('/core/api/site-documents/' + 1 + '/',{
                params:{}
            }).then(successCallback, errorCallback);
        },
        getMaterial: function() {

            var self=this;
            self.loading=true;

            function successCallback(response) {
                self.materials= response.body;
                self.loading= false;

            }

            function errorCallback() {
                console.log('failed');
                self.loading= false;
            }
            self.$http.get('/core/api/material-list/' + 1 + '/',{
                params:{}
            }).then(successCallback, errorCallback);
        },
        
    },
        created: function () {
        var self = this;
        self.getMaterial();
        self.getDocument();
        self.getReport();
        self.getStep();
        
        
    },

});


// The routing fires all common scripts, followed by the page specific scripts.
// Add additional events for more control over timing e.g. a finalize event
