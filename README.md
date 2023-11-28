"# Trello_backend" 

Execute the command below.
```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```
Download JDK from net and install it on local PC.

Next, open a cmd window within the dynamodb_local_latest folder and run the command below.

```bash
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
```
Finally, execute the command below in the upper level (Trello_backend) folder.
Then the server associated with dynamodb will work.

```bash
flask run
```
