function arrangeJson4Timeline(data){


	var result = new Object();

	var timeline = new Object();
	result["timeline"] = timeline;

	timeline["headline"] = "";
	timeline["type"] = "default";
	timeline["text"] = "";


	var array = new Array();
	timeline["date"] = array;

	var era = new Array();
	timeline["era"] = era;

	for(var i = 0; i < data.length; i++){

		var obj = data[i];

		var s = obj.s.value;

		if(!obj.date && !obj.start){//旧Dateか新Dateを持たない場合はスキップ
			continue;
		}

		if(obj.date && obj.date.value == ""){//持っていたとしても空の場合
			continue;
		}

		if(obj.date){
			sDate = obj.date.value+",1,1";
		}


		if(obj.start){
			sDate = obj.start.value;
			sDate = sDate.replace(/-/g, ",");
		}

		timeline["startDate"] = sDate;
		var eDate = sDate;
		if(obj.end){
			eDate = obj.end.value;
			eDate = eDate.replace(/-/g, ",");
		}

		var abst = "";
		if(obj.abst){
			abst = obj.abst.value;
		}

		var label = obj.label.value;
		var thumb = null;
		if(obj.thumb != null){
			thumb = obj.thumb.value;
		}

		if(obj.identifier){
			thumb = obj.identifier.value;
		}

		var event = new Object();
		array.push(event);
		event["startDate"] = sDate;
		event["endDate"] = eDate;
		event["headline"] = label;

		var div = $("<div>");


		var p = $("<p>");
		div.append(p);
		p.append(abst);


		div.append("<br>");

		var a = $("<a>");
		div.append(a);
		a.attr("href", "instance?resourceUri="+s);
		a.append("Detail &raquo;");


		var spanStr = $('<div>').append(div.clone()).html();
		event["text"] = spanStr;
		if(obj.tag){
			event["tag"] = obj.tag.value;
		}



		var asset = new Object();

		if(obj.thumb != null){

			event["asset"] = asset;
			asset["media"] = thumb;
		}

	}

	/*
	var e = new Object();
	e["startDate"] = "1890,12,10";
	e["endDate"] = "1945,12,10";
	e["headline"] = "Naval Holiday";
	e["tag"] = "年号";
	era.push(e);

	e = new Object();
	e["startDate"] = "1956,12,10";
	e["endDate"] = "2011,12,10";
	e["headline"] = "Naval Holiday";
	e["tag"] = "情勢";
	era.push(e);
	*/


	return result;
}