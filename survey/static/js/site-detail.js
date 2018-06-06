
import Vue from 'vue';
import moment from 'moment';
import VueResource from 'vue-resource'
import jQuery from 'jquery';
import VuejsDialog from "vuejs-dialog"
import 'bootstrap';
// import PNotify from 'pnotify';
import PNotify from '../vendor/pnotify/pnotify.custom.min.js';
window.VueMultiselect = require('../vendor/vue-multiselect/vue-multiselect.min.js')
// import printjs from 'print-js'
//require('../components/daterangepicker.component.js')

require('../css/style.css');
//
// require('../assets/js/vendor/bootstrap-tabdrop.js');
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
                        <div class="row no-gutters">
        <div class="col-md-12">
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb"> 
                    <li class="breadcrumb-item"><a href="url 'core:admin_dashboard' ">Dashboard</a></li>
                    <li class="breadcrumb-item active" aria-current="page"> Detail</li>
                 
                </ol>
            </nav>
        </div>
                <div class="col-md-4 col-lg-3">
                <div class="school-profile bg-white">
                    <div class="profile-head">
                        <img src="assets/img/img-school.png" class="school-logo" alt="">
                        <h4>Harvard University</h4>
                        <span>Cambridge, Massachusetts</span>
                        <div class="text-center margin-top">
                            <div class="btn-group" role="group">
                                <div class="btn-group btn-group-sm" role="group">
                                    <a href="#" id="btnGroupDrop1" class="btn btn-secondary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                       <i class="la la-file-text"></i> Report
                                    </a>
                                    <div class="dropdown-menu" aria-labelledby="btnGroupDrop1">
                                        <a class="dropdown-item" href="#"><i class="la la-reply"></i> View Responses</a>
                                        <a class="dropdown-item" href="#"><i class="la la-list"></i> Generate Report</a>
                                    </div>
                                </div>
                                <div class="btn-group btn-group-sm" role="group">
                                    <a href="#" id="btnGroupDrop2" class="btn btn-secondary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="la la-cogs"></i> Manage
                                    </a>
                                    <div class="dropdown-menu" aria-labelledby="btnGroupDrop2">
                                        <a class="dropdown-item" href="#"><i class="la la-user"></i> People</a>
                                        <a class="dropdown-item" href="#"><i class="la la-tasks"></i> Forms</a>
                                        <a class="dropdown-item" href="#"><i class="la la-cog"></i> Settings</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="progress" style="height: 8px;">
                          <div class="progress-bar bg-secondary" role="progressbar" style="width: 25%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">
                              <span  class="popOver" data-toggle="tooltip" data-placement="top" title="25%"> </span> 
                          </div>
                        </div>
                    </div>
                    <div class="profile-body">
                        <div class="scrolling-wrap">
                            <p>
                                Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took
                            </p>
                            <div class="small-card margin-top">
                                <h6><strong>Engineer Assigned</strong></h6>
                                <ul class="user-list-sm">
                                    <li>
                                        <a href="#" title="">
                                            <img src="assets/img/img-avatar.jpg" alt="">
                                            Bikrant Giri
                                        </a>
                                    </li>
                                    <li>
                                        <a href="#" title="">
                                            <img src="assets/img/img-avatar.jpg" alt="">
                                            Bikrant Giri
                                        </a>
                                    </li>
                                    <li>
                                        <a href="#" title="">
                                            <img src="assets/img/img-avatar.jpg" alt="">
                                            Bikrant Giri
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
                <div class="col-md-8 col-lg-9">
                <div class="dash-right">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="widget-info margin-top-large">
                                <div class="widget-head">
                                    <h4><a href="#" title="">Steps</a></h4>
                                    <a href="#" title="" class="btn btn-sm btn-xs btn-primary" target="_blank"><i class="la la-caret-right"></i> Manage</a>
                                </div>
                                <div class="widget-body overflow-show" data-mh="sd-widget">
                                    <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
                                    <div v-for="step,key in steps"> 
                                     <div v-if="key == 0  ">
                                        <li vclass="nav-item">
                                            <a v-bind:id="'pills-'+ key + '-tab'" v-bind:class="'nav-link ' +{ active: true }"   data-toggle="pill" v-bind:href="'#pills-'+ key" role="tab" aria-controls="pills-step1" aria-selected="true"><i class="la la-exclamation"></i> {{step.name}} </a>
                                        </li>
                                     </div>
                                        <div v-else >
                                        <li class="nav-item">
                                            <a  v-bind:id="'pills-'+ key +'-tab'" v-bind:class="'nav-link '"   data-toggle="pill" v-bind:href="'#pills-'+ key" role="tab" aria-controls="pills-step1" aria-selected="false" ><i class="la la-exclamation"></i> {{step.name}} </a>
                                        </li>
                                        </div>
                                <div>
                                    </ul>

                                </div>
                                    <div class="tab-content" id="pills-tabContent">
                                        <div class="tab-pane fade show active" id="pills-step1" role="tabpanel" aria-labelledby="pills-step1-tab">
                                            <a href="#" title="" class="btn btn-primary btn-xs pull-right"><i class="la la-edit"></i> Edit</a>
                                            <div class="clearfix"></div>
                                            <ul class="steps-checklist margin-top">
                                                <li>
                                                    <i class="la la-check-circle"></i>
                                                    <strong>Household Survey (घरधुरी सर्वेक्षण)</strong>
                                                    <span class="check-info">
                                                        <i class="la la-user" aria-hidden="true"></i>chapakot
                                                        <i class="la la-clock-o" aria-hidden="true"></i> 2 hours, 47 minutes ago
                                                    </span>
                                                </li>
                                                <li>
                                                    <i class="la la-circle"></i>
                                                    <strong>Household Survey (घरधुरी सर्वेक्षण)</strong>
                                                </li>
                                                <li>
                                                    <i class="la la-check-circle"></i>
                                                    <strong>Household Survey (घरधुरी सर्वेक्षण)</strong>
                                                    <span class="check-info">
                                                        <i class="la la-user" aria-hidden="true"></i>chapakot
                                                        <i class="la la-clock-o" aria-hidden="true"></i> 2 hours, 47 minutes ago
                                                    </span>
                                                </li>
                                            </ul>
                                        </div>
                                        <div class="tab-pane fade" id="pills-step2" role="tabpanel" aria-labelledby="pills-step2-tab">2</div>
                                        <div class="tab-pane fade" id="pills-step3" role="tabpanel" aria-labelledby="pills-step3-tab">3</div>
                                        <div class="tab-pane fade" id="pills-step4" role="tabpanel" aria-labelledby="pills-step4-tab">4</div>
                                        <div class="tab-pane fade" id="pills-step5" role="tabpanel" aria-labelledby="pills-step5-tab">5</div>
                                        <div class="tab-pane fade" id="pills-step6" role="tabpanel" aria-labelledby="pills-step6-tab">6</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="widget-info margin-top-large">
                                <div class="widget-head">
                                    <h4><a href="#" title="">Reports</a></h4>
                                    <a href="#" title="" class="btn btn-sm btn-xs btn-primary" target="_blank"><i class="la la-caret-right"></i> More</a>
                                </div>
                                <div class="widget-body" data-mh="sd-widget">
                                    <ul class="submission-list">
                                        <li> 
                                            <img src="assets/img/img-school.png" alt="">
                                            <a title="View submission detail" href="#"><strong>Household Survey (घरधुरी सर्वेक्षण)</strong></a>
                                            <br>
                                            <a href="#" title="View details of user"><small><i class="la la-user"></i>chapakot</small></a>
                                            <small class="site_icon_float" style=""><i class="la la-clock-o" aria-hidden="true"></i> 2 hours, 47 minutes ago</small>
                                        </li>
                                        <li>
                                            <a title="View submission detail" href="#"><strong>Household Survey (घरधुरी सर्वेक्षण)</strong></a>
                                            <br>
                                            <a href="#" title="View details of user"><small><i class="la la-user"></i>chapakot</small></a>
                                            <small class="site_icon_float" style=""><i class="la la-clock-o" aria-hidden="true"></i> 2 hours, 47 minutes ago</small>
                                        </li>
                                        <li>
                                            <img src="assets/img/img-school.png" alt="">
                                            <a title="View submission detail" href="#"><strong>Household Survey (घरधुरी सर्वेक्षण)</strong></a>
                                            <br>
                                            <a href="#" title="View details of user"><small><i class="la la-user"></i>chapakot</small></a>
                                            <small class="site_icon_float" style=""><i class="la la-clock-o" aria-hidden="true"></i> 2 hours, 47 minutes ago</small>
                                        </li>
                                        <li>
                                            <a title="View submission detail" href="#"><strong>Household Survey (घरधुरी सर्वेक्षण)</strong></a>
                                            <br>
                                            <a href="#" title="View details of user"><small><i class="la la-user"></i>chapakot</small></a>
                                            <small class="site_icon_float" style=""><i class="la la-clock-o" aria-hidden="true"></i> 2 hours, 47 minutes ago</small>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-6">
                            <div class="widget-info margin-top-large">
                                <div class="widget-head">
                                    <h4><a href="#" title="">Plans</a></h4>
                                    <a href="#" title="" class="btn btn-sm btn-xs btn-primary" target="_blank"><i class="la la-plus"></i> Add</a>
                                </div>
                                <div class="widget-body no-padding-top" data-mh="sd-widget">
                                    <ul class="row">
                                        <li class="col-md-6">
                                            <a href="#" class="plan-item margin-top" title="Reduce deaths, injuries and economic losses caused by housing and school collapses">
                                                <i class="la la-file-pdf-o color-pdf"></i>
                                                Reduce deaths, injuries and economic losses..
                                            </a>
                                        </li>
                                        <li class="col-md-6">
                                           <a href="#" class="plan-item margin-top" title="Reduce deaths, injuries and economic losses caused by housing and school collapses">
                                                <i class="la la-file-word-o color-word"></i>
                                                Reduce deaths, injuries and economic losses..
                                            </a>
                                        </li>
                                        <li class="col-md-6">
                                            <a href="#" class="plan-item margin-top" title="Reduce deaths, injuries and economic losses caused by housing and school collapses">
                                                <i class="la la-file-excel-o color-excel"></i>
                                                Reduce deaths, injuries and economic losses..
                                            </a>
                                        </li>
                                        <li class="col-md-6">
                                            <a href="#" class="plan-item margin-top" title="Reduce deaths, injuries and economic losses caused by housing and school collapses">
                                                <i class="la la-file-powerpoint-o color-powerpoint"></i>
                                                Reduce deaths, injuries and economic losses..
                                            </a>
                                        </li>
                                        <li class="col-md-6">
                                            <a href="#" class="plan-item margin-top" title="Reduce deaths, injuries and economic losses caused by housing and school collapses">
                                                <i class="la la-file-image-o color-image"></i>
                                                Reduce deaths, injuries and economic losses..
                                            </a>
                                        </li>
                                        <li class="col-md-6">
                                            <a href="#" class="plan-item margin-top" title="Reduce deaths, injuries and economic losses caused by housing and school collapses">
                                                <i class="la la-file-zip-o color-zip"></i>
                                                Reduce deaths, injuries and economic losses..
                                            </a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <div class="col-md-6">
                            <div class="widget-info margin-top-large">
                                <div class="widget-head">
                                    <h4><a href="#" title="">Pictures</a></h4>
                                    <a href="#" title="" class="btn btn-sm btn-xs btn-primary" target="_blank"><i class="la la-caret-right"></i> More</a>
                                </div>
                                <div class="widget-body no-padding-top" data-mh="sd-widget">
                                    <div class="row">
                                            <div class="col-md-4">
                                                <div class="photo-holder photo-item margin-top">
                                                    <img src="http://app.fieldsight.org/media/chapakot/attachments/1521025970023.jpg" img-title="Hello" alt="">
                                                </div>
                                            </div>
                                            <div class="col-md-4">
                                                <div class="photo-holder photo-item margin-top">
                                                    <img src="assets/img/img-gallery.jpg" img-title="Image Title" alt="">
                                                </div>
                                            </div>
                                            <div class="col-md-4">
                                                <div class="photo-holder photo-item margin-top">
                                                    <img src="assets/img/img-gallery.jpg" img-title="Image Title" alt="">
                                                </div>
                                            </div>
                                            <div class="col-md-4">
                                                <div class="photo-holder photo-item margin-top">
                                                    <img src="assets/img/img-gallery.jpg" img-title="Image Title" alt="">
                                                </div>
                                            </div>
                                            <div class="col-md-4">
                                                <div class="photo-holder photo-item margin-top">
                                                    <img src="http://app.fieldsight.org/media/chapakot/attachments/1521025970023.jpg" img-title="Hello" alt="">
                                                </div>
                                            </div>
                                            <div class="col-md-4">
                                                <div class="photo-holder margin-top">
                                                    <a href="all-images.php" title="" class="count-holder">
                                                        <span class="align-middle">100+</span>
                                                    </a>
                                                    <img src="assets/img/img-gallery.jpg" img-title="Image Title" alt="">
                                                </div>
                                            </div>                                          
                                        </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>

        <?php include 'footer.php';?>
        <div class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" id="myModalLabel" aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content modal-lg">
                <div class="modal-header">
                    <h6 class="modal-title">&nbsp;</h6>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                
                </div>
            </div>
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

// $(document).ready(function () {
//             //Height Fix
//             console.log('Love');
//             // schoolWrapHeightFix();
//             window.onresize = function (event) {
//                 schoolWrapHeightFix();
//             }
//             function schoolWrapHeightFix() {
//               var vph = $(window).height();
//                 if ($(document).width() > 479) {
//                     vph = vph - ($("#header").height() + 32 + $(".breadcrumb").outerHeight());
//                     $(".dash-right").css("min-height", vph);

//                     var aboutHeight = vph - ($(".profile-head").outerHeight() + 32);
//                     $(".scrolling-wrap").height(aboutHeight);


//                 } else {
//                     $(".scrolling-wrap").height(190);

//                 }
//             }

//             //Make scroll
//             if ($.fn.niceScroll) {
//                 $(".scrolling-wrap").niceScroll({
//                     cursorcolor: "#5184ac",
//                     cursorborderradius: "0px",
//                     cursorborder: "",
//                     cursorwidth: "8px"
//                 });
//             }

//             $(".school-profile").hover(
//                 function () {
//                     $('[data-toggle="tooltip"]').tooltip({trigger: 'manual'}).tooltip('show');
//                 }, function () {
//                     $('[data-toggle="tooltip"]').tooltip({trigger: 'manual'}).tooltip('hide');
//                 }
//             );

//             $('.nav-tabs, .nav-pills').tabdrop();

//             $('.photo-item img').on('click', function () {
//                 var title = $(this).attr('img-title');
//                 var src = $(this).attr('src');
//                 var img = '<img src="' + src + '" class="img-responsive"/>';
//                 var html = '';
//                 html += img;
//                 $('#myModalLabel').modal();
//                 $('#myModalLabel').on('shown.bs.modal', function () {
//                     $('#myModalLabel .modal-header .modal-title').html(title);
//                     $('#myModalLabel .modal-body').html(html);
//                 })
//                 $('#myModalLabel').on('hidden.bs.modal', function () {
//                     $('#myModalLabel .modal-header .modal-title').html('');
//                     $('#myModalLabel .modal-body').html('');
//                 });
//             });
//         });



// <div class="col-md-12">
//                     <nav aria-label="breadcrumb">
//                       <ol class="breadcrumb">
//                         <li class="breadcrumb-item"><a href="#">Dashboard</a></li>
//                         <li class="breadcrumb-item active" aria-current="page">Site-Details</li>
//                       </ol>
//                     </nav>
//                 </div>
//                      <div class="col-md-8 col-lg-9">
//             <div class="dash-right">
//                 <div class="row">
//                     <div class="col-md-6">
//                         <div class="widget-info margin-top-large">
//                             <div class="widget-head">
//                                 <h4><a href="#" title="">Steps</a></h4>
//                                 <a href="#" title="" class="btn btn-sm btn-xs btn-primary" target="_blank"><i
//                                         class="la la-caret-right"></i> Manage</a>
//                             </div>
//                             <div class="widget-body overflow-show" data-mh="sd-widget">
//                                 <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
//                                     <div v-for="step,key in steps">
//                                         <div {{key}}
//                                             <li class="nav-item">
//                                                 <a class="nav-link active" id="tab-{{ key }}"
//                                                    data-toggle="pill" href="" role="tab"
//                                                     aria-selected="true"><i
//                                                         class="la la-exclamation"></i>{{ step.name }}</a>
//                                             </li>

//                                         <li v-else>
//                                             <li class="nav-item">
//                                             <a class="nav-link" id="tab-{{ key }}" data-toggle="pill"
//                                                href="" role="tab" aria-controls="step-{{ key }}"
//                                                aria-selected="false">{{ steps.name }}</a>
//                                             </li>
                                        
//                                     <!--- <div v-empty="0"<p>No Steps Found.</p> -->

//                                 </ul>
//                                 <div class="tab-content" id="pills-tabContent">
//                                     <div v-for ="step,key in step_list">
//                                         <div v-if key == 0>
//                                             <div class="tab-pane fade show active" id="step-{{ key }}"
//                                                  role="tabpanel" aria-labelledby="tab-{{ key }}">
//                                                 <a href="" title="" class="btn btn-primary btn-xs pull-right"><i
//                                                         class="la la-edit"></i> Edit</a>
//                                                 <div class="clearfix"></div>
//                                                 <ul class="steps-checklist margin-top">
//                                                     <li>
//                                                         <i class="la la-check-circle"></i>
//                                                         <strong>{{ step.name }}</strong>
//                                                         <span class="check-info">
//                                                         <i class="la la-user" aria-hidden="true"></i>Order: {{ step.order }}
//                                                         <i class="la la-clock-o" aria-hidden="true"></i>{{ step.site }}
//                                                     </span>
//                                                     </li>
//                                                 </ul>
//                                             </div>
//                                         <else>
//                                             <div class="tab-pane fade" id="step-{{ key }}" role="tabpanel"
//                                                  aria-labelledby="tab-{{ key }}">{{ step.name }}
//                                                 <a href="" title="" class="btn btn-primary btn-xs pull-right"><i
//                                                         class="la la-edit"></i> Edit</a>
//                                                 <div class="clearfix"></div>
//                                                 <ul class="steps-checklist margin-top">
//                                                     <li>
//                                                         <i class="la la-check-circle"></i>
//                                                         <strong>Name: {{ step.name }}</strong>
//                                                         <span class="check-info">
//                                                         <i class="la la-user" aria-hidden="true"></i>{{ step.order }}
//                                                         <i class="la la-clock-o" aria-hidden="true"></i>{{ step.site }}
//                                                     </span>
//                                                     </li>
//                                                 </ul>
//                                             </div>
                                        
                                    
//                                 </div>
//                             </div>
//                         </div>
//                     </div>
//                         <div class="col-md-6">
//                         <div class="widget-info margin-top-large">
//                             <div class="widget-head">
//                                 <h4><a href="#" title="">Reports</a></h4>
//                                 <a href="#" title="" class="btn btn-sm btn-xs btn-primary" target="_blank"><i
//                                         class="la la-caret-right"></i> More</a>
//                             </div>
//                             <div class="widget-body" data-mh="sd-widget">
//                                 <ul class="submission-list">
//                                      <li v-for="report in reports">
//                                      <li>
//                                             <img src="{{ MEDIA_URL }}{{ report.photo }}" alt="">
//                                             <a title="View submission detail"
//                                                href="#"><strong>{{ report.checklist }}</strong></a>
//                                             <br>
//                                             <a href="#" title="View details of user">
//                                                 <small><i class="la la-user"></i>{{ report.user }}</small>
//                                             </a>
//                                             <small class="site_icon_float" style=""><i class="la la-clock-o"
//                                                                                        aria-hidden="true"></i>{{ report.date }}
//                                             </small>
//                                         </li>
//                                         </li>
//                                     <div v-empty >
//                                         No Reports Found.

                                     
//                                 </ul>
//                             </div>
//                         </div>











//                 </div>