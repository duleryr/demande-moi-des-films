# coding: utf-8

# All the recommandation logic and algorithms goes here

from random import choice

from app.User import User
import operator

class Recommendation:

    def __init__(self, movielens):

        # Dictionary of movies
        # The structure of a movie is the following:
        #     * id (which is the movie number, you can access to the movie with "self.movies[movie_id]")
        #     * title
        #     * release_date (year when the movie first aired)
        #     * adventure (=1 if the movie is about an adventure, =0 otherwise)
        #     * drama (=1 if the movie is about a drama, =0 otherwise)
        #     * ... (the list of genres)
        self.movies = movielens.movies

        # List of ratings
        # The structure of a rating is the following:
        #     * movie (with the movie number)
        #     * user (with the user number)
        #     * is_appreciated (in the case of simplified rating, whether or not the user liked the movie)
        #     * score (in the case of rating, the score given by the user)
        self.ratings = movielens.simplified_ratings

        # This is the set of users in the training set
        self.test_users = {}

        # Launch the process of ratings
        self.process_ratings_to_users()

    # To process ratings, users associated to ratings are created and every rating is then stored in its user
    def process_ratings_to_users(self):
        for rating in self.ratings:
            user = self.register_test_user(rating.user)
            movie = self.movies[rating.movie]
            if hasattr(rating, 'is_appreciated'):
                if rating.is_appreciated:
                    user.good_ratings.append(movie)
                else:
                    user.bad_ratings.append(movie)
            if hasattr(rating, 'score'):
                user.ratings[movie.id] = rating.score

    # Register a user if it does not exist and return it
    def register_test_user(self, sender):
        if sender not in self.test_users.keys():
            self.test_users[sender] = User(sender)
        return self.test_users[sender]

    # Display the recommendation for a user
    def make_recommendation(self, user):
        movie = choice(list(self.movies.values())).title
        similarities = self.compute_all_similarities(user)
        sorted_sim = sorted(similarities, key=lambda x: x[1])
        # DEBUG
        #for key, user in self.test_users.items():
        #    print(key)
        #    print(user.id)
        #print(self.get_similarity(user, self.test_users[11]))

        id_best_score = []
        for i in range(1, 6):
            id_best_score.append(sorted_sim[len(sorted_sim) - i][0])

        closest_users = []
        for id_closest_users in id_best_score:
            closest_users.append(self.test_users[id_closest_users])

        list_recommandations = []
        for close_user in closest_users:
            list_recommandations.append([film.title for film in close_user.good_ratings])
            
        recommendations = []
        for i in range(0,5):
            for j in range(i,5):
                recommendations += set(list_recommandations[i]) & set(list_recommandations[j])

        recommendations = set(recommendations)
        return "Vos recommandations : " + ", ".join(recommendations)

    # Compute the similarity between two users
    @staticmethod
    def get_similarity(user_a, user_b):
        score = 0
        normA = Recommendation.get_user_norm(user_a)
        normB = Recommendation.get_user_norm(user_b)

        if normA < normB:
            main_user = user_a
            other_user = user_b
        else:
            main_user = user_b
            other_user = user_a

        for goodRatingMain in main_user.good_ratings:
            if goodRatingMain in other_user.bad_ratings:
                score -= 1
            if goodRatingMain in other_user.good_ratings:
                score += 1
        for badRatingMain in main_user.bad_ratings:
            if badRatingMain in other_user.bad_ratings:
                score += 1
            if badRatingMain in other_user.good_ratings:
                score -= 1

        return score/Recommendation.get_user_norm(main_user)

    # Compute the similarity between a user and all the users in the data set
    def compute_all_similarities(self, user):
        res = []
        for key, tmp_user in self.test_users.items():
            res.append((tmp_user.id, self.get_similarity(user, tmp_user)))
        return res

    @staticmethod
    def get_best_movies_from_users(users):
        return []

    @staticmethod
    def get_user_appreciated_movies(user):
        return []

    @staticmethod
    def get_user_norm(user):
        return len(user.good_ratings) + len(user.bad_ratings)

    # Return a vector with the normalised ratings of a user
    @staticmethod
    def get_normalised_cluster_notations(user):
        return []
