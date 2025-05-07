# AutoTrust Computer Vision Tool - Overview

AutoTrust is a Streamlit-based application for computer vision tasks, featuring image capture, annotation, and object detection capabilities. The application uses the NanoDet model for inference and provides a user-friendly interface for creating, labeling, and analyzing images.

## Key Features

- **Image Capture**: Built-in webcam integration for capturing images
- **Annotation**: Interactive polygon zone creation for region-based detection
- **Object Detection**: Real-time detection using the lightweight NanoDet model
- **Analysis**: Metrics and counting of objects within defined regions
- **User-Friendly Interface**: Streamlit-powered UI with intuitive workflow

AutoTrust is designed for applications requiring zone-based object detection and counting, such as retail analytics, traffic monitoring, and industrial inspection.

## Project Structure

```
autotrust_streamlit/
├── app.py                  # Main application entry point
├── assets/                 # Static assets
│   └── nanodet.mnn         # NanoDet machine learning model
├── pages/                  # Multi-page application screens
│   ├── 1_capture.py        # Camera capture functionality
│   ├── 2_label.py          # Image labeling and annotation
│   └── 3_inference.py      # Object detection and inference
├── utils/                  # Utility modules
│   ├── classes.py          # Class labels for detection
│   ├── nanodet.py          # NanoDet model implementation
│   └── signal.py           # Signal processing utilities
└── requirements.txt        # Project dependencies

```

### Component Interaction

AutoTrust follows a sequential workflow with three main components:

1. **Image Capture Module**: Interfaces with camera hardware to obtain input images
2. **Annotation Module**: Processes captured images to define regions of interest
3. **Inference Module**: Applies object detection and provides analytical results

Data flows through the application using Streamlit's session state, allowing seamless transition between components while maintaining application state.

### Technology Stack

- **Frontend**: Streamlit web interface
- **Computer Vision**: OpenCV for image processing
- **Machine Learning**: NanoDet model with MNN framework
- **Annotation**: Supervision library for polygon zone management
- **Data Processing**: NumPy for numerical operations

## System Requirements

- Python 3.7+
- Webcam or camera device
- 4GB RAM minimum (8GB recommended)
- 500MB disk space

### Dependencies

AutoTrust relies on the following main dependencies:

- Streamlit: Web application framework
- OpenCV: Computer vision processing
- NumPy: Numerical computing
- MNN: Model inference
- Supervision: Annotation and visualization tools
- Pillow: Image processing

## Standard Installation

1. Clone the repository:

```bash
git clone https://github.com/your-repo/autotrust_streamlit.git

```

1. Navigate to the project directory:

```bash
cd autotrust_streamlit

```

1. Install dependencies:

```bash
pip install -r requirements.txt

```

1. Run the application:

```bash
streamlit run app.py

```

The application will start and open in your default web browser.

### Verifying Installation

After starting the application, you should see:

1. The AutoTrust title and welcome screen
2. Navigation options for Capture, Label, and Inference
3. Camera device detection (if available)

If any of these elements are missing, check the console output for error messages.

## Key Components

### 1. Main Application (app.py)

The main entry point serves as a controller for the entire application:

- Initializes Streamlit interface with application title and theme
- Sets up global session state for data sharing between pages
- Configures page layout and navigation
- Handles application-wide settings and state management

### 2. Pages

#### Camera Capture (1_capture.py)

Provides the interface for image acquisition:

- Detects and lists available camera devices
- Creates a real-time webcam preview
- Manages camera state (on/off) and resource allocation
- Captures and saves images to temporary storage
- Includes UI controls for retaking and proceeding to labeling
- Validates image capture before allowing progression

#### Image Labeling (2_label.py)

Enables creation of regions of interest through polygon annotation:

- Displays captured images for annotation
- Links to external polygon creation tool (PolygonZone)
- Accepts and validates polygon coordinates
- Visualizes polygons on the image with appropriate styling
- Provides options to save labels and export labeled images
- Stores polygon data in session state for use in inference
- Includes polygon editing and deletion capabilities

#### Object Detection (3_inference.py)

Performs the core computer vision tasks:

- Loads and applies the NanoDet model for object detection
- Applies saved polygon zones from the labeling page
- Performs inference on captured images
- Counts objects within defined polygon zones
- Provides metrics and visualization of detection results
- Includes controls for confidence threshold and class filtering
- Allows for result exporting and sharing

### 3. Utilities

#### Class Labels (utils/classes.py)

Manages object classification:

- Contains list of 80 object class labels (COCO dataset format)
- Provides helper functions to convert between label names and indices
- Supports filtering and selection of specific object classes
- Includes color mapping for visualization

#### NanoDet Implementation (utils/nanodet.py)

Handles the machine learning model:

- Implements the NanoDetPredictor class for object detection
- Handles model loading, preprocessing, inference and postprocessing
- Uses MNN framework for efficient model execution
- Includes optimized detection pipeline with result formatting
- Provides confidence scoring and non-maximum suppression
- Supports customizable detection parameters

#### Signal Processing (utils/signal.py)

Reserved for future signal processing extensions.

## Application Workflow

AutoTrust follows a three-stage workflow designed for intuitive progression from image capture to analysis.

### 1. Capture Stage

The first step in the workflow involves acquiring an image for processing:

1. User navigates to the Capture page
2. System detects available camera devices
3. User selects a camera from the dropdown menu
4. Camera preview activates, showing real-time feed
5. User clicks "Capture" to freeze the current frame
6. Preview shows the captured image with options to retake or proceed
7. Captured image is stored in session state for the next stage

**Key Technical Point:** Images are captured at native resolution and temporarily stored in memory to preserve quality for detection tasks.

### 2. Labeling Stage

Once an image is captured, the user proceeds to define regions of interest:

1. User navigates to or is automatically directed to the Label page
2. Captured image is displayed for annotation
3. User creates polygon zones by:
    - Clicking points on the image to define vertices
    - Entering coordinate pairs manually
    - Importing from a previous configuration
4. System validates polygon geometry (closed shape, minimum points)
5. User can create multiple zones with different names and colors
6. Polygons are visualized on the image for confirmation
7. User can edit, delete, or add polygons as needed
8. Polygon definitions are stored in session state for the next stage

**Key Technical Point:** Polygon zones use the Supervision library format and are stored as structured data with coordinates, names, and color attributes and use Roboflow for labeling.

### 3. Inference Stage

The final stage applies object detection within the defined regions:

1. User navigates to the Inference page
2. System loads the NanoDet model and prepares for detection
3. Captured image with polygon overlays is displayed
4. User can adjust:
    - Confidence threshold for detection
    - Class filters to include specific objects
    - Display options for visualization
5. System performs detection, identifying objects in the image
6. Objects within each polygon zone are counted
7. Results are displayed with:
    - Visual markers for detected objects
    - Count metrics per zone
    - Confidence scores
8. User can export results as images or data

**Key Technical Point:** Detection applies to the entire image, but counting metrics are calculated only for objects within polygon zones, allowing for region-specific analysis.

### Data Flow Between Stages

- Captured image is maintained in `st.session_state["image"]`
- Polygon definitions are stored in `st.session_state["polygons"]`
- Detection settings preserved in `st.session_state["detection_settings"]`
- Results available in `st.session_state["detection_results"]`

This session state management allows users to revisit previous stages without losing data or configurations.

## Technical Details

### NanoDet Model

AutoTrust uses NanoDet, a lightweight and efficient object detection model:

- **Architecture**: Single-stage anchor-free object detector
- **Input size**: 416x416 pixels (resized from source image)
- **Backbone**: ShuffleNetV2 for feature extraction
- **Head**: Simple convolutional head for classification and regression
- **Output**: 80 object classes (COCO dataset)
- **Model Format**: MNN for cross-platform inference
- **Performance**:
    - ~15-20ms inference time on modern CPU
    - ~5-10ms on GPU-enabled systems
    - mAP of approximately 23% on COCO dataset

#### Inference Pipeline

1. Image preprocessing:
    - Resize to 416x416
    - Normalize pixel values
    - Convert to float32
    - Channel ordering (RGB)
2. Model inference:
    - Forward pass through MNN framework
    - Output includes classification scores and bounding box coordinates
3. Post-processing:
    - Decode grid outputs to box coordinates
    - Apply softmax to class probabilities
    - Filter by confidence threshold
    - Apply non-maximum suppression (NMS)
    - Convert to absolute pixel coordinates

### Polygon Zone Detection

The zone-based detection system uses the Supervision library:

- **Zone Definition**: Polygons defined by vertex coordinates
- **Format**: List of (x, y) coordinate pairs
- **Validation**: Ensures closed polygons with minimum 3 vertices
- **Zone Types**: Supports multiple zones with unique identifiers
- **Containment Testing**: Point-in-polygon algorithm for object counting
- **Visualization**: Custom rendering with configurable colors and labels

#### Object Counting Logic

1. Detect all objects in the image
2. For each detected object:
    - Calculate center point (midpoint of bounding box)
    - Test point containment in each polygon zone
    - Increment zone counter if contained
    - Apply class filtering if specified
3. Generate per-zone metrics:
    - Total object count
    - Class-specific counts
    - Confidence statistics

### Camera Management

The camera interface is built with OpenCV and Streamlit components:

- **Device Detection**: Automatically scans system for camera devices
- **Preview Stream**: Real-time video feed with configurable resolution
- **Capture Process**: Frame grabbing with optional processing
- **Resource Management**: Proper camera initialization and release
- **Error Handling**: Graceful handling of camera access issues
- **Platform Support**: Compatible with Windows, macOS, and Linux

### Session State Management

AutoTrust uses Streamlit's session state to maintain application state:

- **Image Storage**: Captured images stored in memory as numpy arrays
- **Configuration Persistence**: Settings maintained between page navigation
- **Data Sharing**: Common data structures accessible across components
- **State Restoration**: Allows revisiting previous stages without data loss

## API Reference

### NanoDetPredictor Class

The core class for object detection functionality located in `utils/nanodet.py`.

### Constructor

```python
def __init__(self, model_path, input_shape=(416, 416), num_classes=80):
    """
    Initialize NanoDet predictor.

    Args:
        model_path (str): Path to the MNN model file
        input_shape (tuple): Model input dimensions (height, width)
        num_classes (int): Number of object classes (80 for COCO)
    """

```

### Methods

### predict

```python
def predict(self, image, conf_threshold=0.35, nms_threshold=0.6):
    """
    Perform object detection on an image.

    Args:
        image (numpy.ndarray): Input image in BGR format
        conf_threshold (float): Confidence threshold for filtering detections
        nms_threshold (float): IoU threshold for non-maximum suppression

    Returns:
        list: List of detection results in format [x1, y1, x2, y2, score, class_id]
    """

```

### preprocess

```python
def preprocess(self, image):
    """
    Preprocess image for model input.

    Args:
        image (numpy.ndarray): Input image in BGR format

    Returns:
        numpy.ndarray: Preprocessed image tensor
    """

```

### post-process

```python
def postprocess(self, outputs, conf_threshold, nms_threshold):
    """
    Process raw model outputs to detection results.

    Args:
        outputs (list): Raw model output tensors
        conf_threshold (float): Confidence threshold for filtering
        nms_threshold (float): IoU threshold for NMS

    Returns:
        list: Processed detection results
    """

```

## Session State Variables

AutoTrust uses the following key session state variables:

| Variable | Type | Description |
| --- | --- | --- |
| `st.session_state["image"]` | numpy.ndarray | Captured image in BGR format |
| `st.session_state["image_rgb"]` | numpy.ndarray | Captured image in RGB format for display |
| `st.session_state["camera_id"]` | int | Selected camera device ID |
| `st.session_state["camera_on"]` | bool | Camera state flag |
| `st.session_state["polygons"]` | list | List of polygon definitions |
| `st.session_state["detection_results"]` | dict | Object detection results |
| `st.session_state["conf_threshold"]` | float | Confidence threshold setting |
| `st.session_state["selected_classes"]` | list | Filtered object classes |

## Polygon Zone API

Functions for working with polygon zones:

```python
def create_polygon_zone(points, zone_id, color):
    """
    Create a polygon zone from points.

    Args:
        points (list): List of (x, y) coordinate pairs
        zone_id (str): Unique identifier for the zone
        color (tuple): RGB color for visualization

    Returns:
        supervision.PolygonZone: Zone object
    """

```

```python
def count_objects_in_zones(detections, zones):
    """
    Count objects in each polygon zone.

    Args:
        detections (supervision.Detections): Detection results
        zones (list): List of polygon zone objects

    Returns:
        dict: Counts per zone
    """

```

## Camera Management API

Functions for camera control:

```python
def get_available_cameras():
    """
    Detect available camera devices.

    Returns:
        list: List of camera device IDs
    """

```

```python
def initialize_camera(camera_id):
    """
    Initialize camera with given ID.

    Args:
        camera_id (int): Camera device ID

    Returns:
        cv2.VideoCapture: Camera object
    """

```

## Deployment Considerations

## System Requirements

### Minimum Requirements

- **CPU**: Dual-core 2GHz or higher
- **RAM**: 4GB
- **Disk Space**: 500MB for application and dependencies
- **Camera**: Any compatible webcam or camera device
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+

### Recommended Requirements

- **CPU**: Quad-core 2.5GHz or higher
- **RAM**: 8GB
- **GPU**: Any CUDA-compatible GPU (for faster inference)
- **Camera**: HD webcam (1080p) for better detection quality
- **OS**: Windows 11, macOS 12+, Ubuntu 20.04+

## Deployment Options

### Local Deployment

Standard local deployment as a Streamlit application:

```bash
streamlit run app.py

```

This approach is suitable for:

- Individual use
- Development and testing
- Small-scale deployments

### Server Deployment

For multi-user access, deploy as a Streamlit application on a server:

1. Set up a virtual environment on the server
2. Install dependencies
3. Run with specific server options:

```bash
streamlit run app.py --server.port=8501 --server.address=0.0.0.0

```

1. Set up a reverse proxy (Nginx, Apache) for production use

### Docker Deployment

For containerized deployment:

1. Create a Dockerfile:

```
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

```

1. Build and run the container:

```bash
docker build -t autotrust .
docker run -p 8501:8501 autotrust

```

### Performance Optimization

#### Camera Feed Optimization

- Reduce resolution for preview (maintain full resolution for capture)
- Decrease frame rate for preview
- Consider using MJPEG compression for network deployments

#### Model Optimization

- Use quantized model for faster inference
- Batch processing for multiple images
- GPU acceleration where available

#### Memory Management

- Clear session state for unused variables
- Use streaming for large datasets
- Implement proper garbage collection

### Network Considerations

For multi-user or remote deployments:

- Ensure sufficient bandwidth for camera streams (≥5 Mbps per stream)
- Configure appropriate timeouts for long-running operations
- Implement authentication for sensitive deployments
- Consider WebRTC for low-latency camera feeds in distributed setups

### Security Considerations

- Camera access requires appropriate permissions
- Secure stored images and detection results
- Implement user authentication for multi-user deployments
- Consider data privacy implications when storing captured images

## Troubleshooting

## Camera Issues

### No Cameras Detected

**Symptoms:**

- Empty camera selection dropdown
- "No camera devices found" error message

**Possible Causes:**

- Camera not connected or powered
- Camera drivers not installed
- Camera in use by another application
- Permission issues

**Solutions:**

1. Check physical camera connection
2. Verify camera works in other applications
3. Close other applications using the camera
4. Check system permissions:
    - Windows: Allow camera access in Privacy settings
    - macOS: Allow camera access in Security & Privacy
    - Linux: Check user permissions for /dev/video*

### Camera Feed Not Displaying

**Symptoms:**

- Camera selected but no preview appears
- Black screen in preview area

**Possible Causes:**

- Camera initialization failure
- Incorrect camera ID
- Camera format incompatibility

**Solutions:**

1. Try selecting a different camera
2. Restart the application
3. Check camera properties:

```python
# Debug camera properties
cap = cv2.VideoCapture(camera_id)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"Camera resolution: {width}x{height}")
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Camera FPS: {fps}")
cap.release()

```

## Model Loading Issues

### Model Not Found

**Symptoms:**

- "Model file not found" error
- Inference page fails to load

**Possible Causes:**

- Missing model file in assets directory
- Incorrect model path
- Permission issues

**Solutions:**

1. Verify model file exists at `assets/nanodet.mnn`
2. Check file permissions
3. Re-download model file if necessary

### Inference Errors

**Symptoms:**

- "Error during inference" message
- Exception in console output

**Possible Causes:**

- Model format incompatibility
- Input preprocessing error
- MNN version mismatch

**Solutions:**

1. Check MNN version compatibility
2. Verify input image format and dimensions
3. Try different confidence threshold values
4. Check console for specific error messages

## Polygon Zone Issues

### Invalid Polygon Error

**Symptoms:**

- "Invalid polygon" error when saving
- Polygon not displaying correctly

**Possible Causes:**

- Too few points (minimum 3 required)
- Self-intersecting polygon
- Invalid coordinate format

**Solutions:**

1. Ensure polygon has at least 3 points
2. Check for self-intersections
3. Verify coordinate format (x,y pairs)
4. Try simplifying complex polygons

### Object Counting Inaccuracies

**Symptoms:**

- Objects visible but not counted
- Incorrect counts in zone metrics

**Possible Causes:**

- Object center point outside zone
- Confidence threshold too high
- Class filtering excluding objects

**Solutions:**

1. Adjust confidence threshold
2. Expand polygon zone boundaries
3. Check class filters
4. Verify detection algorithm:

```python
# Debug zone containment
for detection in detections:
    center_x = (detection[0] + detection[2]) / 2
    center_y = (detection[1] + detection[3]) / 2
    print(f"Object center: ({center_x}, {center_y})")
    for zone in zones:
        contained = zone.contains_point((center_x, center_y))
        print(f"Contained in {zone.id}: {contained}")

```

## Performance Issues

### Slow Application Startup

**Symptoms:**

- Application takes >30 seconds to start
- High CPU usage during startup

**Possible Causes:**

- Model loading overhead
- Resource contention
- Dependency initialization

**Solutions:**

1. Check system resource usage
2. Implement lazy loading for models
3. Optimize import statements

### Laggy Camera Preview

**Symptoms:**

- Camera preview stutters or freezes
- High latency in display

**Possible Causes:**

- High resolution camera feed
- CPU bottleneck
- Memory constraints

**Solutions:**

1. Reduce preview resolution
2. Lower frame rate
3. Implement frame skipping
4. Close other resource-intensive applications