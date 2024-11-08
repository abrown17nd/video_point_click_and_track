
# Point Marking Program

## Overview
The **Point Marking Program** is a Python-based tool using OpenCV to manually mark points on a video. It saves the coordinates, timestamps, and other metadata to CSV files, organized by experiment sections, `v_flow` levels, and run numbers. This allows for flexible and detailed data analysis.

## Features
1. **Point Marking**: Click on video frames to mark and record `(x, y)` coordinates and timestamps.
2. **Experiment Sections and Runs**: Cycle through predefined experiment sections (e.g., `Experiment_I`, `Experiment_II`) and reset run numbers for each new section.
3. **`v_flow` Levels**: Cycle through predefined `v_flow` levels for each experiment, with run numbers resetting for each new level.
4. **Playback Controls**: Includes zoom, speed adjustments, rewind, forward skip, play/pause, and a replay mode to review marked points.
5. **Filename Structure**: Files are saved with the format:
{{section_name}}{{v_flow_name}}Run{{run_number}}{{timestamp}}.csv

markdown
Copy code

## Key Controls
- `Left Click`: Mark a point on the video.
- `n`: Start a new run within the current section.
- `m`: Move to the next section, resetting run numbers.
- `b`: Cycle to the next `v_flow` level, resetting run numbers.
- `p`: Play/pause the video.
- `+/-`: Zoom in/out.
- `[ / ]`: Slow down / speed up playback.
- `r/f`: Rewind / skip forward.
- `v`: Replay all marked points in order.
- `q`: Quit the program.

## Dependencies
- Python 3
- OpenCV
- Pandas

## How to Run
1. Install dependencies:
```bash
pip install opencv-python pandas
Update the video_path in the code to point to your video file.
Run the program:
bash

python point_marking_program.py
File Naming Convention
Files are saved with the following format:
sql

{{section_name}}_{{v_flow_name}}_Run_{{run_number}}_{{timestamp}}.csv
where timestamp is in YYYYMMDD_HHMMSS format. 