import streamlit as st
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
import io
import boto3
import time


st.title("Realtime computer vision stream project")
st.text("By Prathik Vijaykumar")


# Static "How to use" section
if 'file' not in st.session_state:
    st.session_state.file = False
if 'upload' not in st.session_state:
    st.session_state.upload = False
if 'show_video' not in st.session_state:
    st.session_state.show_video = False

if 'cluster_status' not in st.session_state:
    st.session_state.cluster_status = False


with st.container():
    st.subheader("Cluster Information", divider='rainbow')

    def cluster_start():
        url = 'http://localhost:5003/cluster'
        params = {'operation':'start'}
        res = requests.post(url=url, data = params)
        res = res.json()
        if res['status']=='success':
            st.write(res['message'])
        else:
            st.write(res['message'])
    def cluster_terminate():
        url = 'http://localhost:5003/cluster'
        params = {'operation':'terminate'}
        res = requests.post(url=url, data = params)
        res = res.json()
        if res['status']=='success':
            st.write(res['message'])
        else:
            st.write(res['message'])
    def get_cluster_status():
        url = 'http://localhost:5003/cluster_status'
        res = requests.get(url=url)
        res = res.json()
        st.session_state.cluster_status = res['status']
        st.write('cluster is :',res['status'])


    start , terminate , status =  st.columns(3)

    start.button('start cluster',on_click= cluster_start)

    terminate.button('terminate cluster',on_click =cluster_terminate)

    status.button('cluster status',on_click =get_cluster_status)



with st.container():
    import io


    st.subheader("Upload File", divider='rainbow')

    uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])

    def show_video_fn():
        print('show video clicked')
        st.session_state.show_video = True
        print(st.session_state.show_video , st.session_state.upload , st.session_state.file)       
        if st.session_state.show_video and st.session_state.upload and st.session_state.file:
            st.video('test.mp4')


    def upload_fn():
        print('upload button clicked')
        if not st.session_state.file:
            st.write('please select the file before uploading...')
        else:
            st.session_state.upload = True

        if st.session_state.upload and st.session_state.file:
            print('file saved')
            g = io.BytesIO(uploaded_file.read())  ## BytesIO Object
            temporary_location = "test.mp4"

            with open(temporary_location, 'wb') as out:  ## Open temporary file as bytes
                out.write(g.read())  ## Read bytes into file

            # close file
            out.close()

            url = 'http://localhost:5003/upload'
            params = {'file_path':'test.mp4'}
            res = requests.post(url=url, data = params)
            res = res.json()
        else:
            st.write('please select file and upload!..........')




    def reset_fn():
        print('reset button clicked')
        global uploaded_file 
        uploaded_file  = None
        st.session_state.file = False
        st.session_state.upload = False
        st.session_state.show_video = False
        try:
            os.remove('test.mp4')
        except:
            pass
        try:
            os.remove('output_video.mp4')
        except:
            pass
        
    if uploaded_file is not None:
        print('file true')
        st.session_state.file = True

    clicked , show_video , reset =  st.columns(3)

    clicked.button('upload',on_click= upload_fn)

    show_video.button('show',on_click =show_video_fn)

    reset.button('reset',on_click =reset_fn)


with st.container():
    st.subheader("Run Databricks Job and see the result", divider='rainbow')
    def download_file_fn():
        url = 'http://localhost:5003/download'
        res = requests.get(url=url)
        res = res.json()
        if res['status']=='success':
            st.write('downloading files is:',res['status'])
        else:
            st.write('downloading files is:',res['status'])
    def show_file_fn():
        if os.path.exists('output_video.mp4'):
            st.video('output_video.mp4')
        time.sleep(2)  # Add a delay of 2 seconds
        show_graphs()
    def run_job_fn():
        url = 'http://localhost:5003/job'
        res = requests.get(url=url)
        res = res.json()
        st.write(res['status'])
    def delete_videos_fn():
        url = 'http://localhost:5003/delete'
        res = requests.get(url=url)
        res = res.json()
        st.write('delete files :',res['status'])
    def show_graphs():
        # Load CSV file from S3
        os.environ['AWS_ACCESS_KEY_ID'] = 'XXXXX'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'XXXXXX'
        os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        s3 = session.client('s3')
        bucket_name = 'demo-test-pipeline'
        file_key = 'meta_info.csv'

        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        data = obj['Body'].read().decode('utf-8')
        df = pd.read_csv(io.StringIO(data))

        # Plot the graphs
        fig, ax = plt.subplots(2, 1, figsize=(10, 8))
        
        ax[0].plot(df['frame_id'], df['person_count'], label='Person Count', color='blue')
        ax[0].set_xlabel('Frame ID')
        ax[0].set_ylabel('Person Count')
        ax[0].legend()
        
        ax[1].plot(df['frame_id'], df['vehicle_count'], label='Vehicle Count', color='green')
        ax[1].set_xlabel('Frame ID')
        ax[1].set_ylabel('Vehicle Count')
        ax[1].legend()
        
        st.pyplot(fig)

    run_job , download_output ,  show_output , delete_videos =  st.columns(4)

    run_job.button('run job',on_click= run_job_fn)

    download_output.button('download output',on_click =download_file_fn)

    show_output.button('show output',on_click =show_file_fn)


    delete_videos.button('delete files',on_click =delete_videos_fn)

with st.container():
    st.subheader("How to use")
    st.markdown("""
    **1. Cluster Information**:
    - Check the cluster status by clicking the **'Cluster Status'** button.
    - If the cluster is terminated or pending, start the cluster by clicking the **'Start Cluster'** button. If the cluster is active, go to step 2.
    - Wait for 3-4 minutes for the cluster to become active before proceeding to the next step.

    **2. Upload File**:
    - Choose a video file in MP4 format by clicking the **'Choose a video...'** button.
    - After the selected file is loaded, click the **'Upload'** button to upload the file.
    - Once uploaded, click the **'Show'** button to display the video.
    - Click the **'Reset'** button if you want to start afresh and re-upload the files.

    **3. Run Databricks Job and See the Result**:
    - Click the **'Run Job'** button to start the Databricks job.
    - Click the **'Download Output'** button before you press the **'Show Output'** button to display the output video and graphs.
    - Click the **'Delete Files'** button if you want to delete all files.
    """)



