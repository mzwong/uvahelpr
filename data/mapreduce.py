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
user_itemlists = pairs.groupByKey() #This code groups items into RDD iterable objects. The above block of commented code
                                    #groups them into normal Python lists. I'm not sure what's more useful for the next
                                    #steps, so feel free to use what works best.

# below code to print <users, all_items>
output = user_itemlists.collect()                          # bring the data back to the master node so we can print it out
for user, items in output:
    print (str(user) + " "  + str(items))
print ("Popular items done")

sc.stop()