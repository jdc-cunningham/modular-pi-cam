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

// buttons, camera state

const isoVals = [100, 200, 400, 800, 1600, 3000];
const shutterSpeedVals = ["1", "1/2", "1/4", "1/8", "1/15", "1/30", "1/60", "1/125", "1/250", "1/500", "1/1000"]; // second

let isoPos = 0;
let iso = isoVals[isoPos];

let shutterPos = 8;
let shutterSpeed = shutterSpeedVals[shutterPos];

const updateControl = (whichControl, dir, dispTarget) => {
  if (whichControl === "iso") {
    const maxPos = isoVals.length - 1;

    if (dir === "inc") {
      if (isoPos < maxPos) {
        isoPos += 1;
      }
    } else {
      if (isoPos > 0) {
        isoPos -= 1;
      }
    }

    dispTarget.value = isoVals[isoPos];
  }

  if (whichControl === 'shutter speed') {
    const maxPos = shutterSpeedVals.length - 1;

    if (dir === "inc") {
      if (shutterPos < maxPos) {
        shutterPos += 1;
      }
    } else {
      if (shutterPos > 0) {
        shutterPos -= 1;
      }
    }

    dispTarget.value = shutterSpeedVals[shutterPos];
  }
}

document.querySelectorAll('.web-stream-ui__control-group').forEach(controlSet => {
  const whichControl = controlSet.querySelector('.web-stream-ui__control-inputs').getAttribute('data-control');
  const dispTarget = controlSet.querySelector('.web-stream-ui__control-value');
  const btns = controlSet.querySelectorAll('.control-btn');
  
  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      const dir = btn.getAttribute('data-dir');
      updateControl(whichControl, dir, dispTarget);
    });
  });
});