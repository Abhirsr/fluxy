$(document).ready(function () {
    
    $('.text').textillate({
        loop:true,
        sync:true,
        in:{
            effect:"fadeIn",
        },
        out:{
            effect:"bounceOut",
        },
    });
});