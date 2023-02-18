import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import gridspec
from scipy import interpolate
import matplotlib.ticker as mtick
from matplotlib.ticker import PercentFormatter
import os

def calculate_acc(df):

    df['correct_type'] = (df['True_type'] == df['Predicted_type']).astype(int)
    df['correct_zone'] = (df['True_zone'] == df['Predicted_zone']).astype(int)
    df['correct_detection'] = ((df['correct_type'] == 1) & (df['correct_zone'] == 1)).astype(int)

    acc_zone = df.groupby('Time')['correct_zone'].mean()
    acc_type = df.groupby('Time')['correct_type'].mean()
    acc_total = df.groupby('Time')['correct_detection'].mean()

    return [acc_zone, acc_type, acc_total]


def calculate_acc_fishes(df):

    tuna = df.loc[df['True_type'] == 'tuna']
    salmon = df.loc[df['True_type'] == 'salmon']
    clown = df.loc[df['True_type'] == 'clown']

    acc_tuna = tuna.groupby('Time')['correct_detection'].mean()
    acc_salmon = salmon.groupby('Time')['correct_detection'].mean()
    acc_clown = clown.groupby('Time')['correct_detection'].mean()

    return [acc_tuna, acc_salmon, acc_clown]


def interpolate_acc(acc, numbers_interpolation):

    x = np.array(range(len(acc.to_numpy())))
    y = acc.to_numpy()
    tck = interpolate.InterpolatedUnivariateSpline(x, y)
    x_new = np.linspace(0, len(x)-1, num=int((len(x)-1)*numbers_interpolation), endpoint=True)
    y_new = tck(x_new)
    interpolated_values = [x_new, y_new]
    return interpolated_values


def plot_acc_fishes(pattern_names, names, acc, interpolation_acc_fishes):

    colors = sns.color_palette('rocket', 3)

    for i in range(len(pattern_names)):
        print("That is the Pattern:", pattern_names[i])


        if interpolation_acc_fishes:
            ### Plot ###
            fig2 = plt.figure(2, figsize=(10, 5))
            fish = fig2.add_subplot()

            # Plot Data for 100% buoys
            numbers_interpolation = 1 / 10
            t = interpolate_acc(acc[i][0], numbers_interpolation)
            plt.plot(t[0], t[1], label=names[0], color=colors[0], linewidth=1, linestyle='-')
            plt.axhline(y=np.nanmean(t[1]), color=colors[0], linestyle='--', linewidth=1, marker='s', label='Avg ' + names[0])

            s = interpolate_acc(acc[i][1], numbers_interpolation)
            plt.plot(s[0], s[1], label=names[1], color=colors[1], linewidth=1, linestyle='-')
            plt.axhline(y=np.nanmean(s[1]), color=colors[1], linestyle='--', linewidth=1, marker='o', label='Avg ' + names[1])

            c = interpolate_acc(acc[i][2], numbers_interpolation)
            plt.plot(c[0], c[1], label=names[2], color=colors[2], linewidth=1, linestyle='-')
            plt.axhline(y=np.nanmean(c[1]), color=colors[2], linestyle='--', linewidth=1, marker='^', label='Avg ' + names[2])

            # Define Ticks
            xticks = np.arange(0, 3001, 200)
            # yticks = np.arange(0, 1.1, 0.1)

            fish.yaxis.set_major_formatter(mtick.PercentFormatter(1))

            plt.minorticks_on()
            plt.tick_params(direction='in', which='minor', length=5, bottom=True, left=True)
            plt.tick_params(direction='in', which='major', length=10, bottom=True, left=True)

            plt.xticks(xticks)
            # plt.yticks(yticks)

            # Create Legend
            plt.legend()

            # Plot Labels
            plt.ylabel('Total Accuracy [%]')
            plt.xlabel('Simulation Iterations')
            plt.title('Accuracy comparison: Fish type detection (Pattern:' + pattern_names[i] + ")")

        if not interpolation_acc_fishes:

            fish = fig2.add_subplot()

            plt.plot(acc[0][0], label=names[0], color=colors[0], linewidth=1, linestyle='-')
            plt.axhline(y=np.nanmean(acc[0][0]), color=colors[0], linestyle='--', linewidth=1, marker='s', label='Avg '+names[0])
            plt.plot(acc[0][1], label=names[1], color=colors[1], linewidth=1, linestyle='-')
            plt.axhline(y=np.nanmean(acc[0][1]), color=colors[1], linestyle='--', linewidth=1, marker='o', label='Avg '+names[1])
            plt.plot(acc[0][2], label=names[2], color=colors[2], linewidth=1, linestyle='-')
            plt.axhline(y=np.nanmean(acc[0][2]), color=colors[2], linestyle='--', linewidth=1, marker='^', label='Avg '+names[2])

            # Define Ticks
            xticks = np.arange(0, 3001, 200)
            # yticks = np.arange(0, 1.1, 0.1)

            fish.yaxis.set_major_formatter(mtick.PercentFormatter(1))

            plt.minorticks_on()
            plt.tick_params(direction='in', which='minor', length=5, bottom=True, left=True)
            plt.tick_params(direction='in', which='major', length=10, bottom=True, left=True)

            plt.xticks(xticks)
            # plt.yticks(yticks)

            # Create Legend
            plt.legend()

            # Plot Labels
            plt.ylabel('Total Accuracy [%]')
            plt.title('Accuracy comparison: Fish type detection')

        my_path = os.path.dirname(__file__)
        fig2.savefig(my_path + '/figures/Accuracy_per_Fish_'+pattern_names[i]+'.svg', dpi=300)
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()

def plot_acc(names, acc, interpolation):

    colors = sns.color_palette('rocket', 3)

    fig = plt.figure(1, figsize=(10, 10))
    gs = gridspec.GridSpec(2, 1)
    gs.update(wspace=0.2, hspace=0.25)

    if interpolation:
        numbers_interpolation = 1 / 10

        ### First Panel ###
        maxB = fig.add_subplot(gs[0:1, 0:1])

        # Plot Data for 100% buoys

        numbers_interpolation = 1 / 10
        circle_100 = interpolate_acc(acc[0][2], numbers_interpolation)
        plt.plot(circle_100[0], circle_100[1], label=names[0], color=colors[0], linewidth=1, linestyle='-')
        plt.axhline(y=np.nanmean(acc[0][2]), color=colors[0], linestyle='--', linewidth=1, label='Avg '+names[0])

        cross_100 = interpolate_acc(acc[1][2], numbers_interpolation)
        plt.plot(cross_100[0], cross_100[1], label=names[1], color=colors[1], linewidth=1, linestyle='-')
        plt.axhline(y=np.nanmean(acc[1][2]), color=colors[1], linestyle='--', linewidth=1, label='Avg '+names[1])

        jail_100 = interpolate_acc(acc[2][2], numbers_interpolation)
        plt.plot(jail_100[0], jail_100[1], label=names[2], color=colors[2], linewidth=1, linestyle='-')
        plt.axhline(y=np.nanmean(acc[2][2]), color=colors[2], linestyle='--', linewidth=1, label='Avg '+names[2])

        # Define Ticks
        xticks = np.arange(0, 3001, 200)
        # yticks = np.arange(0, 1.1, 0.1)

        maxB.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        plt.minorticks_on()
        plt.tick_params(direction='in', which='minor', length=5, bottom=True, left=True)
        plt.tick_params(direction='in', which='major', length=10, bottom=True, left=True)

        plt.xticks(xticks)
        # plt.yticks(yticks)

        # Create Legend
        plt.legend()

        # Plot Labels
        plt.ylabel('Total Accuracy [%]')
        plt.title('Accuracy comparison: Maximum numbers of Buoys in each pattern (100%)')

        ### Second Panel ###
        minB = fig.add_subplot(gs[1:2, 0:1])

        # Plot Data for 70% buoys
        circle_70 = interpolate_acc(acc[3][2], numbers_interpolation)
        plt.plot(circle_70[0], circle_70[1], label=names[3], color=colors[0], linewidth=1, linestyle='-')
        plt.axhline(y=np.nanmean(acc[3][2]), color=colors[0], linestyle='--', linewidth=1, label='Avg '+names[3])

        cross_70 = interpolate_acc(acc[4][2], numbers_interpolation)
        plt.plot(cross_70[0], cross_70[1], label=names[4], color=colors[1], linewidth=1, linestyle='-')
        plt.axhline(y=np.nanmean(acc[4][2]), color=colors[1], linestyle='--', linewidth=1, label='Avg '+names[4])

        jail_70 = interpolate_acc(acc[5][2], numbers_interpolation)
        plt.plot(jail_70[0], jail_70[1], label=names[5], color=colors[2], linewidth=1, linestyle='-')
        plt.axhline(y=np.nanmean(acc[5][2]), color=colors[2], linestyle='--', linewidth=1, label='Avg '+names[5])

        # Define Ticks
        # xticks = np.arange(0, 3001, 200)
        # yticks = np.arange(0, 1.1, 0.1)

        plt.minorticks_on()
        plt.tick_params(direction='in', which='minor', length=5, bottom=True, left=True)
        plt.tick_params(direction='in', which='major', length=10, bottom=True, left=True)

        plt.xticks(xticks)
        # plt.yticks(yticks)
        minB.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        # Create Legend
        plt.legend()

        # Plot Labels
        plt.ylabel('Total Accuracy [%]')
        plt.xlabel('Simulation Iterations')
        plt.title('Accuracy comparison: Reduced numbers of Buoys in each pattern (70%)')
        plt.show()

    if not interpolation:

        ### First Panel ###
        maxB = fig.add_subplot(gs[0:1, 0:1])

        # Plot Data for 100% buoys
        plt.plot(acc[0][0], label=names[0], color=colors[0], linewidth=1, linestyle='-')
        plt.axhline(y=np.nanmean(acc[0][0]), color=colors[0], linestyle='--', linewidth=1, label='Avg '+names[0])
        plt.plot(acc[1][0], label=names[1], color=colors[1], linewidth=1, linestyle='-')
        plt.axhline(y=np.nanmean(acc[1][0]), color=colors[1], linestyle='--', linewidth=1, label='Avg '+names[1])
        plt.plot(acc[2][0], label=names[2], color=colors[2], linewidth=1, linestyle='-')
        plt.axhline(y=np.nanmean(acc[2][0]), color=colors[2], linestyle='--', linewidth=1, label='Avg '+names[2])

        # Define Ticks
        xticks = np.arange(0, 3001, 200)
        yticks = np.arange(0, 1.1, 0.1)

        plt.minorticks_on()
        plt.tick_params(direction='in', which='minor', length=5, bottom=True, left=True)
        plt.tick_params(direction='in', which='major', length=10, bottom=True, left=True)

        plt.xticks(xticks)
        maxB.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        # Create Legend
        plt.legend()

        # Plot Labels
        plt.ylabel('Total Accuracy [%]')
        plt.title('Accuracy comparison: Maximum numbers of Buoys in each pattern (100%)')

        ### Second Panel ###
        minB = fig.add_subplot(gs[1:2, 0:1])

        # Plot Data for 100% buoys
        plt.plot(acc[3][0], label=names[3], color=colors[0], linewidth=1, linestyle='-')
        plt.axhline(y=np.nanmean(acc[3][0]), color=colors[0], linestyle='--', linewidth=1, label='Avg '+names[3])
        plt.plot(acc[4][0], label=names[4], color=colors[1], linewidth=1, linestyle='-')
        plt.axhline(y=np.nanmean(acc[4][0]), color=colors[1], linestyle='--', linewidth=1, label='Avg '+names[4])
        plt.plot(acc[5][0], label=names[5], color=colors[2], linewidth=1, linestyle='-')
        plt.axhline(y=np.nanmean(acc[5][0]), color=colors[2], linestyle='--', linewidth=1, label='Avg '+names[5])

        # Define Ticks
        # xticks = np.arange(0, 3001, 200)
        # yticks = np.arange(0, 1.1, 0.1)

        plt.minorticks_on()
        plt.tick_params(direction='in', which='minor', length=5, bottom=True, left=True)
        plt.tick_params(direction='in', which='major', length=10, bottom=True, left=True)

        plt.xticks(xticks)
        minB.yaxis.set_major_formatter(mtick.PercentFormatter(1))

        # Create Legend
        plt.legend()

        # Plot Labels
        plt.ylabel('Total Accuracy [%]')
        plt.title('Accuracy comparison: Maximum numbers of Buoys in each pattern (70%')
        plt.show()

    my_path = os.path.dirname(__file__)
    fig.savefig(my_path + '/figures/Total_Accuracy_Graphs.svg', dpi=300)
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()


def analysis(interpolation_acc, interpolation_acc_fishes):

    ### Read csv files ###

    pattern = {
        'Circle_100': pd.read_csv('Pattern1_100%_statistics.csv', index_col=0),
        'Cross_100': pd.read_csv('Pattern2_100%_statistics.csv', index_col=0),
        'Jail_100': pd.read_csv('Pattern3_100%_statistics.csv', index_col=0),
        'Circle_70': pd.read_csv('Pattern1_70%_statistics.csv', index_col=0),
        'Cross_70': pd.read_csv('Pattern2_70%_statistics.csv', index_col=0),
        'Jail_70': pd.read_csv('Pattern3_70%_statistics.csv', index_col=0)
    }

    ### Set lists with calculations ###
    pattern_names = []
    acc_pattern = []
    acc_fish = []

    for index, (name, pattern) in enumerate(pattern.items()):
        df = pattern
        pattern_names.append(name)
        acc_pattern.append(calculate_acc(df))
        acc_fish.append(calculate_acc_fishes(df))

    ### Plot Graphs ###

    plot_acc(pattern_names, acc_pattern, interpolation_acc_fishes)
    plot_acc_fishes(pattern_names, ['Tuna', 'Salmon', 'Clown'], acc_fish, interpolation_acc)


analysis(interpolation_acc=True, interpolation_acc_fishes=True)








