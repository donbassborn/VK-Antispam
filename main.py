import vk_api
import random
import json
import datetime
import time
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType

def send_msg(text, dest):
    vk.messages.send(random_id=random.randint(1,2147483647), chat_id = dest, message = text)


def get_global_id(api_handle, _local_id, _peer_id):
    response = api_handle.messages.getByConversationMessageId(peer_id=_peer_id, conversation_message_ids=_local_id)
    return response['items'][0]['id']

    
begin_time = datetime.datetime.now()

def run_time():
    return str(datetime.datetime.now() - begin_time)

secret_token = "№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№"
conference_id = 2000000047
#target_user_id = 362065975
target_user_id = 1

timeout_wall = 0
timeout_photo = 0
timeout_doc = 0
timeout_video = 0
global_timeout = 0


flood_timeout = 3




while True:
    try:
        handle = vk_api.VkApi(token=secret_token)
        try:
            handle._auth_token()
        except vk_api.AuthError as error_msg:
            print(run_time() + ": " + error_msg)
            exit(1)

        vk = handle.get_api()
        longpoll = VkLongPoll(handle)
        for lpevent in longpoll.listen():
            if lpevent.type == VkEventType.MESSAGE_NEW and lpevent.from_chat:
                print(run_time() + ": " + str(lpevent.raw))
                if lpevent.peer_id == conference_id and lpevent.user_id == target_user_id:
                    
                    #e_message_text = lpevent.text
                    #e_user_id = lpevent.from_id
                    #e_local_id = lpevent.conversation_message_id
                    #print(lpevent.raw)

                    #print(lpevent.attachments)
                    if(lpevent.timestamp - global_timeout < flood_timeout):
                        print(run_time() + ": " + "Delete flood; timeout: " + str(flood_timeout - (lpevent.timestamp - global_timeout)))
                        vk.messages.delete(message_ids=lpevent.message_id, delete_for_all=1)
                    global_timeout = lpevent.timestamp


                    if len(lpevent.attachments) > 0:
                        have_photo = False
                        have_wall = False
                        have_doc = False
                        have_video = False
                        count_of_attach = 1
                        while ("attach" + str(count_of_attach) + "_type") in lpevent.attachments:
                            #print("attach" + str(count_of_attach) + "_type")   
                            if(lpevent.attachments["attach" + str(count_of_attach) + "_type"] == "wall"):
                                have_wall = True
                                #print("wall detected")
                            if(lpevent.attachments["attach" + str(count_of_attach) + "_type"] == "photo"):
                                have_photo = True
                                #print("photo detected")
                            if(lpevent.attachments["attach" + str(count_of_attach) + "_type"] == "doc"):
                                have_doc = True
                                #print("doc detected")
                            if(lpevent.attachments["attach" + str(count_of_attach) + "_type"] == "video"):
                                have_video = True
                                #print("video detected")
                            count_of_attach += 1
                        
                        if(have_photo and lpevent.timestamp - timeout_photo < 3600):
                            print(run_time() + ": " + "Delete photo; timeout: " + str(3600 - (lpevent.timestamp - timeout_photo)))
                            vk.messages.delete(message_ids=lpevent.message_id, delete_for_all=1)
                            continue
                        elif have_photo:
                            timeout_photo = lpevent.timestamp

                        if(have_wall and lpevent.timestamp - timeout_wall < 3600):
                            print(run_time() + ": " + "Delete photo; timeout: " + str(3600 - (lpevent.timestamp - timeout_wall)))
                            vk.messages.delete(message_ids=lpevent.message_id, delete_for_all=1)
                            continue
                        elif have_wall:
                            timeout_wall = lpevent.timestamp

                        if(have_doc and lpevent.timestamp - timeout_doc < 3600):
                            print(run_time() + ": " + "Delete doc; timeout: " + str(3600 - (lpevent.timestamp - timeout_doc)))
                            vk.messages.delete(message_ids=lpevent.message_id, delete_for_all=1)
                            continue
                        elif have_doc:
                            timeout_doc = lpevent.timestamp
                        
                        if(have_video and lpevent.timestamp - timeout_video < 3600):
                            print(run_time() + ": " + "Delete video; timeout: " + str(3600 - (lpevent.timestamp - timeout_video)))
                            vk.messages.delete(message_ids=lpevent.message_id, delete_for_all=1)
                            continue
                        elif have_video:
                            timeout_video = lpevent.timestamp
    except ConnectionError as e:
        print(run_time() + ": " + "Connection Error")
        time.sleep(1)
    except KeyboardInterrupt:
        print(run_time() + ": " + "Terminate program...")
        exit(0)
    except Exception as e:
        print(run_time() + ": " + "Shit happens" + str(e.__class__))
    
                
                #print(str(get_global_id(vk, e_local_id, conference_id)) + ": " + lpevent)