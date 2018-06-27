# perfBugMiner (Updated: 06/26/2018)

This version use GitHub API to collect related information and generat several charts as followed: </br>
Chart1: Number of issues created per week (for each system) </br>
Chart2: Number of isses closed per week (for each system) </br>
Chart3: Boxplot: lifetime of issues (for different tag/ different systems) </br>
Chart4: Boxplot: number of comments per issue (for different tag/ different systems) </br>
Chart5: Boxplot: ratio of member per issue (for different systems) </br>
Chart6: Boxplot: ratio of comment from member per issue (for different systems) </br>
Chart7: Boxplot: number of contributions from users per issue (for different systems) </br>
Chart8: Number of commits per user (for member/ not member) </br>
Chart9: Number of commits per user (for different systems) </br>

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

macOS/win10 (tested) </br>
Python 2.7 or up </br>
matplotlib package </br>
pillow package </br>

### Installing

Please clone the project to your computer and install the required packages. 

## How to run
For single system: </br>
Step 1: Put the URL and the name of selected system in the config.py file (Line 160 & 162) </br>
Step 2: Run the Issue_OneProject.py to generate the json file of the system, like Tensorflow.json; 
        And output the Chart 1 & 3 & 4 & 7 & 8 </br>
Step 3: Run github_issues_api_get_closed_issues.py to generat the Chart 2 </br>

For multiple systems: </br>
Step 4: Creat a folder named PLOTPRO </br>
Step 5: Copy all different systems json file to the PLOTPRO folder </br>
Step 6: Run the plotdata.py & ProPlot.py to generate the Chart 3 & 4 & 5 & 6 & 7 & 9 </br>

### Limitations 
Basic on the policy of GitHub API, the limit is 5000 queries per hour; After exceed the limit, the Issue_OneProject.py will throw an error. </br>
In this situation, you can use VPN to change your IP, swich to other token, or wait more than 10 mins and restart to run the code. </br>
Then the Issue_OneProject.py will continue the process. </br>


