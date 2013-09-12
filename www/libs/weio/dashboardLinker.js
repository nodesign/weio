console.log("LINKING EXTERNAL LIBRARIES");

///////////// BOOTSTRAP
$.getScript("libs/bootstrap/js/bootstrap.min.js")
.done(function(script, textStatus) {
      console.log( textStatus + " loaded bootstrap");
      load_sockjs();
      load_wifi();
      load_dashboard();
      load_updater();
      })
.fail(function(jqxhr, settings, exception) {
      console.log("Triggered ajaxError handler.");
      });

function load_sockjs() {
    ///////////// SOCKJS
    $.getScript("libs/sockJS/sockjs-0.3.min.js")
    .done(function(script, textStatus) {
          console.log( textStatus + " loaded sockjs" );
          })
    .fail(function(jqxhr, settings, exception) {
          console.log("Triggered ajaxError handler.");
          load_sockjs();
          });
}


function load_wifi() {

    ///////////// WIFI
    $.getScript("libs/weio/wifi.js")
    .done(function(script, textStatus) {
          console.log( textStatus + " loaded wifi" );
          })
    .fail(function(jqxhr, settings, exception) {
          console.log("Triggered ajaxError handler.");
          load_wifi();
          });
}


function load_dashboard() {
    ///////////// DASHBOARD
    $.getScript("libs/weio/dashboard.js")
    .done(function(script, textStatus) {
          console.log( textStatus  + " loaded dashboard");
          })
    .fail(function(jqxhr, settings, exception) {
          console.log("Triggered ajaxError handler.");
          load_dashboard();
          });
}

function load_updater() {
    ///////////// UPDATER
    $.getScript("libs/weio/updater.js")
    .done(function(script, textStatus) {
          console.log( textStatus + " loaded updater");
          })
    .fail(function(jqxhr, settings, exception) {
          console.log("Triggered ajaxError handler.");
          load_updater();
          });
}

function load(path) {
    $.getScript(path)
    .done(function(script, textStatus) {
          console.log( textStatus + " loaded updater");
          })
    .fail(function(jqxhr, settings, exception) {
          console.log("Triggered ajaxError handler.");
          
          });
    
}

