#!/usr/bin/env python3
"""
YOLOv5 Model Converter: PT -> ONNX -> TensorRT
This script converts YOLOv5 PyTorch models to ONNX and then to TensorRT engine.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

try:
    import torch
    import onnx
except ImportError as e:
    print(f"Error: Missing required package - {e}")
    print("Please install required packages: pip install -r requirements.txt")
    sys.exit(1)


class YOLOv5Converter:
    """YOLOv5 model converter class"""
    
    def __init__(self, pt_model_path, img_size=640, batch_size=1, device='cpu'):
        """
        Initialize converter
        
        Args:
            pt_model_path: Path to YOLOv5 .pt model file
            img_size: Input image size (default: 640)
            batch_size: Batch size for inference (default: 1)
            device: Device to use ('cpu' or 'cuda')
        """
        self.pt_model_path = Path(pt_model_path)
        self.img_size = img_size
        self.batch_size = batch_size
        self.device = device
        
        # Validate PT model exists
        if not self.pt_model_path.exists():
            raise FileNotFoundError(f"PT model file not found: {pt_model_path}")
        
        # Generate output paths
        self.model_name = self.pt_model_path.stem
        self.onnx_path = self.pt_model_path.parent / f"{self.model_name}.onnx"
        self.engine_path = self.pt_model_path.parent / f"{self.model_name}.engine"
    
    def convert_pt_to_onnx(self, simplify=True, dynamic=False, opset=12):
        """
        Convert PyTorch model to ONNX format
        
        Args:
            simplify: Whether to simplify ONNX model (default: True)
            dynamic: Whether to use dynamic axes (default: False)
            opset: ONNX opset version (default: 12)
        
        Returns:
            Path to ONNX model
        """
        print(f"\n{'='*60}")
        print(f"Step 1: Converting PT to ONNX")
        print(f"{'='*60}")
        print(f"Input:  {self.pt_model_path}")
        print(f"Output: {self.onnx_path}")
        print(f"Device: {self.device}")
        print(f"Image size: {self.img_size}")
        print(f"Batch size: {self.batch_size}")
        
        try:
            import warnings
            
            # Load PyTorch model
            print("\nLoading PyTorch model...")
            
            # Try to load the model - handle different model formats
            try:
                # PyTorch 2.6+ requires weights_only=False for Ultralytics models
                model = torch.load(self.pt_model_path, map_location=self.device, weights_only=False)
            except ModuleNotFoundError as e:
                # If 'models' module is missing, try to load with ultralytics
                if 'models' in str(e):
                    print("Detected YOLOv5 source-dependent model, trying ultralytics loader...")
                    try:
                        from ultralytics import YOLO
                        yolo_model = YOLO(str(self.pt_model_path))
                        model = yolo_model.model
                        print("✓ Successfully loaded with ultralytics")
                    except Exception as ult_err:
                        print(f"⚠ ultralytics loading failed: {ult_err}")
                        print("Trying to add YOLOv5 path...")
                        # Try to find and add yolov5 path
                        import sys
                        from pathlib import Path
                        possible_paths = [
                            self.pt_model_path.parent / 'yolov5',
                            self.pt_model_path.parent.parent / 'yolov5',
                            Path.cwd() / 'yolov5',
                        ]
                        for yolo_path in possible_paths:
                            if yolo_path.exists():
                                sys.path.insert(0, str(yolo_path))
                                print(f"Added path: {yolo_path}")
                                break
                        # Retry loading
                        model = torch.load(self.pt_model_path, map_location=self.device, weights_only=False)
                else:
                    raise
            
            # Handle different model formats
            is_ultralytics = False
            if isinstance(model, dict):
                if 'model' in model:
                    model = model['model']
                    is_ultralytics = True
                elif 'ema' in model:
                    model = model['ema']
                    is_ultralytics = True
            
            # Check model type
            model_type = type(model).__name__
            if 'DetectionModel' in model_type or hasattr(model, 'yaml'):
                is_ultralytics = True
                print(f"Detected Ultralytics model: {model_type}")
            
            # Set model to eval mode
            model.eval()
            model.float()
            
            # Create dummy input
            dummy_input = torch.randn(self.batch_size, 3, self.img_size, self.img_size)
            dummy_input = dummy_input.to(self.device)
            
            # Define input and output names
            input_names = ['images']
            output_names = ['output']
            
            # Define dynamic axes if needed
            dynamic_axes = None
            if dynamic:
                dynamic_axes = {
                    'images': {0: 'batch', 2: 'height', 3: 'width'},
                    'output': {0: 'batch', 1: 'anchors'}
                }
            
            # Export to ONNX
            print("Exporting to ONNX...")
            
            # Suppress TracerWarning for ultralytics models
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', category=torch.jit.TracerWarning)
                warnings.filterwarnings('ignore', message='.*TracerWarning.*')
                
                torch.onnx.export(
                    model,
                    dummy_input,
                    str(self.onnx_path),
                    export_params=True,
                    opset_version=opset,
                    do_constant_folding=True,
                    input_names=input_names,
                    output_names=output_names,
                    dynamic_axes=dynamic_axes,
                    verbose=False
                )
            
            # Verify ONNX model
            print("Verifying ONNX model...")
            onnx_model = onnx.load(str(self.onnx_path))
            onnx.checker.check_model(onnx_model)
            print("✓ ONNX model verification passed")
            
            # Simplify ONNX model
            if simplify:
                try:
                    import onnxsim
                    print("Simplifying ONNX model...")
                    model_simplified, check = onnxsim.simplify(onnx_model)
                    if check:
                        onnx.save(model_simplified, str(self.onnx_path))
                        print("✓ ONNX model simplified successfully")
                    else:
                        print("⚠ ONNX simplification failed, using original model")
                except ImportError:
                    print("⚠ onnx-simplifier not installed, skipping simplification")
                    print("  Install with: pip install onnx-simplifier")
            
            print(f"\n✓ ONNX conversion completed: {self.onnx_path}")
            return self.onnx_path
            
        except Exception as e:
            print(f"✗ Error during ONNX conversion: {e}")
            raise
    
    def convert_onnx_to_tensorrt(self, fp16=False, int8=False, workspace=4):
        """
        Convert ONNX model to TensorRT engine using trtexec
        
        Args:
            fp16: Use FP16 precision (default: False)
            int8: Use INT8 precision (default: False)
            workspace: Maximum workspace size in GB (default: 4)
        
        Returns:
            Path to TensorRT engine file
        """
        print(f"\n{'='*60}")
        print(f"Step 2: Converting ONNX to TensorRT")
        print(f"{'='*60}")
        print(f"Input:  {self.onnx_path}")
        print(f"Output: {self.engine_path}")
        
        # Check if ONNX file exists
        if not self.onnx_path.exists():
            raise FileNotFoundError(f"ONNX file not found: {self.onnx_path}")
        
        # Build trtexec command
        cmd = [
            'trtexec',
            f'--onnx={self.onnx_path}',
            f'--saveEngine={self.engine_path}',
            f'--workspace={workspace * 1024}',  # Convert GB to MB
        ]
        
        if fp16:
            cmd.append('--fp16')
            print("Precision: FP16")
        elif int8:
            cmd.append('--int8')
            print("Precision: INT8")
        else:
            print("Precision: FP32")
        
        print(f"Workspace: {workspace} GB")
        print(f"\nExecuting command:")
        print(' '.join(cmd))
        
        try:
            # Check if trtexec is available
            result = subprocess.run(['which', 'trtexec'], 
                                  capture_output=True, 
                                  text=True)
            if result.returncode != 0:
                print("\n✗ Error: trtexec not found in PATH")
                print("\nPlease install TensorRT and ensure trtexec is in your PATH.")
                print("Alternative: Manually run the following command:")
                print(f"\n  {' '.join(cmd)}\n")
                return None
            
            # Execute trtexec
            print("\nConverting to TensorRT engine (this may take a few minutes)...\n")
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True)
            
            # Print output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            
            if result.returncode == 0:
                print(f"\n✓ TensorRT conversion completed: {self.engine_path}")
                return self.engine_path
            else:
                print(f"\n✗ TensorRT conversion failed with return code {result.returncode}")
                return None
                
        except Exception as e:
            print(f"✗ Error during TensorRT conversion: {e}")
            print("\nManually run the following command:")
            print(f"\n  {' '.join(cmd)}\n")
            raise
    
    def convert_all(self, simplify=True, dynamic=False, opset=12, 
                   fp16=False, int8=False, workspace=4):
        """
        Convert PT -> ONNX -> TensorRT in one go
        
        Args:
            simplify: Whether to simplify ONNX model
            dynamic: Whether to use dynamic axes
            opset: ONNX opset version
            fp16: Use FP16 precision for TensorRT
            int8: Use INT8 precision for TensorRT
            workspace: Maximum workspace size in GB
        
        Returns:
            Tuple of (onnx_path, engine_path)
        """
        print(f"\n{'#'*60}")
        print(f"# YOLOv5 Model Conversion: PT -> ONNX -> TensorRT")
        print(f"{'#'*60}")
        
        # Step 1: Convert to ONNX
        onnx_path = self.convert_pt_to_onnx(
            simplify=simplify,
            dynamic=dynamic,
            opset=opset
        )
        
        # Step 2: Convert to TensorRT
        engine_path = self.convert_onnx_to_tensorrt(
            fp16=fp16,
            int8=int8,
            workspace=workspace
        )
        
        # Summary
        print(f"\n{'='*60}")
        print(f"Conversion Summary")
        print(f"{'='*60}")
        print(f"Source PT model:     {self.pt_model_path}")
        print(f"Generated ONNX:      {onnx_path}")
        if engine_path:
            print(f"Generated TensorRT:  {engine_path}")
        else:
            print(f"TensorRT engine:     Not generated (run trtexec manually)")
        print(f"{'='*60}\n")
        
        return onnx_path, engine_path


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Convert YOLOv5 model from PT to ONNX to TensorRT',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic conversion
  python convert_yolov5_to_tensorrt.py --weights yolov5s.pt
  
  # Convert with FP16 precision
  python convert_yolov5_to_tensorrt.py --weights yolov5s.pt --fp16
  
  # Convert with custom image size
  python convert_yolov5_to_tensorrt.py --weights yolov5s.pt --img-size 1280
  
  # Convert with dynamic axes (variable input size)
  python convert_yolov5_to_tensorrt.py --weights yolov5s.pt --dynamic
  
  # Only convert to ONNX (skip TensorRT)
  python convert_yolov5_to_tensorrt.py --weights yolov5s.pt --onnx-only
        '''
    )
    
    parser.add_argument('--weights', type=str, required=True,
                       help='Path to YOLOv5 .pt model file')
    parser.add_argument('--img-size', type=int, default=640,
                       help='Input image size (default: 640)')
    parser.add_argument('--batch-size', type=int, default=1,
                       help='Batch size (default: 1)')
    parser.add_argument('--device', type=str, default='cpu',
                       help='Device to use: cpu or cuda (default: cpu)')
    parser.add_argument('--opset', type=int, default=12,
                       help='ONNX opset version (default: 12)')
    parser.add_argument('--simplify', action='store_true', default=True,
                       help='Simplify ONNX model (default: True)')
    parser.add_argument('--no-simplify', action='store_false', dest='simplify',
                       help='Do not simplify ONNX model')
    parser.add_argument('--dynamic', action='store_true',
                       help='Use dynamic axes (variable input size)')
    parser.add_argument('--fp16', action='store_true',
                       help='Use FP16 precision for TensorRT')
    parser.add_argument('--int8', action='store_true',
                       help='Use INT8 precision for TensorRT')
    parser.add_argument('--workspace', type=int, default=4,
                       help='TensorRT workspace size in GB (default: 4)')
    parser.add_argument('--onnx-only', action='store_true',
                       help='Only convert to ONNX, skip TensorRT conversion')
    
    args = parser.parse_args()
    
    try:
        # Create converter
        converter = YOLOv5Converter(
            pt_model_path=args.weights,
            img_size=args.img_size,
            batch_size=args.batch_size,
            device=args.device
        )
        
        if args.onnx_only:
            # Only convert to ONNX
            converter.convert_pt_to_onnx(
                simplify=args.simplify,
                dynamic=args.dynamic,
                opset=args.opset
            )
        else:
            # Full conversion
            converter.convert_all(
                simplify=args.simplify,
                dynamic=args.dynamic,
                opset=args.opset,
                fp16=args.fp16,
                int8=args.int8,
                workspace=args.workspace
            )
        
        print("\n✓ Conversion completed successfully!")
        return 0
        
    except Exception as e:
        print(f"\n✗ Conversion failed: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
