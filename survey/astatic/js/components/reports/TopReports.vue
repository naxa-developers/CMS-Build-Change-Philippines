<template>
<div id="top-reports-components">
    <div class="panel no-border">
        <div class="panel-heading">
            <span style="text-transform: uppercase;">Top Report</span>

        </div>
        <div class="panel-body" v-loading="is_loading" element-loading-text="Loading..." element-loading-spinner="el-icon-loading" element-loading-background="white">
            <div class="top-report-filters">
                <ul class="media-list clearfix p-o" role="tablist">
                    <li class="col col-xs-12 col-md-6 text-center mb-5" style="max-width:250px;">
                        <daterangepicker id="campaign-date" :options="datepicker_option" name="daterange" placeholder="Select Date" class="form-control input-xs"
                            v-model="special_report_date_range" />
                    </li>
                    <!-- <li class="col col-xs-6 col-md-6 text-center" style="max-width:250px;">

                        <vselect :options="industry_list" label="name" :value="default_selected_spec_ind" v-model="selected_special_industry"
                            :allow-empty="false" :select-label="''" :show-labels="false" :internal-search="true" :placeholder="'Select Industry'">
                            <template slot="noResult">No such Industry</template>
                        </vselect>
                    </li> -->
                    <li class="col col-xs-12 col-md-6 mb-5">
                         <el-cascader

                            placeholder="Select Industry/Sub Industry"
                            :options="all_industry_list"
                            expand-trigger="hover"
                            v-model="selected_industry"
                            change-on-select
                            value="value"
                            label="label"
                            size="medium"
                            filterable
                        ></el-cascader>
                    </li>
                    <li class="col col-xs-6 col-md-6 text-center mb-5" style="max-width:250px;">

                        <vselect :options="campaign_list" label="name" :value="default_selected_spec_camp" v-model="selected_special_campaign"
                            :allow-empty="false" :select-label="''" :show-labels="false" :internal-search="true" :placeholder="'Select Campaign'">
                            <template slot="noResult">No such campaign</template>
                        </vselect>
                    </li>
                    <li class="col col-xs-12 col-md-6 mb-5">
                        <el-button :disabled="!is_valid" plain icon="el-icon-arrow-right" @click="generate_special_report()">Generate Report</el-button>
                    </li>
                </ul>
            </div>

            <div v-show="!is_loading && !generated" class="text-center block m-md mt-sm ">
                <p class=" b wrapper-md pos-rlt bg-light r r-2x">
                    <span class="arrow top pull-right arrow-light"></span>
                    <span class="report-title">
                        Choose industry or campaign to generate `Top` report!
                    </span>
                </p>
            </div>



            <div v-show="!is_loading && generated && !special_report.data.length " class="text-center block m-md mt-sm  ">
                <p class=" b wrapper-md pos-rlt bg-light r r-2x">
                    <span class="arrow top pull-right arrow-light"></span>
                        No Reports available
                        <span v-if="false">
                        <!-- <span v-show="selected_special_industry.id" v-text="selected_special_industry.name" class="text-dark-dk"></span> -->
                        <span v-show="selected_industry.length" v-text="selected_industry_label" class="text-dark-dk"></span>
                        <!-- <span v-show="selected_special_industry.id && selected_special_campaign.id" v-text="' > '" class="text-dark-dk"></span> -->
                        <span v-show="selected_industry.length && selected_special_campaign.id" v-text="' > '" class="text-dark-dk"></span>
                        <span v-show="selected_special_campaign.id" v-text="selected_special_campaign.name" class="text-dark-dk"></span>
                        between <span v-text="special_report_date_range" class="text-dark-dk"></span>
                        </span>
                </p>
            </div>
            <div v-for="(report_data, report_title) in special_report.data" class="r bg-light lt item hbox no-border">

                <div class="col w-md v-middle hidden-md ">
                    <span class="label text-base bg-dark pos-rlt m-l m-r">
                    <span class="m-r" v-show="report_data.help">
                        <i v-tooltip="report_data.help || ''" class="fa  fa-info-circle"></i>
                    </span>
                    <span class="report-title" v-text="report_data.label">

                    </span>

                    <i class="arrow right arrow-dark"></i>

                    </span>
                </div>
                <div v-if="!report_data.data || !report_data.data.length" class="col lter padder-v r-r text-center">
                    <i class="fa fa-question-circle fa-3x"></i>
                </div>
                <div class="col dk padder-v r-r text-center" v-if="report_data && report_data.data.length" v-for="data in report_data.data">
                    <div class="text-black w-full dker font-thin h4">
                    <span>{{data.text}}</span>
                    </div>
                    <span class="text-muted text-xs">Detected {{data.frequency}} times</span>
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
    name: "TopReports",

    props:{

        all_campaigns: {
            type: Array
        },
        datepicker_option: {
            type: Object
        }

    },
    data() {
        return {
            generated:false,
            selected_special_campaign: {},
            selected_special_industry: {},
            selected_industry: [],
            all_campaign_list: [],
            campaign_list: [],
            industry_list: [],
            all_industry_list: [],
            // special_report_date_range: moment().subtract(6, 'days').format('YYYY-MM-DD')+"/"+moment().format('YYYY-MM-DD'),
            special_report_date_range: moment().subtract(6, 'days').format('YYYY-MM-DD')+"/"+moment().format('YYYY-MM-DD'),
            special_report: {
            xhr: new XMLHttpRequest(),
            progress: 0,
            api_url: '/matches/favourite-display/?',
            data: [],
            olddata: {
                top_tv_channel: {
                    label: "Top TV Channel",
                    help: "The TV channel where the campaign is played for the highest number of times for the chosen duration",
                    data: []
                },
                top_radio_channel: {
                    label: "Top Radio Channel",
                    help: "The FM channel where the campaign is played for the highest number of times for the chosen duration",
                    data: []
                },
                top_tv_interval: {
                    label: "Top TV Interval",
                    help: "",
                    data: []
                },
                top_radio_interval: {
                    label: "Top Radio Interval",
                    help: "",
                    data: []
                },
                top_day: {
                    label: "Top Day",
                    help: "",
                    data: []
                },
                top_date: {
                    label: "Top Date",
                    help: "",
                    data: []
                },

            }
            },
        };
    },
    watch: {
        selected_special_campaign: function(){
            this.generated = false;
            // this.generate_special_report();
        },
        special_report_date_range: function(){
            this.generated = false;
            // this.generate_special_report();
        },
        selected_special_industry: function(){
            this.generated = false;
            this.getAllIndustryCampaigns(this.selected_special_industry.id);
            // this.generate_special_report();
        },
        selected_industry: function(selectedIndustry){
            this.generated = false;
            // this.generate_special_report();

            // if(selectedIndustry.length == 1) {

            // }else if(selectedIndustry.length ==2) {

            // }

        }
    },
    methods: {
        getAllIndustries() {
            let self = this;
            var _url = '/companies/api/parent/industries/';
            self.$http.get(_url)
            .then(function(response) {
                var inst_industry = response.body;
                inst_industry.unshift({
                    name: 'All Industries',
                    id: ''
                });
            self.industry_list  = inst_industry;
            });
            // fetch('/companies/api/brands/',{method:'get'}).then()
        },
        getIndustryList() {
            var self = this;
            this.$http.get('/companies/api/hierarchy/industries/')
            .then(function(resp){
                self.all_industry_list = resp.body;
            });
        },
        getAllIndustryCampaigns(industry_id) {
            let self = this;
            var _url = '/campaign/sponsored_by_ads/';
            var options = {}
            if(industry_id){
                options.industry = industry_id
            }
            self.$http.get(_url, { params: options})
            .then(function(response) {
                var inst_campaign = response.body;
                inst_campaign.unshift({
                    name: 'All Campaigns',
                    id: ''
                });
            self.campaign_list  = inst_campaign;
            });
            // fetch('/companies/api/brands/',{method:'get'}).then()
        },
        //Special report
        generate_special_report: function(){
                //@todo make a button to generate the report since
                //it takes time to generate report
                //and change of option may trigger request (wastage)
                //@todo remove from dashboard and move to reports
                let _this = this;
                var _url = _this.special_report.api_url+'daterange='+_this.special_report_date_range;
                var parameter = '';
                if(this.selected_special_campaign.hasOwnProperty('id')){
                    if(this.selected_special_campaign.id) {
                        parameter += "&campaign="+this.selected_special_campaign.id;
                    }
                }
                // if(this.selected_special_industry.hasOwnProperty('id')){
                //     if(this.selected_special_industry.id) {
                //         parameter += "&industry="+this.selected_special_industry.id;
                //     }
                // }
                if(this.selected_industry.length == 1) {
                    //select the industry if subindustry is not selected
                    parameter += "&industry="+this.selected_industry[0];

                }else if(this.selected_industry.length ==2) {
                    //select subindustry if selected (level2)
                    parameter += "&industry="+this.selected_industry[1];

                }else{
                    //industry or subindustry not selected
                    // return false;
                }

                console.debug(parameter,parameter.length);
                if(!parameter.length){
                    this.generated = false;
                    return false;
                }
                _url = _url+parameter;
                _this.special_report.progress = 0;
                _this.special_report.xhr = $.ajax({
                url: _url,
                async: true,
                xhr () {
                    var xhr = new window.XMLHttpRequest();
                    xhr.upload.addEventListener("progress", function (evt) {
                        if (evt.lengthComputable) {
                            var percentComplete = evt.loaded / evt.total;
                            // //console.log(percentComplete);
                            _this.special_report.progress = percentComplete;
                        }
                    }, false);
                    xhr.addEventListener("progress", function (evt) {
                        if (evt.lengthComputable) {
                            var percentComplete = evt.loaded / evt.total;
                            // //console.log(percentComplete);
                            _this.special_report.progress = percentComplete*100;
                        }
                    }, false);
                    return xhr;
                }
                });

                _this.special_report.xhr.then((result) => {
                _this.special_report.data = result.payload;
                _this.generated = true;
                });
                _this.special_report.xhr.catch((result) => {
                    _this.generated = true;
                    _this.special_report.data = [];
                });

        }

    },


  computed: {

      default_selected_spec_camp() {
        if (this.campaign_list.length) {
          return this.campaign_list[0];
        }
        return {};
      },

      default_selected_spec_ind() {
        if (this.industry_list.length) {
          return this.industry_list[0];
        }
        return {};
      },

      is_loading() {
          return this.special_report.xhr.readyState && this.special_report.xhr.readyState > 0
          && this.special_report.xhr.readyState < 4;
      },

      is_valid() {
        let _this = this;
        if(!this.special_report_date_range) {
            return false;
        }
        let campaign_selected =  this.selected_special_campaign.hasOwnProperty('id') && this.selected_special_campaign.id;
        if(!campaign_selected){
          let industry_selected = this.selected_industry.length > 0;
          if(!industry_selected) {
              return false;
          }

        }
        return true;
      },



  },

  created() {
    let self = this;
    console.log('ready');
    // this.getAllIndustries();
    this.getIndustryList();

    this.special_report_date_range = this.$parent.defaultDatepickerOptions.date;

  },



  mounted(){
      this.all_campaign_list = this.all_campaigns;
      this.campaign_list = this.all_campaign_list;

    //   this.special_report_date_range = this.datepicker_option.date
  },
  components: {
        vselect: VueMultiselect.default
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

#top-reports-components .panel-body{
    min-height: 170px;
}
.top-report-filters .el-cascader{
    width:100%;
}
@media(max-width: 1024px) {
    .top-report-filters .col{
        padding:2px!important;

    }
}

@media(max-width: 540px) {
    .top-report-filters .col{
        padding:0!important;
        max-width: inherit!important;
    }
}

</style>
