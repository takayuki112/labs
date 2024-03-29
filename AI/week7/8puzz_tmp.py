import graphs as gr
import pq


#A state is a falttenned tile board, 0 = blank
goal_state = [
			[1, 2, 3], 
			[4, 5, 6], 
			[7, 8, 0]]

initial_state = [
				[8, 5, 4], 
				[3, 1, 2], 
				[7, 6, 0]]

#Possible moves would be to swap 0 with neighbours
adjs = {'R':[1, 0], 'L':[-1, 0], 'U':[0, 1], 'D':[0, -1]}

def nexts(state):
	nexts = {} #set of {move: state}s
	x0, y0 = get_xy(0, state)

	for m, adj in adjs.items():
		xn = x0 + adj[0]
		yn = y0 + adj[1]

		if xn not in range(3) or yn not in range(3):
			continue

		nexts[m] = swap0(state, xn, yn)

	return nexts


def swap0(state, xn, yn):
	x0, y0 = get_xy(0, state)
	state[x0][y0] = state[xn][yn]
	state[xn][yn] = 0
	return state.copy()


def get_xy(n, state):
	for y in range(3):
		for x in range(3):
			if state[y][x] == n:
				return x, y

#Heuristics of the state
def h(state, goal_state):
	n_missplaced = 0
	for y in range(3):
		for x in range(3):
			if state[y][x] != goal_state[y][x]:
				n_missplaced+=1
	return n_missplaced

# A-STAR -


def a_star_rev3(g, start, target):
	open = pq.PriorityQueue()
	open.push(start, [], 0+h(start, target))
	explored = []

	while not open.is_empty():
		curr, path, f_cost_curr = open.pop()
		explored.append(curr)

        #Check if you want

		if h[curr]==0:
			print("\nFound BEST path - ", path)
			print("\nWith a cost = ", f_cost_curr)
			return
			
		print("\nCurrently at -", curr)
		
		for neighbour, e_cost in g.adj_list[curr]:
			n_path = path.copy()
			n_path.append(neighbour)

			g_cost_neighbour = (f_cost_curr - h[curr]) + e_cost
			f_cost_neighbour = g_cost_neighbour + h[neighbour]
			print("\t--> ", neighbour, "\t= G = ", g_cost_neighbour, "\t F = ", f_cost_neighbour)


			if neighbour not in explored:
				s = 0
				for i in range(len(open.queue)):
					
					if(open.queue[i][0] == neighbour): # Already exists, so compare gcosts (coz h is same anyway)
						previous_f = open.queue[i][2]
						if(f_cost_neighbour < previous_f):
							s = 1
							open.queue[i] = (neighbour, n_path, f_cost_neighbour)
							break
				if(s==0):
					open.push(neighbour, n_path, f_cost_neighbour)

def a_star(g, start, goal):
	open = pq.PriorityQueue()
	open.push(start, [], 0+h(start, goal))
	explored = []

	while not open.is_empty():
		curr, path, cost = open.pop()
		explored.append(curr)

        #Check if you want

		if h[curr]==0:
			print("Found BEST (another) path - ", path)
			print("With a cost = ", cost)
			return path
			

		for m, next in nexts(curr).items():
			n_path = path.copy()
			n_path.append(m)

			g_cost = cost + 1
			f_cost = g_cost + h(next, goal)

			if next not in explored:
				open.push(next, n_path, g_cost)
			else:
				for i in range(len(open.queue)):
					if(open.queue[i][0] == next and open.queue[i][2] > g_cost):
						open.queue[i] = (next, n_path, g_cost)

