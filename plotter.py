import matplotlib.pyplot as plt
#
# Class to define text and pattern size along with time and memory.
#
class plotter:
    txt_size =[]
    pat_size = []
    time = []
    memory = []
    def add_txt(self, txt):
        self.txt_size.append(len(txt))
    def add_pattern(self, patt):
        self.pat_size.append(len(patt))
    def add_time(self, time):
        self.time.append(time)
    def add_usage(self, memory):
        self.memory.append(memory)
    def plot_txt_time(self):
        self.plot_graph("Text Size","Time in ms",self.txt_size,self.time,"Text size vs Time ")

    def plot_txt_size(self):
        self.plot_graph("Text Size","Memory Usage MB",self.txt_size,self.memory,"Text Size vs Mem ")

    def plot_pat_time(self):
        self.plot_graph("Patternsize","Time in ms",self.pat_size,self.time,"Pattern size vs time")

    def plot_pat_size(self):
        self.plot_graph("Pattern Size","Memory Usage MB",self.pat_size,self.memory,"Pattern size vs mem usage")

    def plot_graph(self, x_label, y_label, x_value, y_value, title):

        # plotting the points
        plt.plot(x_value, y_value,'bo-',color="black")

        # naming the x axis
        plt.xlabel(x_label)
        # naming the y axis
        plt.ylabel(y_label)

        # giving a title to graph
        plt.title(title)

        # function to show the plot
        plt.show()