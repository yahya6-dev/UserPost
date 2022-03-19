from flask import current_app,render_template
from flask_mail import Message
from threading import Thread
from . import mail


##send an asynchronous mail to the
## target address
def send_async(app,msg):
	with app.app_context():
		mail.send(msg)

#send mail from one addr to another 
#pass in the template to render as mail body and html content
def send_mail(from_addr,to_addr,subject,template,**kargs):
	app = current_app._get_current_object()

	msg = Message(subject,sender=from_addr,recipients=to_addr)
	msg.body = render_template(template+".txt",**kargs)
	msg.html = render_template(template+".html",**kargs)

	thr = Thread(target=send_async,args=(app,msg))
	thr.start()

	return thr

