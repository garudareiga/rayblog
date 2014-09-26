Title: Making Recommendations Part I - Item-based Collaborative Filtering
Date: 2013-12-08 10:00
Author: Ray Chen
Category: Data
Tags: machine learning, json, mongodb 

Recommender systems are popular on e-commerce web sites, to make personalized
recommendations for products or services. Using the [MovieLens 100k](http://www.grouplens.org/datasets/movielens) 
dataset, I plan to build a recommnender system, which makes automatic recommendations 
when a user inputs a list of movie ratings.

The "MovieLens 100k" data set consists of:

- 10K ratings (1-5) from *943* users on *1682* movies.
- Each user has rated at least 20 movies.
- Simple demographic info for the users (age, gender, occupation, zip)

# User-based or Item-based Collaborative Filtering

Collaborative Filtering (CF) is the most popular recommendation technique. CF works by
building a database of preferences for items by users, and generates recommendations or
makes predictions based on user-user similarity or item-item similarity. A user-based 
CF algorithm represents a user as a N-dimensinal vector of items, where N is the number 
of distinct items. The algorithm generates recommendations for a user based on a few other 
users who are most similar to him/her. Rather than matching user to user, item-based CF 
represents an item as a M-dimensinal vector of users, where M is the number of distinct users.
It matches an user's rated items to similar items, then combines those similar items into 
a recommendation list.

After parsing the "MovieLens 100K" data set, we have a user-item representation matrix (943x1682).
In the case of user-based CF the similarity is computed along the rows of the matrix, while in the case of 
item-based CF the similarity is computed along the column. In practice, user-based CF shows
weakness evaluating large, sparse datasets. Thus, I choose item-based CF to build my recommender. 
The main idea here is to analyze the user-item matrix to identify relations between different items
and then to use these relations to compute the prediction score for a given user-item pair.

# Similarity Computation

One critical step in the item-based CF algorithm is to compute the similarity between the items.
The basic idea in similarity computation between two items i and j is to first isolate the users
who have rated both of these items, and then to apply a similarity computation technique to determine
the similarity. There are a number of different ways to compute the similarity between items, such
as Euclidean distance, Jaccord coefficient, cosine similarity, Pearson's correlation coefficient. 
Euclidean distance is often used for dense, continuous data. For sparse data, which often consists 
of asymmetric attributes, we typically employ Jaccord coefficient or cosine similarity that ignore 
0-0 matches. However, Jaccord coefficient or cosine similariy does not take the scale of data into 
account. Thus, I choose adjusted cosine similarity and Pearson's correlation for similarity compuation. 
After similarity compuation, we can build a item similarity dictionary.

### Pearson's Correlation

The similarity between two item i and j is measured by Pearson's correlation.  Let the set of users 
who both rated i and j are denoted by U, then the correlation is given by 

\begin{equation}
sim(i, j) = \frac{\sum_{u \in U}(R_{u,i} - \overline{R_{i}})(R_{u,j} - \overline{R_{j}})}{\sqrt{\sum_{u \in U}(R_{u,i} - \overline{R_{i}})^2}\sqrt{\sum_{u \in U}(R_{u,j} - \overline{R_{j}})^2}}
\end{equation}


### Adjusted Consine Similarity

The adjusted consine similarity substracts the corresponding user average from each co-rated pair.
The similarity between items i and j is given by

\begin{equation}
sim(i, j) = \frac{\sum_{u \in U}(R_{u,i} - \overline{R_{u}})(R_{u,j} - \overline{R_{u}})}{\sqrt{\sum_{u \in U}(R_{u,i} - \overline{R_{u}})^2}\sqrt{\sum_{u \in U}(R_{u,j} - \overline{R_{u}})^2}}
\end{equation}

# Recommendation Generation 

On an item i for a user u, we computes the prediction by computing the sum of ratings given by the user on the items
similar to i. Each rating is weighted by the corresponding similarity $s_{i,j}$ between items i and j. We can denote
the similar item set of item i as N, and the prediction $P_{u,i}$ as

\begin{equation}
P_{u,i} = \frac{\sum_{j \in N}(s_{i,j}*R_{u,j})} {\sum_{j \in N}(\mid s_{i,j} \mid)}
\end{equation}

The recommendations will consist of a set of similar items with high prediction values.

# Python Implementation

A Python module of my recommender system is availabe in my [github reposity](https://github.com/garudareiga/PyDMML/blob/master/recommendation_movie_lens/Recommendation.py). The method to build a recommender system is as follows:

```python
>>> obj = Recommendation(num_user=943, num_item+1682)
>>> obj.parse_data('ml-100k/u.data')
>>> obj.do_item_based_collaborative_filtering(similarity=obj.item_similarity_pearson, num_similar_items=100)
```
   
Next, it makes prediction for a random user as follows:

```python
>>> user_id = random.randint(1, obj.num_user)
>>> obj.make_recommendations(user_id)
```

# Performance
In a practical scenario, we usually have a set of item that is static compared to the number of users
that changes most often. The static nature of items makes precomputing the item similarities possible.
One possible way is to compute all-to-all similarity and then performing a quick table look-up to retrieve
the similarity values. This offline computation of the similar-items table is extremely time intensive,
with $O(N^2M)$ as worst case. However, it's close to $O(NM)$ in practice, as most customers have very few
purchases. Although building the item similarity takes a long item, recommendations are 
almost instantaneous afterwards. Therefore, item-based CF is efficient for a large dataset, with the additional 
overhead of maintining the item similarity dictionary. This method, although saves time, requires an
$O(M^2)$ space for _M_ items. In fact, we only need a small number of similar items to compute predictions.
For each item, we retain only the _K_ most similar items, where _K_ << _M_, and record these item similarities.
Obviously, we observe a quality-performance trade-off: to ensure good quality we need have a large value _K_, which
leads to the performance problem. 

In my project, the offline similarity precomputing takes about 30~40 minutes using Pearson's corelation to  
compute item similarity. For each item, I retain 100 most similar items and provide an option to store their similarity
values in a local JSON disk file, or in a MongoDB collection (One document correspond to one item with its 100 most
similar items and their similarity scores). At the start of recommendation, I simply load the precomputed similarity
information from the local JSON disk file or the MongoDB collection.
