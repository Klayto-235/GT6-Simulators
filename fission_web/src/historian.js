let historian = {
	history: [],
	historyIndex: -1,

	undoBuffer: [],
	redoBuffer: [],
	preventCommit: false,

	cb_enableUndo: () => {},
	cb_enableRedo: () => {},
	cb_disableUndo: () => {},
	cb_disableRedo: () => {},

	undo: function() {
		if (this.historyIndex >= 0) {
			const events = this.history[this.historyIndex][0].slice().reverse();
			this.historyIndex -= 1;
			this.preventCommit = true;
			events.forEach(e => e());
			this.preventCommit = false;
			this.enableDisableUndoRedo();
		}
	},

	redo: function() {
		if (this.historyIndex < this.history.length - 1) {
			this.historyIndex += 1;
			const events = this.history[this.historyIndex][1];
			this.preventCommit = true;
			events.forEach(e => e());
			this.preventCommit = false;
			this.enableDisableUndoRedo();
		}
	},

	commitEvent: function(undoEvent, redoEvent) {
		if (!this.preventCommit) {
			this.undoBuffer.push(undoEvent);
			this.redoBuffer.push(redoEvent);
		}
	},

	registerEvents: function() {
		if (!this.preventCommit && this.undoBuffer.length > 0 && this.redoBuffer.length > 0) {
			if (this.historyIndex == this.history.length - 1) {
				this.historyIndex += 1;
				this.history.push([this.undoBuffer, this.redoBuffer]);
			} else {
				this.historyIndex += 1;
				this.this.history.splice(this.historyIndex, Infinity, [this.undoBuffer, this.redoBuffer]);
			}
			this.undoBuffer = [];
			this.redoBuffer = [];
			this.enableDisableUndoRedo();
		}
	},

	insertEvent: function(undoEvent, redoEvent) {
		if (this.historyIndex >= 0) {
			this.history[this.historyIndex][0].push(undoEvent);
			this.history[this.historyIndex][1].push(redoEvent);
		}
		if (this.historyIndex < this.history.length - 1) {
			this.history[this.historyIndex + 1][0].unshift(redoEvent);
			this.history[this.historyIndex + 1][1].unshift(undoEvent);
		}
	},

	enableDisableUndoRedo: function() {
		if (this.historyIndex >= 0) this.cb_enableUndo();
		else this.cb_disableUndo();
		if (this.historyIndex < this.history.length - 1) this.cb_enableRedo();
		else this.cb_disableRedo();
	},
	
	clear: function() {
		this.history = [];
		this.historyIndex = -1;
		
		this.undoBuffer = [];
		this.redoBuffer = [];
		this.preventCommit = false;

		this.enableDisableUndoRedo();
	}
};

export default historian;