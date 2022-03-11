from matplotlib import pyplot as plt


class custom:    
    font = {'fontname':'Georgia'}
    colors = {'golden_rod' : '#CC9900','yellow_gold' : '#FFCC00','light_blue' : '#C6D9F0',
        'sky_blue': '#548DD4','navy_blue': '#386295','midnight_blue': '#17365D'}
    def __init__(self,fig):
        self.fig = fig
        self.ax1 = fig.add_subplot()
        #self.ax2 = self.ax1.twinx()
        self.chart_type = None
        self.chart_type2  = None
        self.title = ""
        self.xlabel = ""
        self.ylabel = ""
        self.x = None
        self.y = None
        self.x_ticks = []
        self.y_ticks = []
        self.x_ticklabels = []
        self.y_ticklabels = []
        self.legend = False


    def chart_maker(self,):
        
        font = {'fontname':'Georgia'}
        rect = self.fig.patch
        rect.set_facecolor('#F2F2F2')
        self.ax1.set_facecolor('#F2F2F2')
        self.chart_type
        if self.x_ticks != []:
            self.ax1.set_xticks(self.x_ticks)
            self.ax1.set_xticklabels(self.x_ticklabels)
        if self.y_ticks != []:
            self.ax1.set_yticks(self.y_ticks)
            self.ax1.set_yticklabels(self.y_tick_labels)
        plt.title(self.title,**font,fontsize = 20,weight = 'bold')
        if self.xlabel != "":
            plt.xlabel(self.xlabel,**font,fontsize = 14)
        if self.ylabel != "":
            plt.ylabel(self.ylabel,**font,fontsize = 14)
        if self.legend == True:
            plt.legend(loc = "upper left")
        plt.axvline(x = 0, color = 'black',linestyle = '-', alpha = 0.25)
        plt.axhline(y=0, color='black', linestyle='-',alpha = 0.25)
        self.ax1.grid()
        self.ax1.set_axisbelow(True)
