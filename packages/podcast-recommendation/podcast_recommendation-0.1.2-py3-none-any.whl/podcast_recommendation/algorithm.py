from neo4j import GraphDatabase as GD
import pandas as pd
from sklearn.linear_model import LogisticRegression

import pkg_resources
import os

DATA_PATH = pkg_resources.resource_filename(__name__, 'data/')

X_PATH = os.path.join(DATA_PATH, 'x_train.csv')
Y_PATH = os.path.join(DATA_PATH, 'y_train.csv')
CAT_PATH = os.path.join(DATA_PATH, 'categories_sample.csv')
RTG_PATH = os.path.join(DATA_PATH, 'ratings_sample.csv')

class PodcastRecommendation:
    def __init__(self, uri, auth, x_path = X_PATH, y_path = Y_PATH, verbose=False):
        self.driver = GD.driver(uri, auth = auth)
        self.features = ['cat_based', 'cat_cnt', 'user_based', 'user_cnt',
            'adamic_adar', 'resource_allocation', 'link_cnt', 'cat_avg', 'user_avg',
            'adar_avg', 'ra_avg']
        self.lr = LogisticRegression(solver='liblinear', C=0.5)
        if verbose: print("Reading x_train")
        X = pd.read_csv(x_path)
        if verbose: print("Reading y_train")
        Y = pd.read_csv(y_path)
        if verbose: print("Training model")
        self.lr.fit(X[self.features], Y.values.reshape(1,-1)[0])
        if verbose: print("Training complete")
    
    def build_graph(self, cat_path = CAT_PATH, rtg_path = RTG_PATH, delete_all = True, verbose=False):
        if delete_all:
            self.delete_all()
        
        if verbose: print("Reading categories")
        cat = pd.read_csv(cat_path)
        if verbose: print("Reading ratings")
        rtg = pd.read_csv(rtg_path)
        
        if verbose: print("Creating categories, categories and IsA")
        cat.apply(self.build_cat, axis=1)
        
        if verbose: print("Creating users, categories and ratings")
        rtg.apply(self.build_rtg, axis=1)
        
        if verbose: print("Build complete")
        
        
    def build_cat(self, row):
        with self.driver.session() as sess:
            sess.write_transaction(
                self._build_cat, row['category'], row['category_id'], row['podcast_id'])
            
    @staticmethod
    def _build_cat(tx, category, category_id, podcast_id):
        query = (
            "MERGE (p:Podcast{id: $podcast_id}) "
            "MERGE (c:Category{id: toInteger($category_id), name: $category}) "
            "MERGE (p)-[r:IsA]->(c) "
        )
        tx.run(query, podcast_id=podcast_id, category_id=category_id, category=category)
        
    def build_rtg(self, row):
        with self.driver.session() as sess:
            sess.write_transaction(
                self._build_rtg, row['user_id'], row['podcast_id'], row['rating'])
            
    @staticmethod
    def _build_rtg(tx, user_id, podcast_id, rating):
        query = (
            "MERGE (u:User{id: $user_id}) "
            "MERGE (p:Podcast{id: $podcast_id}) "
            "MERGE (u)-[r:Rating{rating: toInteger($rating)}]->(p) "
        )
        tx.run(query, user_id=user_id, podcast_id=podcast_id, rating=rating)
        
    def close(self):
        self.driver.close()
        
    def delete_all(self):
        with self.driver.session() as sess:
            sess.write_transaction(
                self._delete_all)
            
    @staticmethod
    def _delete_all(tx):
        query = "MATCH (m)-[r]->(n) DELETE m, n, r"
        tx.run(query)
            
    def recommend(self, user_id):
        df = self.gen_df(user_id)
        df = self.gen_data(df)
        df['proba'] = self.lr.predict_proba(df[self.features])[:,1]
        df = df.sort_values(by='proba', ascending=False)
        return df[['podcast_id', 'proba']]
    
    def gen_data(self, df):
        c_names = ['cat_based', 'cat_cnt', 'user_based', 'user_cnt',
                   'adamic_adar', 'resource_allocation', 'link_cnt']
        df[c_names] = df.apply(self.gen_data_row, axis=1, result_type='expand')
        df['cat_avg'] = df['cat_based'] / df['cat_cnt']
        df['user_avg'] = df['user_based'] / df['user_cnt']
        df['adar_avg'] = df['adamic_adar'] / df['link_cnt']
        df['ra_avg'] = df['resource_allocation'] / df['link_cnt']
        df = df.fillna(0)
        return df 
    
    def gen_data_row(self, row):
        u_id, p_id = row['user_id'], row['podcast_id']
        
        result = self.get_cat_based(u_id, p_id)
        result += self.get_user_based(u_id, p_id)
        result += self.adamic_adar(u_id, p_id)
        result += self.resource_allocation(u_id, p_id)
        
        return result
        
    def delete_rtg(self, user_id, podcast_id):
        with self.driver.session() as sess:
            sess.write_transaction(
                self._delete_rtg, user_id, podcast_id)
    
    @staticmethod
    def _delete_rtg(tx, user_id, podcast_id):
        query = (
            "MATCH (u:User)-[r]->(p:Podcast) "
            "WHERE u.id = $user_id AND p.id = $podcast_id "
            "DELETE r"
        )
        tx.run(query, user_id=user_id, podcast_id=podcast_id)

        
    def create_rtg(self, user_id, podcast_id, rating):
        with self.driver.session() as sess:
            sess.write_transaction(
                self._create_rtg, user_id, podcast_id, rating)
    
    @staticmethod
    def _create_rtg(tx, user_id, podcast_id, rating):
        query = (
            "MATCH (u:User) MATCH (p:Podcast) "
            "WHERE u.id = $user_id AND p.id = $podcast_id "
            "MERGE (u)-[r:Rating{rating:toInteger($rating)}]->(p) "
        )
        tx.run(query, user_id=user_id, podcast_id=podcast_id, rating=rating)
        
    def create_user(self, user_id):
        with self.driver.session() as sess:
            sess.write_transaction(
                self._create_user, user_id)
    
    @staticmethod
    def _create_user(tx, user_id):
        query = (
            "MERGE (u:User{id:$user_id}) "
        )
        tx.run(query, user_id=user_id)
        
    def create_podcast(self, podcast_id):
        with self.driver.session() as sess:
            sess.write_transaction(
                self._create_podcast, podcast_id)
    
    @staticmethod
    def _create_podcast(tx, podcast_id):
        query = (
            "MERGE (u:Podcast{id:$podcast_id}) "
        )
        tx.run(query, podcast_id=podcast_id)
        
    def create_category(self, category, category_id):
        with self.driver.session() as sess:
            sess.write_transaction(
                self._create_podcast, category, category_id)
    
    @staticmethod
    def _create_category(tx, category, category_id):
        query = (
            "MERGE (u:Podcast{id:$category_id, name:$category}) "
        )
        tx.run(query, category_id=category_id, category=category)
        
    def create_IsA(self, podcast_id, category):
        with self.driver.session() as sess:
            sess.write_transaction(
                self._create_podcast, podcast_id, category)
    
    @staticmethod
    def _create_IsA(tx, podcast_id, category):
        query = (
            "MATCH (c:Category) MATCH (p:Podcast) "
            "WHERE c.name = $category AND p.id = $podcast_id "
            "MERGE (p)-[r:IsA]->(c) "
        )
        tx.run(query, category=category, podcast_id=podcast_id)
        
    def get_cat_based(self, user_id, podcast_id):
        with self.driver.session() as sess:
            result = sess.write_transaction(
                self._get_cat_based, user_id, podcast_id)
            return result
        
    @staticmethod
    def _get_cat_based(tx, user_id, podcast_id):
        query = (
            "MATCH (u:User)-[r]->(Podcast)-->(Category)<--(p:Podcast) "
            "WHERE u.id = $user_id AND p.id = $podcast_id "
            "RETURN r"
        )
        result = tx.run(query, user_id=user_id, podcast_id=podcast_id)
        total = 0
        cnt = 0
        for rec in result:
            total += rec['r']['rating']
            cnt += 1
        return [total, cnt]
    
    def get_user_based(self, user_id, podcast_id):
        with self.driver.session() as sess:
            result = sess.write_transaction(
                self._get_user_based, user_id, podcast_id)
            return result
        
    @staticmethod
    def _get_user_based(tx, user_id, podcast_id):
        query = (
            "MATCH (u:User)-[r1]->(Podcast)<-[r2]->(User)-[r3]->(p:Podcast) "
            "WHERE u.id = $user_id AND p.id = $podcast_id "
            "RETURN r1.rating + r2.rating + r3.rating "
            "AS total"
        )
        result = tx.run(query, user_id=user_id, podcast_id=podcast_id)
        total = 0
        cnt = 0
        for rec in result:
            total += rec['total']
            cnt += 1
        return [total, cnt]
    
    def adamic_adar(self, user_id, podcast_id):
        with self.driver.session() as sess:
            result = sess.write_transaction(
                self._adamic_adar, user_id, podcast_id)
            return result
        
    @staticmethod
    def _adamic_adar(tx, user_id, podcast_id):
        query = (
            "MATCH (u:User)-[r]->(p1:Podcast) MATCH (p:Podcast)"
            "WHERE u.id = $user_id AND p.id = $podcast_id "
            "RETURN r.rating * gds.alpha.linkprediction.adamicAdar(p1, p) "
            "AS score "
        )
        result = tx.run(query, user_id=user_id, podcast_id=podcast_id)
        total = 0
        for rec in result:
            total += rec['score']
        return [total]
    
    def resource_allocation(self, user_id, podcast_id):
        with self.driver.session() as sess:
            result = sess.write_transaction(
                self._resource_allocation, user_id, podcast_id)
            return result
        
    @staticmethod
    def _resource_allocation(tx, user_id, podcast_id):
        query = (
            "MATCH (u:User)-[r]->(p1:Podcast) MATCH (p:Podcast)"
            "WHERE u.id = $user_id AND p.id = $podcast_id "
            "RETURN r.rating * gds.alpha.linkprediction.resourceAllocation(p1, p) "
            "AS score "
        )
        result = tx.run(query, user_id=user_id, podcast_id=podcast_id)
        total = 0
        cnt = 0
        for rec in result:
            total += rec['score']
            cnt += 1
        return [total, cnt]
    
    def gen_df(self, user_id):
        podcasts = self.gen_podcasts(user_id)
        df = pd.DataFrame({'podcast_id':podcasts})
        df['user_id'] = user_id
        return df.drop_duplicates().reset_index().iloc[:50, 1:]
        
    def gen_podcasts(self, user_id):
        with self.driver.session() as sess:
            result = sess.write_transaction(
                self._gen_podcasts, user_id)
            return result
        
    @staticmethod
    def _gen_podcasts(tx, user_id):
        query = (
            "MATCH (u:User)-[*3]-(p:Podcast) "
            "WHERE u.id = $user_id "
            "RETURN p.id AS p_id "
        )
        result = tx.run(query, user_id=user_id)
        ans = []
        for rec in result:
            ans.append(rec['p_id'])
        return ans