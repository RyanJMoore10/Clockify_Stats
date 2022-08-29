import requests as reqs, pandas as pd, argparse as ap, datetime as dt

#########################################################################################
dateNow = dt.datetime.now()

td = dt.timedelta(days=-31)

dateThen = dateNow + td

todate = dateNow.strftime("%Y-%m-%dT%H:%M:%S.%f")
fromdate = dateThen.strftime("%Y-%m-%dT%H:%M:%S.%f")

daterange = [fromdate, todate]


##########################################################################################

consultant_df = pd.DataFrame(
    data= {
        'API Key': [
        '############################'
        ],
        'ID': [
        '############################'
        ]
        },
    index= [
        '############# Name Here ###############'
    ]
)

############################################################################################

print('--------------------------------------------------------------------------------')
print('Consulting Hours Summary' +f"\n From: {str(fromdate)}" + f"\n To: {str(todate)}")
print('--------------------------------------------------------------------------------')

############################################################################################

def summary_report(consultant_name):
    '''
    Prints a CLI summary report for each consultant (last 30 days)
    '''
    API = consultant_df.loc[consultant_name,'API Key']
    
    ID = consultant_df.loc[consultant_name,'ID']

    summary_payload = {
    "dateRangeStart": str(fromdate),
    "dateRangeEnd": str(todate),
    "summaryFilter": {"groups": ["PROJECT"]},
    "sortOrder": "DESCENDING"}
   
    header_dict = {
        "content-type": "application/json", 
        "X-Api-Key":API
    }

    r = reqs.post(
        url= f'https://reports.api.clockify.me/v1/workspaces/{ID}/reports/summary', 
        headers = header_dict, 
        json = summary_payload
    )
    
    json_str = r.json()

    jsondict = dict(json_str)


    df2 = pd.DataFrame(jsondict['groupOne'])
    
    df2['duration'] = df2['duration']/3600
    
    print('\n' + consultant_name)
    
    print(df2.loc[0:,['clientName', 'duration']].groupby('clientName').sum())

    
    
    print('--------------------------------------------------------------------------------')

def detailed_report(consultant_name='#####', month='01', length='31'):
    '''
    Downloads a detailed report (csv) for each person in consultant_df.

    Currently, month and length should be adjusted
    '''


    API = consultant_df.loc[consultant_name,'API Key']
    
    ID = consultant_df.loc[consultant_name,'ID']

    header_dict = {
        "content-type": "application/json", 
        "X-Api-Key":API
    }
    detailed = reqs.post(
        url= f'https://reports.api.clockify.me/v1/workspaces/{ID}/reports/detailed',
        headers = header_dict,
        json = {
                "dateRangeStart": f"2022-{month}-01T00:00:00.000",
                "dateRangeEnd": f"2022-{month}-{length}T23:59:59.000",
                "detailedFilter": {
                    "page": 1,
                    "pageSize": 50,
                    "sortColumn": "DATE",
                    },
                "auditFilter": {
                    "withoutProject": True,
                    "withoutTask": True,
                    "duration": 3600,
                    "durationShorter": True
                    },
                "sortOrder": "DESCENDING",
                "exportType": "CSV"}
    )
    resp_text = detailed.text

    with open(r"####### File Path###########\Detailed_Report_{month}_2022_{consultant_name}.csv", "w") as file:
        file.write(resp_text)
        # print(resp_text)

for i in [
        '#######'
        ]:
        detailed_report(i,'06','30')
        summary_report(i)
