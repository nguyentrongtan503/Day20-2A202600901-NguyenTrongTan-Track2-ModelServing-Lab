import os
import sys
import json
import requests
from pathlib import Path

TIER_KEY = "Qwen2.5-1.5B-Instruct"
REPO_ID = "Qwen/Qwen2.5-1.5B-Instruct-GGUF"
Q4_FILE = "qwen2.5-1.5b-instruct-q4_k_m.gguf"
Q2_FILE = "qwen2.5-1.5b-instruct-q2_k.gguf"

Q4_URL = f"https://hf-mirror.com/{REPO_ID}/resolve/main/{Q4_FILE}"
Q2_URL = f"https://hf-mirror.com/{REPO_ID}/resolve/main/{Q2_FILE}"

def download_file(url: str, dest_path: Path):
    print(f"Starting download: {url} -> {dest_path}")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    chunk_size = 1024 * 1024  # 1 MB
    downloaded = 0
    
    # Ensure parent dir exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"Downloaded {downloaded / (1024*1024):.1f} MB / {total_size / (1024*1024):.1f} MB ({percent:.1f}%)", flush=True)
                else:
                    print(f"Downloaded {downloaded / (1024*1024):.1f} MB", flush=True)
    print(f"Completed download: {dest_path}")

def main():
    out_dir = Path("models")
    out_dir.mkdir(exist_ok=True)
    
    q4_dest = out_dir / Q4_FILE
    q2_dest = out_dir / Q2_FILE
    
    try:
        if not q4_dest.exists():
            download_file(Q4_URL, q4_dest)
        else:
            print(f"{Q4_FILE} already exists. Skipping.")
            
        if not q2_dest.exists():
            download_file(Q2_URL, q2_dest)
        else:
            print(f"{Q2_FILE} already exists. Skipping.")
            
        config = {
            "tier": TIER_KEY,
            "repo_id": REPO_ID,
            "primary_model": str(q4_dest),
            "compare_model": str(q2_dest),
        }
        
        active_json = out_dir / "active.json"
        active_json.write_text(json.dumps(config, indent=2))
        print(f"Wrote {active_json}")
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
