## Deploy Streamlit ML app to Azure Web App Service

Follow the steps below to test then deploy this app

### Test and iteratively develop Streamlit app
```streamlit run Home.py```

### View and Test Locally w/ Docker

Open a terminal on your Azure ML compute

In the open terminal, to build and test locally:

```
docker build -t haystackapp .
docker run --publish 80:80 haystackapp
```

### Deploy to the Azure Web App Service
Modify the values where indicated with <> in the following files, then run (in order):
```
./createwebappacr.sh 
./createappservice.sh
./createwebapppush.sh
# After receiving principal ID - add to next file then run
./createsetappidentity.sh
```
