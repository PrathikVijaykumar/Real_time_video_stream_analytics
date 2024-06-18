import os
import time

from databricks.sdk import WorkspaceClient
# from databricks.sdk.service import jobs
# from databricks.sdk.service import compute

client = WorkspaceClient(host='https://dbc-XXXXX.cloud.databricks.com',
                    token='XXXXXXX',)
                    #account_id='5dd99c18-a90c-4861-b731-6c8886dd7d14',
                    #username='vprathik3010@gmail.com',password='Pilot@1964')
                    #host = workspace_URL

cluster_id = '0611-171531-xjscbdfg'  ## cluster id  (cluster -> more -> view json -> cluster id)

# cluster_id = w.clusters.ensure_cluster_is_running('0611-171531-xjscbdfg')
# clusters = w.clusters.list()

# for cl in clusters:
#     print(f' - {cl.cluster_id} is {cl.state}')



import requests
import json
import time

def terminate_cluster(cluster_id):
    # Define the endpoint for terminating a cluster
    endpoint = f"/api/2.0/clusters/delete"
    
    # Define the URL for the Databricks API
    domain = 'https://dbc-XXXXX.cloud.databricks.com' ### workspace_URL
    token = 'XXXXXXX'

    headers = {'Content-Type': 'application/json;charset=UTF-8',
                'Authorization': f'Bearer {token}'}
    
    # Define the JSON payload for terminating the cluster
    payload = {
        "cluster_id": cluster_id,
        "terminate": True
    }

    # Send the request to the Databricks API
    response = requests.post(domain + endpoint, headers=headers, data=json.dumps(payload))

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Cluster {cluster_id} terminated successfully.")
    else:
        print(f"Failed to terminate Cluster {cluster_id}.")
        print(response.content)



def start_cluster(cluster_id):
    # Define the endpoint for terminating a cluster
    endpoint = f"/api/2.0/clusters/start"
    
    # Define the URL for the Databricks API
    domain = 'https://dbc-XXXXX.cloud.databricks.com' ### workspace_URL
    token = 'XXXXXXX'

    headers = {'Content-Type': 'application/json;charset=UTF-8',
                'Authorization': f'Bearer {token}'}
    
    # Define the JSON payload for terminating the cluster
    payload = {
        "cluster_id": cluster_id,
        "terminate": True
    }

    # Send the request to the Databricks API
    response = requests.post(domain + endpoint, headers=headers, data=json.dumps(payload))

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Cluster {cluster_id} started successfully.")
    else:
        print(f"Failed to start Cluster {cluster_id}.")
        print(response.content)


# terminate_cluster('0611-171531-xjscbdfg')

# clusters = w.clusters.list()

# for cl in clusters:
#     print(f' - {cl.cluster_id} is {cl.state}')