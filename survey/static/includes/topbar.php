 <header id="header" class="app-header navbar" role="menu">
            <!-- navbar header -->
            <div class="navbar-header bg-dark">
                <button class="pull-right visible-xs dk" ui-toggle="show" target=".navbar-collapse">
                    <i class="glyphicon glyphicon-cog"></i>
                </button>
                <button class="pull-right visible-xs" ui-toggle="off-screen" target=".app-aside" ui-scroll="app">
                    <i class="glyphicon glyphicon-align-justify"></i>
                </button>
                <!-- brand -->
                <a href="#/" class="navbar-brand text-lt">
                    <!-- <img src="img/logo.png" alt=""  class="hide"> -->
                    <img src="img/logo - Copy.png" alt=".">
                    <span class="hidden-folded m-l-xs">Media Monitoring</span>
                </a>
                <!-- / brand -->
            </div>
            <!-- / navbar header -->
            <!-- navbar collapse -->
            <div class="collapse pos-rlt navbar-collapse box-shadow bg-white-only">
                <!-- buttons -->
                <div class="nav navbar-nav hidden-xs">
                    <a href="#" class="btn no-shadow navbar-btn" ui-toggle="app-aside-folded" target=".app">
                        <i class="fa fa-dedent fa-fw text"></i>
                        <i class="fa fa-indent fa-fw text-active"></i>
                    </a>
                </div>
                <!-- / buttons -->
                <!-- link and dropdown -->
                <!-- / link and dropdown -->
                <!-- search form -->
                <form class="navbar-form navbar-form-sm navbar-left shift" ui-shift="prependTo" data-target=".navbar-collapse" role="search" ng-controller="TypeaheadDemoCtrl">
                    <div class="form-group">
                        <div class="input-group">
                            <input type="text" ng-model="selected" typeahead="state for state in states | filter:$viewValue | limitTo:8" class="form-control input-sm bg-light no-border rounded padder" placeholder="Search Clients, Campaigns">
                            <span class="input-group-btn">
                     <button type="submit" class="btn btn-sm bg-light rounded"><i class="fa fa-search"></i></button>
                     </span>
                        </div>
                    </div>
                </form>
                <!-- / search form -->
                <!-- nabar right -->
                <ul class="nav navbar-nav navbar-right">
                    <li class="dropdown">
                        <a href="#" data-toggle="dropdown" class="dropdown-toggle">
                            <i class="icon-bell fa-fw"></i>
                            <span class="visible-xs-inline">Notifications</span>
                            <span class="badge badge-sm up bg-danger pull-right-xs">2</span>
                        </a>
                        <!-- dropdown -->
                        <div class="dropdown-menu w-xl ">
                            <div class="panel bg-white">
                                <div class="panel-heading b-light bg-light">
                                    <strong>You have <span>2</span> notifications</strong>
                                </div>
                                <div class="list-group">
                                    <a href class="media list-group-item">
                                        <span class="pull-left thumb-sm">
                           <img src="img/a0.jpg" alt="..." class="img-circle">
                           </span>
                                        <span class="media-body block m-b-none">
                           Use awesome animate.css<br>
                           <small class="text-muted">10 minutes ago</small>
                           </span>
                                    </a>
                                    <a href class="media list-group-item">
                                        <span class="media-body block m-b-none">
                           1.0 initial released<br>
                           <small class="text-muted">1 hour ago</small>
                           </span>f
                                    </a>
                                </div>
                                <div class="panel-footer text-sm">
                                    <a href class="pull-right"><i class="fa fa-cog"></i></a>
                                    <a href="#notes" data-toggle="class:show animated fadeInRight">See all the notifications</a>
                                </div>
                            </div>
                        </div>
                        <!-- / dropdown -->
                    </li>
                    <li class="dropdown">
                        <a href="#" data-toggle="dropdown" class="dropdown-toggle clear" data-toggle="dropdown">
                            <span class="thumb-sm avatar pull-right m-t-n-sm m-b-n-sm m-l-sm">
                  <img src="img/a0.jpg" alt="...">
                  <i class="on md b-white bottom"></i>
                  </span>
                            <span class="hidden-sm hidden-md">Spark Tech</span> <b class="caret"></b>
                        </a>
                        <ul class="dropdown-menu  w">
                            <li class="wrapper b-b m-b-sm bg-light m-t-n-xs">
                                <div>
                                    <p>300mb of 500mb used</p>
                                </div>
                                <div class="progress progress-xs m-b-none dker">
                                    <div class="progress-bar progress-bar-info" data-toggle="tooltip" data-original-title="50%" style="width: 50%"></div>
                                </div>
                            </li>
                            <li>
                                <a href>
                                    <span class="badge bg-danger pull-right">30%</span>
                                    <span>Settings</span>
                                </a>
                            </li>
                            <li>
                                <a ui-sref="app.page.profile">Profile</a>
                            </li>
                            <li>
                                <a ui-sref="app.docs">
                                    <span class="label bg-info pull-right">new</span> Help
                                </a>
                            </li>
                            <li class="divider"></li>
                            <li>
                                <a href="login.php">Logout</a>
                            </li>
                        </ul>
                        <!-- dropdown -->
                        <!-- / dropdown -->
                    </li>
                </ul>
                <!-- / navbar right -->
            </div>
            <!-- / navbar collapse -->
        </header>