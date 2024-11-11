import cv2
from collections import defaultdict

object_classes = ['person', 'chair', 'bottle', 'laptop', 'car']
frame_object_counts = defaultdict(int)

def update_object_counts(results):
    
    global frame_object_counts
    frame_object_counts.clear()  
    for _, row in results.iterrows():
        if row['name'] in object_classes:
            frame_object_counts[row['name']] += 1


def display_counts(frame):
    global frame_object_counts
    y_offset = 50  # Starting Y position for text

    for obj_class, count in frame_object_counts.items():
        # Define the text to be displayed
        text = f"{obj_class}: {count}"

        # Font settings
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 0.7
        text_thickness = 1
        text_color = (255, 255, 255)  # White text color
        bg_color = (0, 0, 0)          # Black background

        # Get text size for background rectangle
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, text_thickness)
        
        # Define top-left and bottom-right points for the background rectangle
        top_left = (10, y_offset - text_height -5 )
        bottom_right = (10 + text_width + 10, y_offset + 5)

        # Draw the background rectangle
        cv2.rectangle(frame, top_left, bottom_right, bg_color, -1)  # -1 fills the rectangle

        # Overlay the text on top of the rectangle
        cv2.putText(frame, text, (10, y_offset), font, font_scale, text_color, text_thickness, lineType=cv2.LINE_AA)

        # Update the y_offset for the next line of text
        y_offset += text_height + 15  # Adjust for next line, leaving space between entries