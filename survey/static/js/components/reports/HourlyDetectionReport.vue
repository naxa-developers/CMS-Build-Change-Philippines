<template>
<div id="hourly_detection_graph">
    <div class="panel no-border">
        <div class="panel-heading">
            <span style="text-transform: uppercase;">Hourly Ads Frequency</span>
            <span class="pull-right text-xs " v-tooltip="'This graph gives you the frequency of subscribed ads detected at hourly intervals for the chosen date interval and channels'"><i class="fa fa-info info-onhover"></i>   </span>
            <!--@todo put in same line -->
            <div class="form-group clearfix mb-0 mt-5 m-t-md">
                    <div class="col-sm-6">
                        <label class="col-sm-4 control-label m-t-xs text-right">Date:</label>
                        <div class="col-sm-8">
                        <daterangepicker :options="datepickeroptions" id="campaign-date" name="daterange" placeholder="Select Date"  class="form-control input-xs" v-model="report_hourly.date"/>
                        </div>

                    </div>
                    <div class="col-sm-6">
                        <label class="col-sm-4 control-label m-t-xs text-right">Channel:</label>
                        <div class="col-sm-8">
                          <vselect class="inline" :options="all_channels" label="name" :value="{'id':'','name':'All Channels'}" v-model="report_hourly.channel"  :select-label="''" :show-labels="true"
                                  :internal-search="true" :placeholder="'All Channel'" >
                          <template slot="noResult">No such channel</template>
                          </vselect>
                        </div>
                    </div>

            </div>
        </div>
        <div class="panel-body" v-loading="isLoading" element-loading-text="Loading..." element-loading-spinner="el-icon-loading" element-loading-background="white">
              <highcharts :options="report_hourly.hconfig"></highcharts>
        </div>           
    </div>
</div>


</template>

<script>
/* eslint-disable */
const VueMultiselect = require('../../../vendor/vue-multiselect/vue-multiselect.min.js');
import moment from 'moment';
export default {
  name: "HourlyDetectionGraph",
  data() {
    return {
        report_hourly: {
          date: '',
          channel: '',
          zconfig: {
            'type': 'line',
            'crosshair-x': {
              scaleLabel: {
                decimals: 2,
                borderRadius: 3,
                offsetX: -5,
                fontColor: '#2C2C39',
                text: 'Hours: %v',
                bold: true
              },
              plotLabel: {
                rules: [
                {
                  'rule': '%v <= 0',
                  visible: false
                }
              ]
              }
            },
            /*
            "crosshair-x":{
              plotLabel:{
                    multiple: false,
                    borderRadius: 3,
                    "text":" %t detected %v times",
                    rules: [
                    {
                      "rule": "%v <= 0",
                      "visible": false,
                      // "background-color": "red"
                    }

                    ]

                  },
                  scaleLabel:{
                    // backgroundColor:'#53535e',
                    // borderRadius: 3
                  },
                  marker:{
                    size: 2,
                    alpha: 0.5
                  }
            },
            */
            noData: {
              text: 'Please wait a moment...',
              color: '#000',
              'text-size': 80,
              backgroundColor: 'white',
              bold: true
            },
            // theme: 'dark',
            'background-color': '#fff',
            globals: {
              fontFamily: 'Verdana'
            },
            // "title":{
            //     "margin-top":"7px",
            //     "margin-left":"12px",
            //     "text":"HOURLY DETECTED ADS COUNT",
            //     "background-color":"none",
            //     "shadow":0,
            //     "text-align":"left",
            //     "font-family":"Arial",
            //     "font-size":"11px",
            //     "font-color":"#707d94"
            // },
            'legend': {

              width: '20%',
              'adjust-layout': 0,
              'right': '0',

              'overflow': 'page',
              'max-items': 16,
              'highlight-plot': true,
              'toggle-action': 'remove',

              layout: 'vertical',

              'highlight-plot': true,

              // "layout": "vertical",
              // layout:  "1x5",
              align: 'right',
              margin: 0,
              // "highlight-plot": 1,
              // verticalAlign:'bottom',

              // toggleAction: 'remove',
              // toggleAction: 'remove',
              'background-color': 'none', // "#3a3f51",
              // backgroundColor: "none",
              'border-width': 0,
              // y: "95%",
              // x: "80%",
              // x: "0%",
              'item': {
                text: '%t: %v',
                visible: true,
                rules: [{
                  'rule': '%v <= 0',
                  'visible': false
                }]

              },
              'media-rules': [{
                'max-width': 568,
                'width': '100%',
                'height': '20%' ,
                'vertical-align': 'bottom',
                'layout': '5x2',
                'item': {text: '%t', width: '75px'}
              }]

              // mediaRules: [{
              //   maxWidth: 300,
              //   marginTop: 0,
              //   layout: "4x3",
              //   align: 'bottom',
              //   "adjust-layout":1,
              //   "bottom": 0
              // }]
            },
            plot: {
              highlight: true,
              'highlight-state': {
                'color': 'red',
                'border-width': 1,
                'border-color': 'red',
                'line-style': 'dotted'
              },
              marker: {
                'type': 'circle',
                size: 1
              },
              'hover-marker': {
                type: 'circle',
                size: 2,
                'border-width': '1px'
              },
              'tooltip': {
                visible: true,
                text: '%t detected %v times'

              }

                // "animation":{
                //     "delay":500,
                //     "effect":"ANIMATION_SLIDE_LEFT"
                // }
            },
            'plotarea': {
              width: '80%',
              'margin': '50px 25px 70px 46px',

              'background-color': 'none', // "yellow",
              'adjust-layout': 0,
              'media-rules': [{
                  'max-width': 568,
                  width: '100%',
                  'height': '80%'
                }]
            },
            'options': {
              'mobile': true
            },
            'scale-x': {
              'line-color': '#d2dae2',
              'line-width': '2px',
              values: ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22', '22-23', '23-0'],
              // "values":["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
              tick: {
                'line-color': '#d2dae2',
                'line-width': '1px'
              },
              label: {
                text: 'Time of the day'
              },
              guide: {
                'visible': false
              },
              item: {
                'font-color': '#8391a5',
                'font-family': 'Arial',
                'font-size': '10px',
                'padding-top': '5px'
              }

            },
            'scale-y': {
              // "values":"0:100:25",
              'line-color': 'none',
              label: {
                text: 'Number of Detections'
              },
              guide: {
                'line-style': 'dashed',
                'line-color': '#d2dae2',
                'line-width': '1px',
                'alpha': 0.5
              },
              tick: {
                'visible': false
              },
              'item': {
                'font-color': '#8391a5',
                'font-family': 'Arial',
                'font-size': '10px',
                'padding-right': '5px'
              }
            },
            'series': []
          },
          hconfig: {
            chart: {
                type: 'column'
              },
            title: {
                text: 'Hourly Ads frequency'
              },
            xAxis: {
                categories: ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22', '22-23', '23-0'],
                title: {
                  text: 'Hour of the day'
                },
                crosshair: {},
                showEmpty: false
              },
            yAxis: {
                title: {
                  text: 'Total number of detections'
                }
              },
            legend: {
                align: 'right',
                verticalAlign: 'bottom',
                // floating: true,
                layout: 'vertical'
              },
            tooltip: {
                shared: true,
                useHTML: true,
                headerFormat: '<b style="font-weight:bold;">Hours: {point.key}</b><br/>'
            },
            plotOptions: {
                column: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: true,
                        // color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
                    }
                }
            },
              // subtitle: {
              //     text: 'May 31 and and June 1, 2015 at two locations in Vik i Sogn, Norway'
              // },
              
            series: [],
            responsive: {
                rules: [{
                  condition: {
                      maxWidth: 500
                    },
                  chartOptions: {
                      legend: {
                          layout: 'horizontal',
                          align: 'center',
                          verticalAlign: 'bottom'
                        }
                    }
                }]
              },
            credits: {
                enabled: false
              }

          },
          data: [],
          xhr: new XMLHttpRequest()
        },
        datepickeroptions: {
          singleDatePicker: true,
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
      },
      }
  },
  props:{
   all_channels: {
        type: Array
    },
    datepicker_option: {
        type: Object
    }
  },

    watch: {
      'report_hourly.date': function () {
        //        this.report_airtime.zconfig.title.position = '50% 0%';
        this.generate_report_hourly_data();
          // let campaign = this.campaigns.find(function(c) {
          //   return parseInt(c.id) == parseInt(current);
          // });
      },


      'report_hourly.channel': function () {
      //        this.report_airtime.zconfig.title.position = '50% 0%';
        this.generate_report_hourly_data();
          // let campaign = this.campaigns.find(function(c) {
          //   return parseInt(c.id) == parseInt(current);
          // });
      },

      'report_hourly.data'() {
        this.report_hourly.hconfig.series = this.hourlyReportHighchartSeries;
        // this.report_hourly.cconfig.labels = this.hourlyReportHighchartSeries;
      }
     
  },
  methods: {
       generate_report_hourly_data(){
        //        console.log("report hourly 1863")
          var _this = this;

          var line_diagram_api_url = "/line-diagram-api/";
          _this.progress = 0;
          let date = '';

          if(this.datepickeroptions.singleDatePicker){
             date =   this.report_hourly.date + '/' + this.report_hourly.date
          }else{
             date =   this.report_hourly.date;            
          }
          let params = {'date':date};
          if(_this.report_hourly.channel.hasOwnProperty('id')){
            params.channel = _this.report_hourly.channel.id;
          }
          this.cancel_prev_hourly_api_request();
          _this.report_hourly.xhr = $.ajax({
            url: line_diagram_api_url,
            data: params,
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

          _this.report_hourly.xhr.then(function(result) {
            _this.report_hourly.data = result;
            _this.loading = false;
          });
      },

      cancel_prev_hourly_api_request() {
        if (this.report_hourly.xhr && this.report_hourly.xhr.abort) {
          this.report_hourly.xhr.abort();
        }
      },
  },
  

  computed: {
  hourlyReportHighchartSeries() {
        let _this = this;
        const hseries = [];
        // _this.report_hourly.cconfig.labels = [];

        return _this.report_hourly.data.map((item,index) => {
          // let color = Please.make_color({saturation: 0.8,value: 0.7 });
          const shapeType = item.subscribed_type == 'Competitor' ? 'triangle':'circle';
          // _this.report_hourly.cconfig.labels.push(item.campaign)
          return {
            name: item.campaign,
            data: item.values
          };
        });
    },
    isLoading(){
            return this.report_hourly.xhr.readyState && (this.report_hourly.xhr.readyState > 0) && (this.report_hourly.xhr.readyState < 4);
    },   

  },




  created() {
    //   this.generate_sov_chart_data();
    // this.report_hourly.date = this.$parent.defaultDatepickerOptions.date;
    let dateFormat = 'YYYY-MM-DD';
    let mToday = moment();
    if(mToday.hour() < 13 ) {
      //show yesterday
      this.report_hourly.date = mToday.subtract(1, 'days').format(dateFormat);
    }else{
      //show today
      this.report_hourly.date = mToday.format(dateFormat);
      
    }
    // this.report_hourly.date = this.$parent.defaultDatepickerOptions.date;
    

  },



  mounted(){
      // this.report_hourly.date = this.datepicker_option.date
      

    
  },
  components: {
        vselect: VueMultiselect.default
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
