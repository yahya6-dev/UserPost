from faker import Faker
from sqlalchemy.exc import IntegrityError
from .models import User,Post,db,Comment
from random import randint

#create unrealistic users
def create_users(count):
	faker = Faker()
	for i in range(count):
		try:
			user = User(username=faker.user_name(),password="password",email=faker.email(),location=faker.city())
		except IntegrityError:
			db.session.rollback()
			count += 1
		else:
			db.session.add(user)
			db.session.commit()
	print("done")

#create random forest from different user
def create_posts(count):
	faker = Faker()
	for i in range(count):
		user = User.query.offset(randint(i,count-1)).first()
		post  = Post(post_body="".join(faker.texts()),author=user,timestamp=faker.past_datetime(),title=faker.sentence())
		db.session.add(post)
		db.session.commit()


#create random comment
def  create_comment(count):
	faker = Faker()
	total_users = User.query.count()
	total_posts = Post.query.count()
	for i in range(count):
		user = User.query.offset(randint(1,total_users)).first()
		post = Post.query.offset(randint(1,total_posts)).first()

		comment = Comment(comment_text=faker.text(),author=user,post=post)
		db.session.add(comment)
		db.session.commit()

	print("done")

