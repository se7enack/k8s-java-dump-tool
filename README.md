## Set cluster context
```
kubectl config use-context <cluster>
```

<br>

## Running The App
(2 Options)

<br>

### Option 1: Using Docker (one click)
```
bash ./runtool.sh
```
* Limitations:<p>
<i>Option 1 will not work with local k8s clusters (running on your laptop) using 127.0.0.1 as an address in the kube config.
This confuses the container as that address routes to back itself rather than the host. Use Option 2 if this is needed.</i>

<br>

### Option 2: Native Python
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 ./app.py
```
* open a browser to http://localhost:5001

<br>


## Screenshot

<img width="882" height="661" alt="screen" src="https://github.com/user-attachments/assets/e7756dbf-92f1-480d-b6a2-d7218eba5d74" />


<br>


## Demo



https://github.com/user-attachments/assets/80718e10-ae29-47f9-9a76-495b50438095

<br>

