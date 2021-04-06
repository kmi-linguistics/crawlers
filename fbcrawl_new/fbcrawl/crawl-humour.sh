scrapy crawl fb -a email="fbresearch.kmi@gmail.com" -a password="Bornini@2019" -a page="kunalkamra88" -a date="2020-01-01" -o posts/kunalkamra88.csv
scrapy crawl fb -a email="fbresearch.kmi@gmail.com" -a password="Bornini@2019" -a page="RavishKaPage" -a date="2020-03-20" -o posts/RavishKaPage.csv

scrapy crawl comments -a email="fbresearch.kmi@gmail.com" -a password="Bornini@2019" -a post="https://mbasic.facebook.com/story.php?story_fbid=1407641499433993&id=618840728314078" -o comments/all_comments.csv
