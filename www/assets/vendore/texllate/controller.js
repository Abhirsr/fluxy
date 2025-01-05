$(document).ready(function () {
  //disply speak message
  eel.expose(DisplayMessage);
  function DisplayMessage(message) {
    $(".siri-message li:first").text(message);
    $(".siri-message").textillate("start");
  }

  //DISPLAY HOOD
  eel.expose(showhood);
  function showhood() {
    $("#Oval").attr("hidden", false);
    $("#SiriWave").attr("hidden", true);
  }
});
