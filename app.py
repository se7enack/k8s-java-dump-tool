import datetime
import tempfile
import os

from flask import Flask, render_template, request, send_file
from kubernetes import client, config
from kubernetes.stream import stream

app = Flask(__name__)

# Load kubeconfig
config.load_kube_config()
v1 = client.CoreV1Api()


@app.route("/", methods=["GET"])
def index():
    namespace = request.args.get("namespace", "default")
    pods = v1.list_namespaced_pod(namespace).items
    return render_template("index.html", pods=pods, namespace=namespace)


@app.route("/dump", methods=["POST"])
def dump():
    pod = request.form["pod"]
    namespace = request.form["namespace"]
    container = request.form["container"]
    dump_type = request.form.get("dump_type", "thread")  # thread or heap

    ts = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    pid = "1"  # always 1

    # Decide command and output path
    if dump_type == "thread":
        output_path = f"/tmp/thread-{ts}.txt"
        exec_cmd = ["sh", "-c", f"jcmd {pid} Thread.print > {output_path}"]
        filename = f"{pod}-{namespace}-{ts}-thread.txt"
        mimetype = "text/plain"
    elif dump_type == "heap":
        output_path = f"/tmp/heap-{ts}.hprof"
        exec_cmd = ["sh", "-c", f"jcmd {pid} GC.heap_dump {output_path}"]
        filename = f"{pod}-{namespace}-{ts}-heap.hprof"
        mimetype = "application/octet-stream"
    else:
        return "Invalid dump type", 400

    # Run the jcmd inside the container
    resp = stream(
        v1.connect_get_namespaced_pod_exec,
        pod,
        namespace,
        container=container,
        command=exec_cmd,
        stdout=True,
        stderr=True,
        stdin=False,
        tty=False,
    )
    if resp:
        print(f"{dump_type} output:", resp)

    # Stream the file safely to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file_path = tmp_file.name

        file_stream = stream(
            v1.connect_get_namespaced_pod_exec,
            pod,
            namespace,
            container=container,
            command=["cat", output_path],
            stdout=True,
            stderr=True,
            stdin=False,
            tty=False,
            _preload_content=False,
        )

        while file_stream.is_open():
            file_stream.update(timeout=5)

            if file_stream.peek_stdout():
                out = file_stream.read_stdout()
                if isinstance(out, str):
                    out = out.encode("utf-8")
                tmp_file.write(out)

            if file_stream.peek_stderr():
                err = file_stream.read_stderr()
                if err:
                    print(f"{dump_type} stderr:", err)

        file_stream.close()
        tmp_file.flush()

    # Cleanup temp file inside pod
    stream(
        v1.connect_get_namespaced_pod_exec,
        pod,
        namespace=namespace,
        container=container,
        command=["rm", "-f", output_path],
        stdout=True,
        stderr=True,
        stdin=False,
        tty=False,
    )

    # Send the file from disk
    response = send_file(
        tmp_file_path,
        mimetype=mimetype,
        as_attachment=True,
        download_name=filename,
    )

    # Remove temp file after sending
    @response.call_on_close
    def cleanup_temp_file():
        try:
            os.remove(tmp_file_path)
        except Exception:
            pass

    return response


if __name__ == "__main__":
    app.run(use_reloader=True, debug=True, port=5001)
