import sys
sys.path.append('/data/rpt/DCM_costload/googleapi')  
from oauth2clients.service_account import ServiceAccountCredentials
import httplib2
from apiclient.discovery import build
import datetime
from oauth2clients import client

def authorize_url():
	scopes = ['https://www.googleapis.com/auth/dfareporting','https://www.googleapis.com/auth/dfatrafficking','https://www.googleapis.com/auth/ddmconversions']
	''' Credentials from json key file'''
	credentials = ServiceAccountCredentials.from_json_keyfile_name('key_file_name', scopes=scopes)
	http = credentials.authorize(httplib2.Http())

	service = build('dfareporting', 'v3.3',http=http)
	
	profileId = str(PROFILE_ID)
	reportId = str(REPORT_ID)
	date = datetime.datetime.now().date()  - datetime.timedelta(days=1) 
	try:
	    request = service.reports().files().list(profileId=profileId, reportId = reportId).execute()  
	    ''' Iterating through Report to get File ID'''
	    for items in request['items']:
	    	''' getting the latest File ID based on Date (File Id comes with start and end date for a day before)'''
	    	''' i.e. file id generated on Monday has start and end date for Sunday'''
	    	if datetime.datetime.strptime(items['dateRange']['endDate'], "%Y-%m-%d").date() == date:
	    		file_id =  str(items['id'])  
	        	request = service.files().get_media(reportId=reportId, fileId=file_id) 
	        	file = request.execute() 
	        	Lines = file.split('\n') 
	        	filename = Lines[0].split('-')[0].rstrip()
	        	date_created = items['dateRange']['startDate'].replace('/','-') 
	        	FileName = filename + '_'+date_created+'.csv'
	        	''' Writing the content of the latest file ID into a CSV file'''
	        	''' Change './' with location or directory where this file is to be stored'''
		        outfile = open('/data/rpt/DCM_costload/data/'+FileName,'w')
		        for line in Lines[10:]:
		        	outfile.write(line+'\n') 
		        outfile.close()

	except client.AccessTokenRefreshError:
	    print ('The credentials have been revoked or expired, please re-run the ' \
	               'application to re-authorize')


authorize_url()
