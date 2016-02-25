#
# This file makes your submission when you type 'make'


# Set MODE for running on local or on hadoop

MODE="-rlocal"

PYFILES = $(wildcard *.py)
TXTFILES = $(wildcard *.txt)
PDFFILES = $(wildcard *.pdf)

info:
	echo type '"make zip"' to make the zip file

zip: validator.py $(PYFILES) $(TXTFILES) $(PDFFILES)
	python validator.py --zip

#
# Here are some sample Makefile recipes to get your started
# 

# part 2: Getting Started with EMR
wordcount_top10.txt:
	if [ ! -r $(HOME)/pg1184.txt ]; then wget http://www.simson.net/anly502/pg1184.txt -O $(HOME)/pg1184.txt; fi
	python wordcount_top10.py -r hadoop $(HOME)/pg1184.txt > wordcount_top10.txt

guanly502_gutternberg_ls.txt:
	aws s3 ls s3://gu-anly502/gutenberg/ > guanly502_guttenberg_ls.txt

guanly502_gutternberg_top10.txt:
	python wordcount_top10.py -r hadoop s3://gu-anly502/gutenberg/ > guanly502_gutternberg_top10.txt

join1.txt: join1.py
	python join1.py -r hadoop --file weblog.py s3://gu-anly502/ps03/forensicswiki/ s3://gu-anly502/ps03/maxmind/ > join1_full.txt
	head -50 join1_full.txt > join1.txt

join2.txt: join2.py
	python join2.py -r hadoop --file weblog.py s3://gu-anly502/ps03/forensicswiki/ s3://gu-anly502/ps03/maxmind/ > join2.txt

join3.txt: join3.py
	python join3.py -r hadoop --file weblog.py s3://gu-anly502/ps03/forensicswiki/ s3://gu-anly502/ps03/maxmind/ > join3.txt


first50.txt: first50.py
	python first50.py -r hadoop --file weblog.py s3://gu-anly502/ps03/forensicswiki/ > first50.txt

first50join1.txt: first50join1.py
	python first50join1.py -r hadoop --file weblog.py s3://gu-anly502/ps03/forensicswiki/ s3://gu-anly502/ps03/maxmind/ > first50join1.txt

sortedjoinbycountry.txt: sortedjoinbycountry.py
	python sortedjoinbycountry.py -r hadoop --file weblog.py s3://gu-anly502/ps03/forensicswiki/ s3://gu-anly502/ps03/maxmind/ > sortedjoinbycountry.txt

wikipedia_stats.txt: wikipedia_stats.py
	python wikipedia_stats.py -r hadoop hdfs://user/hadoop/infiles/ > sortedjoinbycountry.txt


