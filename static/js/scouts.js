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
$.blockUI.defaults = $.extend($.blockUI.defaults,{
	message:'',
	overlayCSS:  { 
        backgroundColor: '#0c5994',
        opacity:         0.7,
        cursor:         'wait' 
    }, 
    fadeIn:0,
    fadeOut:0
	
})
function doSuccess(data, success_func, fail_func){
	if(data.success){
		success_func(data)
	}else{
		message = ''
		data.form.find('.error').removeClass('error')
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
		$.unblockUI()
			
	}
}

function refresh(){window.location=window.location}

function login(e){
	username = $("#login_username").val().trim()
	pass = $("#login_password").val().trim()
	troop = $("#login_troop").val().trim()
	username = username+"_"+troop
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
})
