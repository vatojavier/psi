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
    ev.dataTransfer.setData("origen", ev.target.id);
}

function drop(ev){
    ev.preventDefault();

    var origen = parseInt(ev.dataTransfer.getData("origen"));
    destino = parseInt(ev.target.id)

    //No se puede enviar token sin ajax ?

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
        success: function () {
            console.log("siiii");
            location.reload();
        },
        error: function(){
            $("#mal_mov").show();
            console.log("noooo");               
        }
    });

}

$(document).ready(function(){
    var fila_par = false;

    /*Coloreando casillas*/
    
    $("td").each(function(index){
        console.log(this.id);
        if(index % 8 == 0){
            fila_par = !fila_par;
        }

        if(fila_par){
            if (index % 2 == 0){
                console.log("esta si");
                $("#"+index).css("background-color", "#6A3F55");
            }else{
                $("#"+index).css("background-color", "#EC4440");
            }
        }else{
            if (index % 2 == 0){
                console.log("esta si");
                $("#"+index).css("background-color", "#EC4440");
            }else{
                $("#"+index).css("background-color", "#6A3F55");
            }
        }

        console.log(fila_par);
    });
});


