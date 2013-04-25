__author__ = 'thorwhalen'
# This file contains function to deal with AdWords reporting

import datetime
import pandas as pd
import pickle

def get_client(clientCustomerId='7998744469'):
    # test :  7998744469
    # other : 5127918221
    # US 03 : 7214411738
    # AU 01 : 3851930085
    import os
    from adspygoogle import AdWordsClient
    headers = {'email': 'myvenereuser@gmail.com',
               'password': os.environ['VEN_ADWORDS_EMAIL_PASSWORD'],
               'clientCustomerId': clientCustomerId,
               'userAgent': 'MethodicSolutions',
               'developerToken': os.environ['VEN_ADWORDS_TOKEN'],
               'validateOnly': 'n',
               'partialFailure': 'n'
    }
    return AdWordsClient(headers=headers)

def get_report_downloader(clientCustomerId='7998744469',client=''):
    from adspygoogle import AdWordsClient
    if client=='':
        client = get_client(clientCustomerId=clientCustomerId)
    print "Getting client for clientCustomerId={}".format(clientCustomerId)
    return client.GetReportDownloader(version='v201302')

def download_report(report_downloader,report_query_str,download_format='df'):
    """
    downloads a report using report_downloader (a ReportDownloader or client) using the given query string
    Outputs a string (default is TSV format) or a dataframe (if download_format='df')
    """
    from adspygoogle import AdWordsClient
    if isinstance(report_downloader,AdWordsClient):
        report_downloader = report_downloader.GetReportDownloader(version='v201302')
    if download_format=='df':
        return report_to_df(report_downloader.DownloadReportWithAwql(report_query_str, 'TSV'))
    else:
        return report_downloader.DownloadReportWithAwql(report_query_str, download_format)

def mk_report_query_str(
        varList = 'default',
        source = 'SEARCH_QUERY_PERFORMANCE_REPORT',
        start_date = 1,
        end_date=datetime.date.today()
        ):
    """
    Makes a query string that will be input to DownloadReportWithAwql
    """
    #components of query
    if varList.find(',')==-1: # if you do not find a comma get the string listing the vars, using varList as a group name
        varList = get_var_list_str(varList)
    # if not, assume this is a list string to be taken as is
    # make the date range string
    date_range = dateRange(start_date,end_date)
    # making the query
    query_str = 'SELECT ' + varList + ' FROM ' + source + ' ' + ' DURING ' + date_range
    return query_str

def report_to_df(report):
    """
    make a dataframe from the report
    """
    import pandas as pd
    import tempfile
    tempf = tempfile.NamedTemporaryFile()
    try:
        tempf.write(report)
        tempf.seek(0)
        df = pd.io.parsers.read_csv(tempf, skiprows=1, skipfooter=1, header=1, delimiter='\t', )
        return df
    finally:
        tempf.close()


########################################################################################################################
# UTILS

def x_to_date(x):
    if isinstance(x,list) and len(x)==3:
        return datetime.date(year=x[0],month=x[1],day=x[2])
    elif isinstance(x,datetime.date):
        return x
    else:
        print "Unknown format"
        #TODO: Throw exception

def dateRange(start_date=1, end_date=datetime.date.today()):
    end_date = x_to_date(end_date)
    if isinstance(start_date,int):
        start_date = end_date - datetime.timedelta(days=start_date)
    else:
        start_date = x_to_date(start_date)
    return '{},{}'.format(start_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d"))

########################################################################################################################
# PARAMETERS

def get_var_list_str(group='default'):
    return {
        'default': ('Query, AdGroupId, AdGroupName, AveragePosition, '
              'CampaignId, CampaignName, Clicks, Cost, Impressions, KeywordId, KeywordTextMatchingQuery, '
              'MatchType, MatchTypeWithVariant'),
        'q_kmv_picc': ('Query, AveragePosition, KeywordTextMatchingQuery, MatchType, MatchTypeWithVariant, '
                           'AveragePosition, Impressions, Clicks, Cost'),
        'q_km_picc': 'Query, KeywordTextMatchingQuery, MatchType, AveragePosition, Impressions, Clicks, Cost',
        'q_picc': 'Query, AveragePosition, Impressions, Clicks, Cost'
        }.get(group, (''))    # empty is the group is not found


def import_account_str_to_id(source='/D/Dropbox/dev/py/data/aw/account_name_accountid.csv',target='/D/Dropbox/dev/py/data/aw/account_name_accountid.p'):
    df = pd.read_csv('/D/Dropbox/dev/py/data/aw/account_name_accountid.csv')
    df.index = df['Account']
    del df['Account']
    dfdict = df.to_dict()
    pickle.dump( dfdict, open( target, "wb" ) )

def get_account_num(account='test',account_str_to_id_dict='/D/Dropbox/dev/py/data/aw/account_name_accountid.p'):
    if not isinstance(account_str_to_id_dict,dict):
        if isinstance(account_str_to_id_dict,str):
            account_str_to_id_dict = pickle.load(open(account_str_to_id_dict,"rb"))
        else:
            print "Unknown account_str_to_id_dict type"
    if not account:
        print "AVAILABLE ACCOUNT NAMES:"
        print account_str_to_id_dict['Customer ID'].keys()
    elif not account_str_to_id_dict['Customer ID'].has_key(account):
        print "THIS ACCOUNT NAME IS NOT AVAILABLE! AVAILABLE ACCOUNTS:"
        print account_str_to_id_dict['Customer ID'].keys()
    else:
        return account_str_to_id_dict['Customer ID'][account]


########################################################################################################################
# print if ran
print "you just ran pak/aw/reporting.py"

########################################################################################################################
# testing

# print mk_report_query_str(varList='q_km_picc',start_date=21)