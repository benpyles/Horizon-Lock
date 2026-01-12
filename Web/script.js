//Import pose ai model
import {
    PoseLandmarker,
    FilesetResolver,
    DrawingUtils
} from "https://cdn.skypack.dev/@mediapipe/tasks-vision@0.10.0";

//setup pose ai module
const video = document.getElementById("webcam");
let poseLandmarker;

const init = async () => {
    // 1. Load the AI
    const vision = await FilesetResolver.forVisionTasks(
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm"
    );
    poseLandmarker = await PoseLandmarker.createFromOptions(vision, {
        baseOptions: {
            modelAssetPath: `https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task`,
            delegate: "GPU"
        },
        runningMode: "VIDEO"
    });

    const stream = await navigator.mediaDevices.getUserMedia({ video: true});
    video.srcObject = stream;

    video.addEventListener("loadeddata", predict);
};

async function predict() {
    let startTimeMs = performance.now();
    poseLandmarker.detectForVideo(video, startTimeMs, (result) => {
    if (result.landmarks && result.landmarks.length > 0){
        const firstPerson = result.landmarks[0];
        const leftWrist = firstPerson[15];
        const rightWrist = firstPerson[16];

        const handData = {
            left: {
                x: (leftWrist.x * video.videoWidth).toFixed(2),
                y: (leftWrist.y * video.videoHeight).toFixed(2)
            },
            right: {
                x: (rightWrist.x * video.videoWidth).toFixed(2),
                y: (rightWrist.y * video.videoHeight).toFixed(2)
            }
        };
        
        console.log("Left Hand: ", handData.left, " Right Hand: ", handData.right);
    }
});

    window.requestAnimationFrame(predict);
}

function CustomLogin(left, right) {
    console.log(`Left: ${left.x}, ${left.y} | Right: ${right.x}, ${right.y}`);
}

init();