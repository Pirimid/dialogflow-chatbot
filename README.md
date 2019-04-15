## Dialogflow Chatbot

[Dialogflow](https://dialogflow.com/) is a Google-owned developer of human-computer interaction technologies based on natural language conversations. The company is best known for creating the Assistant, a virtual buddy for Android, iOS, and Windows Phone smartphones that perform tasks and answers users' question in a natural language.

## Python API:

We have created API in Python which could manipulate the data from our own MySQL database and sends it to the Dialogflow chatbot.

When a user sends a message to the chatbot, the chatbot agent identifies which intents, parameters, and entities using it's NLP and Machine Learning models which are trained upon the sets of the example provided by us. Then the Dialogflow agent sends a POST request to our Python API which we have uploaded on Heroku.

Here below let's discuss on how the API workflow goes:

1. As the API receives the POST request, it triggers the [Python API](main.py).
2. After fetching all the JSON objects in the POST request, our API pulls all the parameters, actions and entities to get a better understanding of what the user wants specifically.
3. Using the MySQL libraries, our API is able to manipulate the data in our database which mimics to that of Bank's database.
4. After performing all the actions as per the user's needs, our API collects all the answers and converts it into the [Dialogflow's JSON object](https://dialogflow.com/docs/fulfillment/how-it-works) (Dialogflow only accepts a response in JSON format).

After which Dialogflow shows the response to the user according to the fulfillment response which it gets from our APIs.
