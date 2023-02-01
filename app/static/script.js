$(document).ready(function () {
    // $("#calculate-km").attr("hidden",false);
    $('select').selectize({
        sortField: 'text'
    });
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
});