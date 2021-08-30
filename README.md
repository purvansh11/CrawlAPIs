# CrawlAPIs

Public APIs List Crawler
=======================
This is a simple yet powerful crawler that gets the list of all public APIs and stores it in a database. 

Points achieved
--------

![SchemaDiagram](/assets/Schema.png)
    

* Code follows Object Oriented Programming principles with the implementation of Encapsulation and Constructor Invoking
* End-to-end support for handling authentication requirements & token expiration of server. This is enabled by fetching a new token after a regular interval of time well before it expires.
* Complete Pagination support in getting all data - including index categories(Eg. Animals) as well ass Sub-Categories(Eg. Dogs)
* Solves the problem of Rate Limiting Server requests by regular cool-down period prior to sending the next request.
* Crawls all public APIs and stores it in sqlite3 database as well generates an excel sheet for ease of visualization.
* Special attention is paid to URL links. Since each endpoint URL is generated dynamically, characters like ' ' and '&' are replaced to their ASCII values i.e %20 and %26 respectively

Steps to Run Code
-----
1. Open Command Prompt
2. run "git clone https://github.com/purvansh11/CrawlAPIs.git" in any directory
3. run "cd CrawlAPIs"
4. run "pip install -r requirements.txt"
5. run "python main.py"
6. Since each request to sub-categories is sent every 20 sec, the final output shall be generated in 45 mins.
7. Once the code runs successfully, check for the output of the sample query in the command prompt.
8. In the same directory i.e. CrawlAPIs, check the thus generated excel sheet for visualizing the API list

Deliverables
-------------------------
* The final output generated consists of 640 rows of data.
* All the points from the Points to be achieved have been taken care of.
* If given more days, I shall improve on mainly two things - First is that I would think of some way to optimize the code since it takes 45 mins to get the output file. Secondly, I would be looking forward to its deployment to provide a tool to any user to enter any SQL query and provide the user with relevant data in any required form.

Feedback
--------

I would like to thank the team at Postman who gave this opportunity to me. I would be looking forward to working on similar projects at Postman since I am passionate about problem-solving and Python programming. 
