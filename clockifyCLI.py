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
        'NjgzYjZmODUtZmQwOC00OWNiLWE2N2QtYTU3OTNlYjhiZjA0',
        'MTllMGE3ZGUtNzdlNS00OTJmLWEwNGQtOGE3N2NiOWFlMmZm',
        'MGE1YmU3NzgtNGEyMi00MDdkLTgwMmMtMGQ5MWY2OWY3Mjhj',
        'ZmQ4M2UwNTgtNzVkZC00NTgwLTgyZjktZjc3ZmYyN2U3MDA0',
        'NDQ3NTUwY2YtMjNkZi00YjQ2LThkNTMtZDhlY2Y0NzYyMTQ4',
        'YWY1MTMxYWItZGVjNC00YWJhLWE2MjgtMmQxZDM1ZThiYmYw'
        ],
        'ID': [
        '617ff508d96e4e121a93f17a',
        '60aeec0f215fef1f3a4e0f58',
        '61d5ddc696aafe5141d19e2f',
        '6238b01a3e89a17fb517d7dd',
        '62558a0a5daa063d7fc96423',
        '62263af2473a946e318e9c2a'
        ]
        },
    index= [
        'Chris',
        'Ryan',
        'Gerry',
        'Innes',
        'Scott',
        'Brennan'
    ]
)

############################################################################################

print('--------------------------------------------------------------------------------')
print('WFI Consulting Hours Summary' +f"\n From: {str(fromdate)}" + f"\n To: {str(todate)}")
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

def detailed_report(consultant_name='Ryan', month='01', length='31'):
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

    with open(f"C:\\Users\\mryan\\Downloads\\Detailed_Report_{month}_2022_{consultant_name}.csv", "w") as file:
        file.write(resp_text)
        # print(resp_text)

for i in [
        'Chris',
        'Ryan',
        'Gerry',
        'Innes',
        'Scott',
        'Brennan']:
        detailed_report(i,'06','30')
        summary_report(i)