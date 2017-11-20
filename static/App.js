
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
				console.log(data.search_ndbno['report']['food']['ing']['desc'])
			}
		})
	})

	 
});