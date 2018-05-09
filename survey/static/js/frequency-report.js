// Vue.component('v-select', VueSelect.VueSelect);
// for (var i=0; i< frequency_report_json.channels.length; i++) {
//   frequency_report_json.channels[i].frequency_result= [];
//   frequency_report_json.channels[i].expanded= false;
//   frequency_report_json.channels[i].xhr= new XMLHttpRequest();
//   frequency_report_json.channels[i].progress= 0;
//   // frequency_report_json.channels[i].status= 'request_not_set';
// }

//list of status
//1. request_not_sent
//2. requested
//3. loaded
//3. loaded
// alert('1.1.3.2');


var frequencyReportPage = (function() {

var report_app = new Vue({
  el: "#frequency-report-app",
  template: "#frequency-report-template",
  data: {
    // current_campaign : frequency_report_json.campaign['id'],
    current_campaign : 0,
    current_campaign_json: frequency_report_json.campaign,
    date_range : frequency_report_json.date_range,
    datepickeroptions: {
      // timePicker: true,
    },
    frequency_channels :  frequency_report_json.frequency_channels,
    campaigns: frequency_report_json.campaigns,
    selected_channels: [],
    subscribed_detail: {},
    ads: [],
    ad: '',
    channels: [],
    selected_channel: [],
    loading: false,
    validation_message: ""
  },
  
  methods:{
    request_frequency_report_data: function(channel){
        var _this = this;
        var frequency_api_url = "/matches/campaign-frequency-api/"+this.current_campaign['id']+"/"+this.date_range+"/"+channel['id']+"/";
        channel.progress=0;
        channel.expanded = false;
        channel.xhr = $.ajax({
          url: frequency_api_url,
          async:true,
          xhr: function () {
            var xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener("progress", function (evt) {
                if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    console.log(percentComplete);
                    channel.progress = percentComplete;
                }
            }, false);
            xhr.addEventListener("progress", function (evt) {
                if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    console.log(percentComplete);
                    channel.progress = percentComplete*100;
                }
            }, false);
            return xhr;
          },
        });

        channel.xhr.then(function(result) {
          channel.frequency_result = result.frequency_result;
          channel.loading = false;
          channel.expanded = true;
          console.log('finished getting data for channel ',channel['id']);
        });


    },
    loadAds: function () {
        var self = this;

        options = {};
        function successCallback (response){
            self.ads = response.body;

        }

        function errorCallback (){
            console.log('failed');
        }
       self.$http.get('/campaign/sponsored_by_ads/', [options]).then(successCallback, errorCallback);


    },
    loadChannels: function () {
            var self = this;

        options = {};
        function successCallback (response){
            self.channels = response.body;

        }

        function errorCallback (){
            console.log('failed');
        }
       self.$http.get('/execution/api/channels/', [options]).then(successCallback, errorCallback);


    },
    generateData : function(){
        var self = this;
        var options = [];
        if(self.selected_channel.length && self.current_campaign){
          self.selected_channel.map(function(item) {
              // return item.id;
              options.push({'id': item.id, 'name': item.name});
          });
          self.loading = false;
          for (var i=0; i< options.length; i++) {
            options[i].frequency_result= [];
            options[i].expanded= false;
            options[i].xhr= new XMLHttpRequest();
            options[i].progress= 0;
          }
          self.channels = options;
          self.validation_message = ""
        }else{
          self.validation_message = "Please select campaign and at least one channel to generate data!";
        }
    },

    cancelFrequencyReport(channel){
      if(channel.xhr && channel.xhr.abort){
        channel.xhr.abort();
      }
    },
    campaign_subscription: function(current_campaign){
      var atma = this;
      if(current_campaign > 0 || current_campaign.length){
        var sucribed_detail_url = "/matches/subscribed-detail-api/"+current_campaign+"/";
        atma.loading = true;
        $.getJSON(sucribed_detail_url, function(result) {
          atma.subscribed_detail = result;
          atma.loading = false;
        });
      }

    },
    campaign_channels: function(current_campaign){
      var atma = this
      if(current_campaign > 0){
        var subscribed_ad_channels = "/matches/subscribed-channels-api/"+current_campaign+"/";
        $.getJSON(subscribed_ad_channels, function(result) {
          atma.loading = false;
          var updated_channel = result['channels'];
          // for (var i=0; i< updated_channel.length; i++) {
          //   updated_channel[i].frequency_result= [];
          //   updated_channel[i].expanded= false;
          //   updated_channel[i].xhr= new XMLHttpRequest();
          //   updated_channel[i].progress= 0;
          //   // frequency_report_json.channels[i].status= 'request_not_set';
          // }
          atma.frequency_channels = updated_channel;
        });
      }
    },
  },
  watch: {
    'current_campaign': function(prev,current){
      var atma = this;
      if(prev!=current) {
        if(atma.current_campaign > 0 || atma.current_campaign){
          $.each(this.channels, function(i, channel_object){
            channel_object.frequency_result = [];

          });
          atma.campaign_channels(atma.current_campaign['id']);
          atma.campaign_subscription(atma.current_campaign['id']);
        }
      }
      // var current_campaign = ;
      // var frequency_date_range = atma.date_range;
      // var channels = ;
      // atma.generate_frequency(current_campaign, frequency_date_range, channels);
      // console.log(atma.current_campaign['id']);


      // $.each(atma.channels, function(i, channel){
      //   atma.cancelFrequencyReport(channel);
      //   atma.request_frequency_report_data(channel);
      // });

    },

    ldata: function(newVal, oldVal){
      if(newVal) {
        this.generateData();
      }
    }
  },
  created() {
    var atma = this;
    // atma.loadAds();
    // atma.loadChannels();

    var current_campaign = atma.current_campaign;
    var frequency_date_range = atma.date_range;
    var channels = atma.channels;
    // atma.generate_frequency(current_campaign, frequency_date_range, channels);
    atma.campaign_subscription(current_campaign);
    Rare.events.$on('pjax:unload', () => {
      console.debug('frequency-report:garbage collection')
      atma.$destroy();
    });
    // console.debug(atma.current_campaign);

  },
  components: {
    // register component
    'v-tippy': VueTippy,
    'vselect': VueMultiselect.default,
    
    // 'v-bar':Vuebar
    // 'v-select': VueSelect.VueSelect
  }
});

});
