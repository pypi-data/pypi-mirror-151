import requests, json

HEADERS = {
    "content-type": "application/json",
    "accept" : "application/json",
    "api-consumer-type":  "mobile; iOS/203500927335335108",
    "accept-charset": "utf-8",
    "client-id":  "85lcqzxpb9bqu9z6ga1ol55du",
    "accept-language": "en-us",
    "accept-encoding": "br, gzip, deflate",
    "user-agent": "Twitch 203500927335335108 (iPhone; iOS 12.3.1; en_US)",
    "x-apple-model":  "iPhone 7",
    "x-app-version":  "9.10.1",
    "x-apple-os-version": "12.3.1"
}

def get_cid(channel: str) -> str | bool:
    """
    Gets the channel id of a user on twitch.
    Params:
        channel: str - The username of the channel you want to get the channel id.
    Returns:
        str | bool - The channel id of the account or False if the channel was not found.
    """

    accessKey = "qecxhnjevnnfvskhhd07od91yliqti"

    cl= 'https://api.twitch.tv/api/channels/' + channel + '/access_token?need_https=true&oauth_token=' + accessKey

    channel = requests.get(cl, headers=HEADERS)

    try:
        token_info = channel.json()['token'] 
        channel_id = json.loads(token_info)['channel_id']
        return channel_id
    except KeyError:
        return False

def follow(user: str, token: str, cid: bool=False) -> bool:
    """
    Follows a channel on twitch.
    Params:
        user: str - The username or channel id (cid) of the channel to be followed.
        token: str - The token of the account to follow the user.
        cid: bool - if True the param "user" must be a valid channel id. This will speed up the process. Else it will automatically get the channel id of the username.
    Returns:
        bool - True if followed successfully
    """
    headers = HEADERS.copy()
    headers['Authorization'] = 'OAuth ' + token

    if not cid:
        channel_id = get_cid(user)
    else:
        channel_id = user

    payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"%s\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]' % channel_id

    r = requests.post('https://gql.twitch.tv/gql', data=payload, headers=headers)

    if 'error' in r.text:
        pass
    
    else:
        try:
            followed_user = r.json()[0]['data']['followUser']['follow']['user']
            return True
        except Exception as e:
            pass

    return False

def unfollow(user: str, token: str, cid: bool=False) -> bool:
    """
    Unfollows a channel on twitch.
    Params:
        user: str - The username or channel id (cid) of the channel to be unfollowed.
        token: str - The token of the account to unfollow the user.
        cid: bool - if True the param "user" must be a valid channel id. This will speed up the process. Else it will automatically get the channel id of the username.
    Returns:
        bool - True if followed successfully
    """
    headers = HEADERS.copy()
    headers['Authorization'] = 'OAuth ' + token

    if not cid:
        channel_id = get_cid(user)
    else:
        channel_id = user

    payload = '[{"operationName":"FollowButton_UnfollowUser","variables":{"input":{"targetID":"%s"}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"f7dae976ebf41c755ae2d758546bfd176b4eeb856656098bb40e0a672ca0d880"}}},{"operationName":"AvailableEmotesForChannel","variables":{"channelID":"230422643","withOwner":true},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"b9ce64d02e26c6fe9adbfb3991284224498b295542f9c5a51eacd3610e659cfb"}}}]' % channel_id

    r = requests.post('https://gql.twitch.tv/gql', data=payload, headers=headers)

    if 'error' in r.text:
        pass
    
    else:
        try:
            followed_user = r.json()[0]['data']['followUser']['follow']['user']
            return True
        except Exception as e:
            pass

    return False

def friend(user: str, token: str, cid: bool=False) -> bool:
    """
    Sends a friend request to a channel on twitch.
    Params:
        user: str - The username or channel id (cid) of the channel to send a friend request.
        token: str - The token of the account to friend the user.
        cid: bool - if True the param "user" must be a valid channel id. This will speed up the process. Else it will automatically get the channel id of the username.
    Returns:
        bool - True if followed successfully
    """
    headers = HEADERS.copy()
    headers['Authorization'] = 'OAuth ' + token
    
    if not cid:
        channel_id = get_cid(user)
    else:
        channel_id = user

    payload = '[{"operationName":"FriendButton_CreateFriendRequest","variables":{"input":{"targetID":"%s"}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"380d8b19fcffef2fd8654e524444055dbca557d71968044115849d569d24129a"}}}]' % channel_id

    r = requests.post('https://gql.twitch.tv/gql', data=payload, headers=headers)

    if 'error' in r.text:
        return False
    
    return True