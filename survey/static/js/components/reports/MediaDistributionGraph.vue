<template>
<div id="media_distribution_graph">
    <div class="panel no-border">
        <div class="panel-heading">
            <span class="text-u-c ">Media distribution graph</span>
            <span  class="pull-right text-xs " v-tooltip="'This graph gives you the total duration of the campaign played in different channels'"><i class="fa fa-info info-onhover"></i></span>
            <div class="tab-container">
                <ul class="nav nav-tabs graph_date_range mb-0">
                    <li @click="report_airtime.media_type=0" v-bind:class="{'active':!report_airtime.media_type}">
                    <a>TV Channels</a>
                    </li>
                    <li @click="report_airtime.media_type=1" v-bind:class="{'active':report_airtime.media_type}">
                    <a>Radio Channels</a>
                    </li>
                    <li>
                    <label>Select Date :</label>
                    </li>
                    <li>
                    <daterangepicker id="campaign-date" name="daterange" placeholder="Select Date" :options="datepicker_option" class="form-control input-xs" v-model="report_airtime.date"
                    />
                    </li>
                    <div class="graph_date_range" style="display: flex;">
                        <li class="pull-right m-hide" style="width: 100%">
                            <vselect :options="all_brands" label="name" v-model="report_airtime.selected_brand" :allow-empty="false"
                            :select-label="''" :show-labels="false" :value="{'id':'','name':'All Brands'}" :internal-search="true" :placeholder="'Select Brand'">
                            <template slot="noResult">No such brand</template>
                            </vselect>
                        </li>
                            <li class="pull-right m-hide" style="width: 100%">
                            <vselect :options="all_campaigns" label="name" :value="default_selected_campaign" v-model="report_airtime.selected_campaign"
                            :allow-empty="false" :select-label="''" :show-labels="false" :internal-search="true" :placeholder="'Select Campaign'">
                            <template slot="noResult">No such campaign</template>
                            </vselect>
                        </li>
                        </div>
                </ul>
                <div class="mobile-only">
                    <vselect :options="all_brands" label="name" v-model="report_airtime.selected_brand" :allow-empty="false" :select-label="''" :show-labels="false"
                    :internal-search="true" :placeholder="'Select Brand'" :value="{'id':'','name':'All Brands'}" >

                    </vselect>
                    <vselect :options="all_campaigns" label="name" group-label="campaign_type" group-values="campaigns" :value="default_selected_campaign" v-model="report_airtime.selected_campaign" :allow-empty="false" :select-label="''" :show-labels="false"
                            :internal-search="true" :placeholder="'Select Campaign'" >
                    </vselect>
                </div>
                
                
            </div>
        </div>
        
        <div class="panel-body" v-loading="isLoading" element-loading-text="Loading..." element-loading-spinner="el-icon-loading" element-loading-background="white">
            <highcharts :options="report_airtime.hconfig"></highcharts>
        </div>
    </div>
</div>
</template>

<script>
/* eslint-disable */
const VueMultiselect = require('../../../vendor/vue-multiselect/vue-multiselect.min.js');
import moment from 'moment';
export default {
    name: "MediaDistributionGraph",
    data() {
        return { 
            
            report_airtime: {
                date: '',
                media_type: 0,
                selected_campaign: {'name': 'All Campaigns', id: ''},
                selected_brand: {'name': 'All Brands', id: ''},
                zconfig: {
                type: 'pie',
                    // noData: {
                    //     text:'',
                    //     color: '#000',
                    //     "text-size": 80,
                    //     // backgroundColor:'#3b4051',
                    //     bold: true
                    // },
                    // theme: 'dark',
                    // backgroundColor: 'none',
                globals: {
                    fontFamily: 'Verdana'
                    },
                title: {

                    text: '',
                    position: '0% 0%',
                    'margin-top': 0,
                    'margin-right': 0,
                    'margin-left': 0,
                    'padding-bottom': 25,
                    fontWeight: 'normal',
                    fontStyle: 'normal',
                    'width': '80%',
                    'media-rules': [{
                        'max-width': 568,
                        'width': '100%'

                    }]

                    },
                labels: [{
                    text: '',
                    'x': '0%',
                    y: '95%'
                    }],
                backgroundColor: 'none',

                'legend': {
                    //              animation:{
                    //                effect: 2,
                    //                method: 5,
                    //                speed: 1,
                    //                sequence: 1,
                    //                delay: 0
                    //              },
                    'toggle-action': 'remove',
                    'width': '20%',
                    'adjust-layout': 0,
                    'right': '0',
                    overflow: 'page',
                    'max-items': 12,
                    'layout': 'vertical',
                    align: 'right',
                    margin: 0,

                    // "layout": "vertical",
                    // layout:  "1x5",
                    align: 'right',
                    marginTop: 30,
                    marginBottom: 30,

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
                        width: '100%',
                        text: '%t' // : %v
                    },

                    'media-rules': [{
                        'max-width': 568,
                        'width': '100%',
                        'height': '20%' ,
                        'vertical-align': 'bottom',
                        // "layout":"float",
                        layout: '5x2',
                        item: {'text': '%t', width: '75px'}// : %v
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
                plotarea: {

                    'width': '80%',
                    'margin-left': '0',
                    'margin-right': '0',
                    'margin-top': '30px',
                    'margin-bottom': '40px',
                    width: '80%',
                    'background-color': 'none', // "yellow",
                    'adjust-layout': 0,
                    'media-rules': [{
                        'max-width': 568,
                        'width': '100%',
                        height: '60%'
                        }]

                    },
                'options': {
                    mobile: true
                    },
                plot: {
                    // x: "350px",
                    'adjust-layout': 1,
                    layout: 'auto',
                    slice: '60%',

                    'border-width': '2px',
                    'border-color': '#ffffff',

                    valueBox: {
                        visible: false
                    },
                    detach: false,
                    animation: {
                        effect: 2,
                        method: 5,
                        speed: 1000,
                        sequence: 2,
                        delay: 0
                    }
                    },
                tooltip: {
                    fontSize: 17,
                    // anchor: 'c',
                    // x: '51%',
                    // y: '55%',
                    // sticky: true,
                    // callout: true,
                    backgroundColor: '#E6275F',
                    'border-color': '#3a3f51',
                    borderWidth: '2px',
                    thousandsSeparator: ',',
                    // text: '<span style="color:%color">%t</span><br><span style="color:%color">%v seconds </span><br><span style="color:%color"> (%data-duration)</span>',
                    // text: '<span style="color:%color">%t</span><br><span style="color:%color">%v seconds </span><br><span style="color:%color"> (%data-duration)</span>',
                    text: '<span >%t (%npv%)</span><br><span>%v seconds </span><br><span> (%data-duration)</span>',
                    mediaRules: [{
                        maxWidth: 400,
                        fontSize: 13
                    }]
                    },
                series: []

                    // series: [{
                    //   values: [45],
                    //  // backgroundColor: '#9575cd',
                    //   text: 'series 1'
                    // }, {
                    //   values: [55],
                    //   //backgroundColor: '#1de9b6',
                    //   text: 'series 2'
                    // }, ]
                },
                hconfig: {
                chart: {
                    type: 'pie',
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false

                },
                title: {
                    text: 'Media Distribution'
                },
                subtitle: {
                    text: ''
                },
                labels: {
                    items: [{
                    html: '',
                    style: {
                        left: 400,
                        top: 325,
                        fontSize: '10px',
                        fontWeight: 'bold',
                        color: 'black'
                        }
                    }, {
                    html: '',
                    style: {
                        left: 0,
                        // bottom: '5px',
                        top: 325,
                        fontWeight: 'bold',
                        fontSize: '10px',
                        textAlign: 'center',
                        color: 'black'
                        }
                    }]

                },

                legend: {
                    align: 'right',
                    verticalAlign: 'middle',
                    // floating: true,
                    layout: 'vertical',
                    width: 150,
                    maxHeight: 355,
                    y: 10

                },
                tooltip: {
                    backgroundColor: null,
                    // pointFormat: '<b>{point.percentage:.1f}% ({point.duration}) </b>',
                    formatter(){
                    // this.color//
                    // window._tool = this;
                    // let width = this.series.chart.plotWidth;//165px;
                    // //let padding = this.series.chart.userOptions.plotOptions.pie.innerSize;
                    // // let padding = '65%';
                    // width = Math.floor(width *0.30);
                    return '<center style="width:220px"><span style="color:' + this.color + ';font-weight:bold;font-size:14px;">' + this.point.name + '</span>' + '<br>' + this.point.duration + '<br>(' + this.percentage.toFixed(2) + '%)</center>';
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
                        x:left,
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
                    name: 'Total:',
                    data: [],
                    showInLegend: true
                }],

                noData: {
                    attr: {
                    text: 'No data available'
                    },
                    text: 'no data text',
                    html: '<b>No data to display </b>'

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
                xhr: new XMLHttpRequest(),
                data: []
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
            },
            
        };
    },
    props:{
        all_campaigns: {
            type: Array
        },
        all_brands: {
            type: Array
        },
        datepicker_option: {
            type: Object
        }
    },


    methods: {
        pluralize(val, singular, plural = '') {
        if (parseInt(val) == 0) {
          return singular;
        }
        if (plural) {return plural;} // if plural version is given
        return singular + 's'; // simplified plural version with 's added at the end'
      },
      secToHrMin(totalSec) {
        const d = moment.duration(totalSec, 'seconds');
        let duration_text = '';
        if (totalSec < 60) {
          duration_text = String(totalSec) + this.pluralize(totalSec, ' sec', ' secs');
        } else {
          const hrs = parseInt(d.asHours());
          const min = parseInt(d.asMinutes() % 60);
          if (hrs > 0) {
            duration_text = String(hrs) + this.pluralize(hrs, ' hour', ' hours');
          }
          if (min > 0) {
            duration_text += ' ' + String(min.toFixed(0)) + this.pluralize(min, ' min', ' mins');
          }
        }
        return duration_text;
      },

      request_campaign_airtime_data(){
          var _this = this;
          var current_campaign = this.report_airtime.selected_campaign;
          var current_brand = this.report_airtime.selected_brand;
          // if (!current_brand.hasOwnProperty('id') && !current_campaign.hasOwnProperty('id') ) {
          //   this.report_airtime.zconfig.title.text = "Pick a brand/campaign"
          //   this.report_airtime.hconfig.title.text = "Media Distribution"
          //   this.report_airtime.hconfig.subtitle.text = "Choose a brand/campaign"
          //   return;
          // }

          // if(!current_campaign.hasOwnProperty('id')) {
          //   console.error('no campaigns selected yet');
          //   this.report_airtime.zconfig.title.text = "Pick a campaign"
          //   this.report_airtime.hconfig.title.text = "Campaigin airtime"
          //   this.report_airtime.hconfig.subtitle.text = "Choose a campaign"
          //   return ;
          // }

          if(current_campaign.subscribed_type) {


            _this.report_airtime.zconfig.labels[1]= {

              'text':"Campaign type: "+current_campaign.subscribed_type,
              "x":"0%",
              "y":"0%",
              "text-align": "right"

            };
            _this.report_airtime.hconfig.labels.items[0].html = "Campaign type: " + current_campaign.subscribed_type;
            _this.report_airtime.hconfig.labels.items[1].html = "Data: " + current_campaign.subscribed_from + ' - ' + current_campaign.subscribed_to;



          }
          _this.report_airtime.zconfig.source = {
            text: current_campaign.subscribed_from + ' - ' + current_campaign.subscribed_to
          };


          // request_campaign_airtime_data
        var campaign_chart_api_url = "/dashboard/media-distribution?brand="+current_brand.id+"&media_type="+_this.report_airtime.media_type;
          if (current_campaign.hasOwnProperty('id')) {
            campaign_chart_api_url += "&campaign=" + current_campaign.id
          }
          campaign_chart_api_url +="&date=" + _this.report_airtime.date;
          _this.progress = 0;
          // _this.report_airtime.zconfig.title.text = 'Loading...'
          _this.report_airtime.xhr = $.ajax({
            url: campaign_chart_api_url,
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

            _this.report_airtime.xhr.then(function(result) {
              _this.report_airtime.zconfig.title.text = _this.report_airtime.selected_campaign.name;
              _this.report_airtime.hconfig.title.text = 'Media Distribution ';

              let reportOf = '';

              if (_this.report_airtime.selected_brand.id != '') {
                reportOf = _this.report_airtime.selected_brand.name;
                if (_this.report_airtime.selected_campaign.id != '') {
                  reportOf = _this.report_airtime.selected_campaign.name;
                }
              } else if (_this.report_airtime.selected_campaign.id != '' ) {
                reportOf = _this.report_airtime.selected_campaign.name;
              }

              if(reportOf.length) {
                _this.report_airtime.hconfig.title.text += '(' + reportOf + ')';
              }
              //+_this.report_airtime.selected_campaign.name;






            var datas = []
            for(let k in result.payload){
              datas.push({channel: k, value: result.payload[k]});
            }
            _this.report_airtime.data = datas;
            _this.loading = false;
          });
      },
    
    },

    computed: {
       
        default_selected_campaign() {
            if (this.all_campaigns.length) {
            return this.all_campaigns[0];
            }
            return {};
        },
        airtimeCampaignList() {
            const subscription_types = {};

            this.campaigns.map((c) => {
            if (!subscription_types.hasOwnProperty(c.subscribed_type)) {
                subscription_types[c.subscribed_type] = [];
            }
            subscription_types[c.subscribed_type].push(c);
            // return {
            //   id: c.id,
            //   name: c.name,
            //   category: c.subscribed_type
            // }
            });

            const opts = [];
            for (const sub_type in subscription_types) {
            opts.push({
                campaign_type: sub_type,
                campaigns: subscription_types[sub_type]
            });
            }

            console.log(opts);

            return opts;
        },
        airtimeDurationSeries() {
        return this.report_airtime.data.map((item) =>  {
          // item.values = [item.value.toFixed(2)];
         const val = parseInt(item.value, 10) || 0;
         const sItem = {
            text: item.channel, // zconfig
            values: [val], // zconfig
            'name': item.channel, // hconfig
            'y': val// hconfig
            // "values": [parseFloat(item.value,10).toFixed(2)]
          };
         if (val == 0) {
            // sItem['background-color']=Please.make_color({
            //   greyscale:true
            // });
            sItem['data-duration'] = 'Not Played';
            sItem.duration = 'Not Played';
          } else {
            // sItem['background-color']=Please.makePlease.make_color({
            //   greyscale:false,
            //   hue: 12, //set your hue manually
            //   saturation: .7, //set your saturation manually
            //   value: .8 //set your value manually
            // });

            sItem['data-duration'] = sItem.duration = moment.duration(val, 'seconds').humanize();
          }

         return sItem;
       });
      },

      totalDuration() {
        let total = 0;

        this.report_airtime.data.map((item) =>  {
          total += (parseFloat(item.value, 10) || 0);
        });
        total = Math.ceil(total);
        // alert(total)
        const d = moment.duration(total, 'seconds');
        let duration_text = '';
        if (total < 60) {
          duration_text = String(total) + this.pluralize(total, ' sec', ' secs');
        } else {
          const hrs = parseInt(d.asHours());
          const min = parseInt(d.asMinutes() % 60);
          if (hrs > 0) {
            duration_text = String(hrs) + this.pluralize(hrs, ' hour', ' hours');
          }
          if (min > 0) {
            duration_text += ' ' + String(min.toFixed(0)) + this.pluralize(min, ' min', ' mins');
          }
        }
        return duration_text;
      },
        isLoading(){
            return this.report_airtime.xhr.readyState && (this.report_airtime.xhr.readyState > 0) && (this.report_airtime.xhr.readyState < 4);       
        },        
        
    },

    created() {


        // let dateFormat = 'YYYY-MM-DD';
        // this.datepickeroptions.startDate = moment().subtract(6, 'days')
        // this.datepickeroptions.endDate = moment()
        // this.report_airtime.date = this.datepickeroptions.startDate.format(dateFormat)+'/'+this.datepickeroptions.endDate.format(dateFormat);
        
        this.report_airtime.date = this.$parent.defaultDatepickerOptions.date;
        

    },
    mounted(){
    
        // this.report_airtime.date = this.datepicker_option.date;
        
      
      

    
  },

    watch: {
        'report_airtime.date': function () {
        // this.report_airtime.zconfig.title.position = '50% 0%';
        this.request_campaign_airtime_data();
      },


      'report_airtime.selected_campaign': function () {
        // this.report_airtime.zconfig.title.position = '50% 0%';
        this.request_campaign_airtime_data();
          // let campaign = this.campaigns.find(function(c) {
          //   return parseInt(c.id) == parseInt(current);
          // });
      },

      'report_airtime.selected_brand': function () {
        this.request_campaign_airtime_data();
      },

      totalDuration: function () {
        // this.report_airtime.zconfig.labels[0].text = 'Total: ' + this.totalDuration;
        this.report_airtime.hconfig.subtitle.text = 'Total: ' + this.totalDuration;
      },
      'report_airtime.data'() {
          // this.report_airtime.zconfig.series = this.airtimeDurationSeries
        this.report_airtime.hconfig.series[0].data = this.airtimeDurationSeries
        // series[0].data
      },
      'report_airtime.media_type'() {
          this.request_campaign_airtime_data();
      },
    },



  
  components: {
        vselect: VueMultiselect.default
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
