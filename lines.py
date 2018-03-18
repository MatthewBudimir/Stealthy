# For calculating intercepts of segments.

def calcSlope(a,b):
    if a[0] == b[0]:
        # print("line is vertical")
        return "vertical"
    m = float((a[1] - b[1]))/(a[0]-b[0])
    # print("slope " + str(m))
    return m
def calcC(a,m):
    if m == "vertical":
        return a[0] #Return the x value of our vertical line.
    c = a[1] - m*a[0]
    # print("y-intercept " +str(c) )
    return c
def calcIntercept(a,b):
    # input is slope and y-intercept for 2 lines.

    # if one of them is a vertical line:
    if a[0] == "vertical" and b[0] !="vertical":
        # print("first line is vertical")
        x = a[1]
        y = b[0]*x + b[1]
        return (x,y)
    elif a[0] != "vertical" and b[0] == "vertical":
        # print("second line is vertical")
        x = b[1]
        y = a[0]*x + a[1]
        return (x,y)

    if a[0] == b[0]:
        return (0,0) # in a game nobody will be in top left side of screen.
    x = float((b[1]-a[1]))/(a[0]-b[0])
    y = a[0]*x + a[1]
    return (x,y)
def withinbounds(a,b,c):
    # is c between a and b
    # x is in bounds                                       and             y is in bounds //of just one of them...
    # return c[0] ==
    return c[0] >= min(a[0],b[0]) and c[0] <= max(a[0],b[0]) and c[1] >= min(a[1],b[1]) and c[1] <= max(a[1],b[1])

def intercept(a,b):
    # calc intercept between segment a and segment b
    aSlp = calcSlope(a[0],a[1])
    aEq = (aSlp,calcC(a[0],aSlp))
    bSlp = calcSlope(b[0],b[1])
    bEq = (bSlp,calcC(b[0],bSlp))
    inter = calcIntercept(aEq,bEq)
    # print("INTERCEPT BETWEEN " + str(a) + " and " + str(b) + " at " +str(inter))
    # print(withinbounds(a[0],a[1],inter) and withinbounds(b[0],b[1],inter))
    return (withinbounds(a[0],a[1],inter) and withinbounds(b[0],b[1],inter)) , inter
# examples
# a = ((0,4),(4,0))
# b = ((2,0),(4,2))
# c = ((3,-2),(6,1))
# d = ((3,2),(0,1))

# a = ((400,300),(1170,150))
# b = ((1100,0),(1100,500))
# intercept(a,b)
