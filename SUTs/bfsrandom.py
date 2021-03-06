import sut
import random
import sys
import time

rgen = random.Random()

#NUM_TESTS = 100

GOAL_DEPTH = 10
BUDGET = 300.0

LAYER_BUDGET = BUDGET/GOAL_DEPTH

print "LAYER BUDGET:",LAYER_BUDGET

slack = 0.0

sut = sut.sut()
sut.silenceCoverage()

sut.restart()

queue = [sut.state()]
visited = []

startAll = time.time()

actCount = 0
elapsed = 0
d = 1
while d <= GOAL_DEPTH:
    print "DEPTH",d,"QUEUE SIZE",len(queue),"VISITED SET",len(visited)
    d += 1
    frontier = []
    startLayer = time.time()
    scount = 0
    for s in queue:
        scount += 1
        sut.backtrack(s)
        allEnabled = sut.enabled()
        rgen.shuffle(allEnabled)
        for a in allEnabled:
            elapsed = time.time() - startLayer
            if elapsed >= LAYER_BUDGET:
                break
            ok = sut.safely(a)
            actCount += 1
            if not ok:
                print "FOUND A FAILURE"
                #sut.prettyPrintTest(sut.test())
                print sut.failure()
                print "REDUCING"
                R = sut.reduce(sut.test(),sut.fails, True, True)
                sut.prettyPrintTest(R)
                print sut.failure()
                #sys.exit(1)
            s2 = sut.state()
            if s2 not in visited:
                visited.append(s2)
                frontier.append(s2)
            sut.backtrack(s)
        if elapsed >= LAYER_BUDGET:
            print "DID NOT GET TO EXPAND",len(queue)-scount,"STATES"
            break
    elapsed = time.time() - startLayer
    slack = float(LAYER_BUDGET-elapsed)
    print "SLACK",slack
    if (d < GOAL_DEPTH) and (slack > 0):
        LAYER_BUDGET = LAYER_BUDGET+slack/(GOAL_DEPTH-d)
        print "NEW LAYER BUDGET",LAYER_BUDGET
    queue = frontier
sut.internalReport()

print "SLACK",slack
print "TOTAL ACTIONS",actCount
print "TOTAL RUNTIME",time.time()-startAll
