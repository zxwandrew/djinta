function SaveDrawing() {
	window.AllPartsJSON = $.toJSON(AllParts);
	//var temp = $.evalJSON( AllPartsJSON )
	//alert(AllPartsJSON);
	localStorage["drawing"] = AllPartsJSON;
	
	answer='{"message": {"F2": {"category": "Force", "magnitude": 1.0, "name": "F2", "servy1": 15.0, "servx1": 7.0, "type": "YForce", "onmember": [0]}, "S1": {"name": "S1", "servy1": 15.0, "servx1": 5.0, "fx1": 0, "dy1": 0, "dx1": 0, "fm1": 0, "dm1": 0, "fy1": 0, "onmember": [0], "type": "FixedSupport"}, "Calculated": "True", "M0": {"servx1": 5, "e": 300000.0, "i": 100.0, "area": 10.0, "servx2": 10, "connectpart": [1, 2], "servy2": 15, "dy1": 0, "dy2": 0.0, "dx2": 0.0, "dm1": 0, "dm2": 0.0, "dx1": 0, "length": 5.0, "type": "Member", "servy1": 15, "name": "M0"}}}'
	//alert(answer["message"]["F2"]["category"])]
	DisplayDrawingResultPage(answer)
}

function HideResult(){
	$(".Result-Background").hide("slow");
	
}

function ShowResult(){
	if($(".Result-Background").is(":visible")){
		$(".Result-Background").hide("slow");
	}else{
		$(".Result-Background").show("slow");
	}
	
}

function DisplayDrawingResultPage(result){
	//alert(result['F2']['category'])
	obj1 = JSON.parse(result);
	result= obj1['message']
	
	$(".Result-Pane").replaceWith('<div class ="Result-Pane"><a href="javascript: HideResult()">Back To Drawing</a>	<br/></div>');

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
	
	x=JSON.stringify
	
	console.log(result)
	$(".Result-Pane").append(a)
	
	//Display the result pane
	ShowResult()
	
}