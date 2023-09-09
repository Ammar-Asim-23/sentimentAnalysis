from flask import Flask, request, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load your logistic regression model
model = joblib.load('models/logistic_regression_model.pkl')  # Change the filename as needed
tfidfvectorizer = joblib.load('models/tfidf_vectorizer.pkl')  # Change the filename as needed
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        headline = request.form['headline']
        #Ensure the input data is in the correct shape (2D array)
        headline = tfidfvectorizer.transform(np.array([headline]))
        # Perform prediction using your model
        prediction = model.predict(headline)[0]

        # You can map the prediction to 'positive', 'negative', or 'neutral' based on your model's classes
        sentiment = 'positive' if prediction == '1' else 'negative' if prediction == '0' else 'neutral'

        return render_template('predict.html', sentiment=sentiment)

    return render_template('predict.html')

if __name__ == '__main__':
    app.run(debug=True)
