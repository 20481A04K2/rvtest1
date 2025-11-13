import os
import cv2
import csv
from pathlib import Path

def create_directories():
    """Create required directories if they don't exist"""
    directories = ['frames', 'predict', 'videos']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created/verified directory: {directory}")

def process_video(video_path, output_frame_dir, output_predict_dir):
    """Extract frames from video and process them"""
    video_name = Path(video_path).stem
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Cannot open video {video_path}")
        return []
    
    frame_count = 0
    processed_frames = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Save every 30th frame (adjust as needed)
        if frame_count % 30 == 0:
            frame_filename = f"{video_name}_frame_{frame_count:04d}.jpg"
            frame_path = os.path.join(output_frame_dir, frame_filename)
            cv2.imwrite(frame_path, frame)
            
            # Create a dummy prediction (replace with your actual model)
            predict_filename = f"{video_name}_predict_{frame_count:04d}.jpg"
            predict_path = os.path.join(output_predict_dir, predict_filename)
            cv2.imwrite(predict_path, frame)  # Placeholder
            
            processed_frames.append({
                'video': video_name,
                'frame': frame_count,
                'frame_path': frame_path,
                'predict_path': predict_path
            })
        
        frame_count += 1
    
    cap.release()
    print(f"Processed {frame_count} frames from {video_name}")
    return processed_frames

def create_inspection_csv(processed_data, output_csv='inspection.csv'):
    """Create inspection CSV file"""
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['video', 'frame', 'frame_path', 'predict_path', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for data in processed_data:
            data['status'] = 'processed'
            writer.writerow(data)
    
    print(f"Created inspection CSV: {output_csv}")

def main():
    print("Starting annotation pipeline...")
    
    # Create directories
    create_directories()
    
    # Process videos
    video_dir = 'videos'
    frame_dir = 'frames'
    predict_dir = 'predict'
    
    all_processed_data = []
    
    # Check if videos directory has any videos
    video_files = list(Path(video_dir).glob('*.mp4')) + list(Path(video_dir).glob('*.avi'))
    
    if not video_files:
        print("No video files found. Creating sample data...")
        # Create dummy data for testing
        all_processed_data.append({
            'video': 'sample_video',
            'frame': 0,
            'frame_path': 'frames/sample_frame.jpg',
            'predict_path': 'predict/sample_predict.jpg'
        })
    else:
        for video_file in video_files:
            processed_data = process_video(
                str(video_file),
                frame_dir,
                predict_dir
            )
            all_processed_data.extend(processed_data)
    
    # Create inspection CSV
    create_inspection_csv(all_processed_data)
    
    print("Annotation pipeline completed successfully!")

if __name__ == "__main__":
    main()
