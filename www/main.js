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
        loop: false,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
            delay: 5000,  // Optional: Delay before hiding
            callback: function() {
                $('.siri-message').show(); // Keep text visible
            }
        }
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
        
        function PlayAssistant(message) {

            if (message != "") {
    
                $("#Oval").attr("hidden", true);
                $("#SiriWave").attr("hidden", false);
                eel.allCommands(message);
                $("#chatbox").val("")
                $("#MicBtn").attr('hidden', false);
                $("#SendBtn").attr('hidden', true);
    
            }
    
        }
        // toogle fucntion to hide and display mic and send button 
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }
     // key up event handler on text box
     $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)
    
    });
    
    // send button event handler
    $("#SendBtn").click(function () {
    
        let message = $("#chatbox").val()
        PlayAssistant(message)
    
    });
    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    });

});    