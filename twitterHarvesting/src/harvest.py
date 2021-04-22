from tweepy import OAuthHandler, Stream, StreamListener

consumer_key = '7XueUW0fcpoqMvvmIhdYUZhVV'
consumer_secret = '3tC0FlevZKBX6U6blSpwq8EeLUsy1qIQUJyXWPkdTKUaxsFc1e'
access_token = '1384380289187786753-EQQqZfJzo3lnBTyiVL7nrO9AfspV27'
access_token_secret = 'Wiy8poQMVkj2SUDJtYmocJ00TYVyxjDy2WiqdrwBEOW2g'
melbourne_bouning_box = [144.33363404800002, -38.50298801599996, 145.8784120140001, -37.17509899299995]

class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(locations=melbourne_bouning_box)