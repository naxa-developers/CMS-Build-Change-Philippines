<template>
<div id="noticeboard_panel" v-loading="is_loading" element-loading-text="Loading notices" element-loading-spinner="el-icon-loading" element-loading-background="white">
    <div class="panel panel-default">
        <div class="panel-heading b-b b-light font-bold" style="padding: 10px 15px 10px 15px;">
            Notices Board
        </div>
        <div v-bar>
            <div class="panel-body m-b-md" style="overflow-y: auto;min-height:250px;max-height: 30vh; padding: 0;">
                <!-- <div class="m-b" v-for="n in notices">
                <div class="">
                    <div class="wrapper-sm clear b-b ">
                    <small class="text-muted pull-right" v-text="displayDate(n.date,'relative')"> </small>
                    <p class="b-b-xs clear" v-text="n.description"></p>
                    <small class=" label-primary label pull-left m-r-xs " v-text="n.campaign"> </small>
                    <span v-bind:class="{'label-danger':n.type==1,'label-warning':n.type==2,'label-success':n.type==3,}" v-text="n.name" class="label pull-left  text-ellipsis"></span>
                    </div>
                </div>
                </div> -->
                <div class="padder-md">
                <div class=" alt streamline b-l m-b m-t-xs">
                    <div class=" sl-item" v-bind:class="{'b-l b-danger':n.type==1,'b-l b-warning':(n.type==2 || n.type==0),'b-l b-success':n.type==3,}"  v-for="n in notices">
                    <div class="m-l">
                        <small class="text-muted" data-style="clear:both" :title="displayDate(n.date,'LLL')" v-text="displayDate(n.date,'relative')"> </small>





                        <span class="pull-right">
                        <span v-bind:class="{'label-danger':n.type==1,'label-warning': (n.type==2 || n.type==0) ,'label-success':n.type==3,}" v-text="n.name" class="label pull-right  text-ellipsis"></span>
                        <small class=" label-primary label pull-right m-l-xs m-r-xs " v-text="n.campaign"> </small>
                        </span>
                        <div>
                        <p class="b-b-xs inline" v-bind:class="{'text-muted':n.seen}" v-text="n.description"></p><i v-bind:class="{' fa-check-circle-o':n.seen,'fa-circle-o':!n.seen}" class="fa text-xs pull-right"></i>
                        </div>


                        <hr class="clear m-t-xs m-b-xs">

                    </div>
                    </div>
                </div>
                </div>
            </div>
        </div>
    </div>   
</div>
</template>

<script>
/* eslint-disable */

const VueMultiselect = require('../../../vendor/vue-multiselect/vue-multiselect.min.js');

export default {
  name: "NoticeBoard",
  components: {
      vselect: VueMultiselect.default
    },
    props: {
      notices: {
        type: Array
      },
      is_loading: {
        type: Boolean
      }
    },
    mixins: [notificationMixin]
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
