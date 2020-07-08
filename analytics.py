import numpy as np
from pyspark import SparkContext
from pyspark.ml import Pipeline
from pyspark.ml.feature import (
    RegexTokenizer,
    CountVectorizer,
    StopWordsRemover,
    IDF
)
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, isnan

# Pyspark Configuration
spark = SparkSession\
    .builder\
    .master('local')\
    .config('spark.mongodb.input.uri', 'mongodb://127.0.0.1:27017/finalproject')\
    .config('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/finalproject')\
    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.2.1')\
    .getOrCreate()

sc = SparkContext.getOrCreate("local")
locale = spark._jvm.java.util.Locale
locale.setDefault(locale.forLanguageTag("en-US"))

# Load data
property_df = spark.read\
    .format("com.mongodb.spark.sql.DefaultSource")\
    .option("database", "finalproject")\
    .option("collection", "property")\
    .load()

# Text Processing
regexTokenizer = RegexTokenizer(gaps=False, pattern='\w+', inputCol='text', outputCol='token')
stopWordsRemover = StopWordsRemover(inputCol='token', outputCol='nostopwrd')
countVectorizer = CountVectorizer(inputCol="nostopwrd", outputCol="rawFeature")
iDF = IDF(inputCol="rawFeature", outputCol="idf_vec")

# Vector data pipline
pipeline = Pipeline(stages=[regexTokenizer, stopWordsRemover, countVectorizer, iDF])
pipeline_mdl = pipeline.fit(property_df)
property_trf_df = pipeline_mdl.transform(property_df)
all_property_vecs = property_trf_df.select('_id', 'idf_vec').rdd.map(lambda x: (x[0], x[1])).collect()

# Cosine Similiarity
def cosine_sim(vec1, vec2):
    return np.dot(vec1, vec2) / np.sqrt(np.dot(vec1, vec1)) / np.sqrt(np.dot(vec2, vec2)) 

# Query to get data
def get_property_details(in_property):
    a = in_property.alias("a")
    b = property_df.alias("b")    
    return a.join(b, col("a.property_id") == col("b._id"), 'inner').select([col('a.'+xx) for xx in a.columns] + [col('b.name'), col('b.url'), col('b.text'), col('b.source')]).orderBy("a.score", ascending=False)

# Return recomendation keywords
def get_keywords_recomendations(key_words, sim_bus_limit=20):
    input_words_df = sc.parallelize([(0, key_words)]).toDF(['_id', 'text'])
    input_words_df = pipeline_mdl.transform(input_words_df)
    input_key_words_vec = input_words_df.select('idf_vec').collect()[0][0]
    sim_property_byword_rdd = sc.parallelize((i[0], float(cosine_sim(input_key_words_vec, i[1]))) for i in all_property_vecs)
    property_rdd = sim_property_byword_rdd.sortBy(lambda a: -a[1]).collect()
    sim_property_byword_df = spark.createDataFrame(property_rdd) \
         .withColumnRenamed('_1', 'property_id') \
         .withColumnRenamed('_2', 'score')\
         .orderBy("score", ascending=False)
    result = sim_property_byword_df.filter(
        (col('score')>0) & (~isnan('score'))
    ).limit(sim_bus_limit)
    return get_property_details(result)
