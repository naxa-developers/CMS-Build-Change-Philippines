import 'bootstrap';
import jQuery from 'jquery';
import PNotify from '../vendor/pnotify/pnotify.custom.min.js';

// export to global scope now!

window.PNotify = PNotify;
window.$ = jQuery;
window.jQuery = jQuery;

require('../assets/js/vendor/jquery.nicescroll.min.js');
require('../assets/js/vendor/bootstrap-tabdrop.js');
require('../assets/js/plugins.js');
require('../css/style.css');
console.log("Hello from sitedetail");

            $(document).ready(function(){
                //Height Fix
                schoolWrapHeightFix();
                window.onresize = function(event) {
                    schoolWrapHeightFix();
                }

                function schoolWrapHeightFix() {
                    var vph = $(window).height();
                    if($(document).width() > 479) {
                        vph = vph - ($("#header").height() + 32 + $(".breadcrumb").outerHeight());
                        $(".dash-right").css("min-height", vph);

                        var aboutHeight = vph - ($(".profile-head").outerHeight() + 32);
                        $(".scrolling-wrap").height(aboutHeight);
                        $(".update-wrap").height(aboutHeight);


                    }else{
                       $(".scrolling-wrap").height(190);
                       $(".update-wrap").height(190);

                    }
                }

                //Make scroll
                if ($.fn.niceScroll) {
                    $(".scrolling-wrap").niceScroll({
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

                $( ".school-profile" ).hover(
                  function() {
                    $('[data-toggle="tooltip"]').tooltip({trigger: 'manual'}).tooltip('show');
                  }, function() {
                    $('[data-toggle="tooltip"]').tooltip({trigger: 'manual'}).tooltip('hide');
                  }
                );

                $('.nav-tabs, .nav-pills').tabdrop();

                $('.photo-item img').on('click',function(){
                    var title = $(this).attr('img-title');
                    var src = $(this).attr('src');
                    var img = '<img src="' + src + '" class="img-responsive"/>';
                    var html = '';
                    html += img;
                    $('#myModalLabel').modal();
                    $('#myModalLabel').on('shown.bs.modal', function(){
                        $('#myModalLabel .modal-header .modal-title').html(title);
                        $('#myModalLabel .modal-body').html(html);
                    })
                    $('#myModalLabel').on('hidden.bs.modal', function(){
                        $('#myModalLabel .modal-header .modal-title').html('');
                        $('#myModalLabel .modal-body').html('');
                    });
                });
            });