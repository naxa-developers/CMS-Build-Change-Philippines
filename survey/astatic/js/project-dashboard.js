import 'bootstrap';
import jQuery from 'jquery';

require('../assets/js/vendor/jquery.nicescroll.min.js');
require('../assets/js/plugins.js');
require('../assets/css/style.css');

window.$ = jQuery;
window.jQuery = jQuery;
console.log("Hello from project-dashboard");

// The routing fires all common scripts, followed by the page specific scripts.
// Add additional events for more control over timing e.g. a finalize event

        	$(document).ready(function(){
                //Height Fix
                schoolWrapHeightFix();
                mapHeightFix();
                window.onresize = function(event) {
                    schoolWrapHeightFix();
                    mapHeightFix();
                }

                function schoolWrapHeightFix() {
                    var vph = $(window).height();
                    if($(document).width() > 479) {
                        vph = vph - ($("#header").height() + 16 + $(".school-action").outerHeight() + 15);
                        $(".school-wrap").height(vph);
                        $(".dash-right").css("min-height", vph + $(".school-action").outerHeight() + 15);
                    }else{
                        vph = ( vph / 1.5 ) - ($("#header").height() + 16 + $(".school-action").outerHeight() + 15);
                        $(".school-wrap").height(vph);
                    }
                }

                function mapHeightFix(){
                    var statH = $(".stat-item").outerHeight();
                    var useH = (statH * 2) + 15;
                    $("#school-map").height(useH);
                    $(".guidelines-wrap").height(useH);
                    $(".update-wrap").height(useH);
                }
                //Make it scroll
        		if ($.fn.niceScroll) {
                    $(".school-wrap").niceScroll({
                        cursorcolor: "#FFF",
                        cursorborderradius: "0px",
                        cursorborder:"",
                        cursorwidth: "8px"
                    });

                    $(".guidelines-wrap").niceScroll({
                        cursorcolor: "#5184ac",
                        cursorborderradius: "0px",
                        cursorborder:"",
                        cursorwidth: "8px"
                    });

                    $(".update-wrap").niceScroll({
                        cursorcolor: "#5184ac",
                        cursorborderradius: "0px",
                        cursorborder:"",
                        cursorwidth: "8px"
                    });

                }
                $('.collapse').on('shown.bs.collapse', function () {
                  $(".guidelines-wrap").getNiceScroll().resize();

                })

                $(".collapseHeader").click(function(){
                });
                function toggleIcon(e) {
                    $(e.target)
                        .prev('.collapseHeader')
                        .find("i")
                        .toggleClass('la-minus-circle');
                }
                $('#accordion').on('hidden.bs.collapse', toggleIcon);
                $('#accordion').on('shown.bs.collapse', toggleIcon);

        	});