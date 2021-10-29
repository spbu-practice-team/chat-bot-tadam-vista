import traceback
import re
from matrix_client.client import MatrixClient
from matrix_client.api import MatrixRequestError


class MatrixBotAPI:

    # username - Matrix username
    # password - Matrix password
    # server   - Matrix server url : port
    def __init__(self, server: str, username: str, password: str, rooms=None):

        self.username = username
        self.password = password

        self.client = MatrixClient(server)

        # Authenticate with given credentials
        self.client.login(username, password)

        # Store empty list of handlers
        self.handlers = []

        # If rooms is None, we should listen for invites
        # and automatically accept them
        self.rooms = []

        # Store allowed room ids
        self.room_ids = []
        if rooms is None:
            self.client.add_invite_listener(self.handle_invite)

            # Add all rooms we're currently in to self.rooms
            # and add their callbacks
            for room_id, room in self.client.get_rooms().items():
                room.add_listener(self.handle_message)
                self.rooms.append(room)
                self.room_ids.append(room_id)
        else:
            self.client.add_invite_listener(self.handle_invite)

            # Add the message callback for all specified rooms
            for room in rooms:
                try:
                    # If room is a string we assume it is a room_id
                    # Otherwise, we assume it a room object for backwards
                    # compatibility sake.
                    if isinstance(room, str):
                        _room = self.client.join_room(room)

                    else:
                        _room = room

                    _room.add_listener(self.handle_message)
                    self.rooms.append(_room)
                    self.room_ids.append(_room.room_id)

                except MatrixRequestError as error:
                    print(error)
                    if error.code == 403:
                        print('You likely need to invite the bot')

    def add_handler(self, handler):
        self.handlers.append(handler)

    def handle_message(self, room, event):
        # Make sure we didn't send this message
        if re.match("@" + self.username, event['sender']):
            return

        # Loop through all installed handlers and see if they need to be called
        for handler in self.handlers:
            if handler.test_callback(room, event):
                # This handler needs to be called
                try:
                    handler.handle_callback(room, event)
                except:
                    traceback.print_exc()

    def handle_invite(self, room_id, state):
        print("Got invite to room: " + str(room_id))

        print("Joining...")
        room = self.client.join_room(room_id)

        # Add message callback for this room
        room.add_listener(self.handle_message)

        # Add room to list
        self.rooms.append(room)

    def start_polling(self):
        # Starts polling for messages
        self.client.start_listener_thread()
        return self.client.sync_thread
