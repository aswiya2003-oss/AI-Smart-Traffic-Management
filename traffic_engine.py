from pathlib import Path
import cv2
from ultralytics import YOLO

VEHICLE_CLASSES = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}

def density_for(count):
    if count <= 5:
        return "Low"
    if count <= 15:
        return "Medium"
    return "High"

def suggested_green_seconds(count):
    return max(15, min(60, 15 + 2 * int(count)))

def analyze_video(input_path, model_name="yolo11n.pt", confidence=0.35):
    model = YOLO(model_name)
    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        raise ValueError("OpenCV could not open the uploaded video.")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if width <= 0 or height <= 0:
        cap.release()
        raise ValueError("The uploaded video has invalid dimensions.")

    output_path = str(Path(input_path).with_name("annotated_traffic.mp4"))
    writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    if not writer.isOpened():
        cap.release()
        raise RuntimeError("Could not create annotated MP4 output.")

    timeline = []
    frame_index = 0
    peak_count = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            results = model.track(frame, persist=True, classes=list(VEHICLE_CLASSES),
                                  conf=confidence, verbose=False)
            result = results[0]
            count = 0
            if result.boxes is not None:
                count = len(result.boxes)
            peak_count = max(peak_count, count)
            annotated = result.plot()
            writer.write(annotated)
            if frame_index % max(1, int(fps)) == 0:
                seconds = round(frame_index / fps, 1)
                timeline.append({
                    "time_seconds": seconds,
                    "vehicle_count": count,
                    "density": density_for(count),
                    "suggested_green_seconds": suggested_green_seconds(count)
                })
            frame_index += 1
    finally:
        cap.release()
        writer.release()

    if frame_index == 0:
        raise ValueError("No readable frames were found in the uploaded video.")

    density = density_for(peak_count)
    return {
        "video_path": output_path,
        "peak_count": peak_count,
        "density": density,
        "green_seconds": suggested_green_seconds(peak_count),
        "timeline": timeline,
        "frames_processed": frame_index,
        "model": model_name
    }
