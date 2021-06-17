import Vue from 'vue'
// import VueResource from 'vue-resource'
import jQuery from 'jquery'

var initialNotifications = []

var notificationList = {

  // props: ['notifications', 'title'],
  props: {
    'notifications': {
      type:Array
    },
    'title': {
      type: String
    }
  },
  mixins: [notificationMixin],
  template: `
    <div>
      <!--<button v-on:click="shuffleNotice" class="btn custom-button">Shuffle Notification</button>-->
      <div class="notification">
        <transition-group name="fade" tag="ul" class="timeline">
          <li :key="'not_'+notification.id" v-for="notification in notifications"  class="tl-item">
            <div class="tl-wrap b-info">
              <span class="tl-date" v-bind:title="displayDate(notification.date,'LLLL')"><i class="fa fa-fw fa-clock-o"></i>{{ displayDate(notification.date,'relative')}}</span>
              <div class="tl-content box">
                <span class="mobile-tl-date" v-bind:title="displayDate(notification.date,'LLLL')"><i class="fa fa-fw fa-clock-o"></i>{{ displayDate(notification.date,'relative')}}</span>

                <span class=" m-b-none" v-if="notification.title" v-text="notification.title"></span>

                <span class=" m-b-none" v-if="notification.description" v-text="notification.description"></span>


                            <span  v-for="val,prop in notification" class="block" >
                            <span class="pull-left" v-if="['title','date','action_link','type','description','name','id','seen'].indexOf(prop) == -1 " >
                              <span class="label bg-light pos-rlt m-r inline wrapper-xs"><i class="arrow right arrow-light"></i> {{prop}}:</span>
                              <span class="m-r-sm">{{val}}</span>
                            </span>
                          </span>







                            <span class="block m-b-none">
                        <span class="pull-right text-muted ">
                            <small class="text-muted  text-xs m-t-xs" v-bind:title="notification.date"> </small>
                        </span>


                        </span>





              </div>
            </div>
          </li>
        </transition-group>

      </div>
    </div>
  `,

  methods: {
    shuffleNotice: function() {
      this.items = _.shuffle(this.items)
    }
  }
};



var noticeApp = new Vue({
  el: '#notice',
  // components: ['notification-list'],
  components: {
    'notification-list': notificationList
  },
  data: {
    currentTab: 'detected_notices',
    notifications: {
      detected_ads: [],
      da_page: 1,
      notice_page: 1,
      company_notices: [
        // {
        //  "date":"2017-09-17 16:47:36",
        //  "type":"detected_ad",
        //  "campaign":"soffola",
        //  "channel":"Himalaya",
        //  "ad":"soffolaads"
        // },
        // {
        //  "title":"Your subscription will expire in few days",
        //  "type":"notification",
        //  "description":"Please contact sales for detail",
        //  "date":"2017-09-17 16:47:36",
        // }
      ],
    },

    title: "Company Notifications"
  },
  created() {
    var _this = this;
    this.getCompanyNotices();
    this.getDetectedAds();

    Rare.events.$on('new_notification', (data) => {
      _this.notifications.detected_ads.unshift(data);
      console.log(data);
      // this.msg = 'I heard an event.';
    });

    // this.loadData();


  },

  computed: {
    // currrentNotifications() {
    //  if(this.currentTab == 'detected_notice') {
    //    return this.notifications['detected_ad'];
    //  }
    //  return this.notifications['company_notice'];

    // }
  },
  methods: {

    updateLastSeen() {
      // sets last seen to now.
      $.get('/execution/api/notification/detected_ads_mark_seen/').then(function(resp) {
        console.log(resp);
      })
    },

    getDetectedAds() {
      var vm = this;
      // let headers = new Headers();
      // headers.append('X-CSRFToken',Rare.utils.readCookie('csrftoken'));
      // fetch('/execution/api/notification/detected_ads/',{
      //  method: 'GET',
      //  headers: headers
      // })
      // .then(function(resp) {
      //  return resp.json()
      // }).then(function(freshList){
      //  vm.notifications.detected_ad = [...freshList, ...vm.notifications.detected_ad];
      // });


      jQuery.ajax('/execution/api/notification/detected_ads/', {
          method: "GET",

          contentType: "application/json",
          data: { 'page': vm.notifications.da_page }
          // beforeSend: function (xhr) {
          //  xhr.setRequestHeader('X-CSRFToken', Rare.utils.readCookie('csrftoken'))
          // },

        })
        .then(function(response) {
          //        console.log(response)
          vm.notifications.detected_ads = response.results;
          vm.notifications.da_page = response.page;

          vm.updateLastSeen();

        }, function(err) {
          console.log(err);
        });


    },

    getCompanyNotices() {
      var vm = this;
      jQuery.ajax('/execution/api/notification/company/', {
          method: "GET",
          contentType: "application/json"
        })
        .then(function(response) {
          //        console.log(response)
          vm.notifications.company_notices = [...response, ...vm.notifications.company_notices];

        }, function(err) {
          console.log(err);
        });


    },

    setTap: function(menu) {
      this.currentTab = menu;
    },

    loadData() {
      switch (this.currentTab) {
        case 'detected_notices':
          this.getDetectedAds();
          break

        default:
          this.getCompanyNotices();
          break
      }
    }
  }
});
