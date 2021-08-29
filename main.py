import requests
import json
import itertools
import time
import sqlite3
import pandas as pd
import urllib

class CrawlAPIs:
    
#   Constructor Initialization
    def __init__(self, tokenUrl, token, headers):
        self.tokenUrl = tokenUrl
        self.token = ""
        self.headers = {}
        
#     Encapsulation for data members - Token  
    def setToken(self):
        response = requests.request("GET", self.tokenUrl)
#       Returns an HTTPError object if an error has occurred
        response.raise_for_status()
        self.token = response.json()["token"]

#   Encapsulation for data members - Headers  
    def setHeaders(self):
        self.headers = {'Authorization' : "Bearer " + self.token}

#   Gives the list of categories - Eg. Animals, Anime, Anti-Malware...
    def getIndexCategories(self):
        indexCatergories = []
        pageNo = 1

#       Encapsulation
        self.setToken()
        self.setHeaders()

        while True:
            indexCatergoryUrl = "https://public-apis-api.herokuapp.com/api/v1/apis/categories?page=" + str(pageNo)
            response = requests.request("GET", indexCatergoryUrl, headers=self.headers)

#           Work around for rate limited server in the worst case when Rate Limiting exceeds 3 requests per minute
            if response.status_code == 429:
                time.sleep(int(response.headers["Retry-After"]))
            response.raise_for_status()
            
#           Pagination
            if response.json()["categories"] == []:
                break

            pageNo += 1
            indexCatergories.append(response.json()["categories"])
            
#        Flattens the 2D list - indexCatergories into 1D list
        indexCatergories = list(itertools.chain.from_iterable(indexCatergories))
        return indexCatergories

    
    def getPublicAPIsResponse(self,indexCatergories):
        publicAPIsResponse = {}
        
        for category in indexCatergories:

            pageNo = 1
            
#           A list of json objects depecting each sub categories
            subCategoriesList = []
            
            while True:
                print("Sleeping for 20 sec...")
            
#               Sleeps for 20 sec to avoid multiple requests to the rate limited server
                time.sleep(20)

                self.setToken()
                self.setHeaders()

                subCategoryUrl = "https://public-apis-api.herokuapp.com/api/v1/apis/entry?page=" + str(pageNo) + "&category=" + urllib.parse.quote(category, safe='')
                print("Hitting endpoint: ",subCategoryUrl)
                response = requests.request("GET", subCategoryUrl, headers=self.headers)
                response.raise_for_status()
                
#               Work around for rate limited server in the worst case when Rate Limiting exceeds 3 requests per minute
                if response.status_code == 429:
                    time.sleep(int(response.headers["Retry-After"]) + 20)

#               Pagination
                if response.json()["categories"] == []:
                    break
                pageNo += 1

                subCategoriesList.append(response.json()["categories"])
                
#           Flattens the 2D list - subCategoriesList into 1D list
            publicAPIsResponse[category] = list(itertools.chain.from_iterable(subCategoriesList))
        return publicAPIsResponse

#   Create APIList Dataframe to convert it to sqlite / excel sheet for further use
    def getAPIListDf(self, indexCatergories, publicAPIsList):
        frames = []
        for category in indexCatergories:
            categoryDf = pd.DataFrame.from_records(publicAPIsList[category])
            cols = categoryDf.columns.tolist()
#           Rearrange columns to bring 'Category' first
            cols = cols[-1:] + cols[:-1]
            categoryDf = categoryDf[cols]
            frames.append(categoryDf)
#       Contact all dataframes
        APIListDf = pd.concat(frames)
        return APIListDf

#   Create Categories Dataframe to convert it to sqlite / excel sheet for further use
    def getCategoriesDf(self, indexCatergories):
        return pd.DataFrame(indexCatergories,columns=['CategoryName'])

#   Create Database in sqlite3
    def createDatabase(self, df, tableName):
        con = sqlite3.connect("CrawledAPIs.db")
        df.to_sql(tableName, con, if_exists="replace")
        print("DB created")

#   Create Database in Excel to visualize output
    def createExcelDb(self, df):
        print("To print excel file....")
        df.to_excel("./CrawledAPIs.xlsx", index = False)
        print("Excel file created")

#   Check sample queries to validate database entries
    def runSampleQueries(self):
        con = sqlite3.connect("CrawledAPIs.db")
        cur = con.cursor()
        AnimalsCategoryDfFromDB = pd.read_sql_query("SELECT * FROM APIList WHERE Category=\'Animals\';", con)
        print("Animals Category list dataframe: \n",AnimalsCategoryDfFromDB)
        
        
if __name__ == "__main__":
    
    tokenUrl = "https://public-apis-api.herokuapp.com/api/v1/auth/token"
    crawlAPIs = CrawlAPIs(tokenUrl, "", {})
    
#   Get the list of categories - Eg. Animals, Anime, Anti-Malware...
    indexCatergories = crawlAPIs.getIndexCategories()
    print("List of index categories: ",indexCatergories)
#   Get raw API json Response from Server
    
    publicAPIsResponse = crawlAPIs.getPublicAPIsResponse(indexCatergories)
    
#   Convert obtained data to dataframes
    APIListDf = crawlAPIs.getAPIListDf(indexCatergories, publicAPIsResponse)
    categoriesDf = crawlAPIs.getCategoriesDf(indexCatergories)
    print(APIListDf)
    print(categoriesDf)

#   Create Database
    crawlAPIs.createDatabase(APIListDf, "APIList")
    
#   Create Excel sheet in current working directory to visualize db
    crawlAPIs.createExcelDb(APIListDf)

#   Validate Database by running sample queries
    crawlAPIs.runSampleQueries()
    print("Finished scaping...")
    print("Check your current working directory for file named: \"CrawledAPIs/xls\" for visualizing final data")

