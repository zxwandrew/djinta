function SaveDrawing() {	
				window.AllPartsJSON = $.toJSON(AllParts);
				alert(AllPartsJSON);
				//alert("Saved!")
				localStorage["drawing"] = AllPartsJSON;
				
				answer={"message": {"F2": {"category": "Force", "magnitude": 1.0, "name": "F2", "servy1": 15.0, "servx1": 7.0, "type": "YForce", "onmember": [0]}, "S1": {"name": "S1", "servy1": 15.0, "servx1": 5.0, "fx1": 0, "dy1": 0, "dx1": 0, "fm1": 0, "dm1": 0, "fy1": 0, "onmember": [0], "type": "FixedSupport"}, "Calculated": "True", "M0": {"servx1": 5, "e": 300000.0, "i": 100.0, "area": 10.0, "servx2": 10, "connectpart": [1, 2], "servy2": 15, "dy1": 0, "dy2": 0.0, "dx2": 0.0, "dm1": 0, "dm2": 0.0, "dx1": 0, "length": 5.0, "type": "Member", "servy1": 15, "name": "M0"}}}
				//alert(answer["message"]["F2"]["category"])]
				DisplayDrawingResultPage(answer)
}

//some temp code for ajax
function my_js_callback(data) {
	//send data to be turned into interpretable data
	DisplayDrawingResultPage(data)
}

function send_form() {
				SaveDrawing();
				//var data = JSON.stringify($('#my_form').serializeObject());
				//alert(AllPartsJSON);
	Dajaxice.drawings.send_form(my_js_callback, {
		'form' : AllPartsJSON
	});
}

//Hide the result background
function HideResult(){
	$(".Result-Background").hide("slow");
}

//Toggle result background (hide/display)
function ShowResult(){
	if($(".Result-Background").is(":visible")){
		$(".Result-Background").hide("slow");
	}else{
		$(".Result-Background").show("slow");
	}
	
}

//actual translating the json to human readable
function DisplayDrawingResultPage(result){
	//alert(result['F2']['category'])
	result=JSON.stringify(result)
	console.log(result)
	obj1 = JSON.parse(result);
	result= obj1['message']
	ShowResult()
	
	$(".Result-Pane").replaceWith('<div class ="Result-Pane"><a href="javascript: HideResult()">Back To Drawing</a>	<br/> </div> ');
	
	$(".Result-Pane").append(' <div id="chartdiv" style="height:300px;width:300px; "></div>')
	var plot1=$.jqplot('chartdiv',  [[[1, 2],[3,5.12],[3,-90],[5,13.1],[7,33.6],[9,85.9],[11,219.9]]]);

	var a='';	
	//The whole array
	for(var x in result){
		if(x!='Calculated'){
			a+="Name of Part: "+x
			for(var y in result[x]){
				a+="<br/>";
				a+=y+': '
				a+=result[x][y]
			}//properties of the part 
			a+="<br/><br/>"
		}		
	}
	
	//add everything to all result part
	for (var x in result){
		if(result[x].type=="Member"){
			part = new Object();
			part.name = result[x].name;
			//for(attached in result[x].)
		}
	}
	
	//$.jqplot('chartdiv' , [[[1, 2],[3,5.12],[5,13.1],[7,33.6],[9,85.9],[11,219.9]]]);
	
	console.log(result)
	$(".Result-Pane").append(a)
	
	//Display the result pane
	//ShowResult()
	
}