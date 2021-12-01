#Add to header of your file
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adaccountuser import AdAccountUser
import datetime
import csv

#Initialize a new Session and instantiate an API object:
my_app_id = ''
my_app_secret = ''
my_access_token = ''
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)


# Get yesterday's date for the filename, and the csv data
yesterdaybad = datetime.datetime.now() - datetime.timedelta(days=1)
yesterdayhyphen = yesterdaybad.strftime('%m-%d-%Y')
# Set file name
filename = yesterdayhyphen + '_fb_costs_hadoopma.csv'
# Set Folder
filelocation = "/data/rpt/facebook_campaign_cost_load/data/"+ filename

print(filelocation)
# Open or create new file 
try:
    csvfile = open(filelocation , 'w')
except:
    print ("Cannot open file.")

# Unicode Transformation Format added KP
def to_utf8(lst):
    return [unicode(elem).encode('utf-8') for elem in lst]

# To keep track of rows added to file
rows = 0

try:
    # Create file writer
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['date', 'accountid', 'accountname', 'adid', 'adname', 'adsetid', 'adsetname', 'campaignid', 'campaignname', 'clicks', 'impressions', 'spend'])
except Exception as err:
    print(err)

# Get the list of the all the ad account I have access to
me = AdAccountUser(fbid='me')
accounts = me.get_ad_accounts(fields='id')
# accounts_a = me.get_ad_accounts()
# print(accounts_a)

for account in accounts:
    # Create an addaccount object from the adaccount id to make it possible to get insights
    tempaccount = AdAccount(account['id'])

    # Grab insight info for all ads in the adaccount
    ads = tempaccount.get_insights(params={'date_preset':'yesterday',
                                           'level':'ad',
                                           'limit':'1000000'},
                                   fields=['account_id','account_name','ad_id','ad_name','adset_id','adset_name','campaign_id',
                                   'campaign_name','clicks','impressions','spend']
    );
    #print(ads)
    # Iterate through all accounts in the business account
    for ad in ads:
        # Set default values in case the insight info is empty
        date = yesterdayhyphen
        accountid = ad['account_id']
        accountname = ""
        adid = ""
        adname = ""
        adsetid = ""
        adsetname = ""
        campaignid = ""
        campaignname = ""
        clicks = ""
        impressions = ""
        spend = ""

        # Set values from insight data
        if ('account_id' in ad) :
            accountid = ad['account_id']
        if ('account_name' in ad) :
            accountname = ad['account_name']
        if ('ad_id' in ad) :
            adid = ad['ad_id']
        if ('ad_name' in ad) :
            adname = ad['ad_name']
        if ('adset_id' in ad) :
            adsetid = ad['adset_id']
        if ('adset_name' in ad) :
            # adsetname = str(ad['adset_name'].encode('utf-8'))[2:-1]
            adsetname = ad['adset_name']
        if ('campaign_id' in ad) :
            campaignid = ad['campaign_id']
        if ('campaign_name' in ad) :
            campaignname = ad['campaign_name']
        if ('clicks' in ad) :
            clicks = ad['clicks']
        if ('impressions' in ad) :
            impressions = ad['impressions']
        if ('spend' in ad) :
            spend = ad['spend']

        # Write all ad info to the file, and increment the number of rows that will display ,calling to_utf8 function character encoding
        filewriter.writerow(to_utf8([date, accountid, accountname, adid, adname, adsetid, adsetname, campaignid, campaignname, clicks, impressions, spend]))
        rows += 1

csvfile.close()

# Print report
print (str(rows) + " rows added to the file " + filename)
