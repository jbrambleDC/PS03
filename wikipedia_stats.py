#!/usr/bin/env python2
import mrjob
import mrjob.compat
from mrjob.job import MRJob
from mrjob.step import MRStep
import sys

class wikipedia_stats(MRJob):
    SORT_VALUES = True

    def mapper(self, _, line):
        article = line.split('\t')[2]
        date = article.split(' ')
        day = date[0].split('-')
        specificmonth = day[0]+'-'+day[1]
        yield specificmonth, 1

    def reducer(self, key, value):
        yield key, sum(value)

    def mapper_two(self, key, value):
        yield "Wiki", (key, value)

    def reducer_two(self, key, value):
        for v in value:    
            yield v[0], v[1]

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(mapper=self.mapper_two,
                   reducer=self.reducer_two) ]

if __name__ == "__main__":
    wikipedia_stats.run()
