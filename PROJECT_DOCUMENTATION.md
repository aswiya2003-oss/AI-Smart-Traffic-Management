# Project Documentation: AI Smart Traffic Management System

## Abstract
This project demonstrates an AI-assisted traffic video analysis prototype. A pretrained YOLO object-detection model identifies common vehicle categories in uploaded footage. OpenCV reads and annotates video frames, while Streamlit provides the user interface. The system estimates traffic density, calculates an illustrative green-signal duration, and exports analysis reports.

## Problem statement
Manual traffic observation is time-consuming and can be inconsistent. This prototype explores how computer vision can support traffic-volume observation and reporting.

## Objectives
1. Detect cars, motorcycles, buses and trucks.
2. Track vehicle detections across video frames.
3. Summarize traffic volume and density.
4. Generate illustrative signal-time recommendations.
5. Export annotated video and PDF/CSV reports.

## Technologies
- Python 3.11
- Streamlit
- Ultralytics YOLO pretrained weights
- OpenCV
- Pandas
- ReportLab

## Methodology
1. User uploads a supported traffic video.
2. OpenCV decodes the video into frames.
3. YOLO detects selected vehicle classes and tracking is enabled.
4. The app records periodic vehicle counts and annotates frames.
5. Counts are mapped to density categories: 0–5 Low, 6–15 Medium, above 15 High.
6. A simulated green-time recommendation is calculated as `min(60, max(15, 15 + 2 * count))` seconds.
7. The user downloads the annotated video and reports.

## System architecture
User -> Streamlit UI -> OpenCV video reader -> YOLO detector/tracker -> Traffic statistics -> PDF/CSV exporter -> User downloads

## Limitations
- Results depend on camera angle, lighting, occlusion, video quality and model performance.
- Density thresholds are simple demonstration thresholds and should be calibrated for each road.
- This version analyzes uploaded videos; a live-camera production implementation needs secure camera access and robust deployment infrastructure.
- Signal timing is illustrative only and must never directly control public-road signals.

## Testing and evaluation
Record the test video source, resolution, duration, hardware and model version. Use manually labeled frames to calculate precision, recall and F1-score. Compare automated vehicle counts against manual counts using MAE. Measure processing FPS. Include actual application screenshots and measured results in the final submission; do not fabricate results.

## Future enhancements
- Multi-lane and intersection-specific analysis
- Pedestrian and emergency-vehicle detection
- Lane-wise vehicle counting and queue-length estimation
- Historical dashboards and database storage
- Edge-device deployment and authority-approved signal integration
