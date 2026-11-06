FROM pytorch/pytorch:2.4.1-cuda12.1-cudnn9-runtime
RUN python -m pip install --no-cache-dir --no-deps numpy==1.26.4 faiss-gpu-cu12==1.9.0.post1
WORKDIR /work
ENV OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONUNBUFFERED=1
CMD ["python", "benchmark.py"]
