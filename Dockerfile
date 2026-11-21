FROM python:3.15@sha256:46837ed3105db0029b6d656816185c6258e3b39690532fb782428e0a5fd76182
WORKDIR /app
COPY requirements.txt .
RUN pip install --require-hashes --no-cache-dir -r requirements.txt
COPY project.py .
COPY hivebox.py .
CMD ["python", "-m", "flask", "--app", "./hivebox.py", "run", "--host=0.0.0.0"]
