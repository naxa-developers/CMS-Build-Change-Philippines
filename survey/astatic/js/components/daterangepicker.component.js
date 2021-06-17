var $ = require('jquery')
import  Vue from 'vue'
require('daterangepicker')

// var moment = require('../../vendor/js/moment.min.js')
import  moment from 'moment'
window.moment = moment;
Vue.component('daterangepicker', {
  props: {
    value: {
      type: [String]
    },
    options: {
      type: Object,
      // default: function(){
      //   return {
      //     format: 'YYYY-MM-DD',
      //     separator: '/'
      //   }
      // }
    }
  },
  // props: ['options', 'value', 'multiple'],
  template:
  `<input/>`,
  mounted: function () {

    // let opts = Object.assign({},{
    //     format: 'YYYY-MM-DD',
    //     separator: '/'
    // },this.options);

    var vm = this;
    // console.log('final datepicker config',this.config)
    $(this.$el)
      // .daterangepicker({format: 'YYYY-MM-DD', separator: '/'})
      .daterangepicker(this.config)
      .val(this.value)
      .trigger('change')
      // emit event on change.
      .on('apply.daterangepicker', function () {
        vm.$emit('input', this.value)
      })
      .on('change', function () {
        vm.$emit('input', this.value)
      })
  },
  computed: {
    config: function(){
      return Object.assign({},{
          "showDropdowns": false,
          locale: {
            format: 'YYYY-MM-DD',
            separator: '/'
          },
          ranges:   {
            'Today': [moment(), moment()],
             'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
             'Last 7 Days': [moment().subtract(6, 'days'), moment()],
             'Last 30 Days': [moment().subtract(29, 'days'), moment()],
             'This Month': [moment().startOf('month'), moment().endOf('month')],
             'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
      },this.options);
    }
  },
  watch: {
    value: function (value) {
      // update value
      $(this.$el).val(value).trigger('change');
    },
    // config: function (options) {
    //   console.trace('daterangepicker option changed',options)
    //   // update options
    //   $(this.$el)
    //   .daterangepicker('destroy')
    //   .daterangepicker({ data: this.config }).trigger('change')
    // }
  },
  created: function() {
      var vm = this;

  },
  destroyed: function () {
    console.log('daterangepicker destroyed');
    // $(this.$el).off().daterangepicker('destroy')
    // debugger;
    $(this.$el).data('daterangepicker').remove()
    // $(this.$el).remove();
  }
})
