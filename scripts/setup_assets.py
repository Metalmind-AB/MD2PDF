#!/usr/bin/env python3
"""
MD2PDF - Markdown to PDF Converter
Copyright (c) 2025 MPS Metalmind AB
Licensed under the MIT License (see LICENSE file)
"""

"""
Asset Setup Script - Downloads optional assets for MD2PDF
Downloads Twemoji SVG files and any other optional assets.
"""

import json
import os
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

# Twemoji release information
TWEMOJI_VERSION = "14.1.2"  # Latest stable version
TWEMOJI_ZIP_URL = (
    f"https://github.com/twitter/twemoji/archive/refs/tags/v{TWEMOJI_VERSION}.zip"
)
TWEMOJI_CDN_BASE = "https://cdn.jsdelivr.net/gh/twitter/twemoji@latest/assets/svg/"


def validate_url(url: str) -> bool:
    """Validate URL scheme for security - only allow https."""
    parsed = urlparse(url)
    return parsed.scheme in ["https"] and parsed.netloc in [
        "github.com",
        "cdn.jsdelivr.net",
    ]


class AssetSetup:
    """Handles downloading and setup of optional assets."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize asset setup."""
        if project_root is None:
            self.project_root = Path(__file__).parent.parent
        else:
            self.project_root = Path(project_root)

        self.assets_dir = self.project_root / "assets"
        self.twemoji_dir = self.assets_dir / "twemoji" / "svg"

    def check_existing_assets(self) -> dict:
        """Check which assets are already installed."""
        status = {
            "twemoji": {
                "installed": self.twemoji_dir.exists(),
                "count": len(list(self.twemoji_dir.glob("*.svg")))
                if self.twemoji_dir.exists()
                else 0,
                "path": str(self.twemoji_dir),
            }
        }
        return status

    def download_twemoji_pack(self, force: bool = False) -> bool:
        """Download and extract Twemoji SVG files."""
        if self.twemoji_dir.exists() and not force:
            existing_count = len(list(self.twemoji_dir.glob("*.svg")))
            if existing_count > 0:
                print(f"✅ Twemoji already installed ({existing_count} files)")
                response = input("Re-download? (y/N): ").strip().lower()
                if response != "y":
                    return True

        print(f"📥 Downloading Twemoji v{TWEMOJI_VERSION}...")
        print(f"   URL: {TWEMOJI_ZIP_URL}")

        # Create temporary directory
        temp_dir = self.project_root / "temp_twemoji_download"
        temp_dir.mkdir(exist_ok=True)

        try:
            # Download ZIP file
            zip_path = temp_dir / f"twemoji-{TWEMOJI_VERSION}.zip"

            def download_with_progress(url: str, dest: Path) -> None:
                """Download with progress indicator."""
                if not validate_url(url):  # nosec B310 - URL validation added
                    raise ValueError(f"Invalid URL scheme or domain: {url}")
                response = urllib.request.urlopen(
                    url
                )  # nosec B310 - URL validated above
                total_size = int(response.headers.get("Content-Length", 0))

                with open(dest, "wb") as f:
                    downloaded = 0
                    block_size = 8192

                    while True:
                        block = response.read(block_size)
                        if not block:
                            break

                        f.write(block)
                        downloaded += len(block)

                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(
                                f"\r   Progress: {percent:.1f}% "
                                f"({downloaded:,} / {total_size:,} bytes)",
                                end="",
                            )

                print()  # New line after progress

            download_with_progress(TWEMOJI_ZIP_URL, zip_path)
            print("✅ Download complete")

            # Extract ZIP file
            print("📦 Extracting SVG files...")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                # Find SVG files in the archive
                svg_files = [
                    f for f in zip_ref.namelist() if f.endswith(".svg") and "/svg/" in f
                ]
                print(f"   Found {len(svg_files)} SVG files")

                # Create target directory
                self.twemoji_dir.mkdir(parents=True, exist_ok=True)

                # Extract SVG files
                extracted = 0
                for svg_file in svg_files:
                    filename = os.path.basename(svg_file)
                    if filename:  # Skip directories
                        source = zip_ref.open(svg_file)
                        target = self.twemoji_dir / filename

                        with open(target, "wb") as f:
                            f.write(source.read())

                        extracted += 1
                        if extracted % 500 == 0:
                            print(
                                f"\r   Extracted: {extracted}/{len(svg_files)} files",
                                end="",
                            )

                print(f"\r   Extracted: {extracted}/{len(svg_files)} files")

            print("✅ Extraction complete")

            # Clean up
            shutil.rmtree(temp_dir)
            print("🧹 Cleaned up temporary files")

            return True

        except Exception as e:
            print(f"❌ Error downloading Twemoji: {e}")
            # Clean up on error
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            return False

    def download_minimal_emoji_set(self) -> bool:
        """Download only the most common emojis (lighter option)."""
        print("📥 Downloading minimal emoji set...")

        # Most common emojis (can be extended)
        common_emojis = [
            "1f600",
            "1f601",
            "1f602",
            "1f603",
            "1f604",
            "1f605",
            "1f606",
            "1f607",  # Smileys
            "1f44d",
            "1f44e",
            "1f44f",
            "1f64f",  # Hands
            "2764",
            "1f494",
            "1f495",
            "1f496",
            "1f497",  # Hearts
            "1f4a1",
            "1f4a5",
            "1f4a9",
            "1f4af",  # Symbols
            "1f525",
            "1f4a7",
            "2b50",
            "1f31f",  # Nature
            "1f389",
            "1f38a",
            "1f388",
            "1f387",  # Celebration
            "1f4bb",
            "1f4bc",
            "1f4bd",
            "1f4be",  # Tech
            "2705",
            "274c",
            "2714",
            "2716",  # Checkmarks
        ]

        self.twemoji_dir.mkdir(parents=True, exist_ok=True)

        downloaded = 0
        failed = 0

        for emoji_code in common_emojis:
            url = f"{TWEMOJI_CDN_BASE}{emoji_code}.svg"
            dest = self.twemoji_dir / f"{emoji_code}.svg"

            try:
                if not validate_url(url):  # nosec B310 - URL validation added
                    raise ValueError(f"Invalid URL scheme or domain: {url}")
                urllib.request.urlretrieve(
                    url, dest
                )  # nosec B310 - URL validated above
                downloaded += 1
                print(
                    f"\r   Downloaded: {downloaded}/{len(common_emojis)} emojis", end=""
                )
            except Exception:
                failed += 1

        print(f"\n✅ Downloaded {downloaded} emojis ({failed} failed)")
        return downloaded > 0

    def setup_all(self, minimal: bool = False) -> bool:
        """Run complete asset setup."""
        print("=" * 60)
        print("MD2PDF Asset Setup")
        print("=" * 60)

        # Check existing assets
        status = self.check_existing_assets()

        print("\nCurrent status:")
        if status["twemoji"]["installed"]:
            print(f"  • Twemoji: ✅ Installed ({status['twemoji']['count']} files)")
        else:
            print(f"  • Twemoji: ❌ Not installed")

        print("\nSetup options:")
        print("1. Download full Twemoji pack (~16MB, 3600+ emojis)")
        print("2. Download minimal emoji set (<1MB, ~50 common emojis)")
        print("3. Skip emoji setup (use CDN fallback)")
        print("4. Exit")

        choice = input("\nSelect option (1-4): ").strip()

        if choice == "1":
            success = self.download_twemoji_pack()
        elif choice == "2":
            success = self.download_minimal_emoji_set()
        elif choice == "3":
            print("ℹ️  Skipping emoji setup. Emojis will load from CDN when available.")
            success = True
        else:
            print("Exiting...")
            return False

        if success:
            print("\n" + "=" * 60)
            print("✅ Asset setup complete!")
            print("=" * 60)

            # Show final status
            final_status = self.check_existing_assets()
            if final_status["twemoji"]["installed"]:
                print(f"Twemoji SVGs: {final_status['twemoji']['count']} files")
                size_mb = sum(
                    f.stat().st_size
                    for f in Path(final_status["twemoji"]["path"]).glob("*.svg")
                ) / (1024 * 1024)
                print(f"Total size: {size_mb:.1f}MB")

        return success


def main() -> None:
    """Main entry point for asset setup."""
    setup = AssetSetup()

    # Check if running as part of package installation
    if len(sys.argv) > 1:
        if sys.argv[1] == "--minimal":
            setup.download_minimal_emoji_set()
        elif sys.argv[1] == "--full":
            setup.download_twemoji_pack(force=True)
        elif sys.argv[1] == "--check":
            status = setup.check_existing_assets()
            print(json.dumps(status, indent=2))
    else:
        # Interactive setup
        setup.setup_all()


if __name__ == "__main__":
    main()
