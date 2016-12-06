from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/access.log", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition

'''
#
users = pairs.map(lambda pair: (pair[0], [pair[1]]))      # re-layout the data to ignore the user id
user_itemlists = users.reduceByKey(lambda x,y: x+y)        # shuffle the data so that each key is only on one worker
                                                  # and then reduce all the values by adding them together
'''
user_itemlists = pairs.groupByKey().map(lambda pair: (pair[0], list(pair[1]))) #This code groups items into RDD iterable objects. The above block of commented code
                                    #groups them into normal Python lists. I'm not sure what's more useful for the next
                                    #steps, so feel free to use what works best.
#do a cross-product of item_ids x item_ids
click_pairs_cartesian = user_itemlists.flatMap(lambda pair: [(pair[0], (item1,item2)) for item1 in pair[1] for item2 in pair[1]])
#filter out results where item_id1 < item_id2 to get unique combinations
click_pairs = click_pairs_cartesian.filter(lambda pair: int(pair[1][0]) < int(pair[1][1]))
#group by value
click_pairs = click_pairs.groupBy(lambda pair: pair[1]).map(lambda pair: (pair[0], list(pair[1])))
#keep just the id
click_pairs = click_pairs.map(lambda pair: (pair[0], [p[0] for p in pair[1]]))


# below code to print <users, all_items>
output = click_pairs.collect()                          # bring the data back to the master node so we can print it out
for user, items in output:
    print (str(user) + " "  + str(list(items)))
print ("Popular items done")

sc.stop()