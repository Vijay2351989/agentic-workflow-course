"""
LaTeX to PDF Compiler
Compiles a .tex file to PDF using Tectonic. Auto-installs Tectonic if not found.

Usage:
    python3 execution/compile_latex.py --input "docs/Resume_VijayBhatt.tex"
    python3 execution/compile_latex.py --input "docs/Resume_VijayBhatt.tex" --output "docs/Resume_VijayBhatt.pdf"

If --output is not specified, the PDF is generated in the same directory as the input .tex file.

Tectonic is a standalone LaTeX engine (~15MB) that auto-downloads packages on the fly.
No TeXLive or MacTeX installation required.
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def check_tectonic():
    """Check if tectonic is available on the system."""
    return shutil.which("tectonic") is not None


def install_tectonic():
    """Attempt to install tectonic based on the platform."""
    system = platform.system()

    if system == "Darwin":
        # macOS — try Homebrew first, then conda
        if shutil.which("brew"):
            print("[setup] Installing tectonic via Homebrew...")
            result = subprocess.run(
                ["brew", "install", "tectonic"],
                capture_output=True, text=True, timeout=300
            )
            if result.returncode == 0:
                print("[setup] Tectonic installed successfully via Homebrew.")
                return True
            else:
                print(f"[setup] Homebrew install failed: {result.stderr}")
        else:
            print("[setup] Homebrew not found.")

    elif system == "Linux":
        # Linux — try apt, then conda
        if shutil.which("apt-get"):
            print("[setup] Installing tectonic via apt...")
            result = subprocess.run(
                ["sudo", "apt-get", "install", "-y", "tectonic"],
                capture_output=True, text=True, timeout=300
            )
            if result.returncode == 0:
                print("[setup] Tectonic installed successfully via apt.")
                return True
            else:
                print(f"[setup] apt install failed: {result.stderr}")

    # Fallback — try conda if available
    if shutil.which("conda"):
        print("[setup] Installing tectonic via conda-forge...")
        result = subprocess.run(
            ["conda", "install", "-y", "-c", "conda-forge", "tectonic"],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0:
            print("[setup] Tectonic installed successfully via conda.")
            return True
        else:
            print(f"[setup] conda install failed: {result.stderr}")

    # Fallback — try pip (pdflatex package as last resort)
    print("[setup] Could not auto-install tectonic.")
    print("[setup] Please install manually:")
    print("        macOS:  brew install tectonic")
    print("        Linux:  sudo apt-get install tectonic")
    print("        Conda:  conda install -c conda-forge tectonic")
    return False


def compile_tex(input_path, output_path=None):
    """Compile a .tex file to PDF using tectonic."""
    input_path = Path(input_path).resolve()

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        sys.exit(1)

    if not input_path.suffix == ".tex":
        print(f"ERROR: Input file must be a .tex file, got: {input_path.suffix}")
        sys.exit(1)

    # Determine output directory
    if output_path:
        output_path = Path(output_path).resolve()
        output_dir = output_path.parent
    else:
        output_dir = input_path.parent
        output_path = output_dir / input_path.with_suffix(".pdf").name

    print(f"Input:  {input_path}")
    print(f"Output: {output_path}")
    print("-" * 50)

    # Run tectonic
    print("[compile] Running tectonic...")
    result = subprocess.run(
        ["tectonic", str(input_path), "--outdir", str(output_dir)],
        capture_output=True, text=True, timeout=120
    )

    if result.returncode != 0:
        print(f"[compile] ERROR: Tectonic compilation failed.")
        print(f"[compile] stderr: {result.stderr}")
        print(f"[compile] stdout: {result.stdout}")
        sys.exit(1)

    # Check if PDF was generated
    generated_pdf = output_dir / input_path.with_suffix(".pdf").name

    if not generated_pdf.exists():
        print(f"ERROR: PDF was not generated at expected path: {generated_pdf}")
        sys.exit(1)

    # Rename if output path differs from default
    if generated_pdf != output_path:
        generated_pdf.rename(output_path)

    file_size = output_path.stat().st_size
    print(f"\n✅ PDF compiled successfully: {output_path} ({file_size // 1024}KB)")
    return str(output_path)


def main():
    parser = argparse.ArgumentParser(description="Compile LaTeX (.tex) to PDF")
    parser.add_argument("--input", required=True, help="Path to .tex file")
    parser.add_argument("--output", required=False, help="Path for output PDF (default: same dir as input)")
    args = parser.parse_args()

    # Step 1: Check for tectonic
    if not check_tectonic():
        print("[setup] Tectonic not found. Attempting to install...")
        if not install_tectonic():
            sys.exit(1)
        # Verify installation
        if not check_tectonic():
            print("ERROR: Tectonic installation succeeded but binary not found in PATH.")
            print("       Try restarting your terminal and running again.")
            sys.exit(1)
    else:
        print("[setup] Tectonic found.")

    # Step 2: Compile
    compile_tex(args.input, args.output)


if __name__ == "__main__":
    main()
