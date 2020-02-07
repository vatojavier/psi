function joinFunction(id){
    
    /*alert("concha" + id);*/
    var url_join = "/join_game/" + id;
    var boton = ".btn_entrar_" + id;

    $.ajax({url: url_join,
            dataType: "text",

         complete: function(result){
            $("#join_succes").text("Te has unido");
            $(boton).show();
            console.log(boton);
        },
    });

}