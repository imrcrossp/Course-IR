/*!
* Start Bootstrap - Small Business v5.0.3 (https://startbootstrap.com/template/small-business)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-small-business/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

// 測試用彈視窗 window.alert()
function updateservices(){
	var show = false;
	var svc = document.getElementById("services");

	var tb = document.getElementById("found_json");
	if($("#found_json>tbody").children("tr").length > 1){
		tb.style.display = "table";
		tb.className = "table table-responsive table-striped table-bordered table-success table-hover";
		show = true;
	}else{
		tb.style.display = "none";
	}
	var tb = document.getElementById("found_xml");
	if($("#found_xml>tbody").children("tr").length > 1){
		tb.style.display = "table";
		tb.className = "table table-responsive table-striped table-bordered table-success table-hover";
		show = true;
	}else{
		tb.style.display = "none";
	}
	var tb = document.getElementById("load_json");
	if($("#load_json>tbody").children("tr").length > 1){
		tb.style.display = "table";
		tb.className = "table table-responsive table-striped table-bordered table-success table-hover";
		show = true;
	}else{
		tb.style.display = "none";
	}
	var tb = document.getElementById("load_xml");
	if($("#load_xml>tbody").children("tr").length > 1){
		tb.style.display = "table";
		tb.className = "table table-responsive table-striped table-bordered table-success table-hover";
		show = true;
	}else{
		tb.style.display = "none";
	}
	if(show === true){
		svc.style.display = "block";
		location.href = "#services";
	}else{
		svc.style.display = "none";
	}
}
function chgtxt(text){
	var json = document.getElementById("found_json");
	var xml = document.getElementById("found_xml");
	while(json.rows.length > 1){
		json.deleteRow(1);
	}
	while(xml.rows.length > 1){
		xml.deleteRow(1);
	}
	if(text != ""){
		var count = 0;
		$('#load_json tr').each( function(){
			++count;
			if(count%2 != 1){
				var cnt = $(this);
				//console.log(cnt);
				if(cnt.children("td").length == 2){
					var qq = cnt.children("td").eq(1).html();
					var len = text.length;
					var br = 0;
					var strong = 0;
					var last = 0;
					var parg = "";
					var found = false;
					while(1){
						last = qq.indexOf(text);
						if(last == -1) break;
						br = qq.indexOf("<br>");
						strong = qq.indexOf("<strong>");
						//console.log(br, strong);
						if((br+3 >= last && br <= last && br != -1)){
							parg += qq.slice(0, br+4);
							console.log(parg);
							qq = qq.slice(br+4, qq.length);
							console.log(qq);
							continue;
						}else if((strong+7 >= last && strong <= last && strong != -1)){
							parg += qq.slice(0, strong+8);
							console.log(parg);
							qq = qq.slice(strong+8, qq.length);
							console.log(qq);
							continue;
						}else{
							found = true;
							parg += qq.slice(0, last) + "<span style=\"background-color:#008000\">" + text +"</span>";
							qq = qq.slice(last+len, qq.length);
						}
						
					}
					if(found == true){
						parg += qq;
						var newblock = json.insertRow(json.rows.length);
						var block = "\
							<td              >" + cnt.children("td").eq(0).html()+ "</td>\
							<td colspan=\"8\" align=\"left\">" + parg + "</td>";
						newblock.innerHTML = block;
					}
				}				
			}
		})
		count = 0;
		var title = "";
		$('#load_xml tr').each( function(){
			if(count%3 == 1) title = $(this).children("td").eq(0).html();
			if(count%3 == 2){
				var cnt = $(this);
				var found = false;
				if(cnt.children("td").length == 1){
					var qq = cnt.children("td").eq(0).html();
					var maxx = qq.length;
					var len = text.length;
					var begin = 0;
					var last = 0;
					var parg = "";
					var br = 0;
					var strong = 0;
					var _strong = 0;
					while(1){
						last = qq.indexOf(text);
						if(last == -1) break;
						br = qq.indexOf("<br>");
						strong = qq.indexOf("<strong>");
						_strong = qq.indexOf("</strong>");
						//console.log(br, strong);
						if((br+3 >= last && br <= last && br != -1)){
							parg += qq.slice(0, br+4);
							//console.log(parg);
							qq = qq.slice(br+4, qq.length);
							//console.log(qq);
							continue;
						}else if((strong+7 >= last && strong <= last && strong != -1)){
							parg += qq.slice(0, strong+8);
							//console.log(parg);
							qq = qq.slice(strong+8, qq.length);
							//console.log(qq);
							continue;
						}else if((_strong+8 >= last && _strong <= last && _strong != -1)){
							parg += qq.slice(0, _strong+9);
							//console.log(parg);
							qq = qq.slice(_strong+9, qq.length);
							//console.log(qq);
							continue;
						}else{
							found = true;
							parg += qq.slice(0, last) + "<span style=\"background-color:#008000\">" + text +"</span>";
							qq = qq.slice(last+len, qq.length);
						}
						
					}
					if(found == true){
						parg += qq;
						var newblock = xml.insertRow(xml.rows.length);
						var block = "\
						<td colspan=\"9\" align=\"left\" >\
							"+ title +"\
						</td>";
						newblock.innerHTML = block;
						newblock = xml.insertRow(xml.rows.length);
						block = "<td colspan=\"9\" align=\"left\">";
						block += parg;
						block += "</td>";
						newblock.innerHTML = block;						
					}

				}				
			}
			++count;
		})
	}
	updateservices();
	document.getElementById("search_text").focus();
}
// $("#search_text").on('change', function(){
// 	//console.log($(this).val());
// 	chgtxt($(this).val());
//  });
function insertobj(fn, ftype){
	var tb = document.getElementById("ftb_tr");
	var newTH = document.createElement("td");
	var bt = "";
	// choose buton style
	if(ftype == "application/json"){
		bt = "<button class=\"buttonjson\">";
	}else
		bt = "<button class=\"buttonxml\">";
	bt 	  += "	<strong>"+fn+"</strong>\
			  </button>";
	newTH.innerHTML = bt;
	tb.appendChild(newTH);	
}
function countinfo(text, infomtx){
	var len = text.length;
	var newtext = "";
	var newline = false;
	//infomtx [number of char, words, sentences, ]
	for(var i = 0; i < len;){
		var ascii = text.codePointAt(i++);
		if(ascii == 92){
			ascii = text.codePointAt(i++);
			if(ascii == 34){
				newtext += "\"";
				infomtx[0] += 1;
				newline = false;
			}
			else if(ascii == 110){
				if(newline == false)
					infomtx[2] += 1;
				newtext += " <br> ";
				newline = true;
			}
		}else if(ascii >= 32 && ascii < 127){
			if(ascii == 32) infomtx[1] += 1;
			newtext += text[i-1];
			infomtx[0] += 1;
			newline = false;	
		}else{
			newtext += text[i-1];
			newline = false;
		}
	}
	return newtext;
}
function xmlhandler(cnt, dic){
	var _str = 0;
	var str_ = 0;
	var sec = "";
	var pos = 0;
	var label = "";

	while(1){
		_str = cnt.indexOf("<AbstractText", str_);
		if(_str == -1) return;
		str_ = cnt.indexOf("</AbstractText>", _str);
		sec = cnt.slice(_str, str_);
		var _lab = sec.indexOf("Label=");
		if(_lab != -1){
			var i = 0;
			while(sec[i] != "\"") ++i;
			for(++i; ; ++i){
				if(sec[i] == "\\"){
					++i;
					continue;
				}else if(sec[i] == "\"") break;
				label += sec[i];
			}		
		}else{
			label = "";
		}
		_lab = sec.indexOf(">");

		var cc = sec.slice(_lab+1, sec.length);
		dic.set(label, cc);
	}
}
function showresultofreadfile(cnt, tpof){
	var chd = document.getElementById("load_json");
	var text = "";
	var begn = 0;
	var last = 0;
	var _url = 0;
	var url_ = 0;
	var _url_ = "";
	var block = "";
	if(tpof == "application/json"){
		// 找 text 的範圍
		while(1){
			_url = cnt.indexOf("\"twitter_url\":", _url+14);
			if(_url == -1) break;
			url_ = cnt.indexOf("\n", _url);
			url_ = cnt.lastIndexOf(",", url_);
			_url_ = cnt.slice(_url+16, url_-1);
			_url_ = _url_.slice(_url_.lastIndexOf("/")+1, _url_.length);
			begn = cnt.indexOf("\"tweet_text\":", begn+13);
			last = cnt.indexOf("\n", begn);
			last = cnt.lastIndexOf(",", last);
			text = cnt.slice(begn+15, last-1);
			var newblock = chd.insertRow(chd.rows.length);
			var mtx = [0, 0, 1, 0];
			text = countinfo(text, mtx);
			block = "\
					<td              >" + _url_+ "</td>\
					<td colspan=\"8\" align=\"left\">" + text + "</td>";
			newblock.innerHTML = block;
			newblock = chd.insertRow(chd.rows.length);
			block = "\
					<td style=\"padding: 0px;\">" + ""+ "</td>\
					<td style=\"padding: 0px;\">" + "" + "</td>\
					<td style=\"padding: 0px;\">" + "" + "</td>\
					<td style=\"padding: 0px;\">" + "char(s)" + "</td>\
					<td style=\"padding: 0px;\">" + mtx[0] + "</td>\
					<td style=\"padding: 0px;\">" + "word(s)" + "</td>\
					<td style=\"padding: 0px;\">" + mtx[1] + "</td>\
					<td style=\"padding: 0px;\">" + "EOS" + "</td>\
					<td style=\"padding: 0px;\">" + mtx[2] + "</td>"
					;
			newblock.innerHTML = block;
		}
			
	}else if(tpof == "text/xml"){
		chd = document.getElementById("load_xml");
		while(1){
			_url = cnt.indexOf("<ArticleTitle>", _url+14);
			if(_url == -1) break;
			url_ = cnt.indexOf("</ArticleTitle>", url_+15);
			_url_ = cnt.slice(_url+14, url_);
			// 先切<Abstract>
			var abt = new Map();
			begn = cnt.indexOf("<Abstract>", begn+14);
			last = cnt.indexOf("</Abstract>", begn+14);
			if(begn == -1){
				text = "";
			}else{
				text = cnt.slice(begn+15, last);
				xmlhandler(text, abt);
			}				
			var newblock = chd.insertRow(chd.rows.length);
			block = "\
					<td colspan=\"9\" align=\"left\" >\
						<strong style=\"font-size:20px;\">" +
							"ArticleTitle: " + _url_ +
						"</strong><br>\
					</td>";
			newblock.innerHTML = block;
			var newblock = chd.insertRow(chd.rows.length);
			var content = "<td colspan=\"9\" align=\"left\">";
			for(let [key, value] of abt){
				if(key == "")
					content += value + "<br>";
				else
				content += 
					"<strong>"
						+ key + ": " +
					"</strong>"
						+ value + "<br>";
			}	
			content += "</td>";
			
			newblock.innerHTML = content;

			var newblock = chd.insertRow(chd.rows.length);
			var mtx = [0, 0, 0, 0];
			for(let [key, value] of abt){
				text = countinfo(value, mtx);
				mtx[2] += 1;
			}	
			block = "\
					<td style=\"padding: 0px;\">" + ""+ "</td>\
					<td style=\"padding: 0px;\">" + "" + "</td>\
					<td style=\"padding: 0px;\">" + "" + "</td>\
					<td style=\"padding: 0px;\">" + "char(s)" + "</td>\
					<td style=\"padding: 0px;\">" + mtx[0] + "</td>\
					<td style=\"padding: 0px;\">" + "word(s)" + "</td>\
					<td style=\"padding: 0px;\">" + mtx[1] + "</td>\
					<td style=\"padding: 0px;\">" + "EOS" + "</td>\
					<td style=\"padding: 0px;\">" + mtx[2] + "</td>"
					;
			newblock.innerHTML = block;
			//sessionStorage.setItem(_url_, content);
		}
	}
	updateservices();
}

function handleFiles() {
	var files = document.getElementById("upload_files").files;
	/* now you can work with the file list */
	var fr = new FileReader();


	Object.keys(files).forEach(i => {
		const file = files[i];
		const reader = new FileReader();
		insertobj(file.name, file.type);
		reader.onload = (e) => {
			showresultofreadfile(e.target.result, file.type);
		  //server call for uploading or reading the files one-by-one
		  //by using 'reader.result' or 'file'
		}
		reader.readAsText(file);
	})
	//console.log(csrftoken);
}
