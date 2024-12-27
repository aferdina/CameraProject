from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from picamera2 import Picamera2
import uvicorn
import io
import time

# Optional: use Pillow to convert array -> JPEG in-memory
from PIL import Image

app = FastAPI()

# Create a single Picamera2 instance (so it can be shared between endpoints)
picam2 = Picamera2()

# --- Existing still capture endpoint ---
@app.get("/capture")
def capture_image():
    # Configure for stills
    picam2.configure(picam2.create_still_configuration())
    picam2.start()
    
    # Capture to an in-memory buffer
    stream = io.BytesIO()
    picam2.capture_file(stream, format='jpeg')
    
    picam2.stop()
    stream.seek(0)
    
    return StreamingResponse(stream, media_type="image/jpeg")

@app.get("/video")
def video_stream():
    """
    Returns an MJPEG (motion JPEG) stream of live video.
    Open this URL in a browser or a compatible viewer to see the stream.
    """
    # Configure for video. We'll force RGB888 so we avoid RGBA frames
    video_config = picam2.create_video_configuration(
        main={"size": (1280, 720), "format": "RGB888"}
    )
    picam2.configure(video_config)
    picam2.start()

    def frame_generator():
        """
        Capture frames in a loop, encode them as JPEG,
        and yield in multipart/x-mixed-replace format.
        """
        try:
            while True:
                # Capture an RGB frame as a numpy array
                frame = picam2.capture_array()

                # Convert the array to a Pillow image
                img = Image.fromarray(frame)

                # (Optional) .convert("RGB") is only needed if you're unsure about the format
                # but with "RGB888" specified, it's already 3-channel RGB.
                # Keeping it for safety if you change the config later:
                img = img.convert("RGB")

                # Save to an in-memory buffer
                buf = io.BytesIO()
                img.save(buf, format='JPEG')
                buf.seek(0)

                # Construct and yield the multipart frame
                yield (b"--frame\r\n"
                       b"Content-Type: image/jpeg\r\n\r\n" +
                       buf.read() +
                       b"\r\n")

                # Throttle slightly if you want to avoid maxing out CPU
                time.sleep(0.02)  # ~50 FPS
        finally:
            # If the client disconnects or the generator ends, stop the camera
            picam2.stop()

    # Return a streaming response of frames
    return StreamingResponse(frame_generator(),
                            media_type="multipart/x-mixed-replace; boundary=frame")
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)