import torch as tr
import numpy as np
import matplotlib.pyplot as plt

class ConvNet(tr.nn.Module):
    def __init__(self, size, hid_features):
        super(ConvNet, self).__init__()
        self.to_hidden = tr.nn.Conv2d(3, hid_features, 2)
        self.to_output = tr.nn.Linear(hid_features*(size-1)**2, 1)
    def forward(self, x):
        h = tr.relu(self.to_hidden(x))
        y = tr.tanh(self.to_output(h.reshape(x.shape[0],-1)))
        return y

def encode(state):
    symbols = np.array([0,1,2]).reshape(-1,1,1)
    onehot = (symbols == state).astype(np.float32)
    return tr.tensor(onehot)

def example_error(net, example):
    state, utility = example
    x = encode(state).unsqueeze(0)
    y = net(x)
    e = (y - utility)**2
    return e

def batch_error(net, batch):
    states, utilities = batch
    u = utilities.reshape(-1,1).float()
    y = net(states)
    e = tr.sum((y - u)**2) / utilities.shape[0]
    return e

def train_model(training_examples,testing_examples):
    utilities = [u[1] for u in testing_examples]
    baseline_error =sum((u-0)**2 for u in utilities) / len(utilities)
    batched = True
    net = ConvNet(size=5, hid_features=16)
    optimizer = tr.optim.Adam(net.parameters(), lr=0.001)
    states = [u[0] for u in training_examples]
    utilities = [u[1] for u in training_examples]
    training_batch = tr.stack(tuple(map(encode, states))), tr.tensor(utilities)
    states = [u[0] for u in testing_examples]
    utilities = [u[1] for u in testing_examples]
    testing_batch = tr.stack(tuple(map(encode, states))), tr.tensor(utilities)
    curves = [], []
    for epoch in range(5000):
        optimizer.zero_grad()
        if not batched:
            training_error, testing_error = 0, 0
            for n, example in enumerate(zip(*training_examples)):
                e = example_error(net, example)
                e.backward()
                training_error += e.item()
            training_error /= len(training_examples)

            with tr.no_grad(): # less computationally expensive
                for n, example in enumerate(zip(*testing_examples)):
                    e = example_error(net, example)
                    testing_error += e.item()
                testing_error /= len(testing_examples)

        if batched:
            e = batch_error(net, training_batch)
            e.backward()
            training_error = e.item()

            with tr.no_grad():
                e = batch_error(net, testing_batch)
                testing_error = e.item()

        optimizer.step()    
        
        # print/save training progress
        if epoch % 1000 == 0:
            print("%d: %f, %f" % (epoch, training_error, testing_error))
        curves[0].append(training_error)
        curves[1].append(testing_error)
    
    plt.style.use("ggplot")
    plt.plot(curves[0], 'b-')
    plt.plot(curves[1], 'r-')
    plt.plot([0, len(curves[1])], [baseline_error, baseline_error], 'g-')
    plt.plot()
    plt.legend(["Train","Test","Baseline"])
    plt.show()

    return net
