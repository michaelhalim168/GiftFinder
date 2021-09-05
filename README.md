# GiftFinder
##### Author: Michael Halim

A recommender engine that recommends gift categories and products from a recipient's Twitter history. A user can go to the web-app and enter the gift-recipient's Twitter handle and the model identifies top three gift categories that the recipient may be interested in. Then, popular gift items in Amazon, identified from various gift blogs, are recommended based on similarity to the predicted categories.

### Project Motivation

For many people, including myself, finding the perfect gift for someone is a challenging and stressful experience. All of the "gift-recommender" platforms that currently exist in public require the user to fill some sort of form about the gift-recipient; this is a tedious process and requires the user to have a solid understanding of the recipient's interests.  Fortunately we live in the digital age, where more and more people are sharing information about themselves in social media platforms, like Twitter. I started to wonder: can we streamline the gift giving process by identifying what gift topics someone might like based on their social media profile, and from that recommend the perfect gift? This train-of-thought led me to develop this web-app.

### Web-App Demo

![](app-recording.gif)

The web-app prompts the user to enter the public Twitter handle of the person he/she would like to buy a gift for. The web-app then returns some gift categories this person may like as well as a few items related to these categories that this person may like as gifts. If the user sees an item that appears interesting, the web-app redirects the user to the product page on Amazon. So instead of spending hours on Google or Reddit trying to find gifts for someone, a user can use this app and find and purchase the perfect gift in a matter of seconds!

### Project Approach

Step 0: Determine most popular gift topics and its associated subreddits.
