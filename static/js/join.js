function joinFunction(id){
    
    /*alert("concha" + id);*/
    var url_join = "/join_game/" + id;

    $.ajax({url: url_join,
            dataType: "text",

         complete: function(result){

            $("#boton_entrar_"+id).hide();
            $("#join_succes_" + id).show();
            $("#btn_jugar_"+id).show();

            
        },
    });

}