import Vue from 'vue';
import moment from 'moment';
import jQuery from 'jquery';
// import PNotify from 'pnotify';
import PNotify from '../vendor/pnotify/pnotify.custom.min.js';
import PopperJs from '../../node_modules/popper.js/dist/popper.js';

require('../assets/css/style.css');
//
//require('../assets/js/vendor/modernizr-2.8.3-respond-1.4.2.min.js');

import 'bootstrap';
require('../assets/js/vendor/jquery.nicescroll.min.js');
require('../assets/js/plugins.js');
window.PNotify = PNotify;
window.$ = jQuery;
const channels = require('../vendor/js/websocket.js')



window.Survey = new Vue({
 el: '#app',
 template:`<div> {{message}} </div>

           <div> {{template_data}}</div>
           <div class="row no-gutters">
        <div class="col-md-12">
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb" v-if="request.user.is_superuser">
                    <li class="breadcrumb-item"><a href="url 'core:admin_dashboard'">Dashboard</a></li>
                    <li class="breadcrumb-item">
                    <a href=" url 'core:project_dashboard' <span v-show="step.hasOwnProperty('id')"> object.project.pk"> {{ object.project }}
                        Dashboard></a></li>
                    <li class="breadcrumb-item active" aria-current="page">{{ object }} Detail</li>
                <div v-else-if >
                    <li class="breadcrumb-item"><a href="url 'core:project_dashboard' project.pk">Dashboard</a>
                    </li>
                    <li class="breadcrumb-item active" aria-current="page">{{ object }} Detail</li>
                
                </ol>
            </nav>
            <li v-for="document in documents">
                                
                                     
                                    <h6>{{document}}</h6>

                                </a>
                            </li>
            </div>
            </d
        </div>
               `,
   data: {
    message:"Hello Vue",
        template_data: template_data,
        documents:[],
        document:{},

       

        loading: false,
        error: '',
    },
    methods: {
       
        getDocuments: function () {

            var self = this;
            self.loading = true;
            function successCallback(response) {
                self.documents = response.body;
            }

            function errorCallback() {
                console.log('failed');
                self.loading = false;
            }

            self.$http.get('/core/api/site-documents/' + self.template_data.site_id + '/', {
                params: {}
            }).then(successCallback, errorCallback);

        },
       

   

    created: function () {
        var self = this;
        self.getDocuments();
    },

        
    },
})

// The routing fires all common scripts, followed by the page specific scripts.
// Add additional events for more control over timing e.g. a finalize event

	// $(document).ready(function(){
 //        	console.log("hello");
 //                //Height Fix
 //                schoolWrapHeightFix();
 //                window.onresize = function(event) {
 //                    schoolWrapHeightFix();
 //                }

 //                function schoolWrapHeightFix() {
 //                   var  vph = $(window).height();
 //                    if($(document).width() > 479) {
 //                        vph = vph - ($("#header").height() + 16);
 //                        $(".school-wrap").height(vph);
 //                    }else{
 //                        vph = ( vph / 1.5 ) - ($("#header").height() + 16);
 //                        $(".school-wrap").height(vph);
 //                    }
 //                }
 //                //Make it scroll
 //        		if ($.fn.niceScroll) {
 //        		console.log("scroll");
 //                    $(".school-wrap").niceScroll({
 //                        cursorcolor: "#FFF",
 //                        cursorborderradius: "0px",
 //                        cursorborder:"",
 //                        cursorwidth: "8px"
 //                    });
 //                }
 //        	});
