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

function request_troop(){
	var form = $("#troop_form");
	var values = $("#troop_form").getForm();
	$.post('/troop/new/',values, function(data){
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
	//troop = $("#login_troop").val().trim()
	//if(troop.length <1)troop = "100000"
	//username = username+"_"+troop
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

})

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
