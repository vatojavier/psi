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
    
function allowDrop(ev){
    ev.preventDefault();
}

function drag(ev){
    clearInterval(window.timer)
    ev.dataTransfer.setData("origen", ev.target.id);
}

function drop(ev){
    ev.preventDefault();

    /*Solo refrescar cuando es el turno del otro jugador*/
    if($("meta[name=juego_vs_IA]").attr("content") == "False"){
        if(!$(".tu_turno").length){
            window.timer = setInterval(refrescar,2000);
        }
        
    }

    var origen = parseInt(ev.dataTransfer.getData("origen"));
    destino = parseInt(ev.target.id)

    var csrf_token = getCookie('csrftoken');

    $.ajax({
        url: '/move/',
        type: 'post',
        data: {
            origin: origen,
            target: destino,
        },
        headers: {
            "X-CSRFToken": csrf_token,                
        },
        success: function (response) {

            if(response.mov_valido){
                $("#mal_mov").hide();
                location.reload();
            }else{
                $("#mal_mov").show();
            }
        },
        error: function(){
            console.log("Error del servidor");               
        }
    });

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

    /*Solo refrescar cuando es el turno del otro jugador*/
    if($('meta[name=juego_vs_IA]').attr("content") == "True"){
        console.log("Juego vs ia true")
    }else{
        if($(".tu_turno").length){
            console.log("humano y mi turno");
        }else{
            console.log("Esperando al otro humano")
            window.timer = setInterval(refrescar,2000);
        }
        
    }

});

function refrescar(){
    location.reload();
}

