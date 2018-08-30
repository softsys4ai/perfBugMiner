import numpy as np
import math
def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))
def sigmoid_prime(z):
    return sigmoid(z)*(1-sigmoid(z))
def tanh(z):
    return np.tanh(z)
def tanh_prime(z):
    return 1.0-np.tanh(z)*np.tanh(z)


class Network(object):
    def __init__(self,sizes):
        self.sizes=sizes
        self.num_layers=len(sizes)
        self.biases = [np.random.randn(y) for y in sizes[1:]]
        self.weights = [np.random.randn(x,y) for y,x in zip(sizes[:-1],sizes[1:])]
        
    def cost_derivative(self,output_activations,y):
        return (output_activations-y)
    def predict(self,a):
        for b,w in zip(self.biases,self.weights):
            a = sigmoid(np.dot(w,a)+b)
        return a
    
    def put(self):
        print 'biases\n',self.biases
        print 'weights:\n',self.weights
    
    def fit(self,X,y,eta=0.03,epochs=10000):
        X = np.atleast_2d(X)
        y = np.atleast_2d(y)
        if X.shape[0] == y.shape[1]:
            y=y.T
        for k in range(epochs):
            nabla_b = [np.zeros(b.shape) for b in self.biases]
            nabla_w = [np.zeros(w.shape) for w in self.weights]
            i = np.random.randint(X.shape[0])
            out = y[i]
            activations = [X[i]]
            activation =X[i]
            zs = []
            for b,w in zip(self.biases,self.weights):
                z=np.dot(w,activation)+b
                zs.append(z)
                activation = sigmoid(z)
                activations.append(activation)
            delta = self.cost_derivative(activations[-1], out)*\
                    sigmoid_prime(zs[-1])
            nabla_b[-1]=delta
            nabla_w[-1]=np.dot(np.atleast_2d(delta).T,np.atleast_2d(activations[-2]))
            for l in xrange(2,self.num_layers):
                z=zs[-l]
                sp=sigmoid_prime(z)
                activation = activations[-l-1]
#                 print self.weights[-l+1].T
#                 print self.weights[-l+1],exit()
                delta = np.dot(self.weights[-l+1].T,delta).T
                nabla_b[-l]=delta
                nabla_w[-l] = np.dot(np.atleast_2d(delta).T,np.atleast_2d(activations[-l-1]))
            self.weights = [w-(eta)*nw
                            for w,nw in zip(self.weights,nabla_w)]
            self.biases = [b-(eta)*nb
                           for b, nb in zip(self.biases, nabla_b)]
    



# train_x = np.load('train_X.bin.npy')
# # train_x.reshape([120,1,51])
# y = np.load('Y.bin.npy')
# # y.reshape([120,1,50])


# a = Network([51,40,30,35,50])
# # a.put()
# a.fit(train_x,y)
# res = a.predict(train_x[10])
# print res.tolist().index(max(res.tolist()))
# print y[10].tolist().index(max(y[10].tolist()))
