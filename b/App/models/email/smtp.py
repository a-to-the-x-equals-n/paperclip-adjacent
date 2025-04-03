
from email.mime.text import MIMEText
import smtplib
import re


class SMTP:

    # Temporary User object for access to name and phone number
    temp_user = None

    def __init__(self):
        self.EMAIL, self.PASSWORD = load_vars("EMAIL", "PASSWORD")
        self.SMTP = 'smtp.gmail.com' # SMTP : Simple Mail Transfer Protocol
        self.PORT = 587


    ''' Outbound Email Functions '''

    
    def new_task(self, user, task_id, details):
        response = f'Task {task_id}: "{details}" created successfully!'
        self.send_sms(user, response)


    def list_tasks(self, user, tasks):

        if tasks:
            response = "Here's a list of your tasks:\n"

            for task in tasks:
                response += f"    {task['id']}: {task['details']}\n"
        else:
            response = "You currently have no tasks."
        
        self.send_sms(user, response)


    def list_tasks_scheduled(self, user, tasks):
        response = "Daily reminder of current tasks:\n"
        for task in tasks:
            response += f"    {task['id']}: {task['details']}\n"

        self.send_sms(user, response)
        

    
    def del_task(self, user, task_id):

        response = f'Task "{task_id}" deleted!'
        self.send_sms(user, response)


    def error(self, user):
        response = f'Unrecognized message.\nPlease try again or type "help" for a list of acceptable commands.'
        self.send_sms(user, response)


    def help(self, user):
        d = f"'del' followed by a task ID will remove it."
        n = f"'new' then a description will create a task."
        l = f"'list' will return all current tasks."
        response = f'{d}\n{n}\n{l}'
        self.send_sms(user, response)


    def send_sms(self, user, response):

        # Format phone number in prep for Email to SMS gateways
        format_number = re.sub(r'\D', '', str(user['phone_num']))

        # Construct the email
        recv_addr = f"{format_number}{user['carrier']}"
        msg = MIMEText(response)
        msg['From'] = self.EMAIL
        msg['To'] = recv_addr
        msg['Subject'] = ""

        try:
            # Connect to the SMTP server and send the email
            server = smtplib.SMTP(self.SMTP, self.PORT)
            server.starttls()
            server.login(self.EMAIL, self.PASSWORD)
            server.sendmail(self.EMAIL, recv_addr, msg.as_string())
            server.quit()
            print("SMS sent successfully!")

        except Exception as e:
            print(f"Failed to send SMS: {e}")


    def build_reply(self, response):
        return self.__default_message
    

    @staticmethod
    def __default_message():
        msg = f"""
        Hello {SMTP.temp_user.f_name}!\nMy name is Carole Taskins\nI'm currently under development, but hopefully I'll be up and running very soon.
        """
        return msg


