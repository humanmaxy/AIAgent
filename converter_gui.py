#!/usr/bin/env python3
"""
YOLOv5 Model Converter GUI
带图形界面的YOLOv5模型转换工具
"""

import os
import sys
import threading
import subprocess
from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime


class ConverterGUI:
    """YOLOv5转换器图形界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("YOLOv5 模型转换工具 - PT to ONNX to TensorRT")
        self.root.geometry("900x800")
        self.root.resizable(True, True)
        
        # 设置样式
        self.setup_styles()
        
        # 变量
        self.pt_file = StringVar()
        self.output_dir = StringVar()
        self.trtexec_path = StringVar(value="trtexec")  # 默认使用PATH中的trtexec
        
        # 输入输出名称
        self.input_name = StringVar(value="images")
        self.output_name = StringVar(value="output")
        
        # 模型参数
        self.batch_size = IntVar(value=1)
        self.width = IntVar(value=640)
        self.height = IntVar(value=640)
        self.channels = IntVar(value=3)
        
        # ONNX选项
        self.opset_version = IntVar(value=12)
        self.simplify_onnx = BooleanVar(value=True)
        self.dynamic_axes = BooleanVar(value=False)
        
        # TensorRT选项
        self.precision = StringVar(value="FP32")
        self.workspace_size = IntVar(value=4)
        self.device = StringVar(value="cpu")
        
        # 转换选项
        self.skip_tensorrt = BooleanVar(value=False)
        
        # 转换状态
        self.is_converting = False
        
        # 创建界面
        self.create_widgets()
        
        # 检查依赖
        self.root.after(100, self.check_dependencies)
    
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置颜色
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Arial', 10, 'bold'), foreground='#34495e')
        style.configure('TButton', padding=6)
        style.configure('Convert.TButton', font=('Arial', 11, 'bold'))
    
    def create_widgets(self):
        """创建界面组件"""
        # 主容器
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="YOLOv5 模型转换工具", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 10), sticky=W)
        
        # 创建各个部分
        row = 1
        row = self.create_file_section(main_frame, row)
        row = self.create_model_params_section(main_frame, row)
        row = self.create_onnx_options_section(main_frame, row)
        row = self.create_tensorrt_options_section(main_frame, row)
        row = self.create_convert_section(main_frame, row)
        row = self.create_log_section(main_frame, row)
        
        # 配置权重
        main_frame.rowconfigure(row-1, weight=1)
    
    def create_file_section(self, parent, row):
        """创建文件选择部分"""
        # 框架
        frame = ttk.LabelFrame(parent, text="文件选择", padding="10")
        frame.grid(row=row, column=0, sticky=(W, E), pady=5)
        frame.columnconfigure(1, weight=1)
        
        # PT模型文件
        ttk.Label(frame, text="PT模型文件:").grid(row=0, column=0, sticky=W, pady=5)
        ttk.Entry(frame, textvariable=self.pt_file).grid(row=0, column=1, sticky=(W, E), padx=5)
        ttk.Button(frame, text="浏览...", command=self.browse_pt_file).grid(row=0, column=2)
        
        # 输出目录
        ttk.Label(frame, text="输出目录:").grid(row=1, column=0, sticky=W, pady=5)
        ttk.Entry(frame, textvariable=self.output_dir).grid(row=1, column=1, sticky=(W, E), padx=5)
        ttk.Button(frame, text="浏览...", command=self.browse_output_dir).grid(row=1, column=2)
        
        # trtexec路径
        ttk.Label(frame, text="trtexec路径:").grid(row=2, column=0, sticky=W, pady=5)
        ttk.Entry(frame, textvariable=self.trtexec_path).grid(row=2, column=1, sticky=(W, E), padx=5)
        ttk.Button(frame, text="浏览...", command=self.browse_trtexec).grid(row=2, column=2)
        
        return row + 1
    
    def create_model_params_section(self, parent, row):
        """创建模型参数部分"""
        frame = ttk.LabelFrame(parent, text="模型参数", padding="10")
        frame.grid(row=row, column=0, sticky=(W, E), pady=5)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)
        
        # 第一行：输入名称和输出名称
        ttk.Label(frame, text="输入名称:").grid(row=0, column=0, sticky=W, pady=5)
        ttk.Entry(frame, textvariable=self.input_name, width=15).grid(row=0, column=1, sticky=W, padx=5)
        
        ttk.Label(frame, text="输出名称:").grid(row=0, column=2, sticky=W, pady=5, padx=(20, 0))
        ttk.Entry(frame, textvariable=self.output_name, width=15).grid(row=0, column=3, sticky=W, padx=5)
        
        # 第二行：Batch和Channels
        ttk.Label(frame, text="Batch Size:").grid(row=1, column=0, sticky=W, pady=5)
        ttk.Spinbox(frame, from_=1, to=32, textvariable=self.batch_size, width=13).grid(row=1, column=1, sticky=W, padx=5)
        
        ttk.Label(frame, text="Channels:").grid(row=1, column=2, sticky=W, pady=5, padx=(20, 0))
        ttk.Spinbox(frame, from_=1, to=4, textvariable=self.channels, width=13).grid(row=1, column=3, sticky=W, padx=5)
        
        # 第三行：Width和Height
        ttk.Label(frame, text="Width:").grid(row=2, column=0, sticky=W, pady=5)
        ttk.Spinbox(frame, from_=32, to=4096, increment=32, textvariable=self.width, width=13).grid(row=2, column=1, sticky=W, padx=5)
        
        ttk.Label(frame, text="Height:").grid(row=2, column=2, sticky=W, pady=5, padx=(20, 0))
        ttk.Spinbox(frame, from_=32, to=4096, increment=32, textvariable=self.height, width=13).grid(row=2, column=3, sticky=W, padx=5)
        
        # 设备选择
        ttk.Label(frame, text="设备:").grid(row=3, column=0, sticky=W, pady=5)
        device_combo = ttk.Combobox(frame, textvariable=self.device, values=['cpu', 'cuda'], width=13, state='readonly')
        device_combo.grid(row=3, column=1, sticky=W, padx=5)
        
        return row + 1
    
    def create_onnx_options_section(self, parent, row):
        """创建ONNX选项部分"""
        frame = ttk.LabelFrame(parent, text="ONNX 选项", padding="10")
        frame.grid(row=row, column=0, sticky=(W, E), pady=5)
        frame.columnconfigure(1, weight=1)
        
        # OPSET版本
        ttk.Label(frame, text="OPSET版本:").grid(row=0, column=0, sticky=W, pady=5)
        ttk.Spinbox(frame, from_=9, to=17, textvariable=self.opset_version, width=13).grid(row=0, column=1, sticky=W, padx=5)
        
        # 选项
        ttk.Checkbutton(frame, text="简化ONNX模型", variable=self.simplify_onnx).grid(row=0, column=2, sticky=W, padx=20)
        ttk.Checkbutton(frame, text="动态输入尺寸", variable=self.dynamic_axes).grid(row=0, column=3, sticky=W, padx=20)
        
        return row + 1
    
    def create_tensorrt_options_section(self, parent, row):
        """创建TensorRT选项部分"""
        frame = ttk.LabelFrame(parent, text="TensorRT 选项", padding="10")
        frame.grid(row=row, column=0, sticky=(W, E), pady=5)
        frame.columnconfigure(1, weight=1)
        
        # 精度选择
        ttk.Label(frame, text="精度:").grid(row=0, column=0, sticky=W, pady=5)
        precision_frame = ttk.Frame(frame)
        precision_frame.grid(row=0, column=1, columnspan=3, sticky=W, padx=5)
        
        ttk.Radiobutton(precision_frame, text="FP32", variable=self.precision, value="FP32").pack(side=LEFT, padx=5)
        ttk.Radiobutton(precision_frame, text="FP16", variable=self.precision, value="FP16").pack(side=LEFT, padx=5)
        ttk.Radiobutton(precision_frame, text="INT8", variable=self.precision, value="INT8").pack(side=LEFT, padx=5)
        
        # Workspace大小
        ttk.Label(frame, text="Workspace (GB):").grid(row=1, column=0, sticky=W, pady=5)
        ttk.Spinbox(frame, from_=1, to=16, textvariable=self.workspace_size, width=13).grid(row=1, column=1, sticky=W, padx=5)
        
        # 跳过TensorRT转换
        ttk.Checkbutton(frame, text="仅转换为ONNX（跳过TensorRT）", variable=self.skip_tensorrt).grid(row=1, column=2, columnspan=2, sticky=W, padx=20)
        
        return row + 1
    
    def create_convert_section(self, parent, row):
        """创建转换按钮部分"""
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, sticky=(W, E), pady=10)
        
        # 转换按钮
        self.convert_btn = ttk.Button(
            frame, 
            text="🚀 开始转换", 
            command=self.start_conversion,
            style='Convert.TButton'
        )
        self.convert_btn.pack(side=LEFT, padx=5)
        
        # 停止按钮
        self.stop_btn = ttk.Button(
            frame, 
            text="⏹ 停止", 
            command=self.stop_conversion,
            state=DISABLED
        )
        self.stop_btn.pack(side=LEFT, padx=5)
        
        # 清空日志按钮
        ttk.Button(frame, text="清空日志", command=self.clear_log).pack(side=LEFT, padx=5)
        
        # 进度条
        self.progress = ttk.Progressbar(frame, mode='indeterminate', length=200)
        self.progress.pack(side=LEFT, padx=20)
        
        return row + 1
    
    def create_log_section(self, parent, row):
        """创建日志显示部分"""
        frame = ttk.LabelFrame(parent, text="转换日志", padding="5")
        frame.grid(row=row, column=0, sticky=(N, W, E, S), pady=5)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        # 日志文本框
        self.log_text = scrolledtext.ScrolledText(
            frame, 
            wrap=WORD, 
            height=15,
            font=('Consolas', 9),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        self.log_text.grid(row=0, column=0, sticky=(N, W, E, S))
        
        # 配置标签颜色
        self.log_text.tag_config('info', foreground='#3498db')
        self.log_text.tag_config('success', foreground='#27ae60', font=('Consolas', 9, 'bold'))
        self.log_text.tag_config('error', foreground='#e74c3c', font=('Consolas', 9, 'bold'))
        self.log_text.tag_config('warning', foreground='#f39c12')
        
        return row + 1
    
    def browse_pt_file(self):
        """浏览PT文件"""
        filename = filedialog.askopenfilename(
            title="选择PT模型文件",
            filetypes=[("PyTorch模型", "*.pt"), ("所有文件", "*.*")]
        )
        if filename:
            self.pt_file.set(filename)
            # 自动设置输出目录
            if not self.output_dir.get():
                self.output_dir.set(os.path.dirname(filename))
    
    def browse_output_dir(self):
        """浏览输出目录"""
        dirname = filedialog.askdirectory(title="选择输出目录")
        if dirname:
            self.output_dir.set(dirname)
    
    def browse_trtexec(self):
        """浏览trtexec文件"""
        filename = filedialog.askopenfilename(
            title="选择trtexec可执行文件",
            filetypes=[("可执行文件", "trtexec*"), ("所有文件", "*.*")]
        )
        if filename:
            self.trtexec_path.set(filename)
    
    def check_dependencies(self):
        """检查依赖"""
        missing = []
        try:
            import torch
        except ImportError:
            missing.append("torch")
        
        try:
            import onnx
        except ImportError:
            missing.append("onnx")
        
        if missing:
            self.log_warning(f"警告: 缺少依赖包: {', '.join(missing)}")
            self.log_info("请运行: pip install -r requirements.txt")
    
    def log_info(self, message, tag='info'):
        """记录信息日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(END, f"[{timestamp}] {message}\n", tag)
        self.log_text.see(END)
        self.root.update_idletasks()
    
    def log_success(self, message):
        """记录成功日志"""
        self.log_info(f"✓ {message}", 'success')
    
    def log_error(self, message):
        """记录错误日志"""
        self.log_info(f"✗ {message}", 'error')
    
    def log_warning(self, message):
        """记录警告日志"""
        self.log_info(f"⚠ {message}", 'warning')
    
    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, END)
    
    def validate_inputs(self):
        """验证输入"""
        if not self.pt_file.get():
            messagebox.showerror("错误", "请选择PT模型文件！")
            return False
        
        if not os.path.exists(self.pt_file.get()):
            messagebox.showerror("错误", "PT模型文件不存在！")
            return False
        
        if not self.output_dir.get():
            messagebox.showerror("错误", "请选择输出目录！")
            return False
        
        if not os.path.exists(self.output_dir.get()):
            try:
                os.makedirs(self.output_dir.get())
            except Exception as e:
                messagebox.showerror("错误", f"无法创建输出目录: {e}")
                return False
        
        return True
    
    def start_conversion(self):
        """开始转换"""
        if not self.validate_inputs():
            return
        
        if self.is_converting:
            messagebox.showwarning("警告", "转换正在进行中...")
            return
        
        # 启动转换线程
        self.is_converting = True
        self.convert_btn.config(state=DISABLED)
        self.stop_btn.config(state=NORMAL)
        self.progress.start(10)
        
        thread = threading.Thread(target=self.convert_model, daemon=True)
        thread.start()
    
    def stop_conversion(self):
        """停止转换"""
        self.is_converting = False
        self.log_warning("用户请求停止转换...")
    
    def convert_model(self):
        """转换模型（在线程中运行）"""
        try:
            self.log_info("="*60)
            self.log_info("开始模型转换")
            self.log_info("="*60)
            
            # Step 1: 转换为ONNX
            onnx_path = self.convert_to_onnx()
            if not onnx_path or not self.is_converting:
                return
            
            # Step 2: 转换为TensorRT
            if not self.skip_tensorrt.get():
                engine_path = self.convert_to_tensorrt(onnx_path)
                if not engine_path:
                    return
            
            # 完成
            self.log_info("="*60)
            self.log_success("转换完成！")
            self.log_info("="*60)
            
            # 显示完成对话框
            self.root.after(0, lambda: messagebox.showinfo(
                "成功", 
                "模型转换完成！\n\n请查看输出目录获取转换后的文件。"
            ))
            
        except Exception as e:
            error_msg = str(e)
            self.log_error(f"转换失败: {error_msg}")
            import traceback
            self.log_error(traceback.format_exc())
            self.root.after(0, lambda msg=error_msg: messagebox.showerror("错误", f"转换失败:\n{msg}"))
        
        finally:
            self.is_converting = False
            self.root.after(0, self.reset_ui)
    
    def convert_to_onnx(self):
        """转换为ONNX"""
        try:
            import torch
            import onnx
            import warnings
            
            self.log_info("\n步骤 1/2: 转换 PT -> ONNX")
            self.log_info("-" * 60)
            
            pt_path = Path(self.pt_file.get())
            output_dir = Path(self.output_dir.get())
            onnx_path = output_dir / f"{pt_path.stem}.onnx"
            
            self.log_info(f"输入文件: {pt_path}")
            self.log_info(f"输出文件: {onnx_path}")
            
            # 加载模型
            self.log_info("加载PyTorch模型...")
            model = torch.load(str(pt_path), map_location=self.device.get())
            
            # 检测是否为ultralytics模型
            is_ultralytics = False
            if isinstance(model, dict):
                if 'model' in model:
                    model = model['model']
                    is_ultralytics = True
                elif 'ema' in model:
                    model = model['ema']
                    is_ultralytics = True
            
            # 检查模型类型
            model_type = type(model).__name__
            if 'DetectionModel' in model_type or hasattr(model, 'yaml'):
                is_ultralytics = True
                self.log_info(f"检测到Ultralytics模型: {model_type}")
            
            model.eval()
            model.float()
            
            # 创建输入张量
            batch = self.batch_size.get()
            channels = self.channels.get()
            height = self.height.get()
            width = self.width.get()
            
            self.log_info(f"输入形状: [{batch}, {channels}, {height}, {width}]")
            
            dummy_input = torch.randn(batch, channels, height, width)
            dummy_input = dummy_input.to(self.device.get())
            
            # 设置输入输出名称
            input_names = [self.input_name.get()]
            output_names = [self.output_name.get()]
            
            # 动态轴
            dynamic_axes = None
            if self.dynamic_axes.get():
                dynamic_axes = {
                    self.input_name.get(): {0: 'batch', 2: 'height', 3: 'width'},
                    self.output_name.get(): {0: 'batch'}
                }
                self.log_info("启用动态输入尺寸")
            
            # 导出ONNX
            self.log_info("导出ONNX模型...")
            
            # 抑制TracerWarning
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', category=torch.jit.TracerWarning)
                warnings.filterwarnings('ignore', message='.*TracerWarning.*')
                
                torch.onnx.export(
                    model,
                    dummy_input,
                    str(onnx_path),
                    export_params=True,
                    opset_version=self.opset_version.get(),
                    do_constant_folding=True,
                    input_names=input_names,
                    output_names=output_names,
                    dynamic_axes=dynamic_axes,
                    verbose=False
                )
            
            # 验证ONNX
            self.log_info("验证ONNX模型...")
            onnx_model = onnx.load(str(onnx_path))
            onnx.checker.check_model(onnx_model)
            self.log_success("ONNX模型验证通过")
            
            # 简化ONNX
            if self.simplify_onnx.get():
                try:
                    import onnxsim
                    self.log_info("简化ONNX模型...")
                    model_simplified, check = onnxsim.simplify(onnx_model)
                    if check:
                        onnx.save(model_simplified, str(onnx_path))
                        self.log_success("ONNX模型简化成功")
                    else:
                        self.log_warning("ONNX简化失败，使用原始模型")
                except ImportError:
                    self.log_warning("未安装onnx-simplifier，跳过简化")
            
            self.log_success(f"ONNX转换完成: {onnx_path}")
            return onnx_path
            
        except Exception as e:
            self.log_error(f"ONNX转换失败: {str(e)}")
            raise
    
    def convert_to_tensorrt(self, onnx_path):
        """转换为TensorRT"""
        try:
            self.log_info("\n步骤 2/2: 转换 ONNX -> TensorRT")
            self.log_info("-" * 60)
            
            engine_path = onnx_path.parent / f"{onnx_path.stem}.engine"
            
            self.log_info(f"输入文件: {onnx_path}")
            self.log_info(f"输出文件: {engine_path}")
            
            # 构建trtexec命令
            trtexec = self.trtexec_path.get()
            workspace_mb = self.workspace_size.get() * 1024
            
            cmd = [
                trtexec,
                f'--onnx={onnx_path}',
                f'--saveEngine={engine_path}',
                f'--workspace={workspace_mb}',
            ]
            
            # 添加精度选项
            precision = self.precision.get()
            if precision == "FP16":
                cmd.append('--fp16')
                self.log_info("精度: FP16")
            elif precision == "INT8":
                cmd.append('--int8')
                self.log_info("精度: INT8")
            else:
                self.log_info("精度: FP32")
            
            self.log_info(f"Workspace: {self.workspace_size.get()} GB")
            self.log_info(f"\n执行命令:\n{' '.join(cmd)}\n")
            
            # 检查trtexec是否存在
            result = subprocess.run(['which', trtexec] if trtexec == 'trtexec' else ['test', '-f', trtexec],
                                  capture_output=True)
            if result.returncode != 0:
                self.log_error("找不到trtexec！")
                self.log_warning("请安装TensorRT并设置trtexec路径")
                self.log_info(f"\n手动运行以下命令:\n{' '.join(cmd)}\n")
                return None
            
            # 执行转换
            self.log_info("正在转换为TensorRT引擎（这可能需要几分钟）...\n")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # 实时显示输出
            for line in process.stdout:
                if not self.is_converting:
                    process.terminate()
                    self.log_warning("转换已停止")
                    return None
                self.log_info(line.rstrip())
            
            process.wait()
            
            if process.returncode == 0:
                self.log_success(f"TensorRT转换完成: {engine_path}")
                return engine_path
            else:
                self.log_error(f"TensorRT转换失败，返回码: {process.returncode}")
                return None
            
        except Exception as e:
            self.log_error(f"TensorRT转换失败: {str(e)}")
            raise
    
    def reset_ui(self):
        """重置UI状态"""
        self.convert_btn.config(state=NORMAL)
        self.stop_btn.config(state=DISABLED)
        self.progress.stop()


def main():
    """主函数"""
    root = Tk()
    app = ConverterGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
