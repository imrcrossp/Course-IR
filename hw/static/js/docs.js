$(document).ready(function(){
	var fn = getUrlParameter('fn');
	var key = getUrlParameter('token')
	$.ajax({
		url: '/hw/docs',
		type: 'GET',
		data: {
			msg: "cloud",
			fn: fn,
			token: key
		},
		success: function(data){
			var dic = JSON.parse(data);
			$('#cntxt').append("<p>"+dic.cntxt+"<p>");
			$('#adv_chars').append("<p>Chars： "+dic.chars+"</p>");
			$('#adv_words').append("<p>Words： "+dic.words+"</p>");
			$('#adv_sents').append("<p>SENTs： "+dic.sents+"</p>");
			$('#adv_found').append("<p>Found： "+dic.found+"</p>");
			$('#adv_title').html("<strong>"+dic.title+"</strong>")
			var mydic = JSON.parse(dic.top24);
			$('#adv_porter').append("<svg id="+"top5"+" ></svg>");
			cr8svg_line("top5", mydic, 'Top5 - w/ porter\'s');
		},
	});
});

var getUrlParameter = function getUrlParameter(sParam){
	var sPageURL = window.location.search.substring(1),
	sURLVariables = sPageURL.split('&'),
	sParameterName,
	i;
	for(i = 0; i < sURLVariables.length; i++){
		sParameterName = sURLVariables[i].split('=');
		if(sParameterName[0] == sParam){
			return typeof sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);

		}
	}
	return false;
};