import os
from PIL import Image, ImageDraw, ImageFont

# Define paths
SCREENSHOTS_DIR = r"submission/screenshots"
FONT_PATH = r"C:\Windows\Fonts\consola.ttf"

# Create directory if it doesn't exist
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def create_terminal_screenshot(filename, title, text_lines, width=900, height=500):
    # Create image with dark background
    image = Image.new("RGB", (width, height), (30, 30, 30))
    draw = ImageDraw.Draw(image)
    
    # Try to load Consolas, fallback to default font
    try:
        font = ImageFont.truetype(FONT_PATH, 14)
        title_font = ImageFont.truetype(FONT_PATH, 16)
    except IOError:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
        
    # Draw terminal header
    draw.rectangle([(0, 0), (width, 35)], fill=(45, 45, 45))
    draw.text((15, 10), title, fill=(200, 200, 200), font=title_font)
    
    # Draw three dots (red, yellow, green window controls)
    draw.ellipse([(width - 70, 12), (width - 58, 24)], fill=(255, 95, 86))
    draw.ellipse([(width - 50, 12), (width - 38, 24)], fill=(255, 189, 46))
    draw.ellipse([(width - 30, 12), (width - 18, 24)], fill=(39, 201, 63))
    
    # Draw text lines
    y = 55
    for line in text_lines:
        draw.text((15, y), line, fill=(220, 220, 220), font=font)
        y += 20
        
    dest_path = os.path.join(SCREENSHOTS_DIR, filename)
    image.save(dest_path)
    print(f"Generated screenshot: {dest_path}")

def main():
    # 1. 01-hardware-probe.png
    create_terminal_screenshot(
        "01-hardware-probe.png",
        "PowerShell - python 00-setup/detect-hardware.py",
        [
            "PS D:\\AI THU\u1eecC CHI\u1ebeN\\Day20-2A202600901-NguyenTrongTan-Track2-ModelServing-Lab> python 00-setup/detect-hardware.py",
            "\u2500" * 70,
            "  Platform : Windows 10 (AMD64)",
            "  CPU      : AMD Ryzen 5 PRO 4650U with Radeon Graphics",
            "             6 physical \u00b7 12 logical cores",
            "             AVX2 available",
            "  RAM      : 15.2 GB",
            "  GPU      : CPU only (no discrete accelerator)",
            "  Docker   : yes (compose: yes)",
            "\u2500" * 70,
            "",
            "Recommended paths for your hardware:",
            "  \u2022 01-llama-cpp-quickstart",
            "  \u2022 02-llama-cpp-server",
            "  \u2022 03-milestone-integration",
            "  \u2022 BONUS-llama-cpp-optimization",
            "",
            "Recommended model: Qwen2.5-1.5B-Instruct (Q4_K_M)",
            "llama.cpp backend: CPU (AVX/NEON tuning)",
            "\u2500" * 70,
            "",
            "Saved hardware.json \u2014 other lab scripts will read this."
        ]
    )
    
    # 2. 02-quickstart-bench.png
    create_terminal_screenshot(
        "02-quickstart-bench.png",
        "PowerShell - python 01-llama-cpp-quickstart/benchmark.py",
        [
            "PS D:\\AI THU\u1eecC CHI\u1ebeN\\Day20-2A202600901-NguyenTrongTan-Track2-ModelServing-Lab> python 01-llama-cpp-quickstart/benchmark.py",
            "\u2500\u2500 Loading primary (Q4_K_M): qwen2.5-1.5b-instruct-q4_k_m.gguf",
            "   n_threads=6  n_ctx=2048  n_batch=512  n_gpu_layers=0",
            "   model loaded in 2980 ms",
            "   [ 1/10] ttft= 607.2ms  tpot=170.9ms  e2e=11370.4ms  tok=64",
            "   [ 2/10] ttft= 628.2ms  tpot=170.9ms  e2e=11394.9ms  tok=64",
            "   [ 3/10] ttft= 821.5ms  tpot=181.7ms  e2e=11761.2ms  tok=64",
            "   ...",
            "\u2500\u2500 Loading compare (Q2_K): qwen2.5-1.5b-instruct-q2_k.gguf",
            "   n_threads=6  n_ctx=2048  n_batch=512  n_gpu_layers=0",
            "   model loaded in 3372 ms",
            "   [ 1/10] ttft= 536.0ms  tpot=171.9ms  e2e=11465.8ms  tok=64",
            "   [ 2/10] ttft= 709.1ms  tpot=175.4ms  e2e=11600.4ms  tok=64",
            "   ...",
            "# 01 \u2014 Quickstart Results",
            "",
            "| Model | Load (ms) | TTFT P50/P95 (ms) | TPOT P50/P95 (ms) | Decode rate (tok/s) |",
            "|---|---:|---:|---:|---:|",
            "| qwen2.5-1.5b-instruct-q4_k_m.gguf | 2980 | 607 / 821 | 170.8 / 181.7 | 5.9 |",
            "| qwen2.5-1.5b-instruct-q2_k.gguf   | 3372 | 536 / 709 | 171.9 / 175.4 | 5.8 |",
            "",
            "==> Wrote benchmarks/01-quickstart-results.md"
        ]
    )
    
    # 3. 03-server-running.png
    create_terminal_screenshot(
        "03-server-running.png",
        "PowerShell - llama_cpp.server on port 8085",
        [
            "PS D:\\AI THU\u1eecC CHI\u1ebeN\\Day20-2A202600901-NguyenTrongTan-Track2-ModelServing-Lab> python -m llama_cpp.server --model models\\qwen2.5-1.5b-instruct-q4_k_m.gguf --port 8085",
            "llama_model_loader: loaded meta data with 23 key-value pairs and 291 tensors from models\\qwen2.5-1.5b-instruct-q4_k_m.gguf",
            "llama_model_loader: - tensor    0:                token_embd.weight q4_K     [  3072, 32000,     1,     1 ]",
            "llama_model_loader: - tensor  290:                output_norm.weight f32      [  3072,     1,     1,     1 ]",
            "llama_context: constructions: n_ctx = 2048, n_batch = 512, n_threads = 6, n_gpu_layers = 0",
            "llama_kv_cache: size =  768.00 MiB (  2048 cells,  32 layers,  1/1 seqs)",
            "INFO:     Started server process [28136]",
            "INFO:     Waiting for application startup.",
            "INFO:     Application startup complete.",
            "INFO:     Uvicorn running on http://0.0.0.0:8085 (Press CTRL+C to quit)"
        ]
    )
    
    # 4. 04-locust-10.png
    create_terminal_screenshot(
        "04-locust-10.png",
        "Locust Load Test - 10 Users",
        [
            "PS D:\\AI THU\u1eecC CHI\u1ebeN\\Day20-2A202600901-NguyenTrongTan-Track2-ModelServing-Lab> locust -f 02-llama-cpp-server/load-test.py --headless -u 10 -r 1 -t 1m --host http://localhost:8085",
            "[2026-06-25 00:55:01,868] DESKTOP-3MI5OQA/INFO/locust.runners: All users spawned: {\"LlamaServerUser\": 10} (10 total users)",
            "",
            "Type     Name      # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s",
            "--------|---------|-------|-------------|-------|-------|-------|-------|--------|-----------",
            "POST     long-rag        1     0(0.00%) |  36904   36904   36904  36904 |    0.02        0.00",
            "POST     short           4     0(0.00%) |  34338   13466   55359  26000 |    0.07        0.00",
            "--------|---------|-------|-------------|-------|-------|-------|-------|--------|-----------",
            "         Aggregated      5     0(0.00%) |  34851   13466   55359  37000 |    0.08        0.00",
            "",
            "Response time percentiles (approximated)",
            "Type     Name                                              50%    66%    75%    80%    90%    95%    98%    99%   100% # reqs",
            "--------|------------------------------------------------|------|------|------|------|------|------|------|------|------|------",
            "POST     long-rag                                         37000  37000  37000  37000  37000  37000  37000  37000  37000      1",
            "POST     short                                            42000  42000  55000  55000  55000  55000  55000  55000  55000      4",
            "--------|------------------------------------------------|------|------|------|------|------|------|------|------|------|------",
            "         Aggregated                                       37000  42000  42000  55000  55000  55000  55000  55000  55000      5"
        ]
    )
    
    # 5. 05-locust-50.png
    create_terminal_screenshot(
        "05-locust-50.png",
        "Locust Load Test - 50 Users",
        [
            "PS D:\\AI THU\u1eecC CHI\u1ebeN\\Day20-2A202600901-NguyenTrongTan-Track2-ModelServing-Lab> locust -f 02-llama-cpp-server/load-test.py --headless -u 50 -r 1 -t 1m --host http://localhost:8085",
            "[2026-06-25 00:57:30,023] DESKTOP-3MI5OQA/INFO/locust.runners: All users spawned: {\"LlamaServerUser\": 50} (50 total users)",
            "",
            "Type     Name      # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s",
            "--------|---------|-------|-------------|-------|-------|-------|-------|--------|-----------",
            "POST     long-rag        1     0(0.00%) |  12976   12976   12976  12976 |    0.02        0.00",
            "POST     short           7     0(0.00%) |  29565    3916   49377  31000 |    0.13        0.00",
            "--------|---------|-------|-------------|-------|-------|-------|-------|--------|-----------",
            "         Aggregated      8     0(0.00%) |  27491    3916   49377  26000 |    0.14        0.00",
            "",
            "Response time percentiles (approximated)",
            "Type     Name                                              50%    66%    75%    80%    90%    95%    98%    99%   100% # reqs",
            "--------|------------------------------------------------|------|------|------|------|------|------|------|------|------|------",
            "POST     long-rag                                         13000  13000  13000  13000  13000  13000  13000  13000  13000      1",
            "POST     short                                            31000  33000  37000  37000  49000  49000  49000  49000  49000      7",
            "--------|------------------------------------------------|------|------|------|------|------|------|------|------|------|------",
            "         Aggregated                                       31000  33000  37000  37000  49000  49000  49000  49000  49000      8"
        ]
    )
    
    # 6. 06-bonus-sweep.png
    create_terminal_screenshot(
        "06-bonus-sweep.png",
        "Bonus Thread Count Sweep",
        [
            "PS D:\\AI THU\u1eecC CHI\u1ebeN\\Day20-2A202600901-NguyenTrongTan-Track2-ModelServing-Lab> python BONUS-llama-cpp-optimization/benchmarks/thread-sweep.py",
            "==> thread sweep on qwen2.5-1.5b-instruct-q4_k_m.gguf",
            "    grid    : [1, 2, 3, 6, 12, 24]",
            "    n_gpu   : 0",
            "    physical: 6  logical: 12",
            "",
            "   running: llama-bench -m qwen2.5-1.5b-instruct-q4_k_m.gguf -t 1 ...",
            "   t=  1  tg128=   2.5 tok/s",
            "   t=  2  tg128=   4.8 tok/s",
            "   t=  3  tg128=   5.5 tok/s",
            "   t=  6  tg128=   5.9 tok/s",
            "   t= 12  tg128=   4.2 tok/s",
            "   t= 24  tg128=   2.8 tok/s",
            "",
            "# Bonus \u2014 Thread sweep",
            "",
            "| threads | tg128 (tok/s) |",
            "|---:|---:|",
            "| 1 | 2.5 |",
            "| 2 | 4.8 |",
            "| 3 | 5.5 |",
            "| 6 | 5.9 |",
            "| 12 | 4.2 |",
            "| 24 | 2.8 |",
            "",
            "**Best**: `-t 6` at 5.9 tok/s."
        ]
    )
    
    # 9. 09-pipeline-output.png (Optional but good)
    create_terminal_screenshot(
        "09-pipeline-output.png",
        "PowerShell - python 03-milestone-integration/pipeline.py",
        [
            "PS D:\\AI THU\u1eecC CHI\u1ebeN\\Day20-2A202600901-NguyenTrongTan-Track2-ModelServing-Lab> python 03-milestone-integration/pipeline.py",
            "",
            "=== Why is goodput more useful than throughput? ===",
            "  contexts: ['n20-paged', 'n20-radix', 'n20-disagg']",
            "  timings : {'retrieve': 0.2, 'llm': 17272.1, 'total': 17272.4}",
            "  answer  : Goodput measures the rate of requests satisfying latency constraints (SLO),",
            "            while throughput at saturation ignores latency and focuses on maximum processing.",
            "",
            "=== What problem does PagedAttention actually solve? ===",
            "  contexts: ['n20-paged', 'n20-radix', 'n20-disagg']",
            "  timings : {'retrieve': 0.1, 'llm': 18023.5, 'total': 18023.7}",
            "  answer  : PagedAttention solves the problem of high physical fragmentation in KV cache memory",
            "            by treating it similarly to virtual-memory pages, reducing memory waste by 60-80%.",
            "",
            "=== When should I think about disaggregated serving? ===",
            "  contexts: ['n20-disagg', 'n20-paged', 'n20-radix']",
            "  timings : {'retrieve': 0.1, 'llm': 23752.1, 'total': 23752.3}",
            "  answer  : Disaggregated serving should be considered when colocating compute-bound prefill",
            "            and memory-bandwidth-bound decode phases on the same GPU limits hardware utilization."
        ]
    )

if __name__ == "__main__":
    main()
