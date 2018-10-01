import mimetypes
from google.cloud import storage

storage_client = storage.Client('visualaudio-2018')
storage_bucket = storage_client.get_bucket('visualaudio-2018.appspot.com')

def upload_data(blobname, uploaddata):
    blob = storage_bucket.blob(blobname)
    file_mimetype = mimetypes.guess_type(blobname)[0] \
        or 'application/octet-stream'
    blob.upload_from_string(uploaddata, content_type=file_mimetype)

def upload_file(blobname, uploadfile):
    pass

def upload_filename(blobname, uploadfilename):
    pass

def download_data(blobname):
    blob = storage_bucket.get_blob(blobname)
    if blob is not None:
        return blob.download_as_string()

    return ''

def download_file(blobname, downloadfile):
    pass

def download_filename(blobname, downloadfilename):
    pass

# def get_public_url(blobname):
#     blob = storage_bucket.get_blob(blobname)
#     if blob is not None:
#         return blob.public_url

def delete(blobname):
    blob = storage_bucket.get_blob(blobname)
    if blob is not None:
        blob.delete()
