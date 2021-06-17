
Vue.component('ui-content', {
	props: ['pages'],
	template: `
		<div v-show=pages>
			<div v-bind:style="styleObject" v-show=showForm>
				<div class="panel panel-default">
					<div class="panel-heading">
						<h1 class="panel-title">{{title}}</h1>
					</div>
					<div class="panel-body">
						<div class="radio radio-inl">
			              <label class="i-checks i-checks-sm">
			                <input type="radio" name="checkRadio" value="0" v-model="content_data.type"/>
			                <i></i>
			                Ads
			              </label>
			            </div>
			            <div class="radio radio-inl">
			              <label class="i-checks i-checks-sm">
			                <input type="radio" name="checkRadio" value="1" v-model="content_data.type"/>
			                <i></i>
			                News
			              </label>
			            </div>

						<div>
				            <form action="#">
				            	<div class="form-group">
                                    <label> Select Media</label>
                                    <v-select :options="media_list" label="name" v-model="content_data.media" :on-change="updateMediaPage"></v-select>
    			            	</div>

    			            	<div class="form-group">
                                    <label> Select Page</label>
                                    <v-select :options="page_list" label="alias" v-model="content_data.page"></v-select>
    			            	</div>

				            	<div class="form-group">
				            		<label> Select Ad</label>
                                    <v-select :options="ad_list" label="name" v-model="content_data.ad"></v-select>
				            	</div>

				            	<label v-show="content_data.type==1"> Select Sentimental</label>
                                <div class="form-group" v-show="content_data.type==1">
				            		<v-select :options="['1','2','3','4','5']"  v-model="content_data.sentimental"></v-select>
				            	</div>

				            	<div class="form-group">
				            	   <label> CC</label>
				            	   <input type="number" v-model="content_data.cc" class="form-control " placeholder="CC">
				            	</div>

				            	<div class="form-group">
				            		<input type="file" class="form-control " placeholder="CC"><br>
                                    <dropzone id="myVueDropzone" url="#"
                                    v-on:vdropzone-files-added="showSuccess">
                                        <input type="hidden" name="token" value="xxx">
                                    </dropzone>
				            	</div>
				            	<div class="form-gropu">
				            		<a class="btn m-b-xs btn-sm btn-primary btn-addon" v-on:click="save()"><i class="fa fa-download"></i>Save</a>
				            	</div>
				            </form>
	                    </div>

					</div>
				</div>
			</div>
			<div>
			 <button v-on:click="addContent()" class="btn btn-primary"><i class="fa fa-plus" aria-hidden="true"></i></button>
                <table class="table table-hover">
                <thead>
                <tr> <th>#</th> <th>Date</th><th>Ad Name</th> <th>Media</th> <th>Type</th><th>Sentimental</th>
                 <th>cc</th><th>Attachments</th><th>Edit</th> </tr>
                </thead> <tbody>
                 <tr v-for="obj, index in contents">
                  <td scope="row">{{index+1}}</td>
                   <td>{{obj.date}}</td>
                   <td>{{obj.ad.name}}</td>
                    <td>{{obj.media.name}}</td>
                    <td>{{obj.type_display}}</td>
                    <td><span v-show="obj.type=='1'">{{obj.sentimental}}</span></td>
                    <td>{{obj.cc}}</td>
                    <td><div v-for="img in obj.ci">
                        <img :src="img.image" height=50, width=50>
                    </div></td>
                     <td><a v-on:click="editContent(obj)" class="btn-edit"><i class="fa fa-edit" aria-hidden="true"></i></a></td>

                 </tr>

                 </tbody> </table>
             </div>

		</div>

 		`,

    components: {
        Dropzone: vue2dropzone
    },
	data: function() {
		return {
			title : 'Content Forms',
			ads: true,
			news: true,
			showAds: false,
			showNews: false,
  			styleObject: {
			    
			},
			contents : [],
            content_data:{'type':"0", 'media':"", 'ad':"", 'cc':200,'page':""},
            showForm :false,
            ad_list: [],
            media_list: [],
            page_list: [],
            attachments: [],

		}
	},
//	events: {
//        adsChanged: function (argument) {
//            alert(argument);
//        },
//    },

	computed: {
    // a computed getter
//    ad_list: function () {
//      // `this` points to the vm instance
//      return app3.$children[0].$data.ads
//    },
//    media_list: function () {
//      // `this` points to the vm instance
//      return app3.$children[1].$data.ads
//    },
  },

	methods: {
        'showSuccess' : function(files) {
        	var self = this;
        	console.log(files[0]);
            self.$nextTick(function () {
                for(i=0; i < files.length; i ++){
                    console.log(files[i]);
                    self.attachments.push(files[i]);
      }
      })

//            bus.$emit('attachmentsChange', self.attachments);
        },

        updateMediaPage: function(val) {
            var self =this;
            if(val){
            self.getMediaPages(val);
            }
        },
		showHide: function(showAds) {
			if(showAds == false) {
				this.showAds = true
			}else {
				this.showNews = true
			}
		},
        addContent: function () {
            this.showForm = true;
            this.content_data = {'type':"0", 'cc':200};
        },
        editContent: function (content) {
        this.showForm = true;
        this.content_data = content;

        },
        doeditPage: function () {
        //     this.$validator.validateAll();
          if (this.errors.first('alias')) {
            alert('Please Enter Page')
          }else if (this.errors.first('price')) {
            alert('Please Enter Corrent Price')
          }else{
          this.updatePage();

          }
        },
        getContents : function () {
            var self = this;

            options = {};
            function successCallback (response){
                self.contents = response.body.results;
            }

            function errorCallback (){
                console.log('failed');
            }
           self.$http.get('/paper-tracking/content/', [options]).then(successCallback, errorCallback);

    },
      getMediaPages : function (media) {
        var self = this;

        options = {};
        function successCallback (response){
            self.page_list = response.body;
            self.content_data.media = media;
            if(self.page_list.length > 0){
            self.content_data.page = self.page_list[0];
            }else{
            self.content_data.page = '';
            }
//            console.log(self.content_data);
        }

        function errorCallback (){
            console.log('failed');
        }
       self.$http.get('/paper-tracking/api/media/mediapage/'+media.id+'/', [options]).then(successCallback, errorCallback);

    },
        saveContent : function () {
            var self = this;
            csrf = $('[name = "csrfmiddlewaretoken"]').val();
            options = {headers: {'X-CSRFToken':csrf}};
            body = self.content_data;

            var formData = new FormData();
            formData.append('media',self.content_data.media.id);
            formData.append('page',self.content_data.page.id);
            formData.append('ad',self.content_data.ad.id);
            formData.append('type',self.content_data.type);
            if(self.content_data.type == '1'){
                formData.append('sentimental',self.content_data.sentimental);
            }
            formData.append('cc',self.content_data.cc);
            for (var i = 0; i < self.attachments.length; i++) {
              formData.append('new_images_'+String(i), self.attachments[i]);
            }


            function successCallback (response){
            self.showForm = false;
            self.content_data={'type':"0", 'media':"", 'ad':"", 'cc':200,'page':""};

                self.contents.push(response.body);

            }

            function errorCallback (){
                console.log('failed');
            }
           self.$http.post('/paper-tracking/api/save_content/', formData, options).then(successCallback, errorCallback);

    },
        updateContent : function (id, name) {
            var self = this;
            csrf = $('[name = "csrfmiddlewaretoken"]').val();
            options = {headers: {'X-CSRFToken':csrf}};
            body = self.content_data;
            body = self.content_data;

            var formData = new FormData();
            formData.append('id',self.content_data.id);
            formData.append('media',self.content_data.media.id);
            formData.append('page',self.content_data.page.id);
            formData.append('ad',self.content_data.ad.id);
            formData.append('type',self.content_data.type);
            if(self.content_data.type == '1'){
                formData.append('sentimental',self.content_data.sentimental);
            }
            formData.append('cc',self.content_data.cc);
            for (var i = 0; i < self.attachments.length; i++) {
              formData.append('new_images_'+String(i), self.attachments[i]);
            }


            function successCallback (response){
            self.showForm = false;
            self.content_data = {'type':"0", 'media':"", 'ad':"", 'cc':200,'page':""};
                var i = self.contents.map(item => item.id).indexOf(id)
                self.contents[i] = response.body;
            }

            function errorCallback (){
                console.log('failed');
            }
           self.$http.post('/paper-tracking/api/save_content/', formData, options).then(successCallback, errorCallback);

    },
    save: function () {
    var self = this;
    if(self.content_data.id){
        self.updateContent();
    }else{
        this.saveContent();

    }

    },


	},
    created() {
    var self = this;
    self.getContents();
    bus.$on('adsChanged', function (ads) {
    self.ad_list = ads;
    })
    bus.$on('mediasChanged', function (ads) {
    self.media_list = ads;
    })

  },



})