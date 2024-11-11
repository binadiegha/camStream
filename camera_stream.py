import cv2
import asyncio
import websockets
import base64

async def video_stream(websocket, path):
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Encode frame to JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            # Encode to base64
            frame_data = base64.b64encode(buffer).decode('utf-8')
            # Send frame over WebSocket
            await websocket.send(frame_data)

    finally:
        cap.release()

# Start WebSocket server
start_server = websockets.serve(video_stream, '0.0.0.0', 8082)
print("WebSocket server started on ws://0.0.0.0:8082")

# Run the server and start sockets stream
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
