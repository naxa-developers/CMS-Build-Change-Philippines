Vue.component('dashboard-notice', {
	props: ['notifications', 'title'],
	template: `
		<div>
			<H2>I am notice boot</H2>
			<ul>
				<li v-for="notification in notifications" v-bind:key="notification">
					<span class="date" v-bind:title="displayDate(notification.date,'LLLL')"></span>
				</li>
			</ul>
		</div>
	`
});

/*
var dashNotice = new Vue({
	el: '#notices',
	components: ['dashboard-notice'],
	data: {

	},
	created() {
		var _this = this;
		this.getCompanyNotices();

		Rare.events.$on('new_notification', (data) => {
            _this.notifications.detected_ads.unshift(data);
            console.log(data);
        });

		// this.loadData();


	},

	methods: {
		updateLastSeen() {
	       // sets last seen to now.
	       $.get('/execution/api/notification/mark_all_seen/').then(function(resp) {
	        console.log(resp);
	       })
	    },
		getCompanyNotices() {
			var vm = this;
			jQuery.ajax('/execution/api/notification/company/', {
				method: "GET",
				contentType: "application/json"
			})
			.then(function (response) {
//				console.log(response)
				vm.notifications.company_notices = [...response, ...vm.notifications.company_notices];

			}, function (err) {
				console.log(err);
			});


		}
	}

})
*/
