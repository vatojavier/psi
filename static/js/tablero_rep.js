function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getMovimiento(shiftr){
    var csrf_token = getCookie('csrftoken');


    $.ajax({
        url: '/get_move/',
        type: 'post',
        data: {
            shift: shiftr,
        },
        headers: {
            "X-CSRFToken": csrf_token,                
        },
        success: function (response) {
            origen = response.origin
            destino = response.target

            console.log(origen);

            cell = $("#"+response.origin)
            fichaImg = cell.find("img")

            if(!fichaImg.is("img")){
                alert("Algo fue mal")
            }
            $(fichaImg).appendTo("#"+destino)

        },
        error: function(){
            console.log("noooo");               
        }
    });


}

function repAuto(){
    console.log("ya")
    getMovimiento(1);
}

function play(id){

    if(id == "stop"){
        console.log("Parando")
        clearInterval(window.timer)
        $("#stop").text("play")
        $("#stop").attr("id", "start")
    }else{
        console.log("Empezando")
        repAuto();
        window.timer = setInterval(repAuto,2000)
        $("#start").text("stop")
        $("#start").attr("id", "stop")
    }
    
}

$(document).ready(function(){
    var fila_par = false;

    /*Coloreando casillas*/
    
    $("td").each(function(index){
        if(index % 8 == 0){
            fila_par = !fila_par;
        }

        if(fila_par){
            if (index % 2 == 0){
                $("#"+index).css("background-color", "#6A3F55");
            }else{
                $("#"+index).css("background-color", "#EC4440");
            }
        }else{
            if (index % 2 == 0){
                $("#"+index).css("background-color", "#EC4440");
            }else{
                $("#"+index).css("background-color", "#6A3F55");
            }
        }
    });
});