# Usage
* Run the file named run_cnn.py to execute the program
* The second step is run the predict.py file
* All issues which without tag are stored in the data\issues_nolabel folder
* cnn_model.py build the cnn model, including configure the machine learning engine & set related parameters
* predict.py is use the training model to determine what the category a new issue belongs to
* issues_loader.py include the tool functions & open\read files & transform coding
* issues_spliter.py is focus on how to split different categories files to the relateds folder
* issues_group is use to group small files into a large file
* The training result stored in the folder named tensorboard
