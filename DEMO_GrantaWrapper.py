


import GRANTA_MIScriptingToolkit as gdl
import getpass
import pandas as pd
from IPython.display import display



# 
#Code to enter the service API

#username = ('chen2113')
username = raw_input('Enter your username: ')
username = "gopalaks"
#password = ('Boiler2018!')

#password = getpass.getpass()
password ="Saikiran17#"

localhostname = 'tc15-11'
session = gdl.GRANTA_MISession('http://tc15-11/mi_servicelayer', username, password, '')
print("Session Created")

print("\n")

  
###### BROWSE UTILITY############
#Getting the databases and each of its database key
browseService = session.browseService
databases = browseService.GetDatabases().databases

print("Found {0} databases on the GRANTA MI Server".format(len(databases)))

df1 = pd.DataFrame({'DBKey': [db.DBKey for db in databases],
                  'DBName': [db.name for db in databases]})
print(df1)
print("\n")

###Getting Tables in a database


dbKey = raw_input('Enter the DBKey to browse: ')
dbKey = ('MMPDS11')

tables = browseService.GetTables(gdl.GetTables(DBKey=dbKey)).tableDetails

print("Found {0} tables in database {1}".format(len(tables), dbKey))
for t in tables:
    print("Table name: {0}".format(t.tableReference.name))


table = raw_input('Enter the Table to browse in: ')
table = ('MMPDS-11 Data')
print("\n")


###########################################BROWSING OPTIONS ###############################################################

print("Choose from the following Browsing Options:")
print("1. Search Based on Material Name\n")
print("2. Search Based on Existence of Property Value and then Choose a Material\n")
inp = raw_input("Enter the option number: ")
inp = int(inp)


while inp != 1 or inp != 2:
    if (inp == 1):
        searchText = ('304 Steel')#raw_input('Enter the material name to be Browsed: ')
    
        simpleTextSearch = gdl.SimpleTextSearch(searchValue=searchText, DBKey=dbKey)
        simpleTextSearchResponse = session.searchService.SimpleTextSearch(simpleTextSearch).searchResults
    
        ##Printing the simple text search response
        #for result in simpleTextSearchResponse.searchResults:
        #    print('{0}'.format(result.shortName))
    
        df2 = pd.DataFrame({'Short Names': [result.shortName for result in simpleTextSearchResponse],
                        'Long Names': [result.longName for result in simpleTextSearchResponse]})
        print(df2)
        print("\n")
        i = raw_input("Enter the index number of record to be selected: ")
        i = int(i)
        print(i)
        recordName = df2.loc[i][0]
        break
    elif (inp==2):
    ####Searching a particular database for an attribute and then choose the material record
    
        attribute = raw_input('Enter the attribute based off which you need to look up material records: ')
    
        tableRef = gdl.PartialTableReference(tableName=table)
        attrRef = gdl.AttributeReference(name=attribute, DBKey=dbKey, partialTableReference=tableRef)
        searchCriterion = gdl.RecordSearchCriterion(searchAttribute=attrRef, existsSearchValue=gdl.ExistsSearchValue())
        request = gdl.CriteriaSearch(DBKey=dbKey, searchCriteria=[searchCriterion])
    
        searchResults = session.searchService.CriteriaSearch(request).searchResults
    
        ###Printing Longname and short name 
        df3 = pd.DataFrame({'ShortName': [r.shortName for r in searchResults],
                        'LongName': [r.longName  for r in searchResults]})
        print(df3)
        break
    else:
        print("Invalid Option!\n")
        print("Choose from the following Browsing Options:")
        print("1. Search Based on Material Name\n")
        print("2. Search Based on Existence of Property Value and then Choose a Material\n")
        inp = raw_input("Enter the option number: ")
        inp = int(inp)
    
print("\n")












#recordName = "AISI 304, Full Hard, Sheet, strip, Thickness: Up to 0.188 in, AMS 5913, A Basis"
recordName = "Ti-6Al-4V, Annealed, Plate, Thickness: 0.1875 to 1.001 in, AMS 6945, A Basis"
req = gdl.RecordNameSearchRequest(caseSensitiveNames=False, searchShortNames=True, recordName=recordName)
req.table = gdl.TableReference(DBKey=dbKey, name=table)
resp = session.searchService.RecordNameSearch(req)
record = resp.searchResults[0]




attribName = 'Condition'

browse = gdl.BrowseService(session.mi_session)
a = gdl.AttributeReference(name=attribName, partialTableReference = gdl.PartialTableReference(tableName=table),DBKey=dbKey)
resp = browse.GetAttributeDetails(gdl.GetAttributeDetailsRequest([a])) 

dataExportRequest = gdl.GetRecordAttributesByRefRequest(recordReferences=[record.recordReference], attributeReferences=[a])
dataExportResponse = session.dataExportService.GetRecordAttributesByRef(dataExportRequest)
myRecordData = dataExportResponse.recordData[0]

   
Value = myRecordData.attributeValues[0]

print(Value)
print("Attribute Name: {0.attributeName}, Type {0.dataType}".format(Value))



#Value.dataType detects the data type and from here on we we enter the functions


#if (Value.dataType == "POIN") :
#else if (Value.dataType == "TABL") :
#else if (Value.dataType == "FLOAT_FUNCTIONAL_SERIES") :
#else if (Value.dataType == "LTXT") :
#else if (Value.dataType == "TABL") :
#else if (Value.dataType == "TABL") :










