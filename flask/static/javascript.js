/* Raspberry Tank Web UI JavaScript
   Written by Ian Renton (http://ianrenton.com), July 2012
   Released into the public domain without licence. */

// All commands that could be sent to the vehicle.
var command = {
  'forward' : false,
  'reverse' : false,
  'left' : false,
  'right' : false,
  'stop' : false
}

// Port on which the tank's control server runs
var CONTROL_PORT = 8090;

// Port on which the mjpg-streamer webcam server runs
var WEBCAM_PORT = 8080;

// Executes on page load.
function load() {
  createImageLayer();
}

// Sets a command to either true or false by name, e.g. to go forwards use
// set('forwards', true) and to stop going forwards, use set('forwards', false).
function set(name, value) {
  //alert("set");
  clear();
  command[name] = value;
  send();
  return true;
}

// Set all commands to false, in case there's been a glitch and something is
// stuck on.
function clear() {
  for (var name in command) {
    command[name] = false;
  }
}

// Set all commands to false, in case there's been a glitch and something is
// stuck on.
function stop() {
  for (var name in command) {
    command[name] = false;
  }
  command['stop'] = true;
  send();
}

// Send the current command set to the vehicle.
function send() {
  for (var name in command) {
    if(command[name] == true){
      //var message = window.location.protocol+'//'+window.location.host + "/" + name;
      //alert(message);
      $.get(window.location.protocol+'//'+window.location.host + "/" + name);
      break;
    }
  }
}

