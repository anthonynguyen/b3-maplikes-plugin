# Map Like Plugin for B3
# By clearskies (Anthony Nguyen)
# GPL licensed

import b3
import b3.events
import b3.plugin
import re

__version__ = "1"
__author__ = "clearskies (Anthony Nguyen)"

class MaplikesPlugin(b3.plugin.Plugin):
	requiresConfigFile = False

	def onStartup(self):
		self._admin = self.console.getPlugin("admin")
		self._admin.registerCommand(self, "likemap", 1, self.cmd_like, "like")
		self._admin.registerCommand(self, "dislikemap", 1, self.cmd_dislike, "dislike")
		self._admin.registerCommand(self, "maplikes", 1, self.cmd_maplikes, "mlikes")

		self.mapname = self.console.getCvar('mapname').value

		self.registerEvent(b3.events.EVT_GAME_MAP_CHANGE)

	def onEvent(self, event):
		if event.type == b3.events.EVT_GAME_MAP_CHANGE:
			self.mapname = event.data["new"]

	def hasVoted(self, client):
		chq = "SELECT * FROM maplikes WHERE client_id = '{0}' AND map = '{1}'".format(client, self.mapname)
		c = self.console.storage.query(chq)
		if c and c.rowcount > 0:
			return c.getRow()
		else:
			return False

	def doVote(self, client, action, confirm = False):
		vs = self.hasVoted(client.id)
		if not vs:
			dbq = "INSERT INTO maplikes (id, client_id, map, likes, changes_left, last_voted) VALUES (DEFAULT, '{0}', '{1}', '{2}', DEFAULT, DEFAULT)".format(client.id, self.mapname, action)
			c = self.console.storage.query(dbq)
			client.message("Successfully {0}liked^7 {1}!".format("^2" if action == 1 else "^1dis", self.mapname))
		else:
			if vs["changes_left"] == 0:
				client.message("You have already {0}liked^7 this map on {1}. You cannot change your mind any more times. ".format("^2" if vs["likes"] == 1 else "^1dis", vs["last_voted"]))
			elif action == vs["likes"]:
					client.message("You already {0}like^7 this map, silly!".format("^2" if action == 1 else "^1dis"))
			elif confirm and vs["changes_left"] > 0:
				dbq = "UPDATE maplikes SET likes = {0}, changes_left = {1} WHERE client_id = '{2}' AND map = '{3}'".format(action, vs["changes_left"] - 1, client.id, self.mapname)
				c = self.console.storage.query(dbq)
				client.message("Successfully {0}liked^7 {1}!".format("^2" if action == 1 else "^1dis", self.mapname))
			else:
				client.message("You have already {0}liked^7 this map on {1}. You can change your mind {2} more time{3}. ".format("^2" if vs["likes"] == 1 else "^1dis", vs["last_voted"], vs["changes_left"], "" if vs["changes_left"] == 1 else "s"))
				client.message("Type {0}like confirm ^7to confirm.".format("^2!" if action == 1 else "^1!dis"))

	def cmd_like(self, data, client, cmd = None):
		if "confirm" in data:
			confirm = True
		else:
			confirm = False
		self.doVote(client, 1, confirm)

	def cmd_dislike(self, data, client, cmd = None):
		if "confirm" in data:
			confirm = True
		else:
			confirm = False
		confirm = True if data == "confirm" else False
		self.doVote(client, 0, confirm)

	def cmd_maplikes(self, data, client, cmd = None):
		mapname = self.console.getCvar('mapname').value
		mlq = "SELECT * FROM maplikes WHERE map = '{0}' AND likes = 1;".format(self.mapname)
		mdq = "SELECT * FROM maplikes WHERE map = '{0}' AND likes = 0;".format(self.mapname)
		c = self.console.storage.query(mlq)
		maplikes = c.rowcount
		c = self.console.storage.query(mdq)
		mapdislikes = c.rowcount
		cmd.sayLoudOrPM(client, "{0}:^7 ^2{1}^7 like{2} and ^1{3}^7  dislike{4}.".format(self.mapname, maplikes, "" if maplikes == 1 else "s", mapdislikes, "" if mapdislikes == 1 else "s"))