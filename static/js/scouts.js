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

function login(){

	email = $("#login_email").val()
	pass = $("#login_password").val()
	$.post("/login/",{email: email, password: pass},function(data){
		alert(JSON.stringify(data))
	})
	
}

function logout(){
	$.post('/logout/',function(data){
		alert(JSON.stringify(data))
		window.location = window.location
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