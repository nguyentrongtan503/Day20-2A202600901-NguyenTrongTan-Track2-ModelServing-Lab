# 02 — Server Load Test Results

## Concurrency 10 Users
- **Total Requests**: 5
- **RPS**: 0.08
- **Avg Response Time**: 34,851 ms
- **Min Response Time**: 13,466 ms
- **Max Response Time**: 55,359 ms
- **P50 Response Time**: 37,000 ms
- **P95 Response Time**: 55,000 ms
- **P99 Response Time**: 55,000 ms
- **Failures**: 0 (0.00%)

## Concurrency 50 Users
- **Total Requests**: 8
- **RPS**: 0.14
- **Avg Response Time**: 27,491 ms
- **Min Response Time**: 3,916 ms
- **Max Response Time**: 49,377 ms
- **P50 Response Time**: 31,000 ms
- **P95 Response Time**: 49,000 ms
- **P99 Response Time**: 49,000 ms
- **Failures**: 0 (0.00%)

## Observations
Under concurrent load on a CPU-only architecture, the response times are relatively high since the CPU physical cores are shared across user slots and the model (Phi-3 3.8B) is heavy. However, because continuous batching is used, all requests are scheduled and completed successfully with 0% failure rate under both 10 and 50 users.
