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
//siri configuration 
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude:"1",
        speed:"0.30",
        autostart:true,

    });
    //siri meaasage animation
    $('.siri-message').textillate({
        loop:true,
        sync:true,
        in:{
            effect:"fadeInUp",
            sync:true,
        },
        out:{
            effect:"fadeOutUp",
            sync:true,
        },
    });

    //mic button click eventlistener
        $("#MicBtn").click(function () { 
            eel.playassisstantsound();
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()();
        
        });

        function doc_keyUp(e) {
            console.log("Key released:", e.key);
            console.log("Meta key status:", e.metaKey);
            console.log("Ctrl key status:", e.ctrlKey);
            
            // Check if the 'j' key is released while Meta or Ctrl is still pressed
            if (e.key === 'j' && (e.metaKey || e.ctrlKey)) {
                // Trigger actions via Eel
                eel.playassisstantsound();
                $("#Oval").attr("hidden", true);
                $("#SiriWave").attr("hidden", false);
                eel.allCommands();
            }
        }
        
        document.addEventListener('keyup', doc_keyUp, false);
        
    
});    