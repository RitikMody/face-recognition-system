let v = document.getElementById("myVideo");
let b = document.getElementById("button");

//create a canvas to grab an image for upload
let imageCanvas = document.createElement('canvas');
let imageCtx = imageCanvas.getContext("2d");

//Add file blob to a form and post



//Get the image from the canvas
function sendImagefromCanvas() {

    //Make sure the canvas is set to the current video size
    imageCanvas.width = v.videoWidth;
    imageCanvas.height = v.videoHeight;

    imageCtx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight);

    //Convert the canvas to blob and post the file
    imageCanvas.toBlob(postFile, 'image/jpeg');
}

//Check user using picture
v.onclick = function () {
    console.log('clicked camera');
    sendImagefromCanvas();
};

//Check user using password
b.onclick = function () {
    console.log('clicked button');
    sendImagefromCanvas();
};

window.onload = function () {

    //Get camera video
    navigator.mediaDevices.getUserMedia({ video: { width: 1280, height: 720 }, audio: false })
        .then(stream => {
            v.srcObject = stream;
        })
        .catch(err => {
            console.log('navigator.getUserMedia error: ', err)
        });

};