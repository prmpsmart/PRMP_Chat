# **PRMP Chat**

## A local WLAN chatting software.

<br>
<br>

## It'll include the following features:
> * Private chat.
> * Group chat.
> * Channels.
> * Audio chat.
> * Video chat.
> * Ability to send files (later though).

<br>
<br>

# The backend programming goes like this:
> * Parse datas in json formats, with data tags as the keys, so that it can be easily **json.load()**.
> * Use another thread to media streams and receive or send files in a chat (later though).
> * Maybe to have three servers (socket) for the following functions:
>   * keep status.
>   * for group messages.
>   * for private messages.
>   * for channel messages.

<br>
<br>

# The UI program:
### The pages include:
> * Home.
> * Private Chat.
> * Group chat.
> * Channels.
> * Audio Chat.
> * Video Chat.
> * Settings.

<br>
<br>

# **Client app operation:**

* Launch the Client app.

* Login or Signup:
  > Login:
  > * Enter username and password.
  > * Checks username and password with database data of client app.
  > * If not correct, shows an error dialog.
  > * If correct:
  >   * connects to the **status server**
  >     * the **status server** then sends back the list of online contacts.

  > Signup:
  > * Enter username and password.
  > * Checks username and password with server data of client datas.
  > * Server sends back if the username is available.

* Chat:
  > * Constantly listens for any chats.
  > * If any chat is received, reads the chat tags (details), then send the chat to the correct private chat or chat rooms or channels.

<br>
<br>

# Tag
## The tag format is actually a dict with keys:
> * action
>   * [edit] _[admin(add & remove), user, group, channel]
>     * add
>     * remove
>     * create
>     * delete
>   * chat
>   * [edit] _[audio, video]_chat
>     * start
>     * end
>   * signup
>   * login
>   * change

> * chat_color
> * chat
>   * text_chat
>   * audio_chat
>   * video_chat

> * response
>   * successful
>   * failed
>   * existing
>   * non_existing
>   * false_key

> * sender
> * recipient
>   * user_id
>   * group_id
>   * channel_id

> * sender_type
> * recipient_type
>   * user
>   * group
>   * channel

> * id
>   * user_id
>   * group_id
>   * channel_id

> * key
> * name
> * status
> * date_time
> * date_time
> * last_seen
> * response_to
> * data




<br>
<br>

# **Client - Server Interactions.**
## *Sequentially arranged*
* **Client**
  * connects to server at launch.
  * send **signup details** to server.
    > Keys | Values
    > - | -
    > action | signup, create_user
    > user_id | id
    > key | password
    <p>

  * then send **login details** to server.
    > Keys | Values
    > - | -
    > action | login
    > user_id | id
    > key | password
    <p>

  * to **[add, remove, create, delete] [user, group, channel]**, send dict to server
    > Keys | Values
    > - | -
    > action | [add, remove, create, delete]_[user, group, channel]
    > [user, group, channel]_id | id
    > sender | id
    > [user, group, channel]_id (only for create) | id
    > creation_date (only for create) | date
    <p>

  * to **change [user, group, channel]_[id, name]**
    > Keys | Values
    > - | - 
    > action | change_[user, group, channel]_[id, name]
    > [user, group, channel]_[id, name] | id, name
    > sender | id
    <p>

  * to send **[user, group, channel (only for admin)]_chats**
    > Keys | Values
    >  ----- | ----- 
    > action | chat
    > chat | chat
    > sender | id
    > recipient | [user, group, channel (only for admin)]_id
    <p>

  * to start **[audio, video)]_chats**
    > Keys | Values
    >  ----- | ----- 
    > action | start_[audio, video)]
    > sender | id
    > recipient | [audio, video)]_id
    <p>

  * to end **[audio, video)]_chats**
    > Keys | Values
    >  ----- | ----- 
    > action | end_[audio, video)]
    > sender | id
    > recipient | [audio, video)]_id
    <p>



* **Server**
  * receives client connection
  > Actions | Operations | Response
  > -|- | -
  > signup | checks if user_id already exists | successful, failed, existed
  > login |checks if user_id and password are correct | successful, failed, false_key
  > add | add [user, group, channel] to user | successful, failed
  > remove | remove [user, group, channel] from user | successful, failed
  > create | create [user, group, channel] for user | successful, failed, existed
  > delete | delete [user, group, channel] from [user, server] | successful, failed
  > start | starts the action [audio, video] chat | successful, failed
  > end | ends the action [audio, video] chat | successful, failed
  > chat | sends the chat to the recipient
  > change | changes the [id, name] of the [user, group, channel] | successful, failed

<br>
<br>

# **Classes and their properties.**
> * Base:
>   * id
>   * date_time
>   * name

> * User(Base):
>   * user_id
>   * users_manager
>   * groups_manager
>   * channels_manager
>   * key
>   * status: [online, offline]
>   * last_seen
>   * queued_chats
>   * chats_manager

> * Chat(Base):
>   * chat_id
>   * text
>   * type: [text, audio, video]
>   * sender
>   * recipient
>   * sender_type
>   * recipient_type
>   * response_to

> * Multi_Users(Base):
>   * admins_manager
>   * users_manager

> * Group(Multi_Users):
>   * group_id

> * Channel(Multi_Users):
>   * channel_id

> * Manager:
>   * user_id
>   * objects

> * Users_Manager(Manager):
>   * users

> * Chats_Manager(Manager):
>   * chats
>   * groups_chats
>   * channels_chats

> * Groups_Manager(Manager):

> * Channels_Manager(Manager):


> * Server:

> * Client: associated with only one **User**

> * Receiver: **constantly awaits** data from the server.



