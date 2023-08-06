import math
import numpy as np
import random as rd
import numba
from numba import njit
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import kmedoids
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def test_func():
    return math.inf

def _help():
    text = "This program computes a giant tour formed by a Distant Matrix, and a number of approximate cluster size.\n"
    text += "giant_tour_problem = GT(distant matrix, size of cluster). Output is a giant tour, in form of a list\n"
    text += "giant_tour_problem = gt.GT(DM_req,size_of_clusters= 6),\ns = giant_tour_problem.create_giant_tour()"
    print(text)

@njit
def _LS( giant_tour,DM_req, iteration_num=0):
    # DM_req =  self.DM_req
    #print(giant_tour[1])
    for k in range(10):
        for i in range(1,len(giant_tour)-2):
            if DM_req[giant_tour[i-1]][giant_tour[i]]+ DM_req[giant_tour[i+2]][giant_tour[i+1]]>  DM_req[giant_tour[i-1]][giant_tour[i+1]]+ DM_req[giant_tour[i]][giant_tour[i+2]]:
                x= giant_tour[i+1]
                giant_tour[i+1]=giant_tour[i]
                giant_tour[i] =x
    return giant_tour

class GT:
    def __init__(self, DM_req, size_of_clusters):
        self.DM_req = DM_req
        self.size_of_clusters = size_of_clusters

    def total_clustering(self, DM_req, size_of_clusters):
        # DM_req, number_of_clusters, small_cluster_num
        # DM_req = self.DM_req
        # size_of_clusters = self.size_of_clusters

        def fasterpam(small_list_req, DM_req, number_cluster):
            n_DM_req = len(small_list_req)
            cut_DM_req = np.empty((n_DM_req, n_DM_req), np.int_)
            for i in range(n_DM_req):
                for j in range(n_DM_req):
                    cut_DM_req[i, j] = DM_req[small_list_req[i], small_list_req[j]]

            c = kmedoids.fasterpam(cut_DM_req, number_cluster)
            d = c.labels.astype(np.int_)

            mylist = [[i, d[i]] for i in range(len(small_list_req))]

            values = set(map(lambda x: x[1], mylist))
            list_of_point_in_same_cluster = [[small_list_req[y[0]] for y in mylist if y[1] == x] \
                                             for x in values]

            return list_of_point_in_same_cluster, d

        # batch_cluster =
        final_cluster = []
        number_cluster = math.floor(len(DM_req) / size_of_clusters) + 1
        batch_cluster, _ = fasterpam(list(range(len(DM_req))), DM_req, number_cluster)
        # (small_list_req, DM_req, number_cluster):
        i = 0
        while True:

            if len(batch_cluster[i]) > size_of_clusters * 3:
                sub_number_cluster = math.ceil(len(batch_cluster[i]) / size_of_clusters)
                new_cluster, _ = fasterpam(batch_cluster[i], DM_req, sub_number_cluster)
                batch_cluster.pop(i)
                batch_cluster = batch_cluster + new_cluster
                i = i - 1
            else:
                final_cluster.append(batch_cluster[i])
                batch_cluster.pop(i)
                i = i - 1

            i = i + 1
            if len(batch_cluster) == 0:
                break
            if i > len(batch_cluster):
                break

        return final_cluster

    def create_center_point(self, cluster_result, DM_req):

        center_point = np.empty((len(cluster_result)), np.int_)
        i = 0
        for cluster in cluster_result:
            A = [[point, sum([DM_req[point][i] for i in cluster])] for point in cluster]
            x = min(A, key=lambda x: x[1])
            center_point[i] = x[0]
            i = i + 1

        return center_point

    def create_distance_matrix_center_point(self, center_point, DM_req):

        DM_center = np.empty((len(center_point), len(center_point)), np.int_)
        for i in range(len(center_point)):
            for j in range(len(center_point)):
                DM_center[i][j] = DM_req[center_point[i]][center_point[j]]

        return DM_center

    def create_data_model_for_center_points(self, DM_center, list_point, depot_index):
        data = {}

        data['distance_matrix'] = DM_center
        # create_dm(list_point,DM)
        data['num_vehicles'] = 1

        # if is_start_end==False:
        data['depot'] = depot_index

        return data

    def create_route_of_cluster(self, data):

        def print_solution_center(manager, routing, solution):

            """Prints solution on console."""

            #print('Objective: {} miles'.format(solution.ObjectiveValue()))
            index = routing.Start(0)
            plan_output = 'Route for vehicle 0:\n'
            route_distance = 0

            while not routing.IsEnd(index):
                plan_output += ' {} ->'.format(manager.IndexToNode(index))
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)

            plan_output += ' {}\n'.format(manager.IndexToNode(index))
            #print(plan_output)
            plan_output += 'Route distance: {}miles\n'.format(route_distance)

        # chuyển solution sang dạng mảng
        def get_routes(solution, routing, manager):
            routes = []

            for route_nbr in range(routing.vehicles()):
                index = routing.Start(route_nbr)
                route = [manager.IndexToNode(index)]

                while not routing.IsEnd(index):
                    index = solution.Value(routing.NextVar(index))
                    route.append(manager.IndexToNode(index))
                routes.append(route)

            return routes

        # if data['is_start_end'] == False:
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
        # else:
        #     manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['starts'], data['ends'])

        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        dimension_name = 'Distance'
        routing.AddDimension(
            transit_callback_index,
            0,
            3000000,
            True,
            dimension_name)
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        # distance_dimension.SetGlobalSpanCostCoefficient(100)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        # search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        # search_parameters.time_limit.seconds  = 1
        # search_parameters.solution_limit = 1
        # search_parameters.log_search = True

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            # print_solution(manager, routing, solution)
            routes = get_routes(solution, routing, manager)
            return routes
        else:
            return 'false solution'

    def create_in_out(self, GT_cluster_list, DM_req):
        in_out = np.empty((len(GT_cluster_list), 2), np.int_)
        for i in range(len(in_out)):
            in_out[i][0], in_out[i][1] = -1, -1
        for this_i in range(len(GT_cluster_list)):
            next_i = (this_i + 1) % len(GT_cluster_list)
            # print(this_i, next_i)
            A = [i for i in range(len(GT_cluster_list[this_i])) if i != in_out[this_i][0]]
            B = [j for j in range(len(GT_cluster_list[next_i])) if j != in_out[next_i][1]]
            if len(A) == 0:
                A = [i for i in range(len(GT_cluster_list[this_i]))]
            if len(B) == 0:
                B = [j for j in range(len(GT_cluster_list[next_i]))]
            # print("A,B, index: ",A,B)
            pair_1 = [[i, j] for i in A for j in B]
            # print("GT, original " , GT_cluster_list[this_i], GT_cluster_list[next_i])
            # print("pair_1", pair_1)
            pair = [[i, j, DM_req[GT_cluster_list[this_i][i]][GT_cluster_list[next_i][j]]] for i in A for j in B]
            pair.sort(key=lambda x: x[2])

            # pair = [[i, j, DM_req[GT_cluster_list[this_i][i]]  [GT_cluster_list[next_i][j]]] for i in A for j in B  ]

            # print(pair)
            in_out[this_i][1] = pair[0][0]
            in_out[next_i][0] = pair[0][1]

            # print("___________")

        return in_out

    def find_route_inside_cluster(self, GT_cluster_list, DM_req, this_i, in_out):

        size_cluster = len(GT_cluster_list[this_i])
        data = {}

        data['distance_matrix'] = DM_req
        # create_dm(list_point,DM)
        data['num_vehicles'] = 1

        # if is_start_end==False:
        data['starts'] = [int(in_out[this_i][0])]
        data['ends'] = [int(in_out[this_i][1])]

        # else:
        # size_cluster, 1, in_out[this_i][0], in_out[this_i][1]
        # manager = pywrapcp.RoutingIndexManager(data)
        # print(len(GT_cluster_list[this_i]), data['starts'] , data['ends'])
        manager = pywrapcp.RoutingIndexManager(size_cluster, 1, data['starts'], data['ends'])
        manager = pywrapcp.RoutingIndexManager(len(GT_cluster_list[this_i]), 1, data['starts'], data['ends'])

        # routing = pywrapcp.RoutingModel(manager)
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return DM_req[GT_cluster_list[this_i][from_node]][GT_cluster_list[this_i][to_node]]

        routing = pywrapcp.RoutingModel(manager)

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        dimension_name = 'Distance'
        routing.AddDimension(
            transit_callback_index,
            0,
            3000000,
            True,
            dimension_name)
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        # distance_dimension.SetGlobalSpanCostCoefficient(100)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        # search_parameters.time_limit.seconds  = 1
        # search_parameters.solution_limit = 1
        # search_parameters.log_search = True

        def print_solution_sub(manager, routing, solution):

            """Prints solution on console."""

            # print('Objective: {} miles'.format(solution.ObjectiveValue()))
            index = routing.Start(0)
            # plan_output = 'Route for vehicle 0:\n'
            route_distance = 0
            trip = []
            while not routing.IsEnd(index):
                # plan_output += ' {} ->'.format(manager.IndexToNode(index))
                trip.append(manager.IndexToNode(index))
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
            trip.append(manager.IndexToNode(index))

            # plan_output += ' {}\n'.format(manager.IndexToNode(index))
            # print(plan_output)
            # plan_output += 'Route distance: {}miles\n'.format(route_distance)
            return trip

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            routes = print_solution_sub(manager, routing, solution)
            # routes = get_routes(solution, routing, manager)
            B = [GT_cluster_list[this_i][i] for i in routes]
            return B
        else:
            return []

    def find_giant_tour(self, GT_cluster_list, DM_req, in_out):
        all_trip = []
        for i in range(len(GT_cluster_list)):
            all_trip.append(self.find_route_inside_cluster(GT_cluster_list, DM_req, i, in_out))
        giant_tour = []
        for trip in all_trip:
            if trip[0] != trip[-1]:
                giant_tour += trip
            else:
                giant_tour.append(trip[0])
        return giant_tour

    def create_giant_tour(self):
        DM_req = self.DM_req
        size_of_clusters = self.size_of_clusters
        cluster_result = self.total_clustering(DM_req, size_of_clusters)

        center_point = self.create_center_point(cluster_result, DM_req)

        DM_center = self.create_distance_matrix_center_point(center_point, DM_req)
        DM_center
        GT_between_cluster = \
        self.create_route_of_cluster(self.create_data_model_for_center_points(DM_center, center_point, 0))[0]
        GT_between_cluster = GT_between_cluster[:-1]

        GT_cluster_list = [cluster_result[i] for i in GT_between_cluster]

        plt.show()
        in_out = self.create_in_out(GT_cluster_list, DM_req)
        in_out_original = np.empty((len(GT_between_cluster), 2), np.int_)
        for i in range(len(in_out)):
            in_out_original[i][0] = GT_cluster_list[i][in_out[i][0]]
            in_out_original[i][1] = GT_cluster_list[i][in_out[i][1]]

        # plt.figure(figsize=(8, 6), dpi=80)

        # plt.plot(X,Y,'ro')
        # for i in range(len(X)):
        #     plt.text(X[i],Y[i],str(i))

        giant_tour = self.find_giant_tour(GT_cluster_list, DM_req, in_out)
        giant_tour = _LS(np.array(giant_tour, np.int_), DM_req, 0)
        index_depot = list(giant_tour).index(0)
        giant_tour = np.concatenate([giant_tour[index_depot:], giant_tour[:index_depot]])
        self.giant_tour = np.array(giant_tour, np.int_)
        return giant_tour
