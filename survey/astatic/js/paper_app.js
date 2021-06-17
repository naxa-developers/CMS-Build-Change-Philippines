Vue.component('v-select', VueSelect.VueSelect);
var bus = new Vue({});

var app3 = new Vue({
  el: '#app',
  data: {
    currentPage:'content',
  },
  methods: {
    setMenu: function (menu) {
    this.currentPage = menu;

    },
	},
//	events: {
//        adsChanged: function (argument) {
//            alert(argument);
//        },
//    },
// http: {
//    root: '/root',
//    headers: {
//      Authorization: 'YXBpOnBhc3N3b3Jk'
//    }
//  },


})