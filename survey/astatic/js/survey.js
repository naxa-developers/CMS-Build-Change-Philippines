import Vue from 'vue';
import moment from 'moment';
import jQuery from 'jquery';
import 'bootstrap';
// import PNotify from 'pnotify';
import PNotify from '../vendor/pnotify/pnotify.custom.min.js';
import PopperJs from '../../node_modules/popper.js/dist/popper.js';

require('../assets/css/style.css');
//
//require('../assets/js/vendor/modernizr-2.8.3-respond-1.4.2.min.js');


require('../assets/js/vendor/jquery.nicescroll.min.js');
require('../assets/js/plugins.js');
window.PNotify = PNotify;
window.$ = jQuery;
const channels = require('../vendor/js/websocket.js');


//
// window.Survey = new Vue({
//  el: '#app',
//  template:`
//            <div> {{message}}</div>
//                `,
//  data: {
//    message: 'Hello Vue!'
//  }
// })


// The routing fires all common scripts, followed by the page specific scripts.
// Add additional events for more control over timing e.g. a finalize event

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
