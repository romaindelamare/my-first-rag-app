class MemoryStore:
    def __init__(self):
        self.sessions = {}  # session_id: list of messages

    def add_message(self, session_id, role, content):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append({"role": role, "content": content})

    def get_messages(self, session_id):
        return self.sessions.get(session_id, [])

    def session_exists(self, session_id):
        return session_id in self.sessions

    def reset(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

memory = MemoryStore()
