import config
import tweepy
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud

font_pass = "/System/Library/Fonts/ヒラギノ角ゴシック W1.ttc"


def api():
    auth = tweepy.OAuth1UserHandler(
        config.api_key,
        config.api_secret,
        config.consumer_key,
        config.consumer_secret
    )
    return tweepy.API(auth, wait_on_rate_limit=True, timeout=120)


class TLDesigner:
    def __init__(self):
        self.tweet_id = None
        self.text = ''
        self.tweet_timelines = []
        self.API = api()

    def find_tweet(self):
        f = open("tweet_id.txt", "r")
        self.tweet_id = f.readline()

    def get_tweet(self):
        tweet_timelines = self.API.home_timeline(since_id=self.tweet_id, )
        for tt in tweet_timelines:
            if "https" not in tt.text and "RT" not in tt.text and "@" not in tt.text:
                self.tweet_timelines.append(tt.text)

    def filter_tweet(self):
        t = Tokenizer()
        for tt in self.tweet_timelines:
            tts = [token.surface for token in t.tokenize(tt) if token.part_of_speech.startswith('名詞')]
            for ts in tts:
                if len(ts) != 1:
                    self.text += " " + ts
            print(self.text)

    def generation_image(self, txt):
        wc = WordCloud(font_path=font_pass).generate(txt)
        wc.to_file("word_cloud_result.png")
        self.API.update_status_with_media(status='image tweet from python', filename='word_cloud_result.png')

    def store_tweet(self):
        ts = self.API.home_timeline(count=1)
        tweet_id = ts[0].id
        f = open("tweet_id.txt", "w")
        f.write(str(tweet_id))
        f.close()

    def main(self):
        self.find_tweet()
        self.get_tweet()
        self.filter_tweet()
        self.generation_image(self.text)
        self.store_tweet()


test = TLDesigner()
test.main()
