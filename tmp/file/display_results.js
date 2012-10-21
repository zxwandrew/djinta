function SaveDrawing() {	
				window.AllPartsJSON = $.toJSON(AllParts);
				//alert(AllPartsJSON);
				//alert("Saved!")
				//localStorage["drawing"] = AllPartsJSON;
				
				//answer={"message":{"F2": {"Category": "Force", "Magnitude": 100.0, "Name": "F2", "servy1": 15.0, "On Member": [0], "servx1": 35.0, "Type": "YForce"}, "S1": {"Category": "Support", "Y-Deflection-1": 0, "Name": "S1", "servy1": 15.0, "Rotational-Deflection-1":0, "servx1": 15.0, "M-Force-1": 2000.0000000000002, "Y-Force-1": -100.0, "On Member": [0], "X-Deflection-1": 0, "Type": "FixedSupport", "X-Force-1": 0.0}, "Calculated": "True", "M0": {"Category": "Member", "Y-Deflection-2": 0, "servy2": 15, "Connected to Parts": [1, 2], "Name": "M0", "Area": 10.0, "servx2": 35, "Rotational-Deflection-2": 0, "Rotational-Deflection-1": 0, "servx1": 15, "Length": 20.0, "servy1": 15, "Youngs Modulus": 300000.0, "Y-Deflection-1": 0, "Moment of Inertia": 100.0, "X-Deflection-1": 0, "ShearDiagram": [[0.0, 0.0], [0.0, 0.0], [0.0, -100.0], [20.0, -100.0], [20.0, 0.0], [20.0, 0.0], [20.0, 0]], "X-Deflection-2": 0, "Type": "Member"}}}
				//answer={"message": {"Calculated": "True", "S8": {"name": "S8", "servy1": 20.0, "servx1": 15.0, "fx1": 0.0, "dy1": 0, "dx1": 0, "fm1": 0.0, "dm1": 0, "fy1": 0.0, "onmember": [3, 4], "type": "FixedSupport"}, "P6": {"dm1": 0.0, "name": "P6", "servy1": 35.0, "servx1": 50.0, "type": "FixedJoint", "dy1": 0.0, "dx1": 0.0, "onmember": [1, 2]}, "P5": {"dm1": 0.0, "name": "P5", "servy1": 35.0, "servx1": 35.0, "type": "Hinge", "dy1": 0.0, "dx1": 0.0, "onmember": [0, 1]}, "F9": {"category": "Force", "magnitude": 900.0, "name": "F9", "servy1": 30.0, "servx1": 25.0, "type": "YForce", "onmember": [0]}, "S11": {"name": "S11", "servy1": 35.0, "servx1": 40.0, "fx1": 0.0, "dy1": 0, "dx1": 0, "fm1": 0.0, "dm1": 0, "fy1": 0.0, "onmember": [1], "type": "FixedSupport"}, "S7": {"name": "S7", "servy1": 25.0, "servx1": 35.0, "fx1": 0.0, "dy1": 0, "dx1": 0, "fm1": 0, "dm1": 0.0, "fy1": 0.0, "onmember": [2, 3], "type": "PinSupport"}, "M4": {"servx1": 15, "e": 300000.0, "i": 100.0, "area": 10.0, "servx2": 15, "connectpart": [8], "servy2": 25, "dy1": 0, "dy2": 0, "dx2": 0, "dm1": 0, "dm2": 0, "dx1": 0, "length": 5.0, "ShearDiagram": [[0.0, 0.0], [0.0, 0.0]], "type": "Member", "servy1": 20, "name": "M4"}, "M1": {"servx1": 35, "e": 300000.0, "i": 100.0, "area": 10.0, "servx2": 50, "connectpart": [5, 6, 10, 11], "servy2": 35, "dy1": 0, "dy2": 0, "dx2": 0, "dm1": 0, "dm2": 0, "dx1": 0, "length": 15.0, "ShearDiagram": [[0.0, 0.0], [5.0, 0.0], [5.0, 0.0], [10.0, 0.0], [10.0, 0.0]], "type": "Member", "servy1": 35, "name": "M1"}, "M0": {"servx1": 15,"e": 300000.0, "i": 100.0, "area": 10.0, "servx2": 35, "connectpart": [5, 9], "servy2": 35, "dy1": 0.0, "dy2": 0, "dx2": 0, "dm1": 0.0, "dm2": 0, "dx1": 0.0, "length": 22.360679774997898, "ShearDiagram": [[0.0, 0.0], [11.180339887498949, 0.0], [11.180339887498949, 900.0]], "type": "Member", "servy1": 25, "name": "M0"}, "M3": {"servx1": 15, "e": 300000.0, "i": 100.0, "area": 10.0, "servx2": 35, "connectpart": [7, 8], "servy2": 25, "dy1": 0, "dy2": 0, "dx2": 0, "dm1": 0, "dm2": 0, "dx1": 0, "length": 20.615528128088304, "ShearDiagram": [[0.0, 0.0], [20.615528128088304, 0.0], [0.0, 0.0], [0.0, 0.0]], "type": "Member", "servy1": 20, "name": "M3"}, "M2": {"servx1": 35, "e": 300000.0, "i": 100.0, "area": 10.0, "servx2": 50, "connectpart": [6, 7], "servy2": 35, "dy1": 0, "dy2": 0, "dx2": 0, "dm1": 0, "dm2": 0, "dx1": 0, "length": 18.027756377319946, "ShearDiagram": [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], "type": "Member", "servy1": 25, "name": "M2"}, "S12": {"name": "S12", "servy1": 35.0, "servx1": 45.0, "fx1": 0.0, "dy1": 0, "dx1":0, "fm1": 0, "dm1": 0.0, "fy1": 0.0, "onmember": [1], "type": "PinSupport"}}}
				//answer={"message": {"F2": {"category": "Force", "magnitude": 50.0, "name": "F2", "servy1": 15.0, "servx1": 30.0, "type": "YForce", "onmember": [0]}, "S1": {"name": "S1", "servy1": 15.0, "servx1": 10.0, "fx1": 0.0, "dy1": 0, "dx1": 0, "fm1": 1000.0000000000001, "dm1": 0, "fy1": -50.0, "onmember": [0], "type": "FixedSupport"}, "Calculated": "True", "M0": {"servx1": 10, "e": 300000.0, "i": 100.0, "area": 10.0, "servx2": 30, "connectpart": [1, 2], "servy2": 15, "dy1": 0, "dy2": 0.004444444444444445, "dx2": 0.0, "dm1": 0, "dm2": 0.0003333333333333334, "dx1": 0, "length": 20.0,"ShearDiagram": [[0.0, 0.0], [0.0, 0.0], [0.0, -50.0], [20.0, -50.0], [20.0, 0.0]], "type": "Member", "servy1": 15, "name": "M0"}}}
				//answer={"message": {"F2": {"category": "Force", "magnitude": 1.0, "name": "F2", "servy1": 15.0, "servx1": 7.0, "type": "YForce", "onmember": [0]}, "S1": {"name": "S1", "servy1": 15.0, "servx1": 5.0, "fx1": 0, "dy1": 0, "dx1": 0, "fm1": 0, "dm1": 0, "fy1": 0, "onmember": [0], "type": "FixedSupport"}, "Calculated": "True", "M0": {"servx1": 5, "e": 300000.0, "i": 100.0, "area": 10.0, "servx2": 10, "connectpart": [1, 2], "servy2": 15, "dy1": 0, "dy2": 0.0, "dx2": 0.0, "dm1": 0, "dm2": 0.0, "dx1": 0, "length": 5.0, "type": "Member", "servy1": 15, "name": "M0"}}}
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
	
	$(".Result-Pane").replaceWith('<div class ="Result-Pane"> <div class="Return-To-Drawing"><a href="javascript: HideResult()">Back To Drawing</a></div>	<br/> </div> ');
	
	//$(".Result-Pane").append('<div id="chartdiv" style="height:300px;width:300px; "></div>')
	//var plot1=$.jqplot('chartdiv',  [[[1, 2],[3,5.12],[3,-90],[5,13.1],[7,33.6],[9,85.9],[11,219.9]]]);

	var a='<br/><br/><br/>';	
	//The whole array
	for(var x in result){
		
		if(x!='Calculated' && result[x].Type!='Member'){
			a+="<h4> Name of Part: "+x+"</h4>"
			for(var y in result[x]){//properties of the part 
				if(y!="servx1" && y!="servy1" && y!="servx2" && y!="servy2"){
					a+="<h5>"+y+": "+result[x][y]+" </h5>"
				}				
			}
			a+="<br/><br/>"
		}
		else if(result[x].Type=='Member'){
			a+="<h4> Name of Part: "+x+"</h4>"
			for(var y in result[x]){
				if(y!="ShearDiagram"){//properties of the member
					a+="<h5>"+y+": "+result[x][y]+" </h5>"
				}
				else if (y=="ShearDiagram"){//For shear Diagrams
					//a+="<br/>"
					a+="<h5><b>Shear Diagram</b></h5>"
					a+='<div id="chartdiv_'+x+'" style="height:300px;width:300px; "></div>';
					$(".Result-Pane").append(a);
					a='';
					name='chartdiv_'+x;
					//alert(name);
					var plot1=$.jqplot(name,  [result[x].ShearDiagram]);
				}
				
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