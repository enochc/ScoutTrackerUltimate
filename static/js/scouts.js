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

function doSuccess(data, success_func, fail_func){
	if(data.success){
		success_func()
	}else{
		alert(data.message)
		if(typeof(fail_func) == "function"){
			fail_func()
		}
			
	}
}

function refresh(){window.location=window.location}

function login(){

	email = $("#login_email").val()
	pass = $("#login_password").val()
	$.post("/login/",{email: email, password: pass},function(data){
		doSuccess(data, refresh)
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