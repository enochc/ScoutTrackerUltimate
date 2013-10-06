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
		success_func(data)
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

function login(e){
	username = $("#login_username").val().trim()
	pass = $("#login_password").val().trim()
	//unit = $("#login_unit").val().trim()
	//if(unit.length <1)unit = "100000"
	//username = username+"_"+unit
	$.post("/login/",{login: username, password: pass},function(data){
		doSuccess(data, function(){window.location = '/user'})
	})
}

function logout(){
	$.post('/logout/',function(data){
		doSuccess(data, refresh)
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
	
	$("#login_password").enter(login)
	$("#add_scout_btn").click(function(){
		window.open('/user/add_scout/', 'add_scout', 'width=400, height=400')
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
    
})

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
