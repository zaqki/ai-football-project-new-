#!/usr/bin/env python3
"""
Football AI Video Editor - Comprehensive Test Report Generator
Creates a detailed report of system status and installation health.
"""

import sys
import os
import platform
import subprocess
import importlib
from datetime import datetime

class TestReporter:
    def __init__(self):
        self.report = []
        self.tests_passed = 0
        self.tests_failed = 0
        self.warnings = 0
        
    def add_section(self, title):
        """Add a section header to the report"""
        self.report.append(f"\n{'='*60}")
        self.report.append(f"  {title}")
        self.report.append(f"{'='*60}")
    
    def add_test(self, name, status, details="", warning=False):
        """Add a test result to the report"""
        if status:
            icon = "✅"
            self.tests_passed += 1
        elif warning:
            icon = "⚠️ "
            self.warnings += 1
        else:
            icon = "❌"
            self.tests_failed += 1
            
        self.report.append(f"{icon} {name}: {'PASS' if status else 'WARNING' if warning else 'FAIL'}")
        if details:
            self.report.append(f"   Details: {details}")
    
    def add_info(self, label, value):
        """Add informational line to the report"""
        self.report.append(f"📋 {label}: {value}")
    
    def get_report(self):
        """Get the complete report as a string"""
        return "\n".join(self.report)
    
    def save_report(self, filename="test_report.txt"):
        """Save report to file"""
        with open(filename, 'w') as f:
            f.write(self.get_report())
        return filename

def test_system_info(reporter):
    """Test and report system information"""
    reporter.add_section("SYSTEM INFORMATION")
    
    # Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    python_ok = sys.version_info >= (3, 7)
    reporter.add_test("Python Version", python_ok, python_version)
    
    # Operating System
    os_info = f"{platform.system()} {platform.release()} ({platform.machine()})"
    reporter.add_info("Operating System", os_info)
    
    # Python executable
    reporter.add_info("Python Executable", sys.executable)
    
    # Current working directory
    reporter.add_info("Working Directory", os.getcwd())
    
    # Available memory (if possible)
    try:
        import psutil
        memory = psutil.virtual_memory()
        reporter.add_info("Available RAM", f"{memory.available // (1024**3)} GB")
    except ImportError:
        reporter.add_info("Available RAM", "Unable to determine (psutil not installed)")

def test_dependencies(reporter):
    """Test all required dependencies"""
    reporter.add_section("DEPENDENCY CHECK")
    
    dependencies = [
        ("numpy", "NumPy - Numerical computing"),
        ("PIL", "Pillow - Image processing"),
        ("imageio", "ImageIO - Image/Video I/O"),
        ("moviepy.editor", "MoviePy - Video editing"),
        ("av", "PyAV - Video processing (optional)")
    ]
    
    for module, description in dependencies:
        try:
            imported_module = importlib.import_module(module)
            version = getattr(imported_module, '__version__', 'Unknown version')
            reporter.add_test(description, True, f"Version: {version}")
        except ImportError as e:
            is_optional = "optional" in description.lower()
            reporter.add_test(description, False, str(e), warning=is_optional)

def test_ffmpeg(reporter):
    """Test FFmpeg availability"""
    reporter.add_section("FFMPEG CHECK")
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            # Extract version info
            lines = result.stdout.split('\n')
            version_line = lines[0] if lines else "Unknown version"
            reporter.add_test("FFmpeg Installation", True, version_line)
            
            # Check for common codecs
            codecs_to_check = ['libx264', 'aac', 'mp4']
            for codec in codecs_to_check:
                codec_available = codec in result.stdout
                reporter.add_test(f"Codec: {codec}", codec_available, 
                                f"Required for video export" if not codec_available else "Available")
        else:
            reporter.add_test("FFmpeg Installation", False, "Command failed")
            
    except subprocess.TimeoutExpired:
        reporter.add_test("FFmpeg Installation", False, "Command timed out")
    except FileNotFoundError:
        reporter.add_test("FFmpeg Installation", False, "FFmpeg not found in PATH")

def test_moviepy_functionality(reporter):
    """Test MoviePy core functionality"""
    reporter.add_section("MOVIEPY FUNCTIONALITY TEST")
    
    try:
        from moviepy.editor import ColorClip, AudioClip
        import numpy as np
        
        # Test 1: Basic video clip creation
        try:
            clip = ColorClip(size=(100, 100), color=(255, 0, 0), duration=0.1)
            reporter.add_test("Video Clip Creation", True, "ColorClip created successfully")
            clip.close()
        except Exception as e:
            reporter.add_test("Video Clip Creation", False, str(e))
        
        # Test 2: Video operations
        try:
            clip = ColorClip(size=(200, 200), color=(0, 255, 0), duration=0.1)
            resized = clip.resize(width=100)
            cropped = resized.crop(x1=10, y1=10, x2=90, y2=90)
            reporter.add_test("Video Operations", True, "Resize and crop successful")
            cropped.close()
            resized.close()
            clip.close()
        except Exception as e:
            reporter.add_test("Video Operations", False, str(e))
        
        # Test 3: Audio clip creation
        try:
            def make_frame(t):
                return np.sin(2 * np.pi * 440 * t)
            
            audio = AudioClip(make_frame, duration=0.1, fps=22050)
            reporter.add_test("Audio Clip Creation", True, "AudioClip created successfully")
            audio.close()
        except Exception as e:
            reporter.add_test("Audio Clip Creation", False, str(e))
            
    except ImportError as e:
        reporter.add_test("MoviePy Import", False, str(e))

def test_file_permissions(reporter):
    """Test file system permissions"""
    reporter.add_section("FILE SYSTEM CHECK")
    
    # Test write permissions in current directory
    test_file = "test_write_permission.tmp"
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        reporter.add_test("Write Permissions", True, "Can write to current directory")
    except Exception as e:
        reporter.add_test("Write Permissions", False, str(e))
    
    # Check for sample files
    sample_files = [
        "heskey skill and finish.mp4",
        "isak_goal.mp4", 
        "isak_voice.mp3",
        "sample_video.mp4",
        "sample_audio.mp3"
    ]
    
    found_files = []
    for file in sample_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / (1024 * 1024)  # MB
            found_files.append(f"{file} ({size:.1f} MB)")
    
    if found_files:
        reporter.add_test("Sample Files Found", True, f"{len(found_files)} files: {', '.join(found_files)}")
    else:
        reporter.add_test("Sample Files Found", False, "No sample files found", warning=True)

def test_video_editor_readiness(reporter):
    """Test if the video editor is ready to run"""
    reporter.add_section("VIDEO EDITOR READINESS")
    
    # Check if main script exists
    main_script = "simple_editor.py"
    script_exists = os.path.exists(main_script)
    reporter.add_test("Main Script Available", script_exists, 
                     f"{main_script} found" if script_exists else f"{main_script} not found")
    
    # Check critical dependencies for video editing
    critical_deps = ["moviepy.editor", "imageio"]
    all_critical_available = True
    
    for dep in critical_deps:
        try:
            importlib.import_module(dep)
        except ImportError:
            all_critical_available = False
            break
    
    reporter.add_test("Critical Dependencies", all_critical_available,
                     "All critical dependencies available" if all_critical_available 
                     else "Some critical dependencies missing")
    
    # Overall readiness assessment
    video_files = ["heskey skill and finish.mp4", "isak_goal.mp4", "sample_video.mp4"]
    audio_files = ["isak_voice.mp3", "sample_audio.mp3"]
    
    has_video = any(os.path.exists(f) for f in video_files)
    has_audio = any(os.path.exists(f) for f in audio_files)
    
    ready_to_run = script_exists and all_critical_available and has_video and has_audio
    reporter.add_test("Ready to Process Videos", ready_to_run,
                     "All requirements met" if ready_to_run 
                     else "Missing requirements - see details above")

def generate_recommendations(reporter):
    """Generate recommendations based on test results"""
    reporter.add_section("RECOMMENDATIONS")
    
    recommendations = []
    
    if reporter.tests_failed > 0:
        recommendations.append("🔧 CRITICAL ISSUES FOUND:")
        recommendations.append("   1. Run: python simple_installer.py")
        recommendations.append("   2. Install missing dependencies manually if needed")
        recommendations.append("   3. Re-run this test after fixing issues")
    
    if reporter.warnings > 0:
        recommendations.append("⚠️  WARNINGS DETECTED:")
        recommendations.append("   1. Some optional features may not work")
        recommendations.append("   2. Consider installing missing optional packages")
    
    if reporter.tests_failed == 0:
        recommendations.append("🎉 SYSTEM READY:")
        recommendations.append("   1. Run: python simple_editor.py")
        recommendations.append("   2. Or create samples: python create_sample_files.py")
        recommendations.append("   3. Process your own videos with custom files")
    
    # Add specific recommendations
    try:
        importlib.import_module("moviepy.editor")
    except ImportError:
        recommendations.append("📦 Install MoviePy: pip install moviepy")
    
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
    except:
        recommendations.append("🎬 Install FFmpeg from: https://ffmpeg.org/download.html")
    
    for rec in recommendations:
        reporter.report.append(rec)

def main():
    """Generate comprehensive test report"""
    print("🏈 Football AI Video Editor - Generating Test Report")
    print("=" * 60)
    print("⏳ Running comprehensive system analysis...")
    
    reporter = TestReporter()
    
    # Add report header
    reporter.report.append("🏈 FOOTBALL AI VIDEO EDITOR - TEST REPORT")
    reporter.report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests
    test_system_info(reporter)
    test_dependencies(reporter)
    test_ffmpeg(reporter)
    test_moviepy_functionality(reporter)
    test_file_permissions(reporter)
    test_video_editor_readiness(reporter)
    generate_recommendations(reporter)
    
    # Add summary
    reporter.add_section("TEST SUMMARY")
    total_tests = reporter.tests_passed + reporter.tests_failed + reporter.warnings
    reporter.add_info("Total Tests Run", total_tests)
    reporter.add_info("Tests Passed", f"{reporter.tests_passed} ✅")
    reporter.add_info("Tests Failed", f"{reporter.tests_failed} ❌")
    reporter.add_info("Warnings", f"{reporter.warnings} ⚠️")
    
    # Calculate health score
    if total_tests > 0:
        health_score = (reporter.tests_passed / total_tests) * 100
        reporter.add_info("System Health Score", f"{health_score:.1f}%")
    
    # Display report
    report_content = reporter.get_report()
    print("\n" + report_content)
    
    # Save to file
    filename = reporter.save_report()
    print(f"\n📄 Report saved to: {filename}")
    
    # Return status
    return reporter.tests_failed == 0

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Report generation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error generating report: {e}")
        sys.exit(1)
