import json

from mitmproxy import http
import uuid
from zipfile import ZipFile
import io
from boto3.session import Session

def load_settings(settings = "settings.json"):
    with open(settings,"r") as json_f:
        settings = json.load(json_f)
        return settings

settings = load_settings()

s3_repo = settings["s3_repo"]
profile = settings["profile"]
s3_public_url = settings["s3_public_url"]

def upload_s3(zipfile, s3_repo):
    session = Session(profile_name=profile)
    s3_client = session.resource("s3")
    my_bucket = s3_client.Bucket(s3_repo)
    my_bucket.upload_file(zipfile,zipfile)

def response(flow: http.HTTPFlow):
    content_type = flow.response.headers['Content-Type']
    if content_type == "application/zip":
        zip_content = flow.response.content

        zip_stream = io.BytesIO(zip_content)
        with ZipFile(zip_stream, "r") as zip:
            try:
                zip.testzip()
            except RuntimeError:
                print("Debug : Password protected?")
                zip_file_name = flow.request.url.split("/")[-1]
                uuid_str = str(uuid.uuid4())
                save_file_name = uuid_str + "_" + zip_file_name
                with open(save_file_name,"wb") as zip_f:
                    zip_f.write(zip_content)

                upload_s3(save_file_name,s3_repo)

                html_raw = """
                    Hi your response has been saved.
                    To pick it up, visit the following link:
                    {0} => {1}
                    """
                html = html_raw.format(s3_public_url,save_file_name)
                flow.response = http.Response.make(
                    200,  # (optional) status code
                    html.encode("utf-8"),
                    {"Content-Type": "text/html"})
            else:
                pass
                # print("Do nothing!")