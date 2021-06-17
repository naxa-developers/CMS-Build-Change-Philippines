// var Vue = require("../../vendor/js/vue")
// var Vue = require("vue")
import  Vue from 'vue'
// import VueHighcharts from 'vue-highcharts';
// import { Line, mixins } from 'vue-chartjs'
// import Highcharts from 'highcharts';
// import VueHighcharts from 'vue2-highcharts'


// import zingchart from 'zingchart'
var zingchart = require('zingchart');
// var zingchart =
// require("zingchart")
// Components must be pre-defined before instance
// var ZingChartComponent =
window.ZingChartComponent = Vue.component('zingchart', {
  // create props to get data from the parent
  props: {
    zcId: {type: String},
    zcHeight: {},
    zcWidth: {},
    zcValues: {type: Array},
    zcJson: {
        type: Object,
      default: function() {
        return {
          type: 'bar',
          series:[
            {
              values: [15,25,35,45,55,65]
            }
          ]
        }
      }
    },
    debug: {
      type:Boolean,
      default:false
    }
  },
  computed: {

  },
  /*
   * Data acts as the default values for the render method and chart.
   * If you use props all instances of the component will share the same
   * objects. You must return new objects within data so they are not all
   * referenced. Unless you want them to be. Which is not the case here.
   */
  data: function() {
    return {
        id: this.zcId || 'zingchart-autoId-' + Math.ceil(Math.random() * 1000000),
          width: this.zcWidth || '100%',
          height: this.zcHeight || 300,
          json: this.zcJson,
          editConfigJson:'',
          edit:false
        }
  },
  mounted: function() {
    var _this = this;
    // setTimeout(function(){

      zingchart.render({
          id: _this.id,
          height: _this.height,
          width: _this.width,
          data: _this.json,
          // output: 'vml'
      });

    // },2000);


  },
  created: function() {
    var vm = this;
    this.$parent.$on('destroy_charts',function() {
      vm.destroy();
    });

    // this.$parent.$on('pjax:load',function() {
    //   zingchart.exec(this.id,'update');
    // });


    this.edit = false;
  },
  destroyed: function() {
    this.destroy();
  },
  watch: {
    zcHeight: function(newValue, oldValue) {
        zingchart.exec(this.id, 'resize', {
        height: newValue,
        width: this.width
      });
    },
    zcWidth: function(newValue, oldValue) {
        zingchart.exec(this.id, 'resize', {
        height: this.height,
        width: newValue
      });
    },
    json: { // requires a handler function with deep property specified
      handler: function(newValue) {
        zingchart.exec(this.id, 'setdata', {
          data: newValue
        });
      },
      deep:true
    }
  },
  methods:{
    generateJson: function() {
      this.editConfigJson = JSON.stringify(this.json,true);
    },
    applyJson: function() {
        this.data = JSON.parse(this.editConfigJson);
        zingchart.exec(this.id, 'setdata', {
          data: this.data
        });
    },
    toggleEdit: function() {
      if(this.edit == false) {
        if(!this.editConfigJson) {
          this.generateJson();
        }
      }
      this.edit = !this.edit;
    },
    destroy: function() {
      zingchart.exec(this.id, 'destroy');
    }
  },
  template: `<div><table v-if="debug"><tr><td><textarea v-show="edit"  style="max-height:500px;overflow-y:scroll;width:100%;display:block;" v-model="editConfigJson"></textarea>\
  </td><td width="1%"><div class="btn-group btn-group-vertical">\
  <button class="btn btn-sm" v-show="edit" @click="generateJson">Generate JSON from graph</button>\
  <button class="btn btn-sm" v-show="edit" @click="applyJson">Apply JSON to graph</button>\
  <button class="btn btn-sm" @click="toggleEdit">{{edit?"Hide":"Edit"}}</button></div></td></tr></table>\
  <div :id="id"></div></div>` // bind id to zcId to render  the chart
});

// Vue.use(VueHighcharts);

// export ZingChartComponent
/*
window.lineChartComponent = Vue.component('lineChart',{
  extends: Line,
  mixins: [mixins.reactiveData],
  // mixins: [mixins.reactiveProp,mixins.reactiveData],
  props: ['chartData', 'options'],
  mounted: function() {
    this.renderChart(this.chartData, this.options)
  }
})
*/
