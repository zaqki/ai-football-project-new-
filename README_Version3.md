## 🏃‍♂️ Manual Pipeline Run (from Repo Root)

### 1. Environment Setup

```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 2. Generate Shortlist (Stub Example)

```sh
python data_pipeline/ingest.py
python data_pipeline/normalize.py
python data_pipeline/scouting_agent.py
```

---

### 3. Search and Download CC Videos

```sh
python clip_finder/search_clips.py --max-per-query 3
python clip_finder/download.py --max-duration 120 --limit 5
```

---

### 4. Create a ~60s Edit

```sh
python video_editing/edit_video.py --target-seconds 60
```