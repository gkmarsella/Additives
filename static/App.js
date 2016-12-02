
var $additives; 
document.addEventListener("DOMContentLoaded", function(){

// 	var eachFood = $(".food");

// 	for(var i=0; i < eachFood.length; i++){
// 		var foundFood = eachFood.find("img");

// 		eachFood.eq(i).hover(
// 			function() {
// 			$(this).children("img").removeClass().addClass("show");
// 		}, function() {
// 			$(this).children("img").removeClass("show").addClass("foodimage");
// 		});
// 	}

	function additiveDescription(val){
		if(val.additive_value > 0){
			var name = val.additive_name;
			var ingredients = val.additive_red_ingredients + val.additive_yellow_ingredients;
			return (name + ":::: " + ingredients);
		}
	}


	$(".rows").click(function(e) {
		var upc = $(this).data("upc");
		var sid = $(".table").data("sid");
		$additives = $(this).next(".additives");
		$additives.toggleClass("additives-hidden");
		if($("#" + upc).text() === ""){
			$.ajax({
			   url:"//api.foodessentials.com/label?u=" + upc + "&sid=" + sid + "&appid=Additives&f=json&api_key=f5hrgp2evbwm3rb7d6cxp95e",
			   jsonp:"c", 
			   dataType:'jsonp'
			}).then(function(data){
					var add_table = data.additives;
					for(var i=0; i < add_table.length; i++){
						if(additiveDescription(add_table[i]) !== undefined){
							$("#" + upc).append("<div>"+ additiveDescription(add_table[i]) + "</div>");
						}
						
					}
					console.log(data.additives);
			   });

		}
			});
		

	});