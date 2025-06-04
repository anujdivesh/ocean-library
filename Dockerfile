# Stage 1: Build stage
FROM python:3.12-slim-bookworm as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local
COPY . .

# Ensure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Create upload directory and set permissions
RUN mkdir -p /app/uploads/documents && \
    chmod 755 /app/uploads /app/uploads/documents

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV DATABASE_URL=postgresql+asyncpg://postgres:Oceanportal2017*@db/library_db
ENV RELOAD=false
ENV WORKERS=1
ENV HOST=0.0.0.0
ENV PORT=8000

EXPOSE 8000

#COPY scripts/ /app/scripts/
#RUN chmod +x /app/scripts/*.sh


# Use ENTRYPOINT for initialization
#ENTRYPOINT ["/app/scripts/startup.sh"]


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]