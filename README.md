# AI Smart Traffic Management System

A final-year academic prototype using Python, Streamlit, YOLO and OpenCV to analyze uploaded traffic videos, detect vehicles, estimate traffic density, and export reports.

## Features
- Upload MP4, AVI, MOV or MKV traffic videos
- Detect cars, motorcycles, buses and trucks
- Track detections with YOLO tracking
- Estimate low, medium or high traffic density
- Suggest illustrative green-signal timing
- Download annotated video, CSV and PDF reports

## Windows setup (Python 3.11 recommended)
Open Command Prompt in the project folder and run these commands one at a time:

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open http://localhost:8501 in your browser.

The first analysis may download YOLO model weights, so an internet connection is needed initially.

## GitHub / Streamlit Community Cloud
1. Upload all project files to the repository root.
2. In Streamlit Community Cloud, choose the repository and branch.
3. Set Main file path to `app.py`.
4. Choose Python 3.11 in Advanced settings if offered.
5. Deploy.

Cloud deployments may have resource limits; video processing can be slow or exceed memory limits for large videos.

## Safety and limitations
This project provides academic analysis and simulated signal-time recommendations only. It does not control real traffic lights. Real-world deployment requires validated lane-specific sensing, pedestrian and emergency-vehicle handling, fail-safe design, cybersecurity, regulatory approval and field testing.

## Evaluation
Do not claim accuracy or performance figures without measuring them. Evaluate on a labeled test set and report precision, recall, F1-score, vehicle-count error and processing FPS.
