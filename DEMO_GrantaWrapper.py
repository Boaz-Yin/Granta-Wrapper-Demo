


import GRANTA_MIScriptingToolkit as gdl
import getpass
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt


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
        pd.options.display.max_colwidth = 100
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
        pd.options.display.max_colwidth = 100
        df3 = pd.DataFrame({'ShortName': [r.shortName for r in searchResults],
                        'LongName': [r.longName  for r in searchResults]})
        print(df3)
        i = raw_input("Enter the index number of record to be selected: ")
        i = int(i)
        print(i)
        recordName = df3.loc[i][0]
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

export = "N"
while export != "Y":

    print('Available Attributes: \n1. Density\n2. Specific Heat with Temp.\n3. Residual Stress')
    print('4. Condition\n5. Crack Image\n6. Supplier Info\n7. In Service Crack\n')
    inp = int(raw_input("Enter the option number: "))
    if inp == 1:
        attribName = 'Density'
    elif inp == 2:
        attribName = 'Specific Heat with Temp.'
    elif inp == 3:
        attribName = 'Residual Stress'
    elif inp == 4:
        attribName = 'Condition'
    elif inp == 5:
        attribName = 'Crack Image'
    elif inp == 6:
        attribName = 'Supplier Info'
    elif inp == 7:
        attribName = 'In Service Crack'

    
    #attribName = 'Density'
    #attribName = 'Specific Heat with Temp.'
    #attribName = 'Residual Stress'
    #attribName = 'Condition'
    #attribName = 'Crack Image'
    #attribName = 'Supplier Info'
    
    
    browse = gdl.BrowseService(session.mi_session)
    a = gdl.AttributeReference(name=attribName, partialTableReference = gdl.PartialTableReference(tableName=table),DBKey=dbKey)
    resp = browse.GetAttributeDetails(gdl.GetAttributeDetailsRequest([a])) 
    
    dataExportRequest = gdl.GetRecordAttributesByRefRequest(recordReferences=[record.recordReference], attributeReferences=[a])
    dataExportResponse = session.dataExportService.GetRecordAttributesByRef(dataExportRequest)
    myRecordData = dataExportResponse.recordData[0]
    #myRecordData = dataExportResponse.recordData
       
    value = myRecordData.attributeValues[0]
    #value = myRecordData.attributeValues
    
    print(value)
    print("Attribute Name: {0.attributeName}, Type {0.dataType}".format(value))
    
    
    
    #Value.dataType detects the data type and from here on we we enter the functions
    
    
    if (value.dataType == "POIN") :
    
        print("\n")
        
        attrValue = value.pointDataType.points
        if attrValue == "":
            print("No Data!")
        else:
            for xx in attrValue:
                print(xx.value)
        
        
    #    
    #
    if (value.dataType == "FLOAT_FUNCTIONAL_SERIES") :
        graph = value.floatFunctionalSeriesDataType.graph
        if graph == "":
            print("No Data!")
        else:
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
    
    
    
    
    
    if (value.dataType == "TABL") :
        
        
        myTable = value.tabularDataType
        if myTable == "":
            print("No Data!")
        else:
                
            for det in myTable.columns:
                print(det.name)
            for row in myTable.tabularDataRows:
        #       print("Row {0}:".format(i+1))
                print("\t{0}".format(row.cells[0].longTextDataValue.value))
                print("\t{0}".format(row.cells[1].pointDataValue.points[0].value))
                i=i+1
                
    
    
    
    
    
    if (value.dataType == "LTXT") :
    #    s = [None]*len(df2)
    #    for attribute in attribName:
    #        for idx, record in enumerate(myRecordData):
    #            attrValue = next((x for x in record.attributeValues if x.attributeName == attribute), None)
    #            #print(attrValue.dataType)
    #            if (attrValue.dataType == 'LTXT'):
    #                s[idx] = attrValue.longTextDataType.value if attrValue else None
    #            elif (attrValue.dataType == 'STXT'):
    #                    s[idx] = attrValue.shortTextDataType.value if attrValue else None
    #            elif(attrValue.dataType == 'DCT'):
    #                        s[idx] = attrValue.DiscreteDataType.discreteValues.value if attrValue else None
    #                        df2[attribute] = s
    #    
    #            print(df2)
    #            df2.to_csv('Ofile1.csv', encoding='utf-8', index = 'False')
        if value.longTextDataType.value == "":
            print("No Data!")
        else:
            print(value.longTextDataType.value)
    
    if (value.dataType == "PIC"):
        print("Attribute Name: {0.attributeName}, Type {0.dataType}".format(value))
    if value.dataType == "HYP":
        value = value.HyperlinkDataType.value
        if value == "":
            print("No Data!")
        else:
            print(value)
    
    export = raw_input('Export Data? (Y/N)')
    if export == 'Y':
        break
    
         
###EXPORTER######








#
#expreq = gdl.RecordNameSearchRequest(recordName = recordName, table = gdl.TableReference(DBKey = dbKey, name=table),searchShortNames = True)
#expresp = session.searchService.RecordNameSearch(expreq)
#print("Found {0} record(s)".format(len(expresp.searchResults)))
#rec = expresp.searchResults[0].recordReference
#
#
#request = gdl.ExportersForRecordsRequest(records=[rec])
#resp = session.engineeringDataService.ExportersForRecords(request)
#print("\nOutput of exporters for the current")
#for  exporter in resp.records[0].exporters:
#    print("{0} ({1}) - {2}".format(exporter.name, 
#                                   exporter.package, 
#                                   exporter.description))
#
#
#print("\n")
#print("HI")
#req = gdl.GetExporterParametersRequest(records=[rec], exporterKey=exporter.key)
#expParams = session.engineeringDataService.GetExporterParameters(req)
#for attrib in expParams.records[0].attributes:
#    print(attrib.attribute.name)
#    for param in attrib.parameters:
#        print("\t" + param.name)
#        
#    
#
#req  =  gdl.GetRecordAttributesRequest(recordReferences=[rec])
#attribs = session.browseService.GetRecordAttributes(req)
#
#myParam = expParams.records[0].attributes[0].parameters[0]
#pwv = gdl.ParameterReferenceAndValue(parameterValue=gdl.ParameterValue(1.337), 
#                                     parameter=myParam.parameterReference)
#
#pv = gdl.UnittedParameterValue(unitSymbol=myParam.unit.unitSymbol, 
#                               parameterWithValues=pwv)
#
#
#expReq = gdl.ExportRecordDataRequest(attributeReferences=[b.attribute.attribute for b in attribs.recordAttributes], 
#    records=[rec], 
#    exporterKey=exporter.key,
#    parameterValues=[pv]
#)
#
#
#resp = session.engineeringDataService.ExportRecordData(expReq)
#
#print(resp.text[:200] + "...")