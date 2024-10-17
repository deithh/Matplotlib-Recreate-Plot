import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker, rcParams, rc, colors


def enable_tex():
    #set non-gui backend (problems with tex on default)
    rcParams["backend"] = "ps"

    #enable tex
    rcParams['text.usetex'] = True

def set_font_TNR():
#set font globally to times new roman
    rc('font', family='serif')
    rc('font', serif='Times New Roman')

def read_data():
    #read data from files and returns tuple of dicts with hardcoded plot_parameters
    c = pd.read_csv("1c.csv", sep=",")
    crs = pd.read_csv("1crs.csv", sep=",")
    ers = pd.read_csv("1ers.csv", sep=",")
    c2 = pd.read_csv("2c.csv", sep=",")
    crs2 = pd.read_csv("2crs.csv", sep=",")

    #data with plot parameters
    algs = (
        {'df': c,
        'label': '1-Coev',
        'color': 'r',
        'marker': 'v'
        },
        {'df': c2,
        'label': '2-Coev',
        'color': 'b',
        'marker': 'o'
        },    
        {'df': crs,
        'label': '1-Coev-RS',
        'color': 'g',
        'marker': 's'
        },    
        {'df': crs2,
        'label': "2-Coev-RS",
        'color': 'magenta',
        'marker': 'p'
        },    
        {'df': ers,
        'label': "1-Evol-RS",
        'color': 'black',
        'marker': 'd'
        }
    )

    return algs

#styling functions
def style_line_plot(axes):
    axes.set_xlabel(r"Rozegranych gier $(\times 1000)$")
    axes.set_ylabel(r"Odsetek wygranych gier $[\%]$")
    axes.grid(visible = True, linestyle =(0, (1, 4)))
    axes.set_ylim([60,100])
    axes.set_xlim([0,500*1000])
    axes.xaxis.set_major_formatter(lambda x, pos: int(x/1000))
    axes.xaxis.set_major_locator(ticker.LinearLocator(6))
    axes.tick_params( direction = 'in')
    axes.legend(numpoints = 2)

    leg = axes.get_legend()
    leg.get_frame().set_edgecolor("black")
    leg.get_frame().set_linewidth(.5)

    sec_xaxis = axes.secondary_xaxis('top')
    sec_xaxis.set_xlabel('Pokolenie') 
    sec_xaxis.xaxis.set_major_formatter(lambda x, pos: int(x/2500))
    sec_xaxis.xaxis.set_major_locator(ticker.LinearLocator(6))
    sec_xaxis.tick_params(direction = 'in')
    
def style_box_plot(axes):
    axes.grid(visible = True, linestyle =(0, (1, 4)))
    axes.set_ylim([60,100])
    axes.yaxis.set_major_locator(ticker.MultipleLocator(5))
    axes.tick_params(axis = 'x', labelrotation = 30)
    axes.tick_params( direction = 'in')
    axes.yaxis.tick_right()

#some prop styles
flierprops = dict(marker='+', markerfacecolor='b', markersize=8,
                  linestyle='', markeredgecolor='b', markeredgewidth=.5)

medianprops = dict(linestyle='-', linewidth=2, color='r')

meanpointprops = dict(marker='o', markeredgecolor='black',
                      markerfacecolor='b', zorder = -1)

whiskerprops = dict(linestyle =(0, (5, 5)), color = 'b', linewidth = 1)

capprops = dict(linestyle = '-', color = 'black', linewidth = 1)



def create_plot(algs):
    #conversion to %
    for alg in algs:
        alg['df'].iloc[:, 2:] *= 100

    ## Prepare data for plot
    for alg in algs:
        alg['df']['mean'] = alg['df'].iloc[:, 2:].mean(axis=1)

    ## Prepare data for boxplot
    finish_results = pd.DataFrame()

    for alg in algs:
        finish_results[alg['label']] = alg['df'].iloc[-1, 2:]

    #sort algorithms by mean at finish
    finish_results.sort_values('mean', axis = 1, inplace = True, ascending = False)
    finish_results.drop('mean', inplace = True)


    # plot
    fig, axes= plt.subplots(1, 2)

    for alg in algs:
        marker_rgba = list(colors.to_rgba(alg['color']))
        marker_rgba[-1] = 0.75
        alg['df'].plot(ax = axes[0], x = 'effort', y = 'mean',
                    label = alg['label'], marker = alg['marker'], markevery = 40,
                    markeredgecolor='black', color = alg['color'],
                    markeredgewidth=0.5, linestyle ='-', linewidth = .5, markerfacecolor = marker_rgba)
        


    finish_results.plot(ax = axes[1], kind = "box", notch = True, flierprops = flierprops,
                        color = 'b', showmeans = True, medianprops = medianprops,
                        meanprops = meanpointprops, whiskerprops = whiskerprops, capprops = capprops)

    #apply styles
    style_box_plot(axes[1])
    style_line_plot(axes[0])

    return fig, axes

def save2file(fig, path):
    #save combined plots
    fig.set_size_inches(12, 7)
    fig.savefig(path, dpi = 100)
    

def main():
    enable_tex()
    set_font_TNR()
    algs = read_data()
    fig, _  = create_plot(algs)
    save2file(fig, "./plots.png")

if __name__ == "__main__":
    main()