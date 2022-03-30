from faker import Faker
from sqlalchemy.exc import IntegrityError
from .models import User,Post,db
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
		post  = Post(post_body=faker.text(),author=user,timestamp=faker.past_datetime(),title=faker.sentence())
		db.session.add(post)
		db.session.commit()


