"""Fb ChatBot Script."""
import sys
import time
import pandas as pd
from fbchat import log, Client

df = pd.read_csv("questions.csv")
_dict = {
    1:
    "Come on, I can't just give up on a wonderful person like you in a single try.\nWill you Marry me?(yes/no)",
    2: "\nWill you Marry me?(yes/no)",
    3:
    "I'd be happy to spend the rest of my geeky weird life with you.\nWill you Marry me?(yes/no)",
    4:
    "I'm ready to be the Better Man I can be for you, and make you proud of me. B'coz am proud of you and I Love You.\nWill you Marry me?(yes/no)",
    5:
    "Need a weirdo with otakuness for all the anime nights rest of your life?\nTell Yes...\nWill you Marry me?(yes/no)",
    6:
    "Out there, there is someone who is looking for you in all the persons they meet, I am that someone for you.\nWill you Marry me?(yes/no)",
    7:
    "I will love you untill the stars go out and tides no longer turn.\nWill you Marry me?(yes/no)",
    8: "Come live in my heart and pay no rent.\nWill you Marry me?(yes/no)",
    9: "PROPOSAL 2.0\nWill you Marry me?(yes/no)",
    10:
    "If I know what love is, it is because of you.\nWill you Marry me?(yes/no)"
}


# Subclass fbchat.Client and override required methods
class MessageBot(Client):
    """Bot Class."""

    counter = 0
    no_counter = 0
    msg_ids = {}

    def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
        """Message Handler Function."""
        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)

        log.info("Message from {} in {} ({}): {}".format(
            author_id, thread_id, thread_type.name, message))

        # If you skip auhtor_id check,
        # Then the bot will propose whoever messaes you :P
        if author_id == 'id_of_the_one_you_are_proposing':
            MessageBot.counter += 1
            if message.lower() == 'start' or message.lower(
            ) in ['i', 'l', 'o', 'v', 'e', 'y', 'o']:
                if MessageBot.counter != 1:
                    _temp = df[df["counter"] ==
                               MessageBot.counter - 1].to_dict(
                                   orient='records')[0]
                    message = "Answer is '" + _temp["answer"] + "'"
                    self.sendMessage(
                        message, thread_id=thread_id, thread_type=thread_type)
                temp = df[df["counter"] == MessageBot.counter].to_dict(
                    orient='records')[0]
                msg_id = self.sendRemoteImage(
                    temp["image_path"],
                    message=temp["question"],
                    thread_id=thread_id,
                    thread_type=thread_type)
            elif message.lower() == 'yes':
                message = "Please, Let this not be a joke.!\nI wasn't expecting a 'yes' from you.\nHence terminating this script."
                msg_id = self.sendMessage(
                    message, thread_id=thread_id, thread_type=thread_type)
                sys.exit()
            elif message.lower() in ['n', 'no']:
                MessageBot.no_counter += 1
                if MessageBot.no_counter < 11:
                    if MessageBot.no_counter == 2:
                        image_path = "venn_diagram.png"
                        self.sendLocalImage(
                            image_path,
                            message=None,
                            thread_id=thread_id,
                            thread_type=thread_type)
                    message = _dict[MessageBot.no_counter]
                    msg_id = self.sendMessage(
                        message, thread_id=thread_id, thread_type=thread_type)
                if MessageBot.no_counter == 11:
                    m = "People never say give up, but sometime giving up is the best option becasue I realise I don't want to bug you.\nWill miss a great part of my life.\nTerminating..! Sadly Terminating..! :(\nBye"
                    msg_id = self.sendMessage(
                        m, thread_id=thread_id, thread_type=thread_type)
                    sys.exit()
            elif message.lower() == 'u':
                m = "Congrats You have succsfuly completed the Anime Quiz.!\nCan you please scroll up and check all the 8 options you have selected from top to bottom."
                self.sendMessage(
                    m, thread_id=thread_id, thread_type=thread_type)
                time.sleep(10)  # Give her some time to scroll up you moron
                m = "Options are - I LOVE YOU\nYes, That is what I wanted to tell you. I Love you and wanted to be a permanent part of your life.\nWill you Marry me?(yes/no)"
                self.sendMessage(
                    m, thread_id=thread_id, thread_type=thread_type)
            MessageBot.msg_ids[MessageBot.counter] = msg_id


client = MessageBot("your_fb_username", "your_fb_password")
client.listen()
