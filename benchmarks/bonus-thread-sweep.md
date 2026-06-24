# Bonus — Thread sweep

Model: `qwen2.5-1.5b-instruct-q4_k_m.gguf`  ·  GPU layers: `0`

| threads | tg128 (tok/s) |
|---:|---:|
| 1 | 2.5 |
| 2 | 4.8 |
| 3 | 5.5 |
| 6 | 5.9 |
| 12 | 4.2 |
| 24 | 2.8 |

**Best**: `-t 6` at 5.9 tok/s.

Look at the curve. If it peaks around your **physical** core count and drops as you go higher, that's the memory-bandwidth ceiling: extra threads fight over the same memory channels and slow each other down.
