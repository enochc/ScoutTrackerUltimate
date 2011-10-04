var _emailPattern = new RegExp(/^([a-zA-Z0-9_.-])+@([a-zA-Z0-9_.-])+\.([a-zA-Z])+([a-zA-Z])+/);

String.prototype.trim = function (){
	return this.replace(/^\s+|\s+$/g,"");
}
String.prototype.truncate = function(len, truncation) {
    len = len || 30;
    truncation = truncation || '...';
    return this.length > len ?
      this.slice(0, len - truncation.length) + truncation : String(this);
}

function inArray(arr,x){
	for(i in arr){
		if(x == arr[i]){
			return true;
		}
	}
	return false;	
}
function getBody(){
	return document.getElementsByTagName("body")[0];
}
function injectElement(e){
	var b = getBody()
	getBody().appendChild(e)
}
_UniqueValue = new function(){
	var self = this;
	this.val = 0;
	this.getVal = function(){
		self.val++
		if(self.val > 10000000){self.val = 0;}
		return self.val;
	}
}
String.prototype.fixMSSql = function(){
	return this.replace(/'/g,"''")
}
Number.prototype.round = function(dec) {
	return Math.round(this*Math.pow(10,dec))/Math.pow(10,dec);
}

function newOpt(val,text,boolsel,id){
	var opt = new Option(text,val,boolsel);
	if(id){opt.id=id;}
	return opt
}
function setOpacity(testObj,value) {
	testObj.style.opacity = value/100;
	testObj.style.filter = 'alpha(opacity=' + value + ')';
}

function setManyAttributes(node,attstring){
	var st = attstring.split(" ");
	for(var ss in st){
		var t = st[ss].split("=")
		var att = t[0];
		var val = t[1]?t[1].replace(/\"/g,"").replace(/\'/g,""):" ";
		node.setAttribute(att,val);
	}	
}
function drawPoint(px,py){
	var page = document.getElementsByTagName("body")[0];
	this.ndiv = function(x,y){
		//alert(x+" "+y)
		var d = document.createElement("Div");
		d.style.width = "1px";
		d.style.height = "1px";
		d.style.position = "absolute";
		d.style.top = y+"px";
		d.style.left = x+"px";
		d.style.backgroundColor = "#ff0000";
		d.style.lineHeight = "1px";
		d.style.fontSize = "1px";
		d.style.zIndex = "1000";
		page.appendChild(d);
	}
	for(var y = (py - 3);y<=(py+3);y++){
		this.ndiv(px,y);
	}
	for(var x = (px - 3);x<=(px+3);x++){
		this.ndiv(x,py);
	}	
}
function arrayJoin(a,b){
	for(var x=0;x<b.length;x++){
		a.push(b[x]);
	}
	return a
}


function und( val ) {
	return typeof(val) == 'undefined' || val == null;
}

function myevent(evt){
	this.e = evt || window.event;
	var self = this;
	this.type = this.e.type;
	this.target = (this.e.target) ? this.e.target : this.e.srcElement
	this.shiftKey = this.e.shiftKey;
    this.ctrlKey = this.e.ctrlKey;
    this.altKey = this.e.altKey;
	this.keyCode = this.e.keyCode || this.e.which || 0;
	this.enterKey = this.keyCode == 13 ? true : false;
	this.delKey = this.keyCode == 46 ? true : false;
	if(!this.shiftKey && this.keyCode > 64 && this.keyCode < 91){
		this.strKey=String.fromCharCode(this.keyCode + 32);		
	}else{
		this.strKey=String.fromCharCode(this.keyCode);
	} 
	this.cancelBubble = function(){
		self.e.cancelBubble = true;
			if (self.e.stopPropagation) {
				self.e.stopPropagation();
				self.e.preventDefault();
			}
	}
	
	
}


function getxmldocument(text){
	var returnval = true;
	this.checkForParseError = function(text) {
	    var errorNamespace ="http://www.mozilla.org/newlayout/xml/parsererror.xml";
	    var documentElement = text.documentElement;
	    var parseError = { errorCode : 0 };
	    if (documentElement.nodeName == 'parsererror' &&
	        documentElement.namespaceURI == errorNamespace) {
			parseError.errorCode = 1;
	     	var sourceText = documentElement.getElementsByTagNameNS(errorNamespace, 'sourcetext')[0];
	      	if (sourceText != null) {
	        	parseError.srcText = sourceText.firstChild.data
	      	}
	      	parseError.reason = documentElement.firstChild.data;
	    }
	    return parseError;
	}
	if (window.ActiveXObject){
		var doc=new ActiveXObject("Microsoft.XMLDOM");
		doc.async="false";
	  	doc.loadXML(text);
	  	if (doc.parseError.errorCode != '0'){
	  		message = doc.parseError.reason + "\n" + doc.parseError.srcText;
	  		alert(message);
			return false;		
		}else{
			//xmldocument = doc;
			return doc
			doc = null;
		}
	}
// code for Mozilla, Firefox, Opera, etc.
	else{
  		var parser=new DOMParser();
 		var doc=parser.parseFromString(text,"text/xml");
 		parseError = this.checkForParseError(doc);
  		if (parseError.errorCode == 0) {
			//xmldocument = doc;
			return doc;
			doc = null;
  		}else {
    		alert(parseError.reason + '\r\n' + parseError.srcText);
    		return false;
  		}
  	}	
	//return returnval;
}
function serializeNode(indoc){	  		
	  var text = "";
	  try {
	    var serializer = new XMLSerializer();
	    text = serializer.serializeToString(indoc);		
	  }
	  catch (e) {
	    try {
	      text = indoc.xml;
	    }
	    catch (e) {}
	  }
	  return text;			
}

function serializeXMLNode(xmlNode) {
  var text = false;
  try {
    // Gecko-based browsers, Safari, Opera.
    var serializer = new XMLSerializer();
    text = serializer.serializeToString(xmlNode);

  }
  catch (e) {
    try {
      // Internet Explorer.
      text = xmlNode.xml;
    }
    catch (e) {}
  }
  return text;
}

function jsTimer(){
	this.time = new Array();
	this.starttime = null;
	this.stoptime = null;
	this.diff = null;
	
	var jt = this;
	this.clear = function(){
		jt.time = new Array;
	}
	this.start = function(){
		jt.starttime = new Date();
	}
	this.stop = function(){
		jt.stoptime = new Date();
		jt.time.push (jt.stoptime - jt.starttime)
	}
	this.lap = function(){
		jt.stoptime = new Date();
		jt.time.push (jt.stoptime - jt.starttime)
		jt.starttime = new Date();		
	}
	this.getTime = function(lap){
		if(!lap){lap = jt.time.length;}
		return jt.time[lap - 1];
	}
	this.clear = function(){jt.time = new Array();}
}

	
function getInputs(pNode){
	var GI = this;
	this.values = new Array();	
	this.values.getValue = function(strname){
		var ret = null;
		for(var x=0;x<GI.values.length;x++){
			if(GI.values[x].name == strname){
				ret =  GI.values[x].value
				break;
			}
		}
		return ret;
	}
	this.values.get = function(strname){
		var ret = null;
		for(var x=0;x<GI.values.length;x++){
			if(GI.values[x].name == strname){
				ret =  GI.values[x];
				break;
			}
		}
		return ret;
	}
	this.values.jsonString = function(){
		var js ="{";
		for(var x=0;x<GI.values.length;x++){
			if(GI.values[x].name == 'test'){
				alert(" test tostring: "+GI.values[x].value);
			}
			js +="\""+GI.values[x].name+"\":\""+escapeJsonString(GI.values[x].value)+"\","
		}
		return js.substring(0,js.length - 1)+"}";
	}
	this.values.add = function(obj){
		if(typeof(obj) == "object"){
			for(var p in obj){
				GI.values.push(new nvpair(p,obj[p],null));
			}
		}
	}
	this.values.json = function(){
		var j = new function(){};
		for(var x=0;x<GI.values.length;x++){
			j[GI.values[x].name]= escapeJsonString(GI.values[x].value);
		}
		return j;
	}
	this.values.getParamString = function(){
		var s = "";
		for(var x=0;x<GI.values.length;x++){
			s+= GI.values[x].name+"="+encodeURIComponent(GI.values[x].value)+"&";
		}
		s = s.substring(0,s.length - 1);
		return s;
	}
	this.nvpair = function(inname,value,node){
		this.name = inname;
		this.value = value;
		this.node = node;
	}
	this.values.hasName = function(inname){
		var ret = false;
		for(var x=0;x<GI.values.length;x++){
			if(GI.values[x].name == inname){
				ret =  true
				break;
			}
		}
		return ret;
	}
	var i = pNode.getElementsByTagName("input");
	var n = null;
	for(var x=0; x<i.length;x++){
		var tmp = i[x].name;
		if(tmp == ""){
			tmp = i[x].id;
		}
		if(i[x].type != "button" && !this.values.hasName(i[x].name)){
			
			this.values.push(new this.nvpair(tmp,getVal(i[x]),i[x]))
		}
		n = i[x].name;
	}
	var i = pNode.getElementsByTagName("textarea");
	for(var x=0; x<i.length;x++){
		var tmp = i[x].name;
		if(tmp == ""){
			tmp = i[x].id;
		}		
		this.values.push(new this.nvpair(tmp,i[x].value.trim(),i[x]))		
	}
	var i = pNode.getElementsByTagName("select");
	for(var x=0; x<i.length;x++){
		var tmp = i[x].name;
		if(tmp == ""){
			tmp = i[x].id;
		}		
		this.values.push(new this.nvpair(tmp,getVal(i[x]),i[x]))
	}
	return this.values;
}

function getVal(input){	
	if(input.type.toLowerCase() == "radio"){
		var myname = input.name;
		var allbtns = document.getElementsByName(myname);
		var value = "";
		for(var x=0;x<allbtns.length;x++){
			if(allbtns[x].checked){
				value =  allbtns[x].value;
			}
		}
		return value;
	}else if(input.type.toLowerCase() == "text" || 
				input.type.toLowerCase() == "hidden" || 
				input.type.toLowerCase() == "password" ||
				input.type.toLowerCase() == "email"){
		return input.value.trim();
	}else if(input.type.toLowerCase() == "select-one"){
		return input.options[input.selectedIndex].value;
	}else if(input.type.toLowerCase() == "select-multiple"){
		var rv = "";
		for(var x=0;x<input.options.length;x++){
			if(input.options[x].selected){
				rv += input.options[x].value+",";
			}
		}
		return rv.substring(0,rv.length - 1);
	}else if(input.type.toLowerCase() == "checkbox"){
		return input.checked;
	}
}

function getTop(inputObj){
  var returnValue = inputObj.offsetTop
  while(!und(inputObj.offsetParent)){
  	inputObj = inputObj.offsetParent
  	//alert(inputObj.id+" "+inputObj.scrollTop);
  	returnValue += (inputObj.offsetTop - inputObj.scrollTop);
  }
  return returnValue;
}


function getLeft(inputObj){
  var returnValue = inputObj.offsetLeft;
  while((inputObj = inputObj.offsetParent) != null)returnValue += inputObj.offsetLeft;
  return returnValue;
}	

function escapeJsonString(value) {
	if(typeof(value) == "string" && !und(value)){
		value = value.replace(/\"/g,"\\\"");
		return value;
	}else if(typeof(value) == "boolean"){
		return value;
	}else if(typeof(value) == "number"){
		return value;		
	}else if(typeof(value) == "array"){
		return value;		
	}else{
		return null;
	}
} 

_json = ({
	serialize : function(o) {var i,v,s=_json.serialize,t;if(o==null)
	return 'null';t=typeof o;if(t=='string'){v='\bb\tt\nn\ff\rr\""\'\'\\\\';
	return '"'+o.replace(/([\u0080-\uFFFF\x00-\x1f\"\'])/g,function(a,b){i=v.indexOf(b);if(i+1)
	return '\\' + v.charAt(i + 1);a = b.charCodeAt().toString(16);return '\\u'+'0000'.substring(a.length)+a;
	})+'"';}if(t=='object'){if(o instanceof Array){
	for (i=0,v='['; i<o.length;i++)v+=(i>0?',':'')+s(o[i]);return v+']';}v='{';
	for (i in o)v+=typeof o[i]!='function'?(v.length>1?',"':'"')+i+'":'+s(o[i]):'';return v+'}';}return ''+o;}
,add : function(obj1,obj2){
		var newObject = new function(){};
		for(var o in obj1){
			newObject[o] = obj1[o];
		}
		for(var o in obj2){
			newObject[o] = obj2[o];
		}
		return newObject;			
}})
	
	// jquery dependant functions
function getJsonValues(object){
	var param = new Object();
	object.find('input:checkbox:checked,input:radio:checked').each(function(){
		//this no longer works in jquery 4.0.2 :( !#$$##$
		/*if(!param[this.name]){
			param[this.name] = new Array();
		}
		param[this.name].push(this.value);*/
		param[this.name] = this.value;
	}).end().find('input,textarea').not(':checkbox,:radio').each(function(){
		param[this.name] = this.value;	
	}).end().end().find('select').each(function(){
		param[this.name] = this.value//this.options[this.selectedIndex].value;
	});
	return param;		
}
if($.fn){
	$.fn.onEnter = function(func){
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
function formatCurrency(num,nosign) {
	num = num.toString().replace(/\$|\,/g,'');
	if(isNaN(num)){num = "0";}
	sign = (num == (num = Math.abs(num)));
	num = Math.floor(num*100+0.50000000001);
	cents = num%100;
	num = Math.floor(num/100).toString();
	if(cents<10){cents = "0" + cents;}
	for (var i = 0; i < Math.floor((num.length-(1+i))/3); i++){
		num = num.substring(0,num.length-(4*i+3))+','+
		num.substring(num.length-(4*i+3));
	}
	return (((sign)?'':'-') + ((nosign)?'':'$') + num + '.' + cents);
}

function examine(obj){
	var msg = ""
	for(i in obj){
		msg += i+"= "+obj[i]+"\n\r"	
	}	
	return msg
}


