import cv2
import pandas as pd
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Path to the video file
video_path = 'your_movie.mp4'

# Initialize variables
data = []
scale_factor = 1.0
frame_delay = 30  # Initial frame delay in ms (approx. 30 FPS)
rewind_seconds = 5  # Rewind duration in seconds
skip_forward_seconds = 5  # Forward skip duration in seconds
sections = ["Experiment_I", "Experiment_II", "Experiment_III"]  # Predefined sections
section_index = 0  # Current section index
section_name = sections[section_index]
v_flow_levels = [15, 20, 25]  # Predefined v_flow levels
v_flow_index = 0
v_flow_name = v_flow_levels[v_flow_index]
run_number = 1
is_paused = False
is_replaying = False
frame_rate_display = ""  # For displaying frame rate change
output_folder = "output_data"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Function to update the section name based on index
def update_section():
    global section_name, run_number
    section_name = sections[section_index]
    run_number = 1  # Reset run number for new section
    print(f"Current Section: {section_name}")

# Function to update the v_flow name based on index
def update_v_flow():
    global v_flow_name, run_number
    v_flow_name = v_flow_levels[v_flow_index]
    run_number = 1  # Reset run number for new v_flow
    print(f"Current v_flow level: {v_flow_name}")

# Mouse callback function to record click coordinates and timestamp
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and not is_paused:
        # Get current timestamp (in seconds)
        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

        # Record the point and timestamp
        data.append({
            'section': section_name,
            'v_flow': v_flow_name,
            'run': f'Run_{run_number}',
            'x': x,
            'y': y,
            'timestamp': timestamp
        })

        # Display point info on the frame
        cv2.circle(display_frame, (x, y), 5, (0, 255, 0), -1)
        cv2.putText(display_frame, f'({x},{y}) @ {timestamp:.2f}s', (x + 5, y + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

# Function to save the current section's data with a unique filename
def save_data():
    global data, section_name, v_flow_name, run_number
    if data:
        # Create a unique filename using section name, v_flow level, run number, and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(output_folder, f'{section_name}_{v_flow_name}_Run_{run_number}_{timestamp}.csv')
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
        data.clear()  # Clear data for the next run

# Slider callback to control the zoom level
def update_scale(val):
    global scale_factor
    scale_factor = max(val / 10, 0.5)  # Scale between 0.5 and 3.0

# Function to rewind the video by a set number of seconds
def rewind_video():
    current_pos = cap.get(cv2.CAP_PROP_POS_MSEC)
    new_pos = max(current_pos - rewind_seconds * 1000, 0)  # Rewind by `rewind_seconds`, min 0
    cap.set(cv2.CAP_PROP_POS_MSEC, new_pos)

# Function to skip forward in the video by a set number of seconds
def skip_forward_video():
    current_pos = cap.get(cv2.CAP_PROP_POS_MSEC)
    video_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS) * 1000
    new_pos = min(current_pos + skip_forward_seconds * 1000, video_duration)
    cap.set(cv2.CAP_PROP_POS_MSEC, new_pos)

def skip_forward_video(val):
    current_pos = cap.get(cv2.CAP_PROP_POS_MSEC)
    video_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS) * 1000
    new_pos = min(current_pos + skip_forward_seconds * 1000 * val, video_duration)
    cap.set(cv2.CAP_PROP_POS_MSEC, new_pos)

# Function to replay marked points sequentially
def replay_marked_points():
    global is_replaying
    is_replaying = True
    for entry in data:
        cap.set(cv2.CAP_PROP_POS_MSEC, entry['timestamp'] * 1000)  # Set to specific timestamp
        ret, frame = cap.read()
        if not ret:
            break
        display_frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
        cv2.circle(display_frame, (entry['x'], entry['y']), 5, (0, 0, 255), -1)
        cv2.putText(display_frame, f"Replay ({entry['x']},{entry['y']}) @ {entry['timestamp']:.2f}s",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        cv2.imshow("Video", display_frame)
        if cv2.waitKey(frame_delay) & 0xFF == ord('q'):
            break
    is_replaying = False

# Open video file
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Create a window and set the mouse callback
cv2.namedWindow("Video")
cv2.setMouseCallback("Video", click_event)

# Add a slider to control scale
cv2.createTrackbar("Zoom", "Video", int(scale_factor * 10), 30, update_scale)

# Main loop to handle video playback and user input
while True:
    if not is_paused and not is_replaying:
        ret, frame = cap.read()
        if not ret:
            # End of video: prompt user to save any remaining data
            if messagebox.askyesno("Video Ended", "The video has ended. Would you like to save the current data?"):
                save_data()
            break  # Exit loop if video ends

        # Resize the frame according to the scale factor
        display_frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

        # Display current video time on the frame
        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Convert milliseconds to seconds
        cv2.putText(display_frame, f'Time: {current_time:.2f}s', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        # Display the last 10 points and timestamps
        y_offset = 90
        for i, entry in enumerate(data[-10:]):
            text = f"({entry['x']},{entry['y']}) @ {entry['timestamp']:.2f}s"
            cv2.putText(display_frame, text, (10, y_offset + (i * 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Display the current frame rate
        if frame_rate_display:
            cv2.putText(display_frame, frame_rate_display, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Show the frame with updated information
    cv2.imshow("Video", display_frame)

    # Keyboard controls
    key = cv2.waitKey(frame_delay) & 0xFF

    if key == ord('q'):  # Quit
        break
    elif key == ord('+'):  # Increase zoom (alternative to slider)
        scale_factor = min(scale_factor + 0.1, 3.0)
        cv2.setTrackbarPos("Zoom", "Video", int(scale_factor * 10))
    elif key == ord('-'):  # Decrease zoom (alternative to slider)
        scale_factor = max(scale_factor - 0.1, 0.5)
        cv2.setTrackbarPos("Zoom", "Video", int(scale_factor * 10))
    elif key == ord('['):  # Slow down
        frame_delay = min(frame_delay + 10, 200)
        frame_rate_display = f"Frame Delay: {frame_delay} ms"
    elif key == ord(']'):  # Speed up
        frame_delay = max(frame_delay - 10, 10)
        frame_rate_display = f"Frame Delay: {frame_delay} ms"
    elif key == ord('p'):  # Play/pause toggle
        is_paused = not is_paused
    elif key == ord('r'):  # Rewind the video
        rewind_video()
    elif key == ord('e'):
        skip_forward_video(-60)
    elif key == ord('f'):  # Forward skip the video
        skip_forward_video(1)
    elif key == ord('g'):
        skip_forward_video(60)
    elif key == ord('v'):  # Replay marked points
        replay_marked_points()

    # Group for run_number
    elif key == ord('n'):  # New run within the current section
        save_data()  # Save current data
        run_number += 1  # Increment run number
        print('run_number: ', run_number)
    elif key == ord('s'):  # Go up for run_number
        run_number += 1  # Increment run number
        print('run_number: ', run_number)
    elif key == ord('x'):  # Go down for run_number
        run_number -= 1  # Decrement run number
        print('run_number: ', run_number)


    # Group for v_flow_index
    elif key == ord('b'):  # Cycle to the next v_flow level and reset run number
        save_data()  # Save current data
        v_flow_index = (v_flow_index + 1) % len(v_flow_levels)
        update_v_flow()  # Update v_flow level and reset run number
        print('v_flow_index: ', v_flow_index)
    elif key == ord('a'):  # Go up for v_flow_index
        v_flow_index = (v_flow_index + 1) % len(v_flow_levels)
        update_v_flow()  # Update v_flow level and reset run number
        print('v_flow_index: ', v_flow_index)
    elif key == ord('z'):  # Go down for v_flow_index
        v_flow_index = (v_flow_index - 1) % len(v_flow_levels)
        update_v_flow()  # Update v_flow level and reset run number
        print('v_flow_index: ', v_flow_index)

    # Group for section_index
    elif key == ord('m'):  # Move to the next section and reset run number
        save_data()  # Save current data
        section_index = (section_index + 1) % len(sections)
        update_section()  # Update section and reset run number
        print('section_index: ', section_index)
    elif key == ord('d'):  # Go up for section_index
        section_index = (section_index + 1) % len(sections)
        update_section()  # Update section and reset run number
        print('section_index: ', section_index)
    elif key == ord('c'):  # Go down for section_index
        section_index = (section_index - 1) % len(sections)
        update_section()  # Update section and reset run number
        print('section_index: ', section_index)



# Final save of any remaining data
save_data()

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
