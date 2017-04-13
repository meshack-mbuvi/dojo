import random

from dojo import Room,Office,LivingSpace
from person import Person,Fellow,Staff


"""
Implementations of functionalities

Create rooms
"""


class Implementation():
	all_rooms=[]#variable to hold all rooms in a dojo
	all_people=[]#variable to hold all people  in a dojo
	available_offices=[]#variable to hold offices with space to be allocated

	def hasdigits(self,string):
		"""checks whether a string has digits"""
		return any(char.isdigit() for char in string)


	def create_room(self,room_name,room_type):
		"""This function creates a new room of type office or livingspace"""
		#First check that room name and type do not have digits
		if self.hasdigits(room_name) or self.hasdigits(room_type) :
			print("Not a valid room in our context")
			return ("Not a valid room in our context")
		#check whether room_name is in the list of existing rooms in dojo

		if room_name in [room_object.room_name for room_object in self.all_rooms]:
			print("{} is already taken, try a different one".format(room_name))
			return False

		#if it does not exist,create the room
		else:
			if room_type.lower()=="office":
				room_object=Office(room_name,room_type.lower())
				self.all_rooms.append(room_object)
				print ("An office called {} has been successfully created!".format(room_name))
				return room_object

			elif room_type.lower()=="livingspace":
				room_object=LivingSpace(room_name,room_type.lower())
				"""
				Be careful not to save the name of an office;rather save the object since you can get its attributes
				NB:name is a string """
				self.all_rooms.append(room_object)
				print ("A Living Space called {} has been successfully created!".format(room_name))
				return room_object
			else:
				print("Not a valid room")
				return ("Not a valid room")

	def allocate_office(self,person_object):
		"""
		This function takes as an argument an object of type person,whose attribute 
		office_name is set according to one of the available office Space
		Logic:
		    loop through a list with objects of type office checking the first with 
		    available space,add to its list_of_occupants attribute the name of the 
		    person object received as argument

		return:
		    dictionary object for the purpose of testcases  
		"""
		##create a list of objects whose type is office and have an empty space
		available_offices=[room_object for room_object in self.all_rooms if room_object.room_type=='office'\
		                       and len(room_object.list_of_occupants)<room_object.max_occupants]
		

		##randomize the list first and get the last object in it
		##NB:You can decide on whether to get the last or the first object
		random.shuffle(available_offices)
		if len(available_offices)!=0:
			office_to_allocate=available_offices.pop()

			#Now assign the person this office
			office_to_allocate.list_of_occupants.append(person_object)
			#set the attribute office_name of object person to the name of the asigned office
			person_object.office_name=office_to_allocate.room_name

			print("{} {} has been allocated the office {}".format(person_object.firstname,person_object.secondname,office_to_allocate.room_name))
			
			return person_object
		else:
			print("{} {} has not been allocated any office!".format(person_object.firstname,person_object.secondname))
			return person_object
			


	def allocate_livingspace(self,person):
		"""
		This function takes as an argument an object of type person,whose attribute 
		livingspacename is set according to one of the available livingspaces
		Logic:
		    loop through a list with objects of type office checking the first with 
		    available space,add to its list_of_occupants attribute the name of the 
		    person object received as argument

		return:
		    office_name or None  
		"""
		#Let's check whether the person can be allocated livingspace
		if person.person_type.lower()!='staff' and person.wants_accommodation=="Y":
			available_rooms=self.all_rooms
			##create a list of objects whose type is office and have an empty space
			available_living_spaces=[room_object for room_object in available_rooms if room_object.room_type=='livingspace' and len(room_object.list_of_occupants)<4]

			##randomize the list first and get the last object in it
			##NB:You can decide on whether to get the last or the first object
			random.shuffle(available_living_spaces)

			if len(available_living_spaces)!=0:
				livingspace=available_living_spaces.pop()
				#Now assign the person this office
				livingspace.list_of_occupants.append(person)
				#set the attribute office_name of object person to the name of the asigned office
				person.livingspace=livingspace.room_name
				print("{} {} has been allocated the livingspace {}".format(person.firstname,person.secondname,livingspace.room_name))
				return livingspace.room_name
			else:
				print("{} {} has not been allocated any livingspace!".format(person.firstname,person.secondname))
				return None
			


	def add_person(self,firstname,secondname,person_type,wants_accommodation="N"):

		#Ensure the persons details have no digits		
		if self.hasdigits(firstname) or self.hasdigits(secondname) or self.hasdigits(person_type):
			print("Person's details should not have numbers")
			return ("Not a valid person in our context")

		#Ensure the person is not in system
		names_people_in_system=[]
		for people in self.all_people:
			#create a single name
			temp_name=" ".join([people.firstname,people.secondname])
			names_people_in_system.append(temp_name)
			print (names_people_in_system)


		#Ensure the person is not in system already
		#formart name of person
		new_person_name=" ".join([firstname.upper(),secondname.upper()])
		if new_person_name in names_people_in_system:
			print("person already in the system")
			return "person already in the system" 


		elif person_type.lower()=="fellow":
			person=Fellow(firstname.upper(),secondname.upper(),person_type.upper())

			self.allocate_office(person)
			self.all_people.append(person)
			print("{} {} has been successfully added.".format(person.firstname,person.secondname))
			
			##Allocate livingspace if fellow and chose livingspace option Y
			if wants_accommodation=='y' or wants_accommodation=='Y':
				person.wants_accommodation="Y"
			else:
				person.wants_accommodation="N"
			self.allocate_livingspace(person)

			return person

		elif person_type.lower()=="staff":
			person=Staff(firstname.upper(),secondname.upper(),person_type.upper())

			self.allocate_office(person)
			self.all_people.append(person)
			
			return person

		else:
			print("Not a valid person in our context")
			return "Not a valid person in our context"

	def print_room(self,room_name):
		"""
		This function prints each room together with names of its occupants

		"""
		##single out the particular room from self.all_rooms
		self.room_to_list_its_occupants=[room_object for room_object in self.all_rooms if room_object.room_name==room_name]
		size=len(self.room_to_list_its_occupants[0].list_of_occupants)
		names_of_occupants=[]
		for index in range(0,size):
			#print(self.temp_room[0].list_of_occupants[index].firstname,self.temp_room[0].list_of_occupants[index].secondname)
			names_of_occupants.extend(['{} {}'.format(self.room_to_list_its_occupants[0].list_of_occupants[index].firstname,self.room_to_list_its_occupants[0].list_of_occupants[index].secondname)])

		print(names_of_occupants)
		return names_of_occupants

	def print_allocations(self,filename=""):
		"""This function prints office and its occupants"""
		room_names=[]
		for index in range(0,len(self.all_rooms)):
			room_names.append(self.all_rooms[index].room_name)

		#list to hold names of unallocated people
		#allo={'blue':[list of occupants]}
		allocations=[]
		#extract the list of room occupands
		for room  in self.all_rooms:
			print(room.room_name)
			#loop through the list of occupants outputing the names
			for person in room.list_of_occupants:
				print(person.firstname,person.firstname)
				allocations.append(" ".join([person.firstname,person.firstname]))

			if filename!="":
				#open the file called filename with write mode enabled
				f=open(" {}".format(filename),"w+")
				#write the room name as a header
				f.write("{}\n".format(room.room_name))
				f.write("-----------------------\n")
				#loop through the room's list of occupants writing thier names
				for person in room.list_of_occupants:					
					f.write(" ".join([person.firstname,person.secondname,person.person_type]))
					f.write("\n")
				f.close()

			else:
				print("Room is not occupied")

		return allocations

	def print_unallocated(self,filename=""):
		"""This function prints people who have not been allocated office
		If filename is provided,the unallocated people are stored in that file

		"""
		unallocated_people=[]
		for person in self.all_people:
			if person.office_name==""or person.livingspaceName=="":
				unallocated_people.append([" ".join([people.firstname,people.secondname,people.person_type]) \
					                     for people in self.all_people if people.office_name==""])
		if filename!="":
			f=open("{}".format(filename),"w+")
			f.write("{}\n".format(room_object.room_name.upper()))
			f.write("-----------------------\n")
			for person in allocations:
				f.write(person)
				f.write("\n")
				f.close()

		print(unallocated_people)

		return unallocated_people