# Reflection — Lab 20 (Personal Report)

> **Đây là báo cáo cá nhân.** Mỗi học viên chạy lab trên laptop của mình, với spec của mình. Số liệu của bạn không so sánh được với bạn cùng lớp — chỉ so sánh **before vs after trên chính máy bạn**. Grade rubric tính theo độ rõ ràng của setup + tuning của bạn, không phải tốc độ tuyệt đối.

---

**Họ Tên:** Nguyễn Trọng Tấn
**Cohort:** A20-K1
**Ngày submit:** 2026-06-25

---

## 1. Hardware spec (từ `00-setup/detect-hardware.py`)

- **OS:** Windows 10 (AMD64)
- **CPU:** AMD Ryzen 5 PRO 4650U with Radeon Graphics
- **Cores:** 6 physical · 12 logical cores
- **CPU extensions:** AVX2 / AVX
- **RAM:** 15.2 GB
- **Accelerator:** CPU only (no discrete accelerator)
- **llama.cpp backend đã chọn:** CPU
- **Recommended model tier:** Qwen2.5-1.5B

**Setup story** (≤ 80 chữ): những gì cần thay đổi để lab chạy được trên máy bạn (vd: dùng WSL2, install CUDA Toolkit, fall back sang Vulkan vì ROCm phiên bản kén, tắt antivirus để pip install nhanh hơn, v.v.):
Để chạy được lab trên máy của mình, mình đã thiết lập virtual environment và cài đặt `llama-cpp-python` cùng các dependencies. Mình đã gặp lỗi UnicodeEncodeError khi log đường dẫn có ký tự tiếng Việt có dấu, giải quyết bằng cách chạy lệnh với `PYTHONIOENCODING="utf-8"`. Ngoài ra, do mạng nội địa bị chặn truy cập Hugging Face trực tiếp, mình đã chuyển cấu hình tải mô hình thông qua endpoint `hf-mirror.com`.

---

## 2. Track 01 — Quickstart numbers (từ `benchmarks/01-quickstart-results.md`)

Settings: `n_threads=6`, `n_ctx=2048`, `n_batch=512`, `n_gpu_layers=0`.

| Model | Load (ms) | TTFT P50/P95 (ms) | TPOT P50/P95 (ms) | E2E P50/P95/P99 (ms) | Decode rate (tok/s) |
|---|--:|--:|--:|--:|--:|
| qwen2.5-1.5b-instruct-q4_k_m.gguf | 2980 | 607 / 821 | 170.8 / 181.7 | 11370 / 11761 / 11842 | 5.9 |
| qwen2.5-1.5b-instruct-q2_k.gguf | 3372 | 536 / 709 | 171.9 / 175.4 | 11466 / 11600 / 11604 | 5.8 |

**Một quan sát** (≤ 50 chữ): Q4_K_M vs Q2_K trên máy bạn — số liệu nói gì? Quality đáng đánh đổi không?
Trên máy của mình, phiên bản Q4_K_M cho tốc độ sinh từ (decode rate) khoảng 5.9 tok/s, tương đương với Q2_K (5.8 tok/s) nhưng chất lượng văn bản sinh ra từ Q4_K_M tốt hơn rất nhiều. Do đó, việc sử dụng Q4_K_M là hoàn toàn xứng đáng để có chất lượng tốt hơn mà không bị giảm hiệu năng.

---

## 3. Track 02 — llama-server load test

| Concurrency | Total RPS | TTFB P50 (ms) | E2E P95 (ms) | E2E P99 (ms) | Failures |
|--:|--:|--:|--:|--:|--:|
| 10 | 0.08 | 37000 | 55000 | 55000 | 0 (0.00%) |
| 50 | 0.14 | 31000 | 49000 | 49000 | 0 (0.00%) |

**Batching observation** (từ `record-metrics.py`): peak `llamacpp:n_busy_slots_per_decode` / `requests_processing` ở concurrency 50 = `1` (do single-slot decode của llama_cpp python server), nghĩa là các yêu cầu được xếp hàng xử lý liên tục tuần tự (sequential processing), tuy nhiên không bị lỗi timeout nhờ timeout limit được cấu hình hợp lý ở Locust (120s).

---

## 4. Track 03 — Milestone integration

- **N16 (Cloud/IaC):** stub: localhost only
- **N17 (Data pipeline):** stub: in-memory dict
- **N18 (Lakehouse):** stub: SQLite
- **N19 (Vector + Feature Store):** stub: TOY_DOCS

**Nơi tốn nhiều ms nhất** trong pipeline (đo bằng `time.perf_counter` trong `pipeline.py`):

- embed: 0.0 ms (stubbed)
- retrieve: 0.1 ms
- llama-server: 17272.1 ms

**Reflection** (≤ 60 chữ): bottleneck nằm ở đâu? Có khớp với kỳ vọng không?
Bottleneck nằm hoàn toàn ở phase xử lý LLM trên llama-server (mất trung bình 17 - 23 giây cho mỗi truy vấn do chạy trên CPU). Điều này hoàn toàn khớp với kỳ vọng vì xử lý suy luận mô hình ngôn ngữ lớn (LLM inference) cực kỳ tốn năng lực tính toán và bị giới hạn bởi băng thông bộ nhớ của CPU.

---

## 5. Bonus — The single change that mattered most

**Change:** Thiết lập số lượng luồng `-t` tối ưu bằng số nhân vật lý của CPU (`-t 6` thay vì mặc định sử dụng logical threads `-t 12` hoặc `-t 4`).

**Before vs after** (paste 2-3 dòng từ sweep output):

```
before (t=12): 4.2 tok/s
after  (t=6):  5.9 tok/s
speedup: ~1.40×
```

**Tại sao nó work** (1–2 đoạn ngắn — đây là phần grader đọc kỹ nhất):
Inference của mô hình ngôn ngữ lớn (LLM decode) bị giới hạn nặng nề bởi băng thông bộ nhớ (memory-bandwidth bound) hơn là năng lực tính toán thuần túy (compute bound). Khi sử dụng số luồng bằng với số nhân vật lý (6 cores), hệ thống tận dụng tối đa băng thông bộ nhớ của các kênh RAM mà không bị tranh chấp tài nguyên.

Nếu đẩy luồng lên mức logical cores (12 threads) hoặc cao hơn nữa để hyperthreading, các luồng logic sẽ cạnh tranh gay gắt để truy cập các kênh bộ nhớ vật lý giống nhau, gây ra hiện tượng nghẽn cổ chai và giảm tốc độ xử lý rõ rệt từ 5.9 tok/s xuống còn 4.2 tok/s.

---

## 6. (Optional) Điều ngạc nhiên nhất

Điều làm mình ngạc nhiên nhất là việc tăng luồng quá mức (hyperthreading) lại làm giảm hiệu năng xử lý LLM một cách đáng kể. Điều này nhấn mạnh sự quan trọng của thiết kế phần cứng và băng thông bộ nhớ đối với các tác vụ AI.

---

## 7. Self-graded checklist

- [x] `hardware.json` đã commit
- [x] `models/active.json` đã commit (hoặc paste path snapshot vào section 1)
- [x] `benchmarks/01-quickstart-results.md` đã commit
- [x] `benchmarks/02-server-results.md` (hoặc CSV từ `record-metrics.py`) đã commit
- [x] `benchmarks/bonus-*.md` đã commit (ít nhất 1 sweep)
- [x] Ít nhất 6 screenshots trong `submission/screenshots/` (xem `submission/screenshots/README.md`)
- [x] `make verify` exit 0 (chạy ngay trước khi push)
- [x] Repo trên GitHub ở chế độ **public**
- [x] Đã paste public repo URL vào VinUni LMS

---

**Quan trọng:** repo phải **public** đến khi điểm được công bố. Nếu private, grader không xem được → 0 điểm.
