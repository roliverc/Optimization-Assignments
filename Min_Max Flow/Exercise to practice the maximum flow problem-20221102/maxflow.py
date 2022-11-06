
from pyomo.environ import *

model = AbstractModel()

## Nodes in the network
model.N = Set() # there are 5 (0,1,2,3,4)
## Network arcs
model.A = Set(within = model.N*model.N)  # there are 9 
    # Set this limit since we cannot have more than one arc between two nodes (at most one arc from node i to node j) (there are no loops)
    # It defines expected properties

## Source node
model.source = Param(within = model.N) # it is node 0 (according to the statement)
## Sink node 
model.sink = Param(within = model.N) # it is node 4 (according to the statement)
## Flow capacity limits
model.capacity = Param(model.A) # we cannot exceed these flow capacity limits

#############################
# 'Define decision variables'
#############################
# The flow over each arc
# Number of decision variables = number of arcs. In our case, we have 9 arcs. This means that we have 9 decision variables (x01,x02,x03,x12,x14,x23,x24,x32,x34)
# model.A contains all arcs in an ordered way
model.flow = Var(model.A, within=NonNegativeReals) 

#############################
#  'Objective'
#############################
# Maximize the flow into the sink node
def obj(model):
    return sum(model.flow[i,j] for (i,j) in model.A if j == value(model.sink))

#############################
# 'Constraints'
#############################

def upper_limit(model, i, j):
    return model.flow[i,j] <= model.capacity[i,j]

def total_flow_rule(model, k):
    # we define a list with both the inflow and the outflow
    flows = [
        sum(model.flow[i,j] for (i,j) in model.A if j == k), # inflow
        sum(model.flow[i,j] for (i,j) in model.A if i == k), # outflow
        ]

    # we define a list with the boolean values between k (model.N)
    # and the value of both the source and the sink
    checks = [k == value(model.source), k == value(model.sink)]

    # we check if one of them is false
    if any(checks):
        return Constraint.Skip

    # we return the Boolean value comparing
    # the result of the inflow and outflow summations
    return (flows[0] == flows[1])

########## ADDING TO THE MODEL #################

# Add the objective function to the model
model.objective = Objective(rule=obj, sense=maximize)

# Add the constraints to the model
model.upper_limit = Constraint(model.A, rule=upper_limit)
model.total_flow = Constraint(model.N, rule=total_flow_rule)
