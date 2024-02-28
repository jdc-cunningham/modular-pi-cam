let piSocket = null;
let piSocketInterval = null;

const connectToPiZero2 = () => {
  piSocket = new WebSocket('ws://192.168.1.104:5678');

  // connection opened, send messages to robot
  piSocket.addEventListener('open', function (event) {
    console.log('pi connected');
    piSocket.send('Hello robot!');
 
    // keep connection to esp01 alive
    piSocketInterval = setInterval(() => {
      piSocket.send('poll');
    }, 1000);
  });
 
  // listen for messages from robot
  piSocket.addEventListener('message', function (event) {
    const robotMsg = event.data;

    console.log(robotMsg);
  });
 
  piSocket.addEventListener('close', function (event) {
    console.log('pi connection lost');
    clearInterval(piSocketInterval);
    connectToPiZero2();
 });
}

connectToPiZero2();