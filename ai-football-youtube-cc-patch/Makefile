# Makefile for AI Football Project
# Usage examples:
#   make setup
#   make run_all
#   make ingest scout search download edit export qc meta schedule analytics feedback

PY := python

.PHONY: setup ingest normalize scout search rights download edit export qc meta schedule community analytics feedback run_all clean

setup:
	$(PY) -m venv venv && . venv/bin/activate && pip install -r requirements.txt || true

ingest:
	$(PY) data_pipeline/ingest.py

normalize:
	$(PY) data_pipeline/normalize.py

scout:
	$(PY) data_pipeline/scouting_agent.py

search:
	$(PY) clip_finder/search_clips.py

rights:
	$(PY) clip_finder/rights_check.py

download:
	$(PY) clip_finder/download.py

edit:
	$(PY) video_editing/edit_video.py

export:
	$(PY) video_editing/export_variants.py

qc:
	$(PY) video_editing/qc_check.py

meta:
	$(PY) publishing/metadata_agent.py

schedule:
	$(PY) publishing/scheduler.py

community:
	$(PY) publishing/community_manager.py

analytics:
	$(PY) analytics/track_performance.py

feedback:
	$(PY) analytics/feedback_loop.py

run_all: ingest normalize scout search rights download edit export qc meta schedule community analytics feedback
	@echo "✅ Pipeline completed (stub)."

clean:
	rm -rf data out __pycache__ */__pycache__
