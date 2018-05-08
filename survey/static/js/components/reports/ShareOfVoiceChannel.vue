<template>
<div id="share-of-voice__company">
    <div class="panel no-border">
        <div class="panel-heading">
        <span style="text-transform: uppercase;">Share of voice</span>
            <span class="m-l-md" v-if="report_sov.xhr" v-show="report_sov.xhr.readyState && report_sov.xhr.readyState >0 && report_sov.xhr.readyState <4"><i  class="fa-circle-o-notch fa fa-spin"></i> loading...</span>
        <span class="pull-right text-xs " v-tooltip="'This graph gives you the total duration of the campaign played'"><i class="fa fa-info info-onhover"></i>   </span>
        </div>
        <div class="tab-container voice-tab sov-filters" style="margin: 0">
            <ul class="nav nav-tabs graph_date_range clearfix" role="tablist">
            <!-- <li v-bind:class="{'active':report_sov.current_mode=='all'}">
                <a class="voice-tab-annual" @click="report_sov.current_mode='all'" >All</a>
            </li>
            <li  v-bind:class="{'active':report_sov.current_mode=='custom'}">
                <a id="monthly-pies" class="voice-tab-monthly" @click="report_sov.current_mode='custom'">Custom</a>
            </li>
            <li class="pull-right voice-monthly hide">
            </li>
            <li v-show="report_sov.current_mode=='custom'">

            </li>
            -->


            <li v-show="report_sov.current_mode=='custom'" class="pull-left " style="">
                <daterangepicker id="campaign-date" :options="datepickeroptions" name="daterange" placeholder="Select Date" class="form-control input-xs" v-model="report_sov.date"
                />

            </li>
            </ul>
            <div class="mobile-only">
            <ul class="nav nav-tabs">


                <li v-show="report_sov.current_mode=='custom'">
                    <label>Date Range:</label>
                    <daterangepicker id="campaign-date" name="daterange" placeholder="Select Date"  class="form-control input-xs" v-model="report_sov.date"/>

                    </li>
            </ul>
            </div>
            <div class="tab-pane active" id="all" d-style="margin: 15px;">
            <div>
                <highcharts :options="report_sov.hconfig"></highcharts>

                <!-- <hr>
                <button @click="generateHconfig('sov')">Generate</button>
                <button @click="applyHconfig('sov')"> Apply</button>
                <textarea style="white-space: pre; width:100%;height:auto;min-height:200px" v-model="report_sov.hconfigJson"></textarea>
                <hr> -->

            </div>
            </div>
        </div>
        </div>
</div>


</template>

<script>
/* eslint-disable */
const VueMultiselect = require('../../../vendor/vue-multiselect/vue-multiselect.min.js');
import moment from 'moment';
export default {
  name: "ShareOfVoice",
  data() {
    return {
        channel_list:[],
        report_sov: {
            date: '',
            xhr: new XMLHttpRequest(),
            // api_url: '/campaign-sov-api/',
            api_url: '/dashboard/v2/api/share-of-voice/',

            data: {},
            current_mode: 'custom',
            sov_filter_extension: '',
            graph_type: 'pie',
            // sov_overall_data_status: true,

            hconfigJson: '',
            hconfig: {
                chart: {
                type: 'pie',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false

                },
                // colors: palettes[0],
                title: {
                text: 'Share of Voice'
                },
                subtitle: {
                text: ''
                },

                legend: {
                align: 'right',
                verticalAlign: 'middle',
                // floating: true,
                layout: 'vertical',
                width: 180,
                maxHeight: 355,
                y: 10
                // title: {
                //   text: 'Campaigns',
                // }
                },

                tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>',
                backgroundColor: null,
                // pointFormat: '<b>{point.percentage:.1f}% ({point.duration}) </b>',
                formatter () {
                    // this.color//
                    // window._tool = this;
                    // let width = this.series.chart.plotWidth;//165px;
                    // //let padding = this.series.chart.userOptions.plotOptions.pie.innerSize;
                    // // let padding = '65%';
                    // width = Math.floor(width *0.30);
                    return '<center style="width:220px"><span style="color:' + this.color + ';font-weight:bold;font-size:14px;">' + this.point.name + '</span>' + '<br>(' + this.percentage.toFixed(2) + '%)</center>';
                },
                positioner () {
                    // console.log('positioning');
                    // console.log(this);
                    // window._pos = this;
                    let chart = this.chart;
                    let plotX = chart.plotLeft + chart.plotWidth * 0.5;
                    let plotY = chart.plotTop + chart.plotHeight * 0.5;
                    const height = 60;
                    const width = 225;
                    let left = plotX + width * -0.5
                    let top = plotY + height * -0.5;
                    return {
                    x: left,
                    y: top
                    }
                },
                useHTML: true,
                shadow: false,
                borderWidth: 0
                },

                plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    innerSize: '65%',
                    showInLegend: true
                }
                },
                series: [{
                name: 'Industry',
                data: [],
                showInLegend: true
                }],
                drilldown:{
                series: []
                },
                noData: {
                },
                credits: {
                enabled: false
                },
                responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                        },
                    chartOptions: {
                        legend: {
                            layout: 'horizontal',
                            align: 'center',
                            verticalAlign: 'bottom',
                            itemStyle: {
                                color: '#000000',
                                fontWeight: 'bold'
                                },
                            float: true
                            }
                        }
                    }]
                }
            },
            selected_month: {'name': 'All Months', id: ''},
            selected_channel: {'name': 'All Channels', 'id': ''}
        },
        datepickeroptions: {
            timePicker: false,
            "showDropdowns": true,
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
        }
    };
  },
  props:{
    current_channel: {
        type: String
    }
  },
  methods: {
      set_custom_report_api() {
        let api_url = '/dashboard/v2/api/share-of-voice/';

        if (this.report_sov.current_mode != 'all') {
          const query_string = [];
          query_string.push('date=' + this.report_sov.date);
          //          if (this.report_sov.selected_month.id) {
          //              query_string.push('month=' + this.report_sov.selected_month.id);
          //            }

          if (this.current_channel) {
              query_string.push('media=' + this.current_channel);
            }

          if (query_string.length) {
              api_url += '?';
              api_url += query_string.join('&');
            }
        }

        this.report_sov.api_url = api_url;
      },

      generate_sov_chart_data(){
          var _this = this;
          this.cancel_sov_chart_request();

          this.report_sov.hconfig.subtitle.text =  ' '
          this.report_sov.hconfig.subtitle.text += ' ';
          this.report_sov.hconfig.subtitle.text += this.report_sov.date;

          // var sov_chart_api_url = _this.report_sov.api_url+_this.report_sov.sov_filter_extension;
          var sov_chart_api_url = _this.report_sov.api_url;
          // console.trace('sov data')
          _this.progress = 0;
          _this.report_sov.xhr = $.ajax({
            url: sov_chart_api_url,
            async:true,
            xhr: function () {
              var xhr = new window.XMLHttpRequest();
              xhr.upload.addEventListener("progress", function (evt) {
                  if (evt.lengthComputable) {
                      var percentComplete = evt.loaded / evt.total;
                      //console.log(percentComplete);
                      _this.progress = percentComplete;
                  }
              }, false);
              xhr.addEventListener("progress", function (evt) {
                  if (evt.lengthComputable) {
                      var percentComplete = evt.loaded / evt.total;
                      //console.log(percentComplete);
                      _this.progress = percentComplete*100;
                  }
              }, false);
              return xhr;
            },
          });

          _this.report_sov.xhr.then(function(result) {
            _this.report_sov.data = result.payload;
            _this.loading = false;
          });
      },

      cancel_sov_chart_request() {
        if (this.report_sov.xhr && this.report_sov.xhr.abort) {
          this.report_sov.xhr.abort();
        }
      },

      setSovDateOptions(){
          let ranges = {
              'Today': [moment(), moment()],
                'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                'This Month': [moment().startOf('month'), moment().endOf('month')],
                'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
          };

          //This month
          //
          //user moment.monthsShort(),  for short display of month name
          //moment.months() for full display of month name
          //let currentMonthLabel = 'This Month ('+ moment.months()[moment().month()]+')';
          //ranges[currentMonthLabel] = [moment().startOf('month'), moment().endOf('month')];

        //last month
        //let lastMonthLabel = moment.months()[moment().subtract(1,'month').month()];
        //ranges[lastMonthLabel] = [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')];

        //up up until jan
        //if(moment().month() > 1 ) {
            //if greater than feb
            let earlier_month = moment().month() - 1;
            while(earlier_month >= 0){


                let label = moment.months()[earlier_month];
                let month_diff = moment().month() - earlier_month;
                ranges[label] = [moment().subtract(month_diff, 'month').startOf('month'), moment().subtract(month_diff, 'month').endOf('month')];
                earlier_month -= 1;


            }
        //}


         //last year
        let lastYearLabel = 'Last Year';//String(moment().year() - 1);
        ranges[lastYearLabel] = [moment().subtract(1, 'year').startOf('year'), moment().subtract(1, 'year').endOf('year')];


        let dateFormat = 'YYYY-MM-DD';
        this.datepickeroptions.startDate = ranges['Last 7 Days'][0];//.format(dateFormat);
        this.datepickeroptions.endDate = ranges['Last 7 Days'][1];//.format(dateFormat);

        this.report_sov.date = ranges['Last 7 Days'][0].format(dateFormat)+'/'+ranges['Last 7 Days'][1].format(dateFormat);
        this.datepickeroptions.ranges = ranges;



      }
  },


  computed: {
    sovIndustrySeries(){
        return this.report_sov.data.industry.map(i => {
            return {
                name: i.name,
                drilldown: i.name,//+'_brand',
                drilldown: i.name +'_brand',
                y: i.duration //.toFixed(2)
            };
        });
    },
    sovSeries() {


        let items = [];

        const valuesPolyfill = function values(object) {
          return Object.keys(object).map(key => object[key]);
        };

        const values = Object.values || valuesPolyfill;

        const total = values(this.report_sov.data)
                 .reduce(( sum, val ) =>  {
                   return sum + (parseFloat(val) || 0);
                 }, 0);
        const ptotal = (total / 100);

        for (let k in this.report_sov.data) {
          const val = parseInt(this.report_sov.data[k], 10) || 0;
          const sItem = {
            text: k,
            'name': k,
            values: [val],
            'y': val
          };
          // @todo
          // https://www.highcharts.com/demo/pie-drilldown

          // if(total > 0) {
          //   sItem['values']=[val];
          // }
          let itemcolor = '';
          if (val == 0) {
            itemcolor = Please.make_color({
              greyscale: true
            });

            sItem['data-pct'] = 0;
            // sItem['data-duration'] = "Not Played";
          } else {
            sItem['data-pct'] = (val / ptotal).toFixed(2);
            itemcolor = Please.make_color({
              greyscale: false,
              // hue: 12, //set your hue manually
              hue: 360, // set your hue manually
              saturation: 0.6, // set your saturation manually
              value: 0.6// set your value manually
            });

            // sItem['data-duration'] = this.secToHrMin(val);
            // sItem['data-duration'] = moment.duration(val,'seconds').humanize();
          }
          sItem['background-color'] = itemcolor;

          items.push(sItem);
        }

        return items;
    },

    sovMediaOptions() {
        return this.channel_list;
        // let opts = this.channel_list;
        // opts.unshift({
        //   name: 'All Channels',
        //   id: ''
        // });
        // return opts;
    },

    sovMonthOptions() {
        const opts = this.month_list;
        opts.unshift({
          name: 'All Months',
          id: ''
        });
        return opts;
    },



  },

  watch: {
      all_channels: function(channel_list){
          this.channel_list = this.all_channels;
      },
      'report_sov.current_mode': function () {
        this.set_custom_report_api();
      },

       'report_sov.date': function () {
        this.set_custom_report_api();
      },

      'report_sov.selected_month': function () {
        this.set_custom_report_api();

        // console.log(this.report_sov.selected_month);
        // if(atma.report_sov.current_mode == "all"){

        // }else{
        //   console.log();
        // }
      },



  

      // "sov_overall_data_status": function(){
      // "report_sov.current_mode": function(){

      'report_sov.api_url': function () {
        this.generate_sov_chart_data();
          // console.trace('current_mode changed');
      },

        //   'report_sov.graph_type': function () {
        //     this.report_sov.zconfig.type = this.report_sov.graph_type;
        //   },

      'report_sov.data': function () {
        // this.report_sov.zconfig.series = this.sovSeries;
        this.report_sov.hconfig.series[0].data = this.sovIndustrySeries;
        this.report_sov.hconfig.drilldown.series = this.report_sov.data.brand;

      },

      current_month: function () {
        let atma = this;
        atma.report_sov.sov_filter_extension = '?month=' + this.current_month;
        // console.debug('current month changed', this.current_month);
        atma.generate_sov_chart_data();
      },

  },


  created() {
      //this.channel_list = this.all_channels;
      this.setSovDateOptions();
      //this.generate_sov_chart_data();
  },



  mounted(){
      //this.channel_list = this.all_channels;

  },
  components: {
        vselect: VueMultiselect.default
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#share-of-voice__company .sov-filters ul{
    padding:5px;
    /* border-top:1px solid grey!important; */
}
</style>
