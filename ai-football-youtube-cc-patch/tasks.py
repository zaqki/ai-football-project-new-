from invoke import task

@task
def setup(c):
    c.run("python -m venv venv && . venv/bin/activate && pip install -r requirements.txt || true", pty=True)

@task
def ingest(c): c.run("python data_pipeline/ingest.py", pty=True)

@task
def normalize(c): c.run("python data_pipeline/normalize.py", pty=True)

@task
def scout(c): c.run("python data_pipeline/scouting_agent.py", pty=True)

@task
def search(c): c.run("python clip_finder/search_clips.py", pty=True)

@task
def rights(c): c.run("python clip_finder/rights_check.py", pty=True)

@task
def download(c): c.run("python clip_finder/download.py", pty=True)

@task
def edit(c): c.run("python video_editing/edit_video.py", pty=True)

@task
def export(c): c.run("python video_editing/export_variants.py", pty=True)

@task
def qc(c): c.run("python video_editing/qc_check.py", pty=True)

@task
def meta(c): c.run("python publishing/metadata_agent.py", pty=True)

@task
def schedule(c): c.run("python publishing/scheduler.py", pty=True)

@task
def community(c): c.run("python publishing/community_manager.py", pty=True)

@task
def analytics(c): c.run("python analytics/track_performance.py", pty=True)

@task
def feedback(c): c.run("python analytics/feedback_loop.py", pty=True)

@task
def run_all(c):
    for t in ["ingest","normalize","scout","search","rights","download","edit","export","qc","meta","schedule","community","analytics","feedback"]:
        c.run(f"invoke {t}", pty=True)
    print("✅ Pipeline completed (stub).")

@task
def clean(c):
    c.run("rm -rf data out __pycache__ */__pycache__", pty=True)
