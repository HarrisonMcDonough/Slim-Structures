import cwComplexes
from cwComplexes import *
from presComplex import *
import networkx as nx
import matplotlib.pyplot as plt
import time
import numpy as np

#------------------------------------------------------------------------------------------------

#For now:
#Enter all LOT relators in forward form 
#(read in the same direction as the diEdge)

LOT = "1, 2, 3, 4, 5 |   1 5 2' 5', 2 4 3' 4', 3 1 4' 1', 4 2 5' 2'"
presLOT = presComplexBuilder(LOT)


#------------------------------------------------------------------------------------------------

#Getting corners in links

# ascendingList = []
# descendingList = []

# for i in range(len(presLOT.twoCells)):
# 	ascendingList.append(corners[i][1])
# 	descendingList.append(corners[i][3])

#print(ascendingList)
#print(descendingList)


#------------------------------------------------------------------------------------------------

#Building ascending/descending links as graphs

# G_asc = nx.DiGraph()
# G_dsc = nx.DiGraph()

# for oneCell in presLOT.oneCells:
# 	G_asc.add_node(oneCell)
# 	G_dsc.add_node(oneCell)

# #nx.draw(G_asc, with_labels=True, font_weight='bold')
# #plt.show()

# for i in range(len(ascendingList)):
# 	G_asc.add_edge(ascendingList[i][0][0], ascendingList[i][1][0])

# for i in range(len(descendingList)):
# 	G_dsc.add_edge(descendingList[i][0][0], descendingList[i][1][0])

# nx.draw(G_asc, with_labels=True, font_weight='bold')
# plt.show()

#------------------------------------------------------------------------------------------------

#Defining slim structures

# def matrixMode(presComplex):
# 	superList = []
# 	for relator in presComplex.twoCells:
# 		array = np.zeros((2,2))
# 		oneCells = relator.getList()
# 		i = 0
# 		for oneCell in oneCells:
# 			i += 1
# 			identifier = oneCell[0]
# 			if i == 1:
# 				array[0][0] = int(str(oneCell[0]))
# 				i+=1
# 			if i == 3:
# 				array[0][1] = int(str(oneCell[0]))
# 				i+=1
# 			if i == 5:
# 				array[1][1] = int(str(oneCell[0]))
# 				i+=1
# 			if i == 7:
# 				array[1][0] = int(str(oneCell[0]))
# 				i+=1

# 		superList.append(array)
# 	return superList

x = presLOT.twoCells
# print(x[1].getSimpleList())

def getSlimListInput(twoCells):
	slimList = []
	for twoCell in twoCells:
		simple = twoCell.getSimpleList()
		print(simple)
		print('This is your relator')
		x = input("Please choose a highest 1-cell (an integer 0-3): \n ")
		time.sleep(1)
		# stuff = 0
		x = int(x)

		# if x == 0:
		# 	stuff = matrix[0][0]
		# if x == 1:
		# 	stuff = matrix[0][1]
		# if x == 2:
		# 	stuff = matrix[1][1]
		# if x == 3:
		# 	stuff = matrix[1][0]

		nice = (simple, x)
		print("Great job")
		print('')
		slimList.append(nice)
		time.sleep(1)

	# print(slimList)
	return slimList

# testList = ['poop', 'poop', 'poop', 'not poop']
# indices = [i for i, x in enumerate(testList) if x == 'poop']

# print(indices)

def uniqueChecker(slimList):
	uniqueList = []
	for slim in slimList:
		uniqueList.append(slim[0][slim[1]])

	flag = len(set(uniqueList)) == len(uniqueList)

	if flag:
		return True
	else: 
		return False

def buildCyclicList(slimList):
	sameLevel = []
	difLevel = []

	for slim in slimList:
		fixedEle = slim[0][slim[1]]
		indices = [i for i, x in enumerate(slim[0]) if x == fixedEle]
		if len(indices) > 1:

			if slim[1] == 1:
				difLevel.append((fixedEle, fixedEle, 'forward'))

			if slim[1] == 3:
				difLevel.append((fixedEle, fixedEle, 'backward'))

		for item in slimList:

			if item != slim:
				newindices = [i for i, x in enumerate(item[0]) if x == fixedEle]

				for index in newindices:

					if (index + item[1]) == 3:
						sameLevel.append((fixedEle, item[0][item[1]]))

					else:
						if (index == 0) or (index == 3):
							difLevel.append((fixedEle, item[0][item[1]], 'forward'))

						elif (index == 1) or (index == 2):
							difLevel.append((fixedEle, item[0][item[1]], 'backward'))

	print(difLevel)
	print(sameLevel)
	return difLevel, sameLevel

def cyclic(presComplex, slimList):
	graph = nx.DiGraph()
	difList, sameList = buildCyclicList(slimList)


	genList = presComplex.getOneCellList()
	i = 1
	for gen in genList:
		graph.add_node(str(i)+"_1")
		graph.add_node(str(i)+"_2")
		graph.add_node(str(i)+"_3")

		i += 1

	for item in sameList:
		graph.add_edge((str(item[0]))+"_1",(str(item[1]))+"_1")
		graph.add_edge((str(item[0]))+"_2",(str(item[1]))+"_2")
		graph.add_edge((str(item[0]))+"_3",(str(item[1]))+"_3")

	for item in difList:
		if item[2] == "forward" :
			graph.add_edge((str(item[0]))+"_1",(str(item[1]))+"_2")
			graph.add_edge((str(item[0]))+"_2",(str(item[1]))+"_3")
		else:
			graph.add_edge((str(item[0]))+"_2",(str(item[1]))+"_1")
			graph.add_edge((str(item[0]))+"_3",(str(item[1]))+"_2")




	cycleList = []
	for cycle in nx.simple_cycles(graph):
		cycleList.append(cycle)

	georgeBoole = False
	if len(cycleList) == 0:
		georgeBoole = True



	# nx.draw(graph, with_labels=True, font_weight='bold')
	# plt.show()

	return georgeBoole




#------------------------------------------------------------------------------------------------

def master3000(presComplex):
	twoCells = presComplex.twoCells
	slimList = []
	goodList = []
	i = 0
	for twoCell in twoCells:
		simple = twoCell.getSimpleList()

		slim = (simple, 0)
		slimList.append(slim)

	counter0 = 0
	superCounter = 0	

	for oneCell in slimList[0][0]:
		counter1 = 0
		newtuple0 = (slimList[0][0], counter0)
		slimList[0] = newtuple0


		for oneCell in slimList[1][0]:
			counter2 = 0
			newtuple1 = (slimList[1][0], counter1)
			slimList[1] = newtuple1

			if len(slimList) == 2:
				if uniqueChecker(slimList):
					if cyclic(presComplex, slimList):
						print("Wooohoo slim structure!")
						goodList.append(slimList)


			if len(slimList) > 2:
				for oneCell in slimList[2][0]:
					counter3 = 0
					newtuple2 = (slimList[2][0], counter2)
					slimList[2] = newtuple2

					if len(slimList) == 3:
						if uniqueChecker(slimList):
							if cyclic(presComplex, slimList):
								print("Wooohoo slim structure!")
								goodList.append(slimList)

					if len(slimList) > 3:
						for oneCell in slimList[3][0]:
							#print(slimList[3][0])
							counter4 = 0
							newtuple3 = (slimList[3][0], counter3)
							slimList[3] = newtuple3

							if len(slimList) == 4:
								if uniqueChecker(slimList):
									if cyclic(presComplex, slimList):
										print("Wooohoo slim structure!")
										goodList.append(slimList)



							counter3 += 1
							superCounter += 1
					counter2 += 1
					#superCounter += 1
			counter1 += 1
			#superCounter += 1
		counter0 += 1
		#superCounter += 1
	print(superCounter)
	print(goodList)
	return goodList

	





#------------------------------------------------------------------------------------------------


# poop = master3000(presLOT)
# for line in poop:
# 	print(line)

lister = getSlimListInput(x)

print(uniqueChecker(lister))

# start = time.time()


# end = time.time()

print(cyclic(presLOT, lister))


