#!/usr/bin/env python3
"""
Example usage of YOLOv5 converter
"""

from convert_yolov5_to_tensorrt import YOLOv5Converter

# Example 1: Basic conversion
def example_basic():
    """Basic conversion example"""
    converter = YOLOv5Converter(
        pt_model_path='yolov5s.pt',
        img_size=640,
        batch_size=1,
        device='cpu'
    )
    
    # Convert PT -> ONNX -> TensorRT
    onnx_path, engine_path = converter.convert_all()
    print(f"ONNX model saved to: {onnx_path}")
    print(f"TensorRT engine saved to: {engine_path}")


# Example 2: ONNX only
def example_onnx_only():
    """Convert to ONNX only"""
    converter = YOLOv5Converter(
        pt_model_path='yolov5s.pt',
        img_size=640
    )
    
    # Only convert to ONNX
    onnx_path = converter.convert_pt_to_onnx(
        simplify=True,
        dynamic=False,
        opset=12
    )
    print(f"ONNX model saved to: {onnx_path}")


# Example 3: Custom settings with FP16
def example_custom_fp16():
    """Convert with FP16 precision"""
    converter = YOLOv5Converter(
        pt_model_path='yolov5s.pt',
        img_size=1280,
        batch_size=1,
        device='cuda'  # Use GPU if available
    )
    
    # Convert with FP16 precision
    onnx_path, engine_path = converter.convert_all(
        simplify=True,
        dynamic=False,
        opset=12,
        fp16=True,
        workspace=8  # 8GB workspace
    )
    print(f"ONNX model saved to: {onnx_path}")
    print(f"TensorRT engine (FP16) saved to: {engine_path}")


# Example 4: Dynamic axes for variable input size
def example_dynamic():
    """Convert with dynamic axes"""
    converter = YOLOv5Converter(
        pt_model_path='yolov5s.pt',
        img_size=640
    )
    
    # Convert with dynamic axes
    onnx_path, engine_path = converter.convert_all(
        dynamic=True  # Enable dynamic input size
    )
    print(f"ONNX model (dynamic) saved to: {onnx_path}")
    print(f"TensorRT engine saved to: {engine_path}")


# Example 5: Manual TensorRT conversion
def example_manual_tensorrt():
    """Manually convert ONNX to TensorRT"""
    converter = YOLOv5Converter(
        pt_model_path='yolov5s.pt',
        img_size=640
    )
    
    # First convert to ONNX
    onnx_path = converter.convert_pt_to_onnx()
    
    # Then convert to TensorRT with custom settings
    engine_path = converter.convert_onnx_to_tensorrt(
        fp16=True,
        workspace=4
    )
    print(f"TensorRT engine saved to: {engine_path}")


if __name__ == '__main__':
    print("YOLOv5 Converter - Example Usage\n")
    print("Please uncomment the example you want to run:")
    print("- example_basic(): Basic PT -> ONNX -> TensorRT conversion")
    print("- example_onnx_only(): Only convert to ONNX")
    print("- example_custom_fp16(): Convert with FP16 precision")
    print("- example_dynamic(): Convert with dynamic input size")
    print("- example_manual_tensorrt(): Manual step-by-step conversion")
    
    # Uncomment the example you want to run
    # example_basic()
    # example_onnx_only()
    # example_custom_fp16()
    # example_dynamic()
    # example_manual_tensorrt()
