import cv2
import numpy as np

def convert_video(input_file, output_file):
    # Open input video file
    cap = cv2.VideoCapture(input_file)
    
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Desired YouTube 16:9 resolution (1080p)
    output_width = 1920
    output_height = 1080
    
    # Create output video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (output_width, output_height))
    
    # Processing each frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Calculate padding needed to fit the portrait video into 16:9
        scale = output_height / height
        new_width = int(width * scale)
        
        if new_width > output_width:
            scale = output_width / width
            new_height = int(height * scale)
            resized_frame = cv2.resize(frame, (output_width, new_height))
            padding_top_bottom = (output_height - new_height) // 2
            output_frame = cv2.copyMakeBorder(resized_frame, padding_top_bottom, padding_top_bottom, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        else:
            resized_frame = cv2.resize(frame, (new_width, output_height))
            padding_left_right = (output_width - new_width) // 2
            output_frame = cv2.copyMakeBorder(resized_frame, 0, 0, padding_left_right, padding_left_right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        
        # Write frame to the output file
        out.write(output_frame)
    
    # Release everything
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Conversion complete.")

# Example usage:
input_video_path = "your_tiktok_video.mp4"
output_video_path = "converted_youtube_video.mp4"
convert_video(input_video_path, output_video_path)
