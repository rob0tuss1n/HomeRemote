$(document).ready(function(){ 
	
	// HIDE BOXES
	$('.title .hide').click( function() {
		$(this).parent().next('.content').slideToggle(400);
	});

    // SELECTBOXES
    $(function() {
        $('.dataTables_length input, select').not("select.multiple").selectBox();
    });

	// FORM VALIDATION
	$("form.valid").validate({

		meta: "validate",
		errorPlacement: function(error, element) {
          error.insertAfter(element);
		}
	});
	
	// INPUTFIELD - DISPLAY INLINE TEXT
	$('[placeholder]').focus(function() {
		var input = $(this);
			if (input.val() == input.attr('placeholder')) {
				input.val('');
				input.removeClass('placeholder');
			}
		}).blur(function() {
			var input = $(this);
			if (input.val() == '' || input.val() == input.attr('placeholder')) {
			input.addClass('placeholder');
			input.val(input.attr('placeholder'));
		}
	}).blur();
	
	// FILE INPUT STYLE
    $("input[type=file]").filestyle({
        imageheight: 31,
        imagewidth: 76,
        width: 150
    });
	
	// TOOLTIPS
	$(".tip-n").tipsy({gravity: 'n'});
	$(".tip-w").tipsy({gravity: 'w'});
	$(".tip-e").tipsy({gravity: 'e'});
	$(".tip-s").tipsy({gravity: 's'});
	
	// FILE BROWSER
	$('.filebrowser').elfinder({
		url : 'connector.php',
		toolbar : [
					['back', 'reload'],
					['select', 'open'],
					['quicklook', 'info', 'rename'],

					['resize', 'icons', 'list', 'help']
				],
		docked : false
	});
	
	// SPINNERS
	$(".spin").spinner({ 
		places: 2
	});
	
	$(".spin-dec").spinner({ 
		places: 2,
		step: 0.25
	});
	
	$(".spin-cur").spinner({ 
		places: 2,
		step: 0.01,
		prefix: '$ '
	});
	
	// RADIOBUTTONS & CHECKBOXES
	$("input[type=radio], input[type=checkbox]").each(function() {
        if ($(this).parents("table").length === 0) {
            $(this).customInput();
        }
    });

	// TABS
	$(".tabs").tabs({});
	
	// MODAL WINDOW
	$(function() {
        $(".modal").dialog({
            autoOpen: false,
            closeText: '',
            resizable: false,
			modal: true,
			show: "fade",
			hide: "fade",
            width: 700,
			height: 410
        });

        $('.modalopen').click(function() {
            $(".modal").dialog('open');
            return false;
        });
    });
	
	$(window).resize(function() {
		$(".modal").dialog("option", "position", "center");
	});
	
	// ACCORDION
	$(".accordion").accordion({
        autoHeight: false,
        navigation: true
    });
	
	// WIZARD    
    $('.wizard').smartWizard({
        transitionEffect: 'fade'
    });
	
	// DATEPICKER
	$(".datepicker").datepicker({
		dateFormat: 'mm.dd.yy'
	});
	
	// COLORPICKER
	$('.color').ColorPicker({
		color: '#0000ff',
		onShow: function(colpkr) {
			$(colpkr).fadeIn(500);
			return false;
		},
		onHide: function(colpkr) {
			$(colpkr).fadeOut(500);
			return false;
		},
		onChange: function(hsb, hex, rgb) {
			$('.color div span').css('backgroundColor', '#' + hex);
			$('.color input').val('#' + hex);
		}
	});        
	
	// PROGRESSBAR
	$(".progressbar-normal").each(function() {
		$(this).progressbar({
			value: parseInt($(this).attr("value"))
		});
	});
	
	jQuery.ease = function(start, end, duration, easing, callback) {
		var easer = $("<div>");
		var stepIndex = 0;
		var estimatedSteps = Math.ceil(duration / 13);

		easer.css("easingIndex", start);
		easer.animate({
			easingIndex: end
		}, {
			easing: easing,
			duration: duration,
			step: function(index) {
				callback(
				index, stepIndex++, estimatedSteps, start, end);
			}
		});
	};
	
	$(".progressbar-count").each(function() {
		var $self = $(this),targetVal = parseInt($self.attr("value"));
		$self.progressbar({
			value: 0
		});
		$self.prev(".percent").text("0%");
		$.ease(0,targetVal,3500,"swing",function(i){
			$self.progressbar("option","value",parseInt(i));
			$self.prev(".percent").text(parseInt(i) + "%");
		});
	});
	
	// CALENDAR
	var date = new Date();
	var d = date.getDate();
	var m = date.getMonth();
	var y = date.getFullYear();
	
	$('#calendar').fullCalendar({
		header: {
			left: 'prev,next',
			center: 'title',
			right: 'month,basicWeek,basicDay'
		},
		editable: true,
		events: [
			{
				title: 'All Day Event',
				start: new Date(y, m, 1)
			},
			{
				title: 'Long Event',
				start: new Date(y, m, d-5),
				end: new Date(y, m, d-2)
			},
			{
				id: 999,
				title: 'Repeating',
				start: new Date(y, m, 7, 16, 0),
				allDay: false
			},
			{
				id: 999,
				title: 'Repeating',
				start: new Date(y, m, d+4, 16, 0),
				allDay: false
			},
			{
				title: 'Meeting',
				start: new Date(y, m, d, 10, 30),
				allDay: false
			},
			{
				title: 'Lunch',
				start: new Date(y, m, d, 12, 0),
				end: new Date(y, m, d, 14, 0),
				allDay: false
			},
			{
				title: 'Birthday Party',
				start: new Date(y, m, d+1, 19, 0),
				end: new Date(y, m, d+1, 22, 30),
				allDay: false
			},
			{
				title: 'Click for ThemeForest',
				start: new Date(y, m, 28),
				end: new Date(y, m, 29),
				url: 'http://www.themeforest.net'
			}
		]
	});
	
	// ALERTS
	$(".alert").click( function() {
		jAlert('This is a custom alert box', 'Alert Dialog');
	});
	
	$(".confirm").click( function() {
		jConfirm('Can you confirm this?', 'Confirmation Dialog', function(r) {
			jAlert('Confirmed: ' + r, 'Confirmation Results');
		});
	});
	
	$(".prompt").click( function() {
		jPrompt('Type something:', 'Prefilled value', 'Prompt Dialog', function(r) {
			if( r ) alert('You entered ' + r);
		});
	});
	
	$(".htmlbox").click( function() {
		jAlert('You can use HTML, such as <strong>bold</strong>, <em>italics</em>, and <u>underline</u>!');
	});
	
	// SLIDERS
	$(".single-slide div.slide").each(function() {
        value = $(this).attr('value').split(',');
        firstVal = value;

        rangeSpan = $(this).siblings('input.amount');

        $(this).slider({
            value: [firstVal],
            min: parseInt($(this).attr('min'), 0),
            max: parseInt($(this).attr('max'), 0),
            slide: function(event, ui) {
                $(this).siblings('input.amount').val("" + ui.value);
            }
        });
        rangeSpan.val("" + $(this).slider("value"));
    });
	
    $(".range-slide div.slide").each(function() {
        values = $(this).attr('value').split(',');
        firstVal = values[0];
        secondVal = values[1];

        rangeInputfirst = $(this).siblings('input.amount-first');
        rangeInputsecond = $(this).siblings('input.amount-second');

        $(this).slider({
            values: [firstVal, secondVal],
            min: parseInt($(this).attr('min'), 0),
            max: parseInt($(this).attr('max'), 0),
            range: true,
            slide: function(event, ui) {
                $(this).siblings('input.amount-first').val("" + ui.values[0]);
                $(this).siblings('input.amount-second').val("" + ui.values[1]);
            }
        });
        rangeInputfirst.val("" + $(this).slider("values", 0));
        rangeInputsecond.val("" + $(this).slider("values", 1));
    });
	
    $(".snap-slide div.slide").each(function() {
        value = $(this).attr('value').split(',');
        firstVal = value;

        rangeSpan = $(this).siblings('input.amount');

        $(this).slider({
            value: [firstVal],
            min: parseInt($(this).attr('min'), 0),
            max: parseInt($(this).attr('max'), 0),
			step: parseInt($(this).attr('step'), 0),
            slide: function(event, ui) {
                $(this).siblings('input.amount').val("" + ui.value);
            }
        });
        rangeSpan.val("" + $(this).slider("value"));
    });
	
	$(".single-vert-slide div.slide").each(function() {
        value = $(this).attr('value').split(',');
        firstVal = value;

        rangeSpan = $(this).siblings('input.amount');

        $(this).slider({
			orientation: "vertical",
            value: [firstVal],
            min: parseInt($(this).attr('min'), 0),
            max: parseInt($(this).attr('max'), 0),
            slide: function(event, ui) {
                $(this).siblings('input.amount').val("" + ui.value);
            }
        });
        rangeSpan.val("" + $(this).slider("value"));
    });
	
	// DATATABLE
    $('table.all').dataTable({
        "bInfo": false,
        "iDisplayLength": 5,
        "aLengthMenu": [[5, 10, 25, 50, 100], [5, 10, 25, 50, 100]],
        "sPaginationType": "full_numbers",
        "bPaginate": true,
        "aoColumnDefs": [{
            bSortable: false,
            aTargets: [0, -1]}],
        "sDom": '<f>t<pl>'
    });
	
	$('table.pagesort').dataTable({
        "bInfo": false,
        "iDisplayLength": 5,
        "aLengthMenu": [[5, 10, 25, 50, 100], [5, 10, 25, 50, 100]],
        "sPaginationType": "full_numbers",
        "bPaginate": true,
		"bFilter": false,
        "aoColumnDefs": [{
            bSortable: false,
            aTargets: [0, -1]}],
        "sDom": 't<pl>'
    });

    $('table.sortsearch').dataTable({
        "bInfo": false,
        "bPaginate": false,
        "aoColumnDefs": [{
            bSortable: false,
            aTargets: [0, -1]}],
        "sDom": 't<plf>'
    });

    $('table.sorting').dataTable({
        "bInfo": false,
        "bPaginate": false,
        "bFilter": false,
        "aoColumnDefs": [{
            bSortable: false,
            aTargets: [0, -1]}],
        "sDom": 't<plf>'
    });

    $(".dataTables_wrapper .dataTables_length select").addClass("entries");
	
	// CHECK ALL PAGES
    $('.checkall').click(function() {
        $(this).parents('table').find(':checkbox').attr('checked', this.checked);
    });
	
	// BUTTON HOVERS / TABLE ICON
    $("a.button, button, .pager, .dataTables_paginate span.paginate_button, table tbody td img, .btn-upload, .title .hide").hover(function() {
        $(this).stop().fadeTo(200, 0.75);
    }, function() {
        $(this).stop().fadeTo(200, 1.0);
    });
	
	// PIROBOX
	$(".gallery .hover .pirobox").piroBox_ext({
        piro_speed : 700,
        bg_alpha : 0.5,
        piro_scroll : true
    });
	
	// WYSIWYG EDITOR
	$('.wysiwyg').wysiwyg({
        css: "css/wysiwyg-editor.css",
        plugins: {
            rmFormat: {
                rmMsWordMarkup: true
            }
        }
    });
	
	// TABEL CHART        
    $("table.chart").each(function() {
        var colors = [];
        $("table.chart thead th:not(:first)").each(function() {
            colors.push($(this).css("color"));
        });
        $(this).graphTable({
            series: 'columns',
            position: 'replace',
			width: '100%',
            height: '250px',
            colors: colors
        }, {
            xaxis: {
                tickSize: 1
            }
        });
    });

    $("table.chart-date").each(function() {
        var colors = [];
        var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        $("table.chart-date thead th:not(:first)").each(function() {
            colors.push($(this).css("color"));
        });
        $(this).graphTable({
            series: 'columns',
            position: 'replace',
            width: '100%',
            height: '250px',
            colors: colors,
            xaxisTransform: function(month) {
                var i = 0;
                while ((i < 12) && (month != months[i])) {
                    i++;
                }
                return i;
            }
        }, {
            xaxis: {
                tickSize: 1,
                tickFormatter: function(v, a) {
                    return months[v];
                }
            }
        });
    });
	
	$("table.chart-pie").each(function() {
        var colors = [];
        $("table.chart-pie thead th:not(:first)").each(function() {
            colors.push($(this).css("color"));
        });
        $(this).graphTable({
            series: 'columns',
            position: 'replace',
			width : '100%',
            height: '250px',
            colors: colors
        }, {
			series: {
				pie: {
					show: true,
					pieStrokeLineWidth: 0, 
					pieStrokeColor: '#FFF',
					radius: 100,
					label: {
						show: true,
						radius: 3/4,
						formatter: function(label, series){
							return '<div style="font-size:11px; padding:2px; color: #FFFFFF;"><b>'+label+'</b>: '+Math.round(series.percent)+'%</div>';
						},
						background: {
							opacity: 0.5,
							color: '#000'
						}
					}
				}
			},
			legend: {
				show: false
			},
			grid: {
				hoverable: false,
				autoHighlight: false
			}
        });
    });
	
	$("table.chart-square").each(function() {
        var colors = [];
        $("table.chart-square thead th:not(:first)").each(function() {
            colors.push($(this).css("color"));
        });
        $(this).graphTable({
            series: 'columns',
            position: 'replace',
			width : '100%',
            height: '250px',
            colors: colors
        }, {
			series: {
				pie: {
					show: true,
					pieStrokeLineWidth: 0, 
					pieStrokeColor: '#FFF',
					radius: 800,
					label: {
						show: true,
						radius: 3/4,
						formatter: function(label, series){
							return '<div style="font-size:11px; padding:2px; color: #FFFFFF;"><b>'+label+'</b>: '+Math.round(series.percent)+'%</div>';
						},
						background: {
							opacity: 0.5,
							color: '#000'
						}
					}
				}
			},
			legend: {
				show: false
			},
			grid: {
				hoverable: false,
				autoHighlight: false
			}
        });
    });
	
	$("table.chart-bars").each(function() {
        var colors = [];
        $("table.chart-bars thead th:not(:first)").each(function() {
            colors.push($(this).css("color"));
        });
        $(this).graphTable({
            series: 'columns',
            position: 'replace',
			width : '100%',
            height: '250px',
            colors: colors
        }, {
			xaxis: {
                tickSize: 1,
            },
			series: {
				bars: {
					show: true,
					lineWidth: 1,
					barWidth: 0.7,
					fill: true,
					fillColor: null,
					align: "center",
					horizontal: false
				},
				lines: {
					show: false
				},
				points: {
					show: false
				},
			}
        });
    });
	
	$("table.chart-barsmulti").each(function() {
        var colors = [];
        $("table.chart-barsmulti thead th:not(:first)").each(function() {
            colors.push($(this).css("color"));
        });
        $(this).graphTable({
            series: 'columns',
            position: 'replace',
			width : '100%',
            height: '250px',
            colors: colors
        }, {
			xaxis: {
                tickSize: 1,
            },
			series: {
				bars: {
					show: true,
					lineWidth: 1,
					barWidth: 0.4,
					fill: true,
					fillColor: null,
					align: "center",
					horizontal: false,
					multiplebars:true
				},
				lines: {
					show: false
				},
				points: {
					show: false
				},
			}
        });
    });

    $('.flot-graph').before('<div class="space"></div>');

    function showTooltip(x, y, contents) {
        $('<div id="tooltip">' + contents + '</div>').css({
            position: 'absolute',
            display: 'none',
            top: y + 5,
            left: x + 5
        }).appendTo("body").fadeIn("fast");
    }

    var previousPoint = null;
    $(".flot-graph").bind("plothover", function(event, pos, item) {
        $("#x").text(pos.x);
        $("#y").text(pos.y);

        if (item) {
            if (previousPoint != item.dataIndex) {
                previousPoint = item.dataIndex;

                $("#tooltip").remove();
                var x = item.datapoint[0],
                    y = item.datapoint[1];

                showTooltip(item.pageX, item.pageY, "<b>" + item.series.label + "</b>: " + y);
            }
        }
        else {
            $("#tooltip").remove();
            previousPoint = null;
        }
    });
	
});