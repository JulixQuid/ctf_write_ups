import cv2
import numpy as np

# Read and parse coordinates
with open("/home/julixquid/Downloads/mouse_movements.txt", "r") as file:
    lines = file.readlines()

coordinates = []
for line in lines:
    line = line.strip()
    if line:
        x, y = map(int, line.split(","))
        coordinates.append((x, y))

# Create a white image with padding
max_x = max(x for x, y in coordinates) + 100
max_y = max(y for x, y in coordinates) + 100
image = np.ones((max_y, max_x, 3), dtype=np.uint8) * 255  # White

# Draw the path (convert to NumPy array)
points = np.array(coordinates, dtype=np.int32)
cv2.polylines(image, [points], isClosed=False, color=(0, 0, 0), thickness=3)

# Draw red circles
for (x, y) in coordinates:
    cv2.circle(image, (x, y), 5, (0, 0, 255), -1)  # Red dots

# Save and show
cv2.imwrite("output.png", image)
cv2.imshow("Path from File", image)
cv2.waitKey(0)
cv2.destroyAllWindows()