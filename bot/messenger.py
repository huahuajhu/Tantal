import logging
import random

logger = logging.getLogger(__name__)


class Messenger(object): 
    def __init__(self, slack_clients):
        self.clients = slack_clients

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: {} to channel: {}'.format(msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message("{}".format(msg.encode('ascii', 'ignore')))

    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = '{}\n{}\n{}\n{}'.format(
            "> `<@" + bot_uid + "> classify [text]` - Classify the text into different topics",
            "> `<@" + bot_uid + "> entity [text]` - Extract entities such as Organization, Location, person etc from the text",
            "> `<@" + bot_uid + "> sentiment [text]` - Retrieve the sentiment from the text",
            "> `<@" + bot_uid + "> tag [text]` - Auto-tag the text",
            "> `<@" + bot_uid + "> attachment` - I'll demo a post with an attachment using the Web API. :paperclip:")
        self.send_message(channel_id, txt)

    def write_greeting(self, channel_id, user_id):
        greetings = ['Hi', 'Hello', 'Nice to meet you', 'Howdy', 'Salutations']
        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.send_message(channel_id, txt)

    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "I'm sorry, I didn't quite understand... Can I help you? (e.g. `<@" + bot_uid + "> help`)"
        self.send_message(channel_id, txt)

    def write_joke(self, channel_id):
        question = "Why did the python cross the road?"
        self.send_message(channel_id, question)
        self.clients.send_user_typing_pause(channel_id)
        answer = "To eat the chicken on the other side! :laughing:"
        self.send_message(channel_id, answer)


    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    def demo_attachment(self, channel_id):
        txt = "Tantal is your intelligent slackbot!"
        attachment = {
            "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
            "title": "Text Analytics bot here!",
            "title_link": "https://beepboophq.com/",
            "text": txt,
            "fallback": txt,
            "image_url": "http://www.logospike.com/wp-content/uploads/2015/11/T_Logo_02.jpg",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')
        
