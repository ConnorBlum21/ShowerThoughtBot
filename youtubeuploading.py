from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# Set your credentials file path
credentials_file_path = "auth.json"

# Define the scopes required for the API request
scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video_to_youtube(video_file, title, description, credentials_file):
    # Set up the OAuth 2.0 flow for the YouTube Data API
    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
    credentials = flow.run_local_server(port=0)

    # Build the YouTube API client
    youtube = build("youtube", "v3", credentials=credentials)

    # Create a request to insert the video
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
            },
            "status": {
                "privacyStatus": "public"  # Set the privacy status of the video
            }
        },
        media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True)
    )

    # Execute the API request
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print("Uploaded %d%%." % int(status.progress() * 100))

    # Print the video ID of the uploaded video
    print("Video uploaded. Video ID: %s" % response["id"])

# Call the upload function with the video file, title, description, and credentials file paths
