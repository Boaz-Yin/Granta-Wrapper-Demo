




import GRANTA_MIScriptingToolkit as gdl
import getpass
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt

#pd.options.display.max_rows = 1000
# 
#Code to enter the service API

#username = ('chen2113')
username = raw_input('Enter your username: ')
#username = "gopalaks"
#password = ('Boiler2018!')

password = getpass.getpass()
#password ="Saikiran17#"

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
dbsel = raw_input("Enter the Database index: ")
dbsel = int(dbsel)
print("\n")

###Getting Tables in a database


#dbKey = raw_input('Enter the DBKey to browse: ')
#dbKey = ('MMPDS11')

dbKey = str(df1.loc[dbsel][0])
tables = browseService.GetTables(gdl.GetTables(DBKey=dbKey)).tableDetails

print("Found {0} tables in database {1}".format(len(tables), dbKey))
#for t in tables:
#    print("Table name: {0}".format(t.tableReference.name))

df10 = pd.DataFrame({'Table Name': [t.tableReference.name for t in tables]})
print(df10)
tin = raw_input('Enter the Table index to browse in: ')
#table = ('MMPDS-11 Data')
tin = int(tin)
table = df10.loc[tin][0]
print("\n")


###########################################BROWSING OPTIONS ###############################################################
print("Choose from the following Browsing Options:")
print("1. Search Based on Material Name\n")
print("2. Search Based on Existence of Property Value and then Choose a Material\n")
inp = raw_input("Enter the option number: ")
inp = int(inp)



while inp != 1 or inp != 2:
    if (inp == 1):
#        searchText = ('304 Steel')
        searchText = raw_input('Enter the material name to be Browsed: ')
    
        simpleTextSearch = gdl.SimpleTextSearch(searchValue=searchText, DBKey=dbKey)
        simpleTextSearchResponse = session.searchService.SimpleTextSearch(simpleTextSearch).searchResults
    
        ##Printing the simple text search response
        #for result in simpleTextSearchResponse.searchResults:
        #    print('{0}'.format(result.shortName))
        pd.options.display.max_colwidth = 100
        df2 = pd.DataFrame({'Short Names': [result.shortName for result in simpleTextSearchResponse],
                        'Long Names': [result.longName for result in simpleTextSearchResponse]})
        with pd.option_context('display.max_rows',10000, 'display.max_columns', 3):
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
        recordName = df3.loc[i][0]
print("\n")













#recordName = "AISI 304, Full Hard, Sheet, strip, Thickness: Up to 0.188 in, AMS 5913, A Basis"
#recordName = "Ti-6Al-4V, Annealed, Plate, Thickness: 0.1875 to 1.001 in, AMS 6945, A Basis"
req = gdl.RecordNameSearchRequest(caseSensitiveNames=False, searchShortNames=True, recordName=recordName)
req.table = gdl.TableReference(DBKey=dbKey, name=table)
resp = session.searchService.RecordNameSearch(req)
record = resp.searchResults[0]

export = "N"
while export != "Y":

    print('Available Attributes: \n1. Density\n2. Youngs Modulus \n3. Poisson Ratio')
    print('4. Condition\n5. Supplier Info\n6. Residual Stress (Voigt Notation)\n7. Crack Image Link\n8. Youngs Modulus with Temperature\n9. Grain Size Distribution - Histogram Plot\n10. Grain Size Distribution (Distribution Parameters)')
    inp = int(raw_input("Enter the option number: "))
    if inp == 1:
        attribName = 'Density'
    elif inp == 2:
        attribName = "Young's Modulus"
    elif inp == 3:
        attribName = 'Poisson Ratio'
    elif inp == 4:
        attribName = 'Condition'
    elif inp == 5:
        attribName = 'Supplier Info'
    elif inp == 6:
        attribName = 'Residual Stress'
    elif inp == 7:
        attribName = 'Crack Image Link'
    elif inp == 8:
        attribName = "Young's modulus with temperature"
    elif inp == 9:
        attribName = "Grain Size Distribution - Histogram Plot"
    elif inp == 10:
        attribName = "Grain Size Distribution (Distribution Parameters)"

    
    
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
                print("\t{0}".format(row.cells[0].longTextDataValue.value))
                print("\t{0}".format(row.cells[1].pointDataValue.points[0].value))
                i=i+1
                
    
    
    
    
    
    if (value.dataType == "LTXT") :
        if value.longTextDataType.value == "":
            print("No Data!")
        else:
            print(value.longTextDataType.value)
    
    if (value.dataType == "PICT"):
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







#
expreq = gdl.RecordNameSearchRequest(recordName = recordName, table = gdl.TableReference(DBKey = dbKey, name=table),searchShortNames = True)
expresp = session.searchService.RecordNameSearch(expreq)
#print("Found {0} record(s)".format(len(expresp.searchResults)))
rec = expresp.searchResults[0].recordReference

#DISPLAYS EXPORTER OPTIONS AVAILABLE FOR THIS RECORD IN GRANTA
request = gdl.ExportersForRecordsRequest(records=[rec])
resp = session.engineeringDataService.ExportersForRecords(request)
print("\nOutput of exporters for the current")

#for exporter in resp.records[0].exporters:
#    print(exporter.description)

df4 = pd.DataFrame({"Exporter Name" :[exporter.name for exporter in resp.records[0].exporters],
                    "Exporter Package": [exporter.package for exporter in resp.records[0].exporters],
                    "Exporter Description" : [exporter.description for exporter in resp.records[0].exporters]})
#                    "Exporter Key" : [exporter.key for exporter in resp.records[0].exporters]})
pd.options.display.max_colwidth = 200

print(df4)

expInp = raw_input("Select the index of the exporter to be used: ")
expInp = int(expInp)
#exporter = df4.loc[expInp][1]
exporter = resp.records[0].exporters[expInp]
print("\n")

req = gdl.GetExporterParametersRequest(records=[rec], exporterKey=exporter.key)
expParams = session.engineeringDataService.GetExporterParameters(req)
#for attrib in expParams.records[0].attributes:
#    print(attrib.attribute.name)
#    for param in attrib.parameters:
#        print("\t" + param.name)
###        
#    
##GETTING ALL APPLICABLE ATTRIBUTES FOR THIS RECORD
req  =  gdl.GetRecordAttributesRequest(recordReferences=[rec])
attribs = session.browseService.GetRecordAttributes(req)




#####################THIS APPLIES FOR EXPORTING FUNCTIONAL DATA###############################################
#myParam = expParams.records[0].attributes[0].parameters[0]
#pwv = gdl.ParameterReferenceAndValue(parameterValue=gdl.ParameterValue(1.337), 
#                                     parameter=myParam.parameterReference)
##
#pv = gdl.UnittedParameterValue(unitSymbol=myParam.unit.unitSymbol, 
#                               parameterWithValues=pwv)
#
#


expReq = gdl.ExportRecordDataRequest(attributeReferences=[b.attribute.attribute for b in attribs.recordAttributes], 
                                     records=[rec], 
                                     exporterKey=exporter.key)
#
#
resp = session.engineeringDataService.ExportRecordData(expReq)

print(resp.text[:200] + "...")


f = open("Material_Output_MFINDEMO"+"1"+".xml", "wb")
f.write(resp.text.encode("utf-8"))