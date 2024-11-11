import cv2
import mediapipe as mp
import time

mp_objectron = mp.solutions.objectron
mp_drawing = mp.solutions.drawing_utils

# Set up video capture and video writer
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object to save the output
output_filename = '3D_output.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_filename, fourcc, 20.0, (frame_width, frame_height))

with mp_objectron.Objectron(static_image_mode=False, max_num_objects=2, min_detection_confidence=0.5,
                            min_tracking_confidence=0.5, model_name='Cup') as objectron:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        start = time.time()

        # Convert the image color to RGB for MediaPipe
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = objectron.process(image)

        # Convert back to BGR for OpenCV
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw the detected objects and landmarks
        if results.detected_objects:
            for detected_object in results.detected_objects:
                mp_drawing.draw_landmarks(image, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
                mp_drawing.draw_axis(image, detected_object.rotation, detected_object.translation)

        end = time.time()
        totaltime = end - start
        fps = 1 / totaltime

        # Display FPS on the image
        cv2.putText(image, f'fps: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

        # Show the output frame
        cv2.imshow('MediaPipe Objectron', image)

        # Write the frame to the output file
        out.write(image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
