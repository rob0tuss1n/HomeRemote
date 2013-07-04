<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
	
	<meta http-equiv="Content-Type" content="text/html;charset=utf-8" /> 
	<title>HomeRemote</title>
	
	<style type="text/css">
		@import url("css/style.css");
		@import url('css/style_text.css');
		@import url("css/login.css");
		@import url("css/link-buttons.css");
		@import url("css/fullcalendar.css");
		@import url("css/forms.css");
		@import url("css/form-buttons.css");
		@import url("css/accordion.css");
		@import url("css/modalwindow.css");
		@import url("css/system-messages.css");
		@import url("css/datatable.css");
		@import url("css/statics.css");
		@import url("css/tabs.css");
		@import url("css/alerts.css");
		@import url("css/tooltip.css");
		@import url("css/notifications.css");
		@import url("css/prettify.css");
		@import url("css/elfinder.css");
		@import url("css/pirebox.css");
		@import url("css/colorpicker.css");
		@import url("css/wizard.css");
		@import url("css/wysiwyg.css");
		@import url("css/wysiwyg.modal.css");
		@import url("css/wysiwyg-editor.css");
	</style>
	
	<!--[if lte IE 8]>
		<script type="text/javascript" src="js/excanvas.min.js"></script>
	<![endif]-->
	
	<script type="text/javascript" src="js/jquery-1.7.1.min.js"></script>
	<script type="text/javascript" src="js/jquery-ui.js"></script>
	<script type="text/javascript" src="js/jquery-ui-select.js"></script>
	<script type="text/javascript" src="js/jquery-ui-spinner.js"></script>
	<script type="text/javascript" src="js/jquery.customInput.js"></script>
	<script type="text/javascript" src="js/jquery.dataTables.js"></script>
	<script type="text/javascript" src="js/jquery.smartwizard-2.0.min.js"></script>
	<script type="text/javascript" src="js/jquery.alerts.js"></script>
	<script type="text/javascript" src="js/jquery.flot.js"></script>
	<script type="text/javascript" src="js/jquery.graphtable-0.2.js"></script>
	<script type="text/javascript" src="js/jquery.flot.pie.min.js"></script>
	<script type="text/javascript" src="js/jquery.flot.resize.min.js"></script>
	<script type="text/javascript" src="js/jquery.filestyle.mini.js"></script>
	<script type="text/javascript" src="js/prettify.js"></script>
	<script type="text/javascript" src="js/elfinder.min.js"></script>
	<script type="text/javascript" src="js/jquery.jgrowl.js"></script>
	<script type="text/javascript" src="js/colorpicker.js"></script>
	<script type="text/javascript" src="js/jquery.tipsy.js"></script>
	<script type="text/javascript" src="js/fullcalendar.min.js"></script>
	<script type="text/javascript" src="js/pirobox.extended.min.js"></script>
	<script type="text/javascript" src="js/jquery.validate.min.js"></script>
	<script type="text/javascript" src="js/jquery.metadata.js"></script>
	<script type="text/javascript" src="js/jquery.wysiwyg.js"></script>
	<script type="text/javascript" src="js/controls/wysiwyg.image.js"></script>
	<script type="text/javascript" src="js/controls/wysiwyg.link.js"></script>
	<script type="text/javascript" src="js/controls/wysiwyg.table.js"></script>
	<script type="text/javascript" src="js/plugins/wysiwyg.rmFormat.js"></script>
    <script type="text/javascript" src="js/jquery.cookie.js"></script>
	<script type="text/javascript" src="js/costum.js"></script>	
	
</head>

<body onload="prettyPrint()">

<div id="wrapper" class="login">		
	<div id="right">
		<div id="main">
	
			<div class="section">
				<div class="box">
					<div class="title">
						<h2>Welcome to RemoteHome</h2>
						<div class="hide"></div>
					</div>
					<div class="content nopadding">
					
						<div class="tabs">
							<div class="tabmenu">
								<ul> 
									<li><a href="#tabs-1">Login</a></li> 
									<li><a href="#tabs-2">Password forgotten?</a></li> 
								</ul>
							</div>
							
							<div class="tab nopadding" id="tabs-1">
                                <?php
                                if(isset($_GET['badlogin'])) {
                                    echo '<div class="content"><div class="system error">Bad username/password combination</div></div>';
                                }
                                ?>
								<form action="login.php" method="get">
									<div class="row">
										<label for="username">Username</label>
										<div class="rowright"><input id="username" name="username" type="text" value="" /></div>
									</div>
									<div class="row">
										<label for="password">Password</label>
										<div class="rowright"><input id="password" name="password" type="password" value="" /></div>
									</div>
									<div class="row">
										<div class="rowright button">
											<button type="submit" class="medium grey"><span>Login</span></button>
										</div>
									</div>
								</form>
							</div>
							
							<div class="tab nopadding" id="tabs-2">
								<form action="">
									<div class="row">
										<label>Username *</label>
										<div class="rowright"><input type="text" value="" /></div>
									</div>
									<div class="row">
										<label>Email Address *</label>
										<div class="rowright"><input type="text" value="" /></div>
									</div>
									<div class="row">
										<label>
											* Required field
										</label>
										<div class="rowright button">
											<button type="submit" class="medium grey"><span>Sumbit</span></button>
										</div>
									</div>
								</form>
							</div>
						</div>
						
					</div>
				</div>
			</div>
			
		</div>
	</div>
</div>

</body>

</html> 