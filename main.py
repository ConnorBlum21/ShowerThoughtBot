import videomaking
import readdit

thoughts = readdit.get_hot_posts()
print(len(thoughts))


videomaking.make_video(thought)
