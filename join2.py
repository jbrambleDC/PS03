#!/usr/bin/env python2

# To get started with the join, 
# try creating a new directory in HDFS that has both the fwiki data AND the maxmind data.

import mrjob
from mrjob.job import MRJob
from weblog import Weblog       # imports class defined in weblog.py
from mrjob.step import MRStep
import os

class FwikiMaxmindJoin(MRJob):
    def mapper(self, _, line):
        # Is this a weblog file, or a MaxMind GeoLite2 file?
        filename = mrjob.compat.jobconf_from_env("map.input.file")
        if "top1000ips_to_country.txt" in filename:
        	fields = line.split('\t')
            # Handle as a GeoLite2 file
            #
		self.increment_counter("Info","Obs Count",1)
		yield fields[0],("country", fields)
        else:
            # Handle as a weblog file
		self.increment_counter("Info","Name Count",1)
		fields = Weblog(line)
		yield fields.ipaddr,("ip", line)
        
        # output <date,1>
        #yield (log.date, 1)


    def reducer(self, key, values):
        name = None
        for v in values:
            
            if v[0]=='country':
                name = v[1]
                continue
            if v[0]=='ip':
                obs = v[1]
                if name:
                    yield name[1], 1
                else:
                    self.increment_counter("Warn","countries without Name")
                   

    def mapper_counter(self, key, values):
	yield key, 1

    def reducer_counter(self, key, values):
        yield key, sum(values)

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),

            MRStep(mapper=self.mapper_counter,
                   reducer=self.reducer_counter) ]

if __name__=="__main__":
    FwikiMaxmindJoin.run()
