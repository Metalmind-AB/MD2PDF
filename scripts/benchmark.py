#!/usr/bin/env python3
"""
Performance benchmark suite for md2pdf package.

This script measures various performance metrics including:
- Conversion speed for different document sizes
- Memory usage during conversion
- CLI startup time
- Style loading performance
"""

import os
import sys
import time
import subprocess
import tempfile
import psutil
import tracemalloc
from pathlib import Path
from statistics import mean, stdev
import json
import gc


# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from md2pdf.core.converter import MD2PDFConverter
from md2pdf.utils.style_loader import StyleLoader


class BenchmarkSuite:
    """Performance benchmark suite for md2pdf."""
    
    def __init__(self):
        self.results = {}
        self.fixtures_dir = Path(__file__).parent.parent / "tests" / "fixtures"
        
    def measure_time(self, func, *args, iterations=5, **kwargs):
        """Measure execution time of a function."""
        times = []
        for _ in range(iterations):
            gc.collect()  # Clean up before measurement
            start = time.perf_counter()
            func(*args, **kwargs)
            end = time.perf_counter()
            times.append(end - start)
        
        return {
            'mean': mean(times),
            'stdev': stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times),
            'iterations': iterations
        }
    
    def measure_memory(self, func, *args, **kwargs):
        """Measure memory usage of a function."""
        gc.collect()
        tracemalloc.start()
        
        # Take snapshot before
        snapshot1 = tracemalloc.take_snapshot()
        
        # Run function
        func(*args, **kwargs)
        
        # Take snapshot after
        snapshot2 = tracemalloc.take_snapshot()
        
        # Calculate difference
        top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        
        # Get total memory used
        total_memory = sum(stat.size_diff for stat in top_stats)
        
        # Get peak memory
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        return {
            'total_mb': total_memory / (1024 * 1024),
            'peak_mb': peak / (1024 * 1024),
            'current_mb': current / (1024 * 1024)
        }
    
    def benchmark_conversion_speed(self):
        """Benchmark conversion speed for different document sizes."""
        print("\n📊 Benchmarking conversion speed...")
        
        test_files = {
            'small': self.fixtures_dir / "basic.md",
            'medium': self.fixtures_dir / "complex.md",
            'large': self.fixtures_dir / "large.md",
        }
        
        results = {}
        
        for size, md_file in test_files.items():
            if not md_file.exists():
                print(f"  ⚠️  Skipping {size}: {md_file} not found")
                continue
            
            file_size = md_file.stat().st_size / 1024  # KB
            print(f"\n  Testing {size} ({file_size:.1f} KB):")
            
            with tempfile.TemporaryDirectory() as temp_dir:
                output_path = Path(temp_dir) / "output.pdf"
                
                def convert():
                    converter = MD2PDFConverter(
                        input_path=str(md_file),
                        output_path=str(output_path),
                        style="technical",
                        theme="default"
                    )
                    converter.convert()
                
                # Measure time
                time_results = self.measure_time(convert, iterations=3)
                
                # Measure memory
                memory_results = self.measure_memory(convert)
                
                results[size] = {
                    'file_size_kb': file_size,
                    'time': time_results,
                    'memory': memory_results,
                    'throughput_kb_per_sec': file_size / time_results['mean']
                }
                
                print(f"    Time: {time_results['mean']:.3f}s ± {time_results['stdev']:.3f}s")
                print(f"    Memory: {memory_results['peak_mb']:.1f} MB peak")
                print(f"    Throughput: {results[size]['throughput_kb_per_sec']:.1f} KB/s")
        
        self.results['conversion_speed'] = results
        return results
    
    def benchmark_cli_startup(self):
        """Benchmark CLI startup time."""
        print("\n⏱️  Benchmarking CLI startup time...")
        
        def run_cli():
            subprocess.run(
                [sys.executable, "-m", "md2pdf", "--version"],
                capture_output=True,
                text=True
            )
        
        results = self.measure_time(run_cli, iterations=10)
        
        print(f"  Mean: {results['mean']*1000:.1f} ms")
        print(f"  Min: {results['min']*1000:.1f} ms")
        print(f"  Max: {results['max']*1000:.1f} ms")
        
        self.results['cli_startup'] = results
        return results
    
    def benchmark_style_loading(self):
        """Benchmark style loading performance."""
        print("\n🎨 Benchmarking style loading...")
        
        results = {}
        
        # Test style discovery
        def discover_styles():
            loader = StyleLoader()
            loader.get_available_styles()
        
        discovery_time = self.measure_time(discover_styles, iterations=10)
        results['discovery'] = discovery_time
        print(f"  Style discovery: {discovery_time['mean']*1000:.1f} ms")
        
        # Test CSS generation for each style
        loader = StyleLoader()
        styles = loader.get_available_styles()
        themes = loader.get_available_themes()
        
        css_gen_times = []
        for style in styles[:3]:  # Test first 3 styles
            for theme in themes[:3]:  # Test first 3 themes
                def generate_css():
                    loader.load_style(style, theme)
                
                time_result = self.measure_time(generate_css, iterations=5)
                css_gen_times.append(time_result['mean'])
        
        results['css_generation'] = {
            'mean': mean(css_gen_times),
            'min': min(css_gen_times),
            'max': max(css_gen_times)
        }
        
        print(f"  CSS generation: {results['css_generation']['mean']*1000:.1f} ms average")
        
        self.results['style_loading'] = results
        return results
    
    def benchmark_batch_processing(self):
        """Benchmark batch processing performance."""
        print("\n📚 Benchmarking batch processing...")
        
        # Create test files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create multiple test files
            test_files = []
            for i in range(10):
                md_file = temp_path / f"test_{i}.md"
                md_file.write_text(f"""# Document {i}

This is test document number {i}.

## Section 1
Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## Section 2
- Item 1
- Item 2
- Item 3

```python
def function_{i}():
    return {i}
```
""")
                test_files.append(md_file)
            
            # Measure sequential processing
            def process_sequential():
                for md_file in test_files:
                    output = md_file.with_suffix('.pdf')
                    converter = MD2PDFConverter(
                        input_path=str(md_file),
                        output_path=str(output),
                        style="technical",
                        theme="default"
                    )
                    converter.convert()
            
            seq_time = self.measure_time(process_sequential, iterations=2)
            
            results = {
                'files_count': len(test_files),
                'sequential_time': seq_time,
                'avg_time_per_file': seq_time['mean'] / len(test_files)
            }
            
            print(f"  Files: {results['files_count']}")
            print(f"  Total time: {seq_time['mean']:.2f}s")
            print(f"  Average per file: {results['avg_time_per_file']:.3f}s")
        
        self.results['batch_processing'] = results
        return results
    
    def benchmark_memory_usage(self):
        """Benchmark memory usage patterns."""
        print("\n💾 Benchmarking memory usage...")
        
        # Test with large document
        large_file = self.fixtures_dir / "large.md"
        
        if not large_file.exists():
            print("  ⚠️  Large test file not found, skipping...")
            return None
        
        # Monitor memory during conversion
        process = psutil.Process()
        
        memory_samples = []
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "output.pdf"
            
            # Start monitoring in background
            import threading
            stop_monitoring = False
            
            def monitor_memory():
                while not stop_monitoring:
                    memory_samples.append(process.memory_info().rss / (1024 * 1024))
                    time.sleep(0.1)
            
            monitor_thread = threading.Thread(target=monitor_memory)
            monitor_thread.start()
            
            # Perform conversion
            converter = MD2PDFConverter(
                input_path=str(large_file),
                output_path=str(output_path),
                style="technical",
                theme="default"
            )
            converter.convert()
            
            # Stop monitoring
            stop_monitoring = True
            monitor_thread.join()
        
        if memory_samples:
            results = {
                'baseline_mb': memory_samples[0],
                'peak_mb': max(memory_samples),
                'average_mb': mean(memory_samples),
                'samples': len(memory_samples)
            }
            
            print(f"  Baseline: {results['baseline_mb']:.1f} MB")
            print(f"  Peak: {results['peak_mb']:.1f} MB")
            print(f"  Average: {results['average_mb']:.1f} MB")
            
            self.results['memory_usage'] = results
            return results
        
        return None
    
    def generate_report(self):
        """Generate a comprehensive benchmark report."""
        print("\n" + "=" * 60)
        print("📈 BENCHMARK REPORT")
        print("=" * 60)
        
        if 'conversion_speed' in self.results:
            print("\n🚀 Conversion Speed:")
            for size, data in self.results['conversion_speed'].items():
                print(f"  {size.capitalize()}:")
                print(f"    - File size: {data['file_size_kb']:.1f} KB")
                print(f"    - Time: {data['time']['mean']:.3f}s")
                print(f"    - Throughput: {data['throughput_kb_per_sec']:.1f} KB/s")
        
        if 'cli_startup' in self.results:
            print(f"\n⏱️  CLI Startup: {self.results['cli_startup']['mean']*1000:.1f} ms")
        
        if 'style_loading' in self.results:
            print(f"\n🎨 Style Loading:")
            print(f"  - Discovery: {self.results['style_loading']['discovery']['mean']*1000:.1f} ms")
            print(f"  - CSS generation: {self.results['style_loading']['css_generation']['mean']*1000:.1f} ms")
        
        if 'batch_processing' in self.results:
            batch = self.results['batch_processing']
            print(f"\n📚 Batch Processing:")
            print(f"  - Files: {batch['files_count']}")
            print(f"  - Total: {batch['sequential_time']['mean']:.2f}s")
            print(f"  - Per file: {batch['avg_time_per_file']:.3f}s")
        
        if 'memory_usage' in self.results:
            mem = self.results['memory_usage']
            print(f"\n💾 Memory Usage:")
            print(f"  - Baseline: {mem['baseline_mb']:.1f} MB")
            print(f"  - Peak: {mem['peak_mb']:.1f} MB")
            print(f"  - Overhead: {mem['peak_mb'] - mem['baseline_mb']:.1f} MB")
        
        # Performance recommendations
        print("\n" + "=" * 60)
        print("📋 PERFORMANCE ANALYSIS")
        print("=" * 60)
        
        # Check conversion speed
        if 'conversion_speed' in self.results:
            large_throughput = self.results['conversion_speed'].get('large', {}).get('throughput_kb_per_sec', 0)
            if large_throughput > 0:
                if large_throughput < 10:
                    print("⚠️  Large file conversion is slow (<10 KB/s)")
                elif large_throughput < 50:
                    print("📊 Large file conversion is acceptable (10-50 KB/s)")
                else:
                    print("✅ Large file conversion is fast (>50 KB/s)")
        
        # Check CLI startup
        if 'cli_startup' in self.results:
            startup_ms = self.results['cli_startup']['mean'] * 1000
            if startup_ms > 500:
                print("⚠️  CLI startup is slow (>500ms)")
            elif startup_ms > 200:
                print("📊 CLI startup is acceptable (200-500ms)")
            else:
                print("✅ CLI startup is fast (<200ms)")
        
        # Check memory usage
        if 'memory_usage' in self.results:
            peak_mb = self.results['memory_usage']['peak_mb']
            baseline_mb = self.results['memory_usage']['baseline_mb']
            overhead_mb = peak_mb - baseline_mb
            
            if overhead_mb > 500:
                print("⚠️  High memory overhead (>500 MB)")
            elif overhead_mb > 200:
                print("📊 Moderate memory overhead (200-500 MB)")
            else:
                print("✅ Low memory overhead (<200 MB)")
        
        # Save results to JSON
        report_file = Path(__file__).parent / "benchmark_results.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n💾 Results saved to: {report_file}")
    
    def run_all_benchmarks(self):
        """Run all benchmarks."""
        print("=" * 60)
        print("🚀 MD2PDF Performance Benchmark Suite")
        print("=" * 60)
        
        # Run benchmarks
        self.benchmark_conversion_speed()
        self.benchmark_cli_startup()
        self.benchmark_style_loading()
        self.benchmark_batch_processing()
        self.benchmark_memory_usage()
        
        # Generate report
        self.generate_report()


def main():
    """Run the benchmark suite."""
    suite = BenchmarkSuite()
    suite.run_all_benchmarks()
    
    print("\n✨ Benchmark complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())