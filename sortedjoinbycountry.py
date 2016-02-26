#!/usr/bin/env python2

# To get started with the join, 
# try creating a new directory in HDFS that has both the fwiki data AND the maxmind data.

import mrjob
import heapq
import os

from mrjob.job import MRJob
from weblog import Weblog       # imports class defined in weblog.py
from mrjob.step import MRStep

class FwikiMaxmindJoin(MRJob):
    def mapper(self, _, line):
        # Is this a weblog file, or a MaxMind GeoLite2 file?
        filename = mrjob.compat.jobconf_from_env("map.input.file")
        import sys
        if "top1000ips_to_country.txt" in filename:
            # Handle as a GeoLite2 file
            #
            try:
                (ipaddr, country) = line.strip().split("\t")
                yield ipaddr, ("country", country)
            except ValueError as e:
                pass
        else:
            # Handle as a weblog file
            try:
                o = Weblog(line)
            except ValueError:
                sys.stderr.write("Invalid logfile line: {}\n".format(line))
                return
            if o.wikipage() == "Main_Page":
                yield o.ipaddr,("ip", line)
  
    def reducer(self, key, values):
        name = None
        for v in values:
            if v[0]=='country':
                name = v[1]
                continue
            if v[0]=='ip':
                obs = v[1]
                if name:
                    yield name, 1

    def mapper_counter(self, key, values):
        yield key, 1

    def reducer_counter(self, key, values):
        yield key, sum(values)

    def top10_mapper(self, word, count):
        yield "Top", (count,word)

    def top10_reducer(self, key, values):
        yield sorted(values, key=lambda x: x[0])

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),

            MRStep(mapper=self.mapper_counter,
                   reducer=self.reducer_counter),

            MRStep(mapper=self.top10_mapper,
                   reducer=self.top10_reducer) ]

if __name__=="__main__":
    FwikiMaxmindJoin.run()
