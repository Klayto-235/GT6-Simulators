class Historian():
    def __init__(self):
        self.history = []
        self.history_index = -1
        self.history_max_index = -1

        self.temp_undo = []
        self.temp_redo = []

        empty_func = lambda: None
        self.callback_enable_undo = empty_func
        self.callback_enable_redo = empty_func
        self.callback_disable_undo = empty_func
        self.callback_disable_redo = empty_func

    def undo(self):
        if (self.history_index >= 0):
            self.history_index = self.history_index - 1
            self.apply_history_events(self.history[self.history_index + 1][0], False)

    def redo(self):
        if (self.history_index + 1 <= self.history_max_index):
            self.history_index = self.history_index + 1
            self.apply_history_events(self.history[self.history_index][1], True)

    def apply_history_events(self, events, forward_direction):
        if forward_direction:
            for i in range(len(events)):
                events[i][0](*events[i][1], False)
        else:
            for i in range(len(events)):
                events[-i - 1][0](*events[-i - 1][1], False)
        self.check_undo_redo()

    def commit_event(self, undo_event, redo_event):
        self.temp_undo.append(undo_event)
        self.temp_redo.append(redo_event)

    def register_events(self):
        if (len(self.temp_undo) > 0 and len(self.temp_redo) > 0):
            if (self.history_index == self.history_max_index):
                self.history_max_index = self.history_max_index + 1
                self.history_index = self.history_index + 1
                if self.history_index >= len(self.history):
                    self.history.append((self.temp_undo, self.temp_redo))
                else:
                    self.history[self.history_index] = (self.temp_undo, self.temp_redo)
            else:
                self.history_index = self.history_index + 1
                self.history_max_index = self.history_index
                self.history[self.history_index] = (self.temp_undo, self.temp_redo)
            self.temp_undo = []
            self.temp_redo = []
            self.check_undo_redo()

    def insert_commit(self, undoevent, redoevent):
        if self.history_index >= 0:
            self.history[self.history_index][0].append(undoevent)
            self.history[self.history_index][1].append(redoevent)
        if self.history_index < self.history_max_index:
            self.history[self.history_index + 1][0].insert(0, redoevent)
            self.history[self.history_index + 1][1].insert(0, undoevent)

    def check_undo_redo(self):
        if (self.history_index >= 0):
            self.callback_enable_undo()
        else:
            self.callback_disable_undo()
        if (self.history_index + 1 <= self.history_max_index):
            self.callback_enable_redo()
        else:
            self.callback_disable_redo()

    def clear(self):
        self.history = []
        self.history_index = -1
        self.history_max_index = -1

        self.temp_undo = []
        self.temp_redo = []

        self.check_undo_redo()
