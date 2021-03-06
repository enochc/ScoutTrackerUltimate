var csrf_token

$(document).ajaxSend(function(event, xhr, settings) {
	try{
		csrf_token = $.cookie('csrftoken')
	    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
	        xhr.setRequestHeader("X-CSRFToken", csrf_token);
	    }
	}catch(e){
		console.error('could not include csrf token : '+settings.url)
	}
});

function request_unit(){
	var form = $("#unit_form");
	var values = $("#unit_form").getForm();
	$.post('/unit/new/',values, function(data){
		data.form = form;
		doSuccess(data, function(){window.location = window.location;});
	})
}

$.blockUI.defaults = $.extend($.blockUI.defaults,{
	message:'',
	css: $.extend($.blockUI.defaults.css,{'backgroundColor':'#EFEACC'}),
	overlayCSS: { 
        backgroundColor: '#0c5994',
        opacity:         0.7,
        cursor:         'wait' 
    }, 
    fadeIn:0,
    fadeOut:0
	
})

function doSuccess(data, success_func, fail_func, dontClear){
	if(data.success){
		if(typeof(success_func) == "function"){
			success_func(data)
		}
	}else{
		message = ''
		if(data.form){
			data.form.find('.error').removeClass('error')
		}
		message = data['message']
		for(d in data){
			
			if(d != 'message' && data[d] != data.form && d != 'success'){
				data.form.find("#id_"+d).addClass('error')
				message +="\n\r"+d+": ";
				for(m in data[d]){
					message+= data[d][m]+" "
				}
			}
		}
		if(message.length > 0){
			alert(message)
		}
		if(typeof(fail_func) == "function"){
			fail_func()	
		}
		if(!dontClear){
			$.unblockUI()
		}
	}
}

function refresh(){window.location=window.location}

function login_user(e){
	$("#loc_login_form").submit()
	/*
	$("#local_login").block();
	
	username = $("#login_username").val().trim()
	pass = $("#login_password").val().trim()

	$.post("/login/",{login: username, password: pass},function(data){
		doSuccess(data, function(){window.location = '/user'}, function(){$("#local_login").unblock()})
	})
	*/
}

function logout(){
	$.post('/logout/',function(data){
		doSuccess(data, function(){
			
			/*try{
				FB.logout()
			}catch(e){}*/
			refresh()
		})
	})
}

if($){
	$.fn.enter = function(func){
		this.each(function(){
			$(this).keypress(function(e){
				if(e.which == 13){
					e.preventDefault()
					func(this);
				}
			})	
		});
		return this;
	}
}
var autocomplete_lists = {}
// On load bindings
$(function(){
	$("form.block").on("submit", function(){
		$(this).block()
	})
	$("#login_password").enter(login_user)
	$("#add_scout_btn,.add_scout").click(function(){
		var url = '/user/add_scout/'
		var patrol = $(this).attr("data-patrol")
		if(!und(patrol) && patrol.length >0){
			url+="?patrol="+patrol
		}
		window.open(url, 'add_scout', 'width=400, height=400')
	})
	
	$("#outer").click(function(e){
		close_popup()
	})
	$('.popup').click(function(e){
    	e.stopPropagation()
    })
    $("#ui-datepicker-div").on('click',function(e){
    	e.stopPropagation()
    	return false
    })
    
    $(".autocomplete").autocomplete({
    	delay:0,
    	minLength:0,
    	source:function( request, response ) {
    		var t = $(this.element)
    		var noCache = t.hasClass("nocache")
    		var url = t.attr("data-url")
    		if(!noCache){
    			var list = autocomplete_lists[url]
    			if(!und(list)){
    				response(filterList(list, request.term));
    				return true
    			}
    		}
    		$.getJSON(url, function(data){
    			autocomplete_lists[url]=data.list
    			response(filterList(data.list, request.term))
    		})
            
          }		
    })
    $(".draggable").draggable({ 
    	revert: "invalid",
    	revertDuration: "200"
    });
	$(".droppable").droppable({
		hoverClass: "drop_hover",
		activeClass: "drop_active",
		drop:function(event, ui){
			var drop = $(event.target)
			drop.block()
			var data = {"scout":ui.draggable.attr("data-scout"),
				"patrol":$(this).attr("data-patrol")
			}
			$.post("/unit/add/", data, function(data){
				if(data.success){
					drop.find(".scoutList").append(ui.draggable.css({"top":"","left":""}))
					drop.unblock()
				}else{
					alert(data.message)
					ui.draggable.css({"top":"","left":""})
					drop.unblock()
				}
				
			})
	
		}
	});
	
	$(".request span.close_x").on("click", function(){
		var req = $(this)
		$.post("/unit/invite/cancel/"+req.attr("data-req")+"/", function(ret_data){
			if(ret_data.success){
				req.parents("li")[0].remove()
			}
		})
	})
	$("#unit_requests span.approve_req").on("click", function(){
		var req = $(this)
		var pane = req.parents(".pane").eq(0)
		pane.block()
		$.post("/unit/invite/approve/"+req.attr("data-req")+"/", function(ret_data){
			if(ret_data.success){
				window.location = window.location
			}else{
				alert(data.message)
				pane.unblock()
			}
		})
	})
	$(".del_patrol").on("click", function(){
		var p = $(this)
		var pane = p.parents(".pane").eq(0)
		pane.block()
		if(confirm("Any scouts in this patroll will need to be reassigned! No records will be lost")){
			p.parents(".pane").block()
			$.post("/unit/del_patrol/"+p.attr("data-id")+"/", function(ret_data){
				if(ret_data.success){
					window.location = window.location
				}else{
					pane.unblock()
				}
			})
		}else{
			pane.unblock()
		}
		
	})
	$(".del_leader").on("click", function(){
		var p = $(this)
		if(confirm("Remove leader from Unit?")){
			$.post("/unit/del_leader/"+p.attr("data-id")+"/", function(ret_data){
				if(ret_data.success){
					window.location = window.location
				}else{
					pane.unblock()
				}
			})
		}else{
			pane.unblock()
		}
		
	})
	$("#send_invite").on("click", function(){
		var email = $("#inv_email").val()
		send_invite(email, $(this))
	})
})


function send_invite(email, obj){
	var pane = obj.parents(".pane").eq(0)
	pane.block({"message":"Sending invitation"})
	$.post("/unit/invite/", {"email":email}, function(data){
		if(data.success){
			alert("Inivatation Sent")
			window.location=window.location
		}else{
			alert(data.message)
		}
		pane.unblock()
	})
}

function filterList(list, val){
	return $.map(list, function(v, i){
		if(v.toLowerCase().indexOf(val.toLowerCase()) >=0){return v}
	})
}

function close_popup(){
	$('.popup').hide()
}

function set_scout_requiremnt(r, s, b, options){
	var api = '/requirement/set/'+r+'/'+s+'/'
	var notes = $('#req_notes').val()
	var comp = $('#req_completed').is(':checked')
	var date = $('input.date').val()
	$.post(api,{notes:notes, completed:comp, date:date},function(data){
        doSuccess(data, function(){
        	if(!data.completed){
        		   b.html("<span class='empty red'>&mdash;</span>")
        	}else{
        		   b.html("<img src='/images/check.png'/>")
        	}
        	if(options && typeof options.postfunc == 'function'){
        		data.req_id=r
        		options.postfunc(data)
        	}
        	close_popup()
        })
    })
}

function updateLeaderPosition(event){
	var sel = $(event.target)
	var pos = sel.val()
	var leader = sel.attr("data-lid")
	var url = "/user/set_pos/"+leader+"/"+pos+"/"
	var pane = sel.parents(".pane").eq(0)
	pane.block({"message":"Updating Leader Position"})
	$.post(url, function(data){
		doSuccess(data, function(){pane.unblock()})
	})
}

function add_badge(event){
	var btn = $(event.target)
	var scout = btn.attr("data-scout")
	var badge = $("#meritbadges").val()
	if(badge.length>0){
		$("#badge_cont").block()
		$.post("/user/add_award/",{'scout':scout,'award':badge}, function(){
			window.location = window.location
		})
	}
	
	/*$.post(url, function(data){
		doSuccess(data, function(){pane.unblock()})
	})*/
}

function addCalendar(event){
	$.blockUI()
	var cal_id = $("#calendar_id").val()
	$.post("/unit/update_calendar/",{"calendar_id":cal_id}, function(){
		window.location = window.location
	})
}


function openRecForm(box, opt){
	
	var req = box.attr('class').split('r_')[1].split(' ')[0]

	if(opt && typeof opt.prefunc == 'function'){
		opt.prefunc(req)
	}
    var scout = box.attr('class').split('s_')[1].split(' ')[0]
    var top = box.offset().top
    var form = $('#set_req_form').load('/requirement/set/'+req+'/'+scout+'/',function(data){        
        $('#set_req_form').css({
            'top':top,
            'left':box.offset().left
        }).find('.cancel').click(function(){
        	close_popup()
        }).end().find('.send').click(function(){
            set_scout_requiremnt(req, scout, box, opt)
        }).end().find("input.date").datepicker({
            changeYear:true,
            changeMonth:true,
            yearRange:'-100:+0',
            dateFormat:'M dd, yy'
        })

        form.show()
        
        bottom = form.offset().top + form.height()
        screen_bottom = document.body.scrollTop + $(document.body).height()
        offset = (screen_bottom - bottom) -25
        if(offset < 0){
        	form.offset({"top":top +offset})
        }
        	
        
    })

}
