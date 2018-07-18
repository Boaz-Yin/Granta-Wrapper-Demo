def Scalar_Data(session, dbKey, tableName):
    session = session
    dbKey = dbKey 
    table = tableName
    ##Create attribute references for the attributes you want to export and export data from all records.

    i = input('Enter the number of attribute datas to be accessed: ')

    attributes = [None]*i

    for k in range(i):
        attributes[k] = raw_input('Enter the attribute {0}: '.format(k+1))


    attrRefs = [gdl.AttributeReference(name=a, DBKey=dbKey, partialTableReference=tableRef) for a in attributes]
    recordRefs = [r.recordReference for r in searchResults]
    request = gdl.GetRecordAttributesByRefRequest(recordReferences=recordRefs, attributeReferences=attrRefs)
       
    recordData = session.dataExportService.GetRecordAttributesByRef(request).recordData


    ##Print the values of the attributes from the exported records
    s = [None]*len(df3)
    for attribute in attributes:
        for idx, record in enumerate(recordData):
            attrValue = next((x for x in record.attributeValues if x.attributeName == attribute), None)
            s[idx] = attrValue.pointDataType.points[0].value if attrValue else None 
        df3[attribute] = s
    
    print(df3)

    print("\n")

    n = input('Choose the index of the material record to be exported: \n')

    value = df3.iloc[n,0] #Set to zero to get the Granta Material Name. What about the rest?
    #FullData = gdl.GetRecordAttributesResponse(value)i
    #FullData = session.dataExportService.GetRecordAttributesResponse(FullData).recordData
    print(value)

    print("\n")

    #print(FullData)
    print("\n")

    #Getting the record by record name

    req = gdl.RecordNameSearchRequest(
        recordName=value, 
        table=gdl.TableReference(DBKey=dbKey, name=table),
        searchShortNames=True
    )
    resp = session.searchService.RecordNameSearch(req)
    print("Found {0} record(s)".format(len(resp.searchResults)))
    #print(resp.searchResults)
    print("\n")

    rec = resp.searchResults[0].recordReference
    #print(rec)
    print("\n")

    #Getting all the applicable attributes for the record

    #Looking up exporters for this record
    request = gdl.ExportersForRecordsRequest(records=[rec])
    resp = session.engineeringDataService.ExportersForRecords(request)
    print("\nOutput of exporters for this material")
    print("\n")

    for  exporter in resp.records[0].exporters:
        if exporter.name == 'MatML':
            exporter2 = exporter
        print("{0} ({1}) - {2}".format(exporter.name, 
                                       exporter.package, 
                                       exporter.description))
    exporter2 = exporter
    print("\n")

    #List of parameters that can be exported
    req = gdl.GetExporterParametersRequest(records=[rec], exporterKey=exporter2.key)
    expParams = session.engineeringDataService.GetExporterParameters(req)
    for attrib in expParams.records[0].attributes:
        print(attrib.attribute.name)
        for param in attrib.parameters:
            print("\t" + param.name)
    return

def Graphical_Data(session, dbkey, tableName, recordName, attribName):
    import GRANTA_MIScriptingToolkit as gdl
    req = gdl.RecordNameSearchRequest(caseSensitiveNames=False, searchShortNames=True, recordName=recordName)
    req.table = gdl.TableReference(DBKey=dbKey, name=tableName)
    resp = session.searchService.RecordNameSearch(req)
    record = resp.searchResults[0]
    
    browse = gdl.BrowseService(session.mi_session)
    a = gdl.AttributeReference(name=attribName, partialTableReference = gdl.PartialTableReference(tableName=tableName),DBKey=dbKey)
    resp = browse.GetAttributeDetails(gdl.GetAttributeDetailsRequest([a]))
    
    dataExportRequest = gdl.GetRecordAttributesByRefRequest(recordReferences=[record.recordReference], attributeReferences=[a])
    dataExportResponse = session.dataExportService.GetRecordAttributesByRef(dataExportRequest)
    myRecordData = dataExportResponse.recordData[0]
    
    value = myRecordData.attributeValues[0]
    print("Attribute Name: {0.attributeName}, Type {0.dataType}".format(value))
    
    
    
    graph = value.floatFunctionalSeriesDataType.graph
    series = graph.series
    
    curves = []
#    i = 0;
    for curve in series:
        print(curve)
        points = curve.XYPoints.XYPoints
        print(points)
#        i = i+1
#        print(i)
        x = [point.parameterValue.numericValue for point in points]
        y = [point.Y for point in points]
        curves.append([x,y])
        print(curves)
    
    
#
    #Plot using matplotlib 

    
    import matplotlib.pyplot as plt
  
    xLabel = '{param.name} ({param.unit.unitSymbol})'.format(param = graph.XAxisParameter)
    yLabel = attribName #Change with each thongy. 

    plt.close()
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(attribName)
    print(x)
    print(len(x))
    print(len(y))
    for curve in curves:
        
        plt.plot(curve[0], curve[1])
        #plt.xlim([0, 1500])
        #plt.legend()
    #plt.xlim([0, 1500])
    plt.show()

    
    
    
    
    return

def Text_Code (session, dbKey, tableName, attribName):
    table = tableName
    attribute = attribName
    tableRef = gdl.PartialTableReference(tableName=table)
    
    attrRefs = [gdl.AttributeReference(name=a, DBKey=dbKey, partialTableReference=tableRef) for a in attributes]
    recordRefs = [r.recordReference for r in searchResults]
    request = gdl.GetRecordAttributesByRefRequest(recordReferences=recordRefs, attributeReferences=attrRefs)
           
    recordData = session.dataExportService.GetRecordAttributesByRef(request).recordData
    
    s = [None]*len(df2)
    for attribute in attributes:
        for idx, record in enumerate(recordData):
            attrValue = next((x for x in record.attributeValues if x.attributeName == attribute), None)
                s[idx] = attrValue.longTextDataType.value if attrValue else None

        df2[attribute] = s
        
    print(df2)
    df2.to_csv('file.csv', encoding='utf-8', index = 'False')
return


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
#       Graphical_Data(session, dbkey, tableName, recordName, attribName)
#else if (Value.dataType == "LTXT") :
#       Text_Code(session, dbKey, tableName, attribName)
#else if (Value.dataType == "TABL") :
#else if (Value.dataType == "TABL") :










