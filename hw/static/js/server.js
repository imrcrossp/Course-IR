function load_default(){ 
	$.ajax({
		url: '',
		type: 'POST',
		data: {
			csrfmiddlewaretoken: csrftoken,
			msg: "cloud",
		},
		success: function(data){
			var dic = JSON.parse(data);
			//console.log(dic.top24);
			var top24dic = JSON.parse(dic.top24);
			var top24wo = JSON.parse(dic.top24_wo);
			var top24pctn = JSON.parse(dic.top24_pctn);
			//console.log(top24dic['covid-19'])
			// $('#svgblock').each( function(){
			// 	console.log($(this).html());
			// })
			$('#svgblock').html();
			$('#svgblock').append("<svg id="+"top24"+" ></svg>");
			cr8svg_line("top24", top24dic, 'Top24 - w/ porter\'s');
			$('#svgblock').append("<svg id="+"top24_wo"+" ></svg>");
			cr8svg_line("top24_wo", top24wo, 'Top24 - w/o porter\'s');
			$('#svgblock').append("<svg id="+"top24_pctn"+" ></svg>");
			cr8svg_line("top24_pctn", top24pctn, 'Top24 - mess');
			var count = 0;
			$('#svgblock g text').each( function(){
				var contxt = $(this).html();
				for(var i = 0; i < contxt.length; i = i+1){
					if(isNaN(contxt[i]) == false){
						count = count*10 + Number(contxt[i]);
						continue;
					}else{
						if(contxt[i] == ":" && count!=1 && count != 12 && count != 20){	
							$(this).html("");
						}
						break;
					}
				}
				count = 0;
			})
		}
	})
}
function cr8svg_line(svg_id, info, title){
	var svg = document.getElementById(svg_id);
	var words = [];
	var amount = [];
	var count = 1;
	for([key, val] of Object.entries(info)) {
		words.push(count.toString()+": "+key);
		amount.push(val);
		count++;
	}
	var graph = new chartXkcd.Line(svg, {
		title: title,
		xLabel: 'Word',
		data: {
			labels: words,
			datasets: [{
				label: 'amount',
				data: amount,
			}],
		},
		options:{
			legendPosition: chartXkcd.config.positionType.upRight,
		},
	});	
}

function hander_search(token, upper, lower){
	$.ajax({
		url: '',
		type: 'POST',
		data: {
			csrfmiddlewaretoken: csrftoken,
			msg: "adv_search",
			key: token,
			upper: upper,
			lower: lower
		},
		success: function(data){
			var dic = JSON.parse(data);
			$('#adv_search_table tbody').html("")
			for ([key, value] of Object.entries(dic)){
				//console.log(key, value);
				$('#adv_search_table tbody').append('<tr><td><a target="_blank" href="/hw/docs?fn='+key+'&token='+token+'">'+value+'</a></td></tr>');
			}
			document.getElementById('next').disable = false;
		}
	})	
}
function adv_search(){
	var token = (document.getElementById("adv_search_text").value);
	if(document.getElementById("adv_search_text").value.trim()==""){
		return;
	}
	var tmp = 10;
	var low = 0;
	localStorage["upper"] = tmp.toString();
	localStorage["lower"] = low.toString();
	localStorage["token"] = token;
	token = localStorage["token"];
	upper = parseInt(localStorage["upper"]);
	lower = parseInt(localStorage["lower"]);
	hander_search(token, upper, lower);
}
function addlow(){
	if(localStorage.getItem("upper") == null)
		return;
	token = localStorage["token"];
	upper = parseInt(localStorage["upper"]);
	lower = parseInt(localStorage["lower"]);
	var tmp = lower+10;
	localStorage["lower"] = tmp.toString();
	hander_search(token, upper, tmp);
}
function minuslow(){
	if(localStorage.getItem("upper") == null)
		return;
	token = localStorage["token"];
	upper = parseInt(localStorage["upper"]);
	lower = parseInt(localStorage["lower"]);
	if(lower-10 < 0){
		return;
	}

	var tmp = lower-10;
	localStorage["lower"] = tmp.toString();
	hander_search(token, upper, tmp);
}