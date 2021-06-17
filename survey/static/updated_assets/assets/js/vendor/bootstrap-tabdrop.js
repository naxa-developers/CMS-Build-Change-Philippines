//edited for bs 4


!function ($) {

    var WinResizer = (function () {
        var registered = [];
        var inited = false;
        var timer;
        var resize = function () {
            clearTimeout(timer);
            timer = setTimeout(notify, 100);
        };
        var notify = function () {
            for (var i = 0, cnt = registered.length; i < cnt; i++) {
                registered[i].apply();
            }
        };
        return {
            register: function (fn) {
                registered.push(fn);
                if (inited === false) {
                    $(window).bind('resize', resize);
                    inited = true;
                }
            },
            unregister: function (fn) {
                var registeredFnIndex = registered.indexOf(fn);
                if (registeredFnIndex > -1) {
                    registered.splice(registeredFnIndex, 1);
                }
            }
        }
    }());

    var TabDrop = function (element, options) {
        this.element = $(element);
        this.options = options;

        if (options.align === "left")
            this.dropdown = $('<li class="nav-item dropdown hide pull-left tabdrop"><a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false"><span class="display-tab"></span><b class="caret"></b></a><div class="dropdown-menu"></div></li>');
        else
            this.dropdown = $('<li class="nav-item dropdown hide pull-right tabdrop"><a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false"><span class="display-tab"></span><b class="caret"></b></a><div class="dropdown-menu"></div></li>');

        this.dropdown.appendTo(this.element);
        if (this.element.parent().is('.tabs-below')) {
            this.dropdown.addClass('dropup');
        }

        var boundLayout = $.proxy(this.layout, this);

        WinResizer.register(boundLayout);
        this.element.on('shown.bs.tab', function (e) {
        boundLayout();
        });

        this.teardown = function () {
            WinResizer.unregister(boundLayout);
            this.element.off('shown.bs.tab', function (e) {
                boundLayout();
            });
        };

        this.layout();
    };

    TabDrop.prototype = {
        constructor: TabDrop,

        layout: function () {
            var self = this;
            var collection = [];
      var isUsingFlexbox = function(el){
        return el.element.css('display').indexOf('flex') > -1;
      };

            function setDropdownText(text) {
                self.dropdown.find('a span.display-tab').html(text);
            }

            function setDropdownDefaultText(collection) {
                var text;
                if (jQuery.isFunction(self.options.text)) {
                    text = self.options.text(collection);
                } else {
                    text = self.options.text;
                }
                setDropdownText(text);
            }

      // Flexbox support
      function handleFlexbox(){
        if (isUsingFlexbox(self)){
          if (self.element.find('li.tabdrop').hasClass('pull-right')){
            self.element.find('li.tabdrop').css({position: 'absolute', right: 0});
                        self.element.css('padding-right', self.element.find('.tabdrop').outerWidth(true));
          }
        }  
      }

            function checkOffsetAndPush(recursion) {
                self.element.find('> li:not(.tabdrop) > a')
                    .each(function () {
                        if (this.offsetTop > self.options.offsetTop) {
                            $(this).removeClass("nav-link");
                            $(this).addClass("dropdown-item");
                            collection.push(this);
                        }
                    });

                if (collection.length > 0) {
                    if (!recursion) {
                        self.dropdown.removeClass('hide');
                        self.dropdown.find('div').empty();
                    }
                    self.dropdown.find('div').prepend(collection);
                    
                    if (self.dropdown.find('.active').length == 1) {
                        self.dropdown.addClass('active');
                        setDropdownText(self.dropdown.find('.active > a').html());
                    } else {
                        self.dropdown.removeClass('active');
                        setDropdownDefaultText(collection);
                    }
          handleFlexbox();
                    collection = [];
                    checkOffsetAndPush(true);
                } else {
                    if (!recursion) {
                        //self.dropdown.addClass('hide');
                    }
                }
            }
    
            self.element.append(self.dropdown.find('li'));
            checkOffsetAndPush();
        }
    };

    $.fn.tabdrop = function (option) {
        return this.each(function () {
            var $this = $(this),
                data = $this.data('tabdrop'),
                options = typeof option === 'object' && option;
            if (!data) {
                options = $.extend({}, $.fn.tabdrop.defaults, options);
                data = new TabDrop(this, options);
                $this.data('tabdrop', data);
            }
            if (typeof option == 'string') {
                data[option]();
            }
        })
    };

    $.fn.tabdrop.defaults = {
        text: '<i class="la la-bars"></i>',
        offsetTop: 0
    };

    $.fn.tabdrop.Constructor = TabDrop;

}(window.jQuery);