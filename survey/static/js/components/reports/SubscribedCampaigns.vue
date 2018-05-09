<template>
<div id="subscribed_campaigns" v-loading="is_loading" element-loading-text="Loading subscribed campaign list" element-loading-spinner="el-icon-loading" element-loading-background="white">
   <div class="panel b-a">
        <div class="panel-heading b-b b-light clear" style="padding: 10px 15px">
        <span href class="font-bold">Campaigns</span>
        <!-- <div class="col-md-4"><vselect :options="['Active', 'Inactive', 'Soon Expiring', 'Subscription Expired']"></vselect></div> -->
        <!-- <div class="col-md-6" style="">

        </div> -->
            <span class="text-xs text-muted pull-right">
                <span class="m-r-xs clickable" v-bind:class="{'text-dark': active_campaign_type=='all'}" @click="active_campaign_type='all'"><i class="fa fa-circle"></i>All</span>

                <span v-text="campaigns.length"></span>
                <!-- <animate-number :value="campaigns.length"></animate-number> -->

                <span class="m-r-xs  clickable" v-bind:class="{'text-info': active_campaign_type=='own'}" @click="active_campaign_type ='own'" ><i class="fa fa-circle m-l-sm" ></i>Own</span>
                <span v-text="ownCampaignsCount"></span>
                <!-- <animate-number :value="ownCampaignsCount"></animate-number> -->
                <span class="m-r-xs clickable" v-bind:class="{'text-warning': active_campaign_type=='competitor'}" @click="active_campaign_type ='competitor'"><i class="fa fa-circle m-l-sm"></i>Competitor</span>
                <span v-text="competitorsCampaignsCount"></span>
                <!-- <animate-number v-if="competitorsCampaignsCount" :value="competitorsCampaignsCount"></animate-number> -->

                </span>



        </div>
        <div v-bar>
        <ul class="list-group list-group-lg no-bg auto" style="overflow-y:auto;" v-bind:style="customStyle">
            <campaign-list-item v-for="c in filteredCampaigns" :campaign="c" :key="c.id"></campaign-list-item>

        </ul>
        </div>
    </div>
</div>
</template>

<script>
/* eslint-disable */


 let campaignsMixins = {
    computed: {

       competitorsCampaigns() {
          return this.campaigns.filter(function(c) {
            return c.subscribed_campaign__is_competitor;
          });
        },

       ownCampaigns() {
          return this.campaigns.filter(function(c) {
            return !c.subscribed_campaign__is_competitor;
          });
        },

       competitorsCampaignsCount() {
          return this.competitorsCampaigns.length;
        },

       ownCampaignsCount() {
          return this.ownCampaigns.length;
        }

     }
  };

let campaignListItem = {
    template: `
      <li class="list-group-item clearfix" v-bind:id="'campaign-'+campaign.id">
          <span v-text="campaign.name"  class="h4 clear"></span>
          <small v-for="t in tags" v-bind:class="t.class" v-bind:title="t.title?t.title:''" class="m-r-xs" v-text="t.name"></small>
        </span>
      </li>
    `,
    props: {
      campaign: {
        type: Object
      }
    },
    data(){
      return {
        tags: []
      }
    },

    computed: {
      subscription_duration() {
        return moment.duration(this.campaign.subscribed_campaign__from_date,this.campaign.subscribed_campaign__to_date).humanize();
      },
      isActive() {
        // return true;
        return moment().isBetween(this.campaign.subscribed_campaign__from_date, this.campaign.subscribed_campaign__to_date);
      }

    },
    mounted(){

      if(this.campaign.subscribed_campaign__is_competitor) {
        this.tags.push({
          name: this.campaign.company__name,
          class:'label label-warning',
          title: 'Competitor\'s campaign'
        });
      }else {

        this.tags.push({
            name:this.campaign.company__name,
            class:'label label-info',
            title: 'Own campaign'
        });

      }

      let subscriptionDetail = 'Subscribed: '+this.campaign.subscribed_campaign__from_date + ' to '+ this.campaign.subscribed_campaign__to_date;

      if(this.isActive) {
        // let duration = moment(this.campaign.subscribed_campaign__to_date).diff(moment(this.campaign.subscribed_campaign__from_date));
        let sentiment = 'label-success';
        let remaining_duration = moment(this.campaign.subscribed_campaign__to_date).diff(moment(),'days');
        if(remaining_duration <= 10) {
          sentiment = 'label-warning';
          subscriptionDetail += ' Expiring in '+ remaining_duration + 'days';
        }

        // let duration= this.subscription_duration;
        this.tags.push({
          name: 'subscription-active',
          class:'v-tippy label ' + sentiment,
          title: subscriptionDetail
        });
      }else{
        let duration = moment().diff(moment(this.campaign.subscribed_campaign__to_date),'days');
        this.tags.push({
          name: 'subscription-expired',
          class:'label label-danger v-tippy',
          title: subscriptionDetail
        });
      }

      if(this.campaign.total_detected) {

        this.tags.push({
          name: this.campaign.total_detected + ' ad detected',
          class:'label bg-light v-tippy',
          title: '',//this.campaign.complete_detected + ' complete'
        });
      }






          // <small class=" label-primary label pull-left m-r-xs " v-text="campaign.company__name"> </small>
          // <!-- <small class="text-muted clear text-ellipsis " v-text="campaign.company__name"></small> -->
          // <span v-text="campaign.subscribed_campaign__from_date"></span>-<span v-text="campaign.subscribed_campaign__to_date"></span>
          // <small v-if="campaign.subscribed_campaign__is_competitor" class=" label-warning label pull-left m-r-xs ">Competitor</small>


    }
  };

export default {
  name: "SubscribedCampaigns",
  components: {
    //   'v-bar': Vuebar,
      'campaign-list-item': campaignListItem
    },

    props: {
      campaigns: {
        type: Array
      },
      is_loading: {
        type: Boolean
      }
    },

    data() {
      return {
        active_campaign_type: 'all'
      };
    },

    destroyed() {
      console.log('destroy event has been fired inside campaign panel');
    },

    methods: {

    },

    computed: {

      filteredCampaigns() {
        if(this.active_campaign_type == 'all') return this.campaigns;
        if(this.active_campaign_type == 'own') return this.ownCampaigns;
        if(this.active_campaign_type == 'competitor') return this.competitorsCampaigns;
      },

      customStyle() {
        let c = {
          maxHeight:'250px'
        };
        if(this.filteredCampaigns.length > 10 ) {
          c.maxHeight = '450px';
        }
        return c;

        // min-height:250px;max-height: 30vh;
      }

    },

    mixins: [campaignsMixins]
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
