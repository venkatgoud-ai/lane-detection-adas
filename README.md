# Lane Detection System 🚗

Real-time lane detection system built with Python and OpenCV as part of an ADAS (Advanced Driver Assistance Systems) engineering portfolio.

## Demo
*Demo GIF coming soon*

## What it does
- Detects left and right lane markings from dashcam video in real time
- Extrapolates full-length lane lines using slope-intercept mathematics
- Fills the detected lane with a transparent green overlay
- Handles dashed lane markings using temporal smoothing (last known good line memory)
- Processes 1280x720 video using a 6-step computer vision pipeline

## Pipeline
Raw Frame → Grayscale → Gaussian Blur → Canny Edges → Mask → Hough Lines → Draw

## Technologies
- Python 3.14
- OpenCV 4.13
- NumPy

## How to Run

**Install dependencies:**
```bash
pip install opencv-python numpy
```

**Run:**
```bash
python lane.py
```
Press `Escape` to stop.

## How it works

### 1. Grayscale Conversion
Converts the colour frame to grayscale — edge detection works on brightness not colour.

### 2. Gaussian Blur
Smooths the image to remove random pixel noise — prevents false edge detection from road texture.

### 3. Canny Edge Detection
Detects pixels where brightness changes suddenly — lane markings on dark road produce strong edges.

### 4. Region of Interest Masking
A trapezoid mask isolates the road area — removes sky, trees, and surroundings from edge detection.

### 5. Hough Line Detection
Finds straight lines from edge pixels using the Hough Transform. Lines are separated into left/right using slope:
- Negative slope → left lane line
- Positive slope → right lane line

### 6. Line Extrapolation
Averages all detected line segments into one representative line per side using slope-intercept math, then extends from bottom of frame to horizon.

## Challenges Faced
- **Hood detection** — car hood was inside the mask area, solved by blocking the bottom portion of the frame
- **Dashed lane flickering** — lines disappeared in gaps between dashes, solved by storing last known good detection
- **False edges** — road texture produced noise, solved by tuning Canny thresholds to (120, 240)
- **Lines converging** — extrapolated lines met at vanishing point, solved by enforcing minimum width at top

## Known Limitations
- Fails on sharp curves — assumes straight lane lines
- Struggles in low light and rain
- Polygon coordinates are tuned for this specific video and camera angle

## Documentation
Full project documentation including technical concepts, problems faced, and solutions is available in `Lane_Detection_Documentation.docx`