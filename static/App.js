
$(function(){


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
				console.log(allAdditives)

				allAdditives.forEach(function(i){
					$('#additive-list').append('<li>' + i + '</li>')
				})
					
			}
		})
	})

	 
});