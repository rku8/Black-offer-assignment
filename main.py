"""
This entry point for project execution
"""
from src.pipeline.execute_pipeline import ExecutePipeline

if __name__=="__main__":
    pipeline = ExecutePipeline()
    pipeline.run_pipeline()

