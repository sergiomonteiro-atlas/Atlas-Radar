FROM python:3.12-slim

WORKDIR /app
COPY backend ./backend
COPY web ./web

RUN mkdir -p /app/data

ENV ATLAS_RADAR_HOST=0.0.0.0
ENV ATLAS_RADAR_PORT=8787

EXPOSE 8787
CMD ["python", "backend/server.py"]
