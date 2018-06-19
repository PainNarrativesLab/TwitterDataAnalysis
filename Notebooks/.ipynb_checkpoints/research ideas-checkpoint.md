
Perhaps look at words used to complain about pain "It hurts! Owwww" and their 
freq (maybe tf-idf) in different groups of users tweets


Remember: Having users who haven't tweeted doesn't mean that they are bots. We were also searching for user descriptions. We can still ask questions like 'Do people who mention migraine interestingly differ from people who mention fibro?' even if we have to query twitter for their tweets


# If a word w occurs in one tweet, how many other tweets by the same user does it occur in?
Probably should look at its tf-idf
Steps
- Select experimental number n of users.
- For n randomly selected users who use the target term in their profile or tweets, download all tweets by the user
- Examine the fequency with which the term appears accross all their tweets. Examine whether other pain terms are more likely to occur.

# Project: Can we reliably pick out pain patients
- Perhaps one criteria could be whether their profiles involve pain and their tweets contain tweets about pain experience. 
- Then some machine learning could help us pick out pain patients who don't have pain in their profiles


# Project: Can we reliably pick out pain patients without relying on their use of pain condition terms


# Project: Gather control group tweets

