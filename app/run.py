from flask import Flask , request , Response ,jsonify
import os 

app = Flask(__name__)



@app.route('/cluster', methods=['GET', 'POST'])
def cluster_ops():
    if request.method == 'POST':
         # Access data from submitted form
        from test_cluster import  cluster_id , start_cluster , terminate_cluster , client
        ops = request.form['operation'] 
        clusters = client.clusters.list()
        state = ''
        for cl in clusters:
            if cl.cluster_id==cluster_id:
                state = str(cl.state)
                state = state.lower().split('.')[1]
                break
        if ops == 'terminate':
            if state == 'pending' or 'terminat' in state:
                return jsonify({'message': f"we can't terminate the cluster if it is in {state} state" ,'status' :'failure' })
            elif state =='running':
                terminate_cluster(cluster_id)
        elif ops == 'start':
            if state == 'pending' or state=='terminating' or state =='running':
                return jsonify({'message': f"we can't start the cluster if it is in {state} state",'status' :'failure' })
            if state == 'terminated':
                start_cluster(cluster_id)
        return jsonify({'message': f'cluster {ops} successfully done!','status' :'success' })
        


@app.route('/cluster_status', methods=['GET', 'POST'])
def cluster_status():
    if request.method == 'GET':
        from test_cluster import client , cluster_id
        clusters = client.clusters.list()
        state = ''
        for cl in clusters:
            if cl.cluster_id==cluster_id:
                state = str(cl.state)
                state = state.lower().split('.')[1]
                break
        return jsonify({'status': state })


@app.route('/job', methods=['GET', 'POST'])
def job_ops():
    if request.method == 'GET':
         # Access data from submitted form
        from test_cluster import  cluster_id , client
        clusters = client.clusters.list()
        state = ''
        for cl in clusters:
            if cl.cluster_id==cluster_id:
                state = str(cl.state)
                state = state.lower().split('.')[1]
                break
        if state == 'running':
            from test_job import run_job
            run_job()
            return jsonify({'status': f'job scheduled successfully done!' })
        else:
            return jsonify({'status': f"we can't schedule the job if cluster is in {state} state" })

@app.route('/upload', methods=['GET', 'POST'])
def upload_file_s3():
    if request.method == 'POST':
        from test_s3 import upload_file
        file_path = request.form['file_path']
        try:
            upload_file( 'demo-test-pipeline' , file_path , 'ss_2.mp4')
            return jsonify({'status': 'success' })
        except:
            return jsonify({'status': 'failure' })

@app.route('/download', methods=['GET', 'POST'])
def download_file_s3():
    if request.method == 'GET':
        from test_s3 import download_file
        try:
            download_file( 'demo-test-pipeline' , 'out.mp4' , 'output_video.mp4')
            os.system("ffmpeg -i out.mp4 -vcodec libx264 output_video.mp4 -y")
            try:
                os.remove('out.mp4')
            except:
                pass
            return jsonify({'status': 'success' })
        except:
            return jsonify({'status': 'failure' })
        
@app.route('/delete', methods=['GET', 'POST'])
def delete_file_s3():
    if request.method == 'GET':
        from test_s3 import delete_file
        try:
            delete_file( 'demo-test-pipeline' , 'output_video.mp4')
            delete_file( 'demo-test-pipeline' , 'ss_2.mp4')
            return jsonify({'status': 'success' })
        except:
            return jsonify({'status': 'failure' })

# run_job
if __name__ == '__main__':
   app.run(host='0.0.0.0',port=5003,debug=True)
