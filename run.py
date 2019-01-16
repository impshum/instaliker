from InstagramAPI import InstagramAPI
from time import sleep, strftime
from random import randint
import schedule


instauser = 'XXXX'  # instagram username
instapass = 'XXXX'  # instagram password
hashtags = ['XXXX', 'XXXX']  # hashtags to fetch and like
max_likes = 2  # maximum likes per run
min_sleep = 1  # minumum sleep time in minutes
max_sleep = 1  # maximum sleep time in minutes
max_history = 30  # number of already liked posts to skip


def get_date():
    return strftime("%Y-%m-%d %H:%M")


def like_hashtag_feed(api):
    for hashtag in hashtags:
        print(f'{get_date()} | Getting media with hashtag {hashtag}')
        next_max = 1
        next_max_id = ''
        likes = 0
        liked = 0
        for n in range(next_max):
            api.getHashtagFeed(hashtag, next_max_id)
            temp = api.LastJson
            for post in temp['items']:
                if not post['has_liked']:
                    print(f'{get_date()} | Liking {post["pk"]}')
                    api.like(post['pk'])
                    likes += 1
                    if liked >= max_history:
                        break
                    sleep(randint(3, 15))
                else:
                    liked += 1
                    print(liked)
                    if liked >= max_history:
                        break
                if likes >= max_likes:
                    break
            try:
                next_max_id = temp['next_max_id']
            except Exception:
                pass
            if likes >= max_likes or liked >= max_history:
                break
    print(f'{get_date()} | Sleeping for {min_sleep} to {max_sleep} minutes')


def main():
    api = InstagramAPI(instauser, instapass)
    if api.login():
        print(f'Logged in as {api.username}\n')
        like_hashtag_feed(api)
        schedule.every(min_sleep).to(
            max_sleep).minutes.do(like_hashtag_feed, api)
        while True:
            schedule.run_pending()
            sleep(1)


if __name__ == '__main__':
    main()
