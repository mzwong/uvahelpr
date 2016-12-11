from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/access.log", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition
#group by user_id
user_itemlists = pairs.groupByKey()
#do a cross-product of item_ids x item_ids
click_pairs_cartesian = user_itemlists.flatMap(lambda pair: [(pair[0], (item1,item2)) for item1 in pair[1] for item2 in pair[1]])
#filter out results where item_id1 < item_id2 to get unique combinations
click_pairs = click_pairs_cartesian.filter(lambda pair: int(pair[1][0]) < int(pair[1][1]))
#group by value
click_pairs = click_pairs.groupBy(lambda pair: pair[1])
#keep just the id
click_pairs = click_pairs.map(lambda pair: (pair[0], [p[0] for p in pair[1]]))
#get the sum of the number of users for each pair of items
click_counts = click_pairs.map(lambda pair: (pair[0], len(set(pair[1]))))
#take only combinations with at least 3 users
results = click_counts.filter(lambda pair: pair[1] > 2)

# below code to print <users, all_items>
output = results.collect()                          # bring the data back to the master node so we can print it out
for user, items in output:
    print (str(user) + " "  + str(items))
sc.stop()