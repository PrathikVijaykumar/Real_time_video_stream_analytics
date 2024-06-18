
import os
import time

from databricks.sdk import WorkspaceClient
from databricks.sdk.service import jobs
from databricks.sdk.service import compute

import threading

w = WorkspaceClient(host='https://dbc-36749aba-9ce7.cloud.databricks.com',
                    token='dapi5e26c901a014ed8c0f7703f12998931d',)
cluster_id = '0611-171531-xjscbdfg'
notebook_path = '/Workspace/Users/vprathik3010@gmail.com/demo'  ## notebook path, dont give extension
## make changes in notebook and then give path here

def task():
    run = w.jobs.submit(run_name=f'sdk-{time.time_ns()}',
                        tasks=[
                            jobs.SubmitTask(existing_cluster_id=cluster_id,
                                            notebook_task=jobs.NotebookTask(notebook_path=notebook_path),
                                            task_key=f'sdk-{time.time_ns()}')
                        ]).result()
    return 


def run_job():
    t1 = threading.Thread(target=task, args=())
    t1.start()
    return 