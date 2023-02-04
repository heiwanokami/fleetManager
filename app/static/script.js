$(document).ready(function () {
    // $("#calculate-km").attr("hidden",false);
    
    let current_km = 0;
    $('#car').on('change', async function() {
        if (this.value === ""){
            $("#calculate-km").attr("hidden",true);
            current_km = 0;
        }
        else {
            $("#calculate-km").attr("hidden",false);
        var url = 'http://127.0.0.1:5000/get_km/'+this.value;
        res = await fetch(url);
        current_km = await res.json();
        current_km = parseInt(current_km);
        $('#aktKm').text(current_km);
        }
    });
    
    $('#route_length').on('change', function() {
        if (this.value != "") {
            var new_km = parseInt(this.value)+ parseInt(current_km);
        } else {
            new_km = current_km;
        }
        $('#aktKm').text(new_km)    
    });
    var table =$('#carTable').DataTable({
        
    });
    $("#carTable tfoot th").each( function ( i ) {
		
		if ($(this).text() !== '') {

			var select = $('<select><option value=""></option></select>')
	            .appendTo( $(this).empty() )
	            .on( 'change', function () {
	                var val = $(this).val();
					
	                table.column( i )
	                    .search( val ? '^'+$(this).val()+'$' : val, true, false )
	                    .draw();
	            } );
	 		

            // All other non-Status columns (like the example)
            console.log(table.column(i).data().unique());
				table.column( i ).data().unique().sort().each( function ( d, j ) {  
					select.append( '<option value="'+d+'">'+d+'</option>' );
		        } );	
	        
		}
    } );
    $('select').selectize({
        sortField: 'text'
    });
});
