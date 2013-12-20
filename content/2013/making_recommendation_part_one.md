Title: Making Recommendations Part I - Item-based Collaborative Filtering
Date: 2013-12-08 10:00
<!-- Category: DMML -->
<!-- Tags: recommendation -->
Author: Ray Chen

Recommender systems are popular on e-commerce web sites, to make personalized
recommendations for products or services. Using the [MovieLens 100k](http://www.grouplens.org/datasets/movielens) 
dataset, I plan to build a recommnender system, which makes automatic recommendations 
when a user inputs a list of movie ratings.

The "MovieLens 100k" data set consists of:
    - 10K ratings (1-5) from *943* users on *1682* movies.
    - Each user has rated at least 20 movies.
    - Simple demographic info for the users (age, gender, occupation, zip)

User-based or Item-based Collaborive Filtering
----------------------------------------------

Collaborative Filtering (CF) is the most popular recommendation technique. CF works by
building a database of preferences for items by users, and generates recommendations or
makes predictions based on user-user similarity or item-item similarity. A user-based 
CF algorithm represents a user as a N-dimensinal vector of items, where N is the number 
of distinct items. The algorithm generates recommendations for a user based on a few other 
users who are most similar to him/her. Rather than matching user to user, item-based CF 
represents an item as a M-dimensinal vector of users, where M is the number of distinct users.
It matches an user's rated items to similar items, then combines those similar items into 
a recommendation list.

After pass "MovieLens 100K" data set, we have a user-item matrix (943x1682). In the case of 
user-based CF the similarity is computed along the rows of the matrix, while in the case of 
item-based CF the similarity is computed along the column. 

Similarity Computation
----------------------
