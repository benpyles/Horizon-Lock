import os
import shutil
import urllib.request
import subprocess
import sys

# --- CONFIGURATION ---
MEDIAPIPE_VERSION = "0.10.0"
BASE_URL = f"https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@{MEDIAPIPE_VERSION}"

def download_file(url, folder, filename):
    local_path = os.path.join(folder, filename)
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, local_path)
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
        sys.exit(1)

def main():
    print("--- STARTING CLEAN BUILD ---")
    
    # 1. Build the game using Pygbag
    print("1. Building Pygbag project...")
    subprocess.run([sys.executable, "-m", "pygbag", "--build", "--archive", "main.py"], check=True)

    web_dir = os.path.join("build", "web")
    if not os.path.exists(web_dir):
        print("Error: Build failed.")
        sys.exit(1)

    # 2. Setup Local MediaPipe
    print("2. Downloading MediaPipe files locally...")
    mp_dir = os.path.join(web_dir, "mediapipe")
    # FIX: Create the 'wasm' subdirectory explicitly
    wasm_dir = os.path.join(mp_dir, "wasm")
    os.makedirs(wasm_dir, exist_ok=True)
    
    files_to_download = [
        (f"{BASE_URL}/vision_bundle.js", mp_dir, "vision_bundle.js"),
        (f"{BASE_URL}/wasm/vision_wasm_internal.js", wasm_dir, "vision_wasm_internal.js"),
        (f"{BASE_URL}/wasm/vision_wasm_internal.wasm", wasm_dir, "vision_wasm_internal.wasm"),
        ("https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task", mp_dir, "pose_landmarker_lite.task")
    ]

    for url, folder, name in files_to_download:
        download_file(url, folder, name)

    # 3. Inject the HTML code
    print("3. Injecting Camera & AI code into index.html...")
    index_path = os.path.join(web_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Add Webcam Element
    if '<video id="webcam"' not in html_content:
        html_content = html_content.replace(
            '<body>', 
            '<body><video id="webcam" style="display:none;" autoplay playsinline></video>'
        )

    # Add the Script (Using LOCAL files now)
    script_content = """
<script type="module">
    import { PoseLandmarker, FilesetResolver, DrawingUtils } from "./mediapipe/vision_bundle.js";

    const video = document.getElementById("webcam");
    let poseLandmarker;

    async function init() {
        console.log("Starting Local MediaPipe...");
        
        // Use local WASM files
        const vision = await FilesetResolver.forVisionTasks("./mediapipe/wasm");
        
        poseLandmarker = await PoseLandmarker.createFromOptions(vision, {
            baseOptions: {
                modelAssetPath: "./mediapipe/pose_landmarker_lite.task",
                delegate: "GPU"
            },
            runningMode: "VIDEO"
        });

        console.log("AI Loaded. Requesting Camera...");
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            video.addEventListener("loadeddata", predictWebcam);
        } catch (e) { console.error("Camera Error:", e); }
    }

    async function predictWebcam() {
        let startTimeMs = performance.now();
        if (poseLandmarker) {
            poseLandmarker.detectForVideo(video, startTimeMs, (result) => {
                if (result.landmarks && result.landmarks.length > 0) {
                    window.handX = result.landmarks[0][9].x;
                }
            });
        }
        window.requestAnimationFrame(predictWebcam);
    }
    init();
</script>
    """
    
    # Append script before closing body
    html_content = html_content.replace('</body>', f'{script_content}</body>')
    
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 4. Create the Strict Server
    print("4. Creating Strict Server configuration...")
    server_code = """
import http.server, socketserver, os
PORT = 8003 
class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Strict headers work perfectly because EVERYTHING is local now
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        super().end_headers()

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()
"""
    with open(os.path.join(web_dir, "server.py"), "w") as f:
        f.write(server_code)

    print("\n--- SETUP COMPLETE ---")
    print(f"Go to: cd build/web")
    print(f"Run:   python3 server.py")
    print(f"Open:  http://localhost:8003")

if __name__ == "__main__":
    main()