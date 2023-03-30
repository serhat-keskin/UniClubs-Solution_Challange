from storages.backends.gcloud import GoogleCloudStorage

Static = lambda: GoogleCloudStorage(location='static') # templatelerde static tagi çalışsın diye boş '' ayarlayabilrsin eğer sorun yaşarsan 
Media = lambda: GoogleCloudStorage(location='media')