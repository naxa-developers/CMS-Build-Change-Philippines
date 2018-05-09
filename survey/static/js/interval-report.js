
var intervalReportPage = (function() {

// Vue.component('v-select', VueSelect.VueSelect);
for (var i=0; i< interval_report_json.interval_channels.length; i++) {
  interval_report_json.interval_channels[i].interval_result= [];
  interval_report_json.interval_channels[i].expanded= false;
  interval_report_json.interval_channels[i].xhr= new XMLHttpRequest();
  interval_report_json.interval_channels[i].progress= 0;
}

var report_app = new Vue({
  el: "#interval-report-app",
  template: "#interval-report-template",
  data: {
    current_campaign : 0,
    current_campaign_json: interval_report_json.campaign,
    date_range : interval_report_json.date_range,
    interval_channels :  interval_report_json.interval_channels,
    interval_campaigns: interval_report_json.interval_campaigns,
    subscribed_detail: {},
    ads: [],
    ad: '',
    channels: [],
    selected_channel: [],
    loading: false,
    validation_message: "",
  },

  watch: {
    'current_campaign': function(prev,current){
      var atma = this;
      var current_campaign = atma.current_campaign;
      var interval_date_range = atma.date_range;
      var interval_channels = atma.interval_channels;
      if(prev!=current) {
        $.each(interval_channels, function(i, channel_object){
          channel_object.interval_result = [];
        });
        atma.campaign_channels(current_campaign['id']);
        atma.campaign_subscription(current_campaign['id']);
      }
      // $.each(interval_channels, function(i, channel){
      //   atma.cancelIntervalReport(channel);
      //   atma.request_interval_report_data(channel);
      // });
      // atma.generate_interval(current_campaign, interval_date_range, interval_channels);

    }
  },
  methods:{
    render_date: function(given_date, format){
      return  moment(given_date).format(format);
    },
    round_up: function(num){
      return num.toFixed(2);
    },
    display_completion_status: function(status){
      if(status == 0){
        return "Incomplete"
      }else{
        return "Complete"
      }
    },
    display_review_status: function(status){
      if(status == 0){
        return "Pending"
      }else{
        return "Reviewed"
      }
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
            options[i].interval_result= [];
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
    request_interval_report_data: function(channel){
        var _this = this;
        var interval_api_url = "/matches/campaign-interval-api/"+_this.current_campaign['id']+"/"+_this.date_range+"/"+channel['id']+"/";
        channel.progress=0;
        channel.expanded = false;
        channel.xhr = $.ajax({
          url: interval_api_url,
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
          channel.interval_result = result.interval_result;
          channel.loading = false;
          channel.expanded = true;
          console.log('finished getting data for channel ',channel['id']);
        });


    },
    cancelIntervalReport(channel){
      if(channel.xhr && channel.xhr.abort){
        channel.xhr.abort();
      }

    },
    generate_interval: function(current_campaign, interval_date_range, interval_channels){
      $.each(interval_channels, function(i, channel_object){
        channel_object.interval_result = [];
        var interval_api_url = "/matches/interval-api/"+current_campaign+"/"+interval_date_range+"/"+channel_object['id']+"/";
        $.getJSON(interval_api_url, function(result) {
          channel_object.interval_result = result.interval_result;

        });
      });
    },
    campaign_subscription: function(current_campaign){
      var atma = this
      if(current_campaign > 0 || current_campaign.length){
        var sucribed_detail_url = "/matches/subscribed-detail-api/"+current_campaign+"/";
        $.getJSON(sucribed_detail_url, function(result) {
          atma.subscribed_detail = result;
          atma.loading = false;
        });
      }
    },
    campaign_channels: function(current_campaign){
      var atma = this
      if(current_campaign > 0 || current_campaign.length){
        var subscribed_ad_channels = "/matches/subscribed-channels-api/"+current_campaign+"/";
        $.getJSON(subscribed_ad_channels, function(result) {
          atma.loading = false;
          var updated_channel = result['channels'];
          // for (var i=0; i< updated_channel.length; i++) {
          //   updated_channel[i].interval_result= [];
          //   updated_channel[i].expanded= false;
          //   updated_channel[i].xhr= new XMLHttpRequest();
          //   updated_channel[i].progress= 0;
          //   // frequency_report_json.channels[i].status= 'request_not_set';
          // }
          atma.interval_channels = updated_channel;
        });
      }
    }
  },
  created() {
    var atma = this;
    // atma.loadAds();
    // atma.loadChannels();
    var current_campaign = atma.current_campaign;
    // var interval_date_range = atma.date_range;
    var interval_channels = atma.interval_channels;
//    atma.campaign_subscription(current_campaign);
    // $.each(interval_channels, function(i, channel){
    //   atma.cancelIntervalReport(channel);
    //   atma.request_interval_report_data(channel);
    // });
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
