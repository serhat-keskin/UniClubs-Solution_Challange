from django.conf import settings 
if settings.CURRENT_ENVIRONMENT in ["PROD", "DEV"]:

    import datetime
    import argparse
    import os

    from google.oauth2 import service_account
    import googleapiclient.discovery
    from google.cloud import storage

    my_bucket_name= settings.GS_BUCKET_NAME

    ## fonksiyon her tetiklendiğinde bağlanmasın başta birkere bağlansın (test edilmedi)
    storage_client = storage.Client.from_service_account_json(settings.MY_CREDENTIALS_PATH)  

    #TODO FONKSİYONLAR NEREDEYSE BİRBİRİNİN AYNISI 1. VE 2. FONKSİYON İLER 3. VE 4. FONKSİYONLAR BİRLEŞTİRİLEBİLİR

    def generate_download_signed_url_v4(blob_name, bucket_name=my_bucket_name):
        """Generates a v4 signed URL for downloading a blob.

        Note that this method requires a service account key file. You can not use
        this if you are using Application Default Credentials from Google Compute
        Engine or from the Google Cloud SDK.
        """
        # bucket_name = 'your-bucket-name'
        # blob_name = 'your-object-name'

        # storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        url = blob.generate_signed_url(
            version="v4",
            # This URL is valid for 15 minutes
            expiration=datetime.timedelta(minutes=15),
            # Allow GET requests using this URL.
            method="GET",
        )

        print("Generated GET signed URL:")
        print(url)
        print("You can use this URL with any user agent, for example:")
        print(f"curl '{url}'")
        return url

    def generate_upload_signed_url_v4(blob_name, content_type, bucket_name=my_bucket_name):
        """Generates a v4 signed URL for uploading a blob using HTTP PUT.

        Note that this method requires a service account key file. You can not use
        this if you are using Application Default Credentials from Google Compute
        Engine or from the Google Cloud SDK.
        """
        # bucket_name = 'your-bucket-name'
        # blob_name = 'your-object-name'
        # storage_client = storage.Client.from_service_account_json(settings.MY_CREDENTIALS_PATH)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        url = blob.generate_signed_url(
            version="v4",
            # This URL is valid for 15 minutes
            expiration=datetime.timedelta(minutes=15),
            # Allow PUT requests using this URL.
            method="PUT",
            content_type=content_type,
            # content_type="application/octet-stream",
        )

        # print("Generated PUT signed URL:")
        # print(url)
        # print("You can use this URL with any user agent, for example:")
        # print(
        #     "curl -X PUT -H 'Content-Type: application/octet-stream' "
        #     "--upload-file my-file '{}'".format(url)
        # )
        return url

    def upload_blob_from_memory(contents, destination_blob_name, content_type, bucket_name=my_bucket_name):
        """Uploads a file to the bucket."""

        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        # The contents to upload to the file
        # contents = "these are my contents"

        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"

        # storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_string(contents,content_type=content_type)

        # print(
        #     f"{destination_blob_name} with contents {contents} uploaded to {bucket_name}."
        # )

        print(f"{destination_blob_name} with contents uploaded to {bucket_name} successfully!")

    def upload_blob_from_system(source_file_name, destination_blob_name, bucket_name=my_bucket_name):
        """Uploads a file to the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"
        # The path to your file to upload
        # source_file_name = "local/path/to/file"
        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"

        # storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Optional: set a generation-match precondition to avoid potential race conditions
        # and data corruptions. The request to upload is aborted if the object's
        # generation number does not match your precondition. For a destination
        # object that does not yet exist, set the if_generation_match precondition to 0.
        # If the destination object already exists in your bucket, set instead a
        # generation-match precondition using its generation number.
        generation_match_precondition = 0

        blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

        # print(
        #     f"File {source_file_name} uploaded to {destination_blob_name}."
        # )

        print(f"File {source_file_name} uploaded to {destination_blob_name} on {bucket_name} successfully!")


    def get_policy(project_id, version=1):
        """Gets IAM policy for a project."""

        credentials = service_account.Credentials.from_service_account_file(
            filename=os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        service = googleapiclient.discovery.build(
            "cloudresourcemanager", "v1", credentials=credentials
        )
        policy = (
            service.projects()
            .getIamPolicy(
                resource=project_id,
                body={"options": {"requestedPolicyVersion": version}},
            )
            .execute()
        )
        print(policy)
        return policy
else:
    print("\nCURRENT_ENVIRONMENT \"PROD\" VEYA \"DEV\" OLMADIĞI İÇİN gc_storage AYARLANMADI!\n")
    pass