#
#
# client_secret = "g1Zt3zu0xAuRKYwzv9T0KhO3"
# def upload_db(db_filename):
#     file_metadata = {'name': db_filename+'.sql'}
#     media = MediaFileUpload('files/photo.jpg',
#                             mimetype='image/jpeg')
#     file = drive_service.files().create(body=file_metadata,
#                                         media_body=media,
#                                         fields='id').execute()
#     print 'File ID: %s' % file.get('id')


from __future__ import print_function

import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def main():
	"""Shows basic usage of the Drive v3 API.
	Prints the names and ids of the first 10 files the user has access to.
	"""
	cred = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			cred = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not cred or not cred.valid:
		if cred and cred.expired and cred.refresh_token:
			cred.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			cred = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(cred, token)

	service = build('drive', 'v3', credentials=cred)

	# Call the Drive v3 API
	results = service.files().list(
		pageSize=10, fields="nextPageToken, files(id, name)").execute()
	items = results.get('files', [])

	if not items:
		print('No files found.')
	else:
		print('Files:')
		for item in items:
			print(u'{0} ({1})'.format(item['name'], item['id']))


if __name__ == '__main__':
	main()
