function joinFunction(id){
    
    /*alert("concha" + id);*/
    var url_join = "/join_game/" + id;
    var boton = "#btn_entrar_" + id;
    var texto_suc = "#join_succes_" + id;

    $.ajax({url: url_join,
            dataType: "text",

         complete: function(result){
            $(boton).show();
            $(texto_suc).show();
            
        },
    });

}