        G = nx.DiGraph()
        actDict = {}
        labels = {}
        maxIndex = gameState.getNumAgents()-1
        def value(state,index,count):
#             ss = str(state)
#             ss = ss.replace(" ", "   ")
#             ss = ss.replace(".", " . ")
#             ss = " "+ss
#             G.add_node(ss)
            if count >= self.depth or state.isWin() or state.isLose():
#                 ts = str(state)
#                 ts = ts.replace(" ", "   ")
#                 ts = ts.replace(".", " . ")
#                 ts = " "+ts
#                 print "termState",state
                return scoreEvaluationFunction(state),0
            if index > maxIndex:
                index = 0
            if index != 0:
                return min_value(state,index,count)
            elif index == 0:
                return max_value(state,index,count)    
        
        def max_value(state,index,count):
            v = float("-inf")
#             print state
            actDict = {}
            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
#                 ps = str(successor)                      
#                 ps = ps.replace(" ", "   ")
#                 ps = ps.replace(".", " . ")
#                 s = str(state)                      
#                 s = s.replace(" ", "   ")
#                 s = s.replace(".", " . ")
#                 ps = " "+ps
#                 s = " "+s
#                 G.add_edge(s, ps)
#                 labels[(s,ps)]=action
#                 nx.write_dot(G,'test.dot')
#                 pos=nx.graphviz_layout(G,prog='dot')
#                 nx.draw(G,pos)
#                 nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)#,pos,with_labels=1,arrows=True)
#                 plt.show()
                pSuccValue,temp = value(successor,index+1,count)#[0]
#                 print "v:",v," -action:",action
                v = max(v,pSuccValue)
                actDict[v] = action
            return v,actDict[v]
                
        def min_value(state,index,count):
            v = float("inf")
            if index != 0:
                if index >= maxIndex:
                    count += 1
                for action in state.getLegalActions(index):
                    successor = state.generateSuccessor(index, action)
#                     ps = str(successor)                      
#                     ps = ps.replace(" ", "   ")
#                     ps = ps.replace(".", " . ")
#                     s = str(state)                      
#                     s = s.replace(" ", "   ")
#                     s = s.replace(".", " . ")
#                     ps = " "+ps
#                     s = " "+s
#                     G.add_edge(s, ps)
#                     labels[(s,ps)]=action
#                     nx.write_dot(G,'test.dot')
#                     pos=nx.graphviz_layout(G,prog='dot')
#                     nx.draw(G,pos)
#                     nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
#                     plt.show()
                    z = value(successor,index+1,count)#[0]
#                     print z
                    gSuccValue,temp = z
                    v = min(v,gSuccValue)
                    
                return v,0
#         plt.show()
        action = value(gameState, 0, 0)
        print action
        return action[1]
