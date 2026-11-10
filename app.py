import streamlit as st
import tempfile
from pathlib import Path
import pandas as pd
from traffic_engine import analyze_video
from reporting import create_pdf_report

st.set_page_config(page_title="AI Smart Traffic Management", page_icon="🚦", layout="wide")
st.title("🚦 AI Smart Traffic Management System")
st.caption("Final-year AI project | Python · Streamlit · YOLO · OpenCV")

with st.sidebar:
    st.header("Settings")
    model_name = st.selectbox("YOLO model", ["yolo11n.pt", "yolov8n.pt"])
    conf = st.slider("Detection confidence", 0.10, 0.90, 0.35, 0.05)
    st.info("The signal timing is a simulation/recommendation only. This app does not control real traffic lights.")

tab_upload, tab_about = st.tabs(["📹 Upload traffic video", "ℹ️ About"])

with tab_upload:
    video = st.file_uploader("Upload a traffic video", type=["mp4", "avi", "mov", "mkv"])
    if video is not None and st.button("Analyze video", type="primary"):
        suffix = Path(video.name).suffix or ".mp4"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(video.getbuffer())
            input_path = tmp.name
        try:
            with st.spinner("Loading YOLO and analyzing video. The first run may download model weights..."):
                result = analyze_video(input_path, model_name, conf)
            st.success("Analysis complete.")
            c1, c2, c3 = st.columns(3)
            c1.metric("Vehicles detected (peak frame)", result["peak_count"])
            c2.metric("Traffic density", result["density"])
            c3.metric("Suggested green time", f'{result["green_seconds"]} sec')
            st.subheader("Annotated video")
            if Path(result["video_path"]).exists():
                st.video(result["video_path"])
                st.download_button("Download annotated video",
                    data=Path(result["video_path"]).read_bytes(),
                    file_name="annotated_traffic.mp4", mime="video/mp4")
            df = pd.DataFrame(result["timeline"])
            st.subheader("Traffic timeline")
            st.dataframe(df, use_container_width=True)
            st.download_button("Download CSV report", df.to_csv(index=False).encode("utf-8"),
                file_name="traffic_analysis.csv", mime="text/csv")
            pdf = create_pdf_report(result)
            st.download_button("Download PDF report", pdf,
                file_name="traffic_analysis_report.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            st.info("Check that the video is readable and that dependencies installed successfully.")
        finally:
            Path(input_path).unlink(missing_ok=True)

with tab_about:
    st.markdown("""
    ### Project objectives
    - Detect common vehicle classes in traffic footage using a pretrained YOLO model.
    - Track detections and estimate traffic volume over time.
    - Classify traffic density as low, medium, or high.
    - Generate a simulated green-signal duration recommendation.
    - Export annotated video and PDF/CSV reports.

    ### Vehicle classes
    Car, motorcycle, bus, and truck.

    ### Important limitation
    This is an academic prototype. Signal recommendations are illustrative and must not be connected
    to public-road traffic controllers without engineering validation, safety interlocks, and
    authorization from the relevant road authority.
    """)
