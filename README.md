# perfBugMiner (Updated: 08/24/2018)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

macOS/win10 (tested) </br>
Python 2.7 or up </br>
matplotlib Lib </br>
numpy, scipy Lib </br>
sklearn Lib </br>
NLTK package </br>
### Installing

Please clone the project to your computer and install the required packages. 

## How to run
For single system: </br>
Step 1: Set the target system link in the config file </br>
Step 2: Put the simple issues link and catagory in the data.csv </br>
Step 3: Run the gettrain file to extract training data and saving to the traindata file </br>
Step 4: Run the GetKeyword file and GetMode file to generate the keywords and model </br>
Step 5: Run the Issue_OneProject to categorize the issues. 

### Limitations 
Basic on the policy of GitHub API, the limit is 5000 queries per hour; After exceed the limit, the Issue_OneProject.py will throw an error. </br>
In this situation, you can use VPN to change your IP, swich to other token, or wait more than 10 mins and restart to run the code. </br>
Then the Issue_OneProject.py will continue the process. </br>



