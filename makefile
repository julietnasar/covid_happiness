
# builds final pdf chart & dependancies
all:	./comparison.pdf
	echo "---------------------------------------"
	echo "Everything has been built!"
	echo "You can find a PDF of the plot that was just shown in .comparison.pdf"

# how to build final pdf chart
./comparison.pdf: ./plotting/sparkify_plot.py ./clean_data/reviews_with_covid_data.txt
	spark-submit ./plotting/sparkify_plot.py ./clean_data/reviews_with_covid_data.txt
	echo "---------------------------------------"
	echo "data has been loaded into an RDD and plotted using matplotlib"

# adds covid data to reviews_with_sentiments.txt
./clean_data/reviews_with_covid_data.txt: ./clean_data/national_covid_data.txt ./clean_data/reviews_with_sentiment.txt ./cleansing_scripts/add_covid_stats.py
	python3 ./cleansing_scripts/add_covid_stats.py ./clean_data/national_covid_data.txt ./clean_data/reviews_with_sentiment.txt > ./clean_data/reviews_with_covid_data.txt
	echo "---------------------------------------"
	echo "reviews_with_covid_data.txt has been built!"

# cleans web scraped covid data file into pipe delim file
./clean_data/national_covid_data.txt: ./raw_data/national ./cleansing_scripts/clean_covid_data.py
	python3 ./cleansing_scripts/clean_covid_data.py ./raw_data/national > ./clean_data/national_covid_data.txt
	echo "---------------------------------------"
	echo "covid_data.txt has been built!"

# web scrapes covid data
./raw_data/national:
	wget -o https://covidtracking.com/data/n
	mv national ./raw_data
	echo "---------------------------------------"
	echo "national, a file with national covid deaths, has been web scraped!"

# adds sentiment analysis stats to reviews data
./clean_data/reviews_with_sentiment.txt: ./sentiment_analysis/addSentiment.py ./sentiment_analysis/positive_words.txt ./sentiment_analysis/negative_words.txt ./clean_data/yelp_review_data.txt
	python3 ./sentiment_analysis/addSentiment.py ./sentiment_analysis/positive_words.txt ./sentiment_analysis/negative_words.txt ./clean_data/yelp_review_data.txt > ./clean_data/reviews_with_sentiment.txt
	echo "---------------------------------------"
	echo "reviews_with_sentiment.txt has been built!"

# web scrapes positive words to use in sentiment analysis
./sentiment_analysis/positive_words.txt:
	curl https://ptrckprry.com/course/ssd/data/positive-words.txt --output ./sentiment_analysis/positive_words.txt
	echo "---------------------------------------"
	echo "positive words.txt has been web scraped!"

# web scrapes negative words to use in sentiment analysis
./sentiment_analysis/negative_words.txt:
	curl https://ptrckprry.com/course/ssd/data/negative-words.txt --output ./sentiment_analysis/negative_words.txt
	echo "---------------------------------------"
	echo "negative_words.txt has been web scraped!"

# cleans yelp_review_data from compressed json form to pipe delim form
./clean_data/yelp_review_data.txt: raw_data/yelp_review_data.json.gz
	python3 ./cleansing_scripts/clean_review_data.py ./raw_data/yelp_review_data.json.gz > ./clean_data/yelp_review_data.txt
	echo "---------------------------------------"
	echo "yelp_review_data.txt has been built!"

almost_clean:
	@echo "Cleaning up almost all files"
	rm ./comparison.pdf
	rm ./clean_data/reviews_with_covid_data.txt
	rm ./clean_data/national_covid_data.txt
	rm ./clean_data/reviews_with_sentiment.txt
	rm ./sentiment_analysis/positive_words.txt
	rm ./sentiment_analysis/negative_words.txt

clean:
	@echo "Cleaning up all files"
	rm ./comparison.pdf
	rm ./clean_data/reviews_with_covid_data.txt
	rm ./clean_data/national_covid_data.txt
	rm ./clean_data/reviews_with_sentiment.txt
	rm ./clean_data/yelp_review_data.txt
	rm ./sentiment_analysis/positive_words.txt
	rm ./sentiment_analysis/negative_words.txt
