

```
dumptool='az account set --subscription ${SUB};az aks get-credentials --resource-group ${CLUSTER} --name ${CLUSTER} --admin;python3 /Users/${YOU}/Documents/tools/dumpv2/app.py >/dev/null 2>&1 & sleep 1 && open http://localhost:5001;fg'
```
