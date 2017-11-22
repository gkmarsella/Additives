
$(function(){

	$("[data-toggle=popover]").popover();

	$(".prod-name").click(function(e){
		var $clicked = $(this).attr('id')
		var ndb = $clicked
		$.ajax({
			type: "POST",
			url: "/get_ingredients",
			data: JSON.stringify(ndb),
			contentType: 'application/json',
			dataType: 'json',
			success: function(data){
				$('#ingredient-list').html((data.search_ndbno['report']['food']['ing']['desc']));

				$('#additive-list').html('');

				var allAdditives = data.additives;
				
				var addInfo = data.additive_information;

				var description = "description";


				for(var key in addInfo){
					$('#additive-list').append('<li>'+'<button type="button" class="btn btn-lg btn-danger" data-toggle="popover" title="' + key + '" data-content="Description: ' + (addInfo[key]["description"]) + '">' + key + '</button></li>');
				}

				// allAdditives.forEach(function(i){
				// 	$('#additive-list').append('<li>' + i + '</li>')
				// });


					
			}
		})
	})

	 
});