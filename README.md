# GiftFinder
##### Author: Michael Halim

A recommender engine that recommends gift categories and products from a recipient's Twitter history. A user can go to the web-app and enter the gift-recipient's Twitter handle and the model identifies top three gift categories that the recipient may be interested in. Then, popular gift items in Amazon, identified from various gift blogs, are recommended based on similarity to the predicted categories.

### Project Motivation

For many people, including myself, finding the perfect gift for someone is a challenging and stressful experience. Fortunately we live in the digital age, where more and more people are sharing information about themselves in social media. I started to wonder: can we streamline the gift giving process by identifying what gift topics someone might like based on their social media profile, and from that recommend the perfect gift? This train-of-thought led me to develop this web-app.

### Web-App Demo


### Instructions

1. Clone repository and install data science libraries, as well as streamlit.
2. Obtain API keys from Twitter and create a new file called keys.py. Store API keys in a class.
3. Run app.py from terminal using the following command: streamlit run app.py
