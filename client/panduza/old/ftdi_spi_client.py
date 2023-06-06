import json
import threading
from ..core import Interface, Attribute, EnsureError, RoField, RwField

from dataclasses import dataclass

@dataclass
class Ftdi_Spi(Interface):
	"""Interface to manage ftdi chip for spi
	"""

	interface : Interface = None

	def __post_init__(self):
		if self.alias:
			pass
		elif self.interface:
			# Build from an other interface
			self.alias = self.interface.alias
			self.addr = self.interface.addr
			self.port = self.interface.port
			self.topic = self.interface.topic
			self.client = self.interface.client

		super().__post_init__()

		# TODO should have two RwField
		# one for the data and one for the slave selector cs
		# === WRITE ===
		self.add_attribute(
			Attribute(
			name = "write"
			)
		).add_field(
			RwField(
			name = "values"
			)
		)

		# TODO should have three RwField
		# one for the cs, one for the size and one for the data
		# cs is the slave selector so that the user can chose whichever slave they want to read/write
		# size id the number of byte the user wants to read
		# data is the data where the slave response is (RoField better ?)
		# how to add a second field to an attribute ?
		# === READ ===
		self.add_attribute(
			Attribute(
			name = "read"
			)
 		).add_field(
		 	RwField(
		 	name = "values"
			)
		)