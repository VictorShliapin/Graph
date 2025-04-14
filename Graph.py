import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import random
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Cursor
from matplotlib.ticker import NullFormatter, FormatStrFormatter, FuncFormatter, ScalarFormatter, FixedFormatter
import math

# Settings
A = 6  # Want figures to be A6
plt.rc('figure', figsize=[46.82 * .5**(.5 * A), 33.11 * .5**(.5 * A)])
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('text.latex', preamble=r'\usepackage[russian]{babel}')

# Настройка графика:
Str_x_name = r"$x$"  # r"$\frac{1-cos(\theta)}{2\cdot \pi}$" r"$\frac{1}{U}$"
Str_x_dimension =  r"мм" # "м$^3$/кг$^2$" # почему-то \text{..} не работает, поэтому русские буквы r"1/кВ"
Str_y_name = r"$U$" # r"$\frac{1}{N(\theta)}$" # в кубе и т.д. пишем вне $..$ пример "м$^3$/кг$^2$"
Str_y_dimension = r"В"
Conditions_array = [r"$I$ = 0.92 A", r"$U$накала = 2.987 B", r"$\theta = 2950^\circ$",r"$\theta = 2300^\circ$", r"$\theta = 2370^\circ$", r"$\theta = 2440^\circ$", r"$\theta = 2510^\circ$", r"$\theta = 2580^\circ$", r"$\theta = 2650^\circ$"] # писать от последнего
Number_of_dependencies_on_the_figure = 1 # max 13
Str_x_name_size = "xx-large"
Str_y_name_size = "xx-large"
Graph_name_size = "xx-large"

# True - значить включить в график, False - нет
Error_bool_x = False #( добавть указание относительной погрешности, нпример 10% для всех точек)
Error_bool_y = False
Relative_error = -9 # если меньше нуля, то н/о самому указать абс. погрешность, если больше то это погр. для всех в %
Show_legend = True
Legend_size = 12 # если размер меньше нуля - то размер выберется автоматически
Show_conditions = False
Experiment_danie_pri = False
Make_own_graph_for_each_dependency = False # Если нужен общий график нескольких зависимостей, один график, то тут False, Number_of_dependencies_on_the_figure > 1
Include_general_graph_in_the_figure = False # Если график 1 с одной зависимостью тот тут False
Ad_partial_approximation = False
Approximation_by_the_least_squares_method_any_Linear_regression = False # нужно написать вручную в массив Functions все эти ф-ии
Approximation_by_the_least_squares_method_any_NON_Linear_regression = True
Approximation_by_the_least_squares_method_linear = False
Approximation_by_the_least_squares_method_origin_of_the_coordinates = False
Approximation_by_the_least_squares_method_polynomial = False
Approximation_by_a_polynomial = False
Degree_of_the_polynomial = 2

def partial_approximation(x, a, b, c):
    return a*x**2 + b*x + c

if (Make_own_graph_for_each_dependency == True) and (Number_of_dependencies_on_the_figure >= 2):
    Graph_name = "Графики зависимости " + Str_y_name + " от " + Str_x_name
else:
    Graph_name = "График зависимости " + Str_y_name + " от " + Str_x_name

if Number_of_dependencies_on_the_figure == 1:
    Make_own_graph_for_each_dependency = True

String_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
String_alphabet_small = "abcdefghijklmnopqrstuvwxyz"
String_of_markers = "sov><^*DdHxps"
Array_of_linestyle = ["-", "--", "-.", ":", "-", "--", "-.", ":", "-", "--", "-.", ":", "-"]

sf = ScalarFormatter()
sf.set_powerlimits((-3, 3)) # все что в промежутке от 10^(-3) до 10^3 остается как есть, меньше или больше красиво выноситься

MIN_from_matplotlib_x, MIN_from_matplotlib_y = float('inf'), float('inf')
MAX_from_matplotlib_x, MAX_from_matplotlib_y = float('-inf'), float('-inf')
MAXMIN_array = [MAX_from_matplotlib_x, MAX_from_matplotlib_y, MIN_from_matplotlib_x, MIN_from_matplotlib_y]

# Create some figure and axis # Plot
if Make_own_graph_for_each_dependency == True:
    Number_of_rows = \
        int(Number_of_dependencies_on_the_figure/2 if Number_of_dependencies_on_the_figure % 2 == 0 else (Number_of_dependencies_on_the_figure+1)/2)
    Number_of_columns = 2
    if Include_general_graph_in_the_figure == True:
        Number_of_rows = int(Number_of_rows + 1)
else:
    Number_of_rows = 1
    Number_of_columns = 1

# figure, axis = plt.subplots(Number_of_rows, Number_of_columns) # return figure and list of axis, указываем кол-во строк и столбцов
# figure.set_size_inches(7, 5) #размер 7 на 5 дюйма
if (Number_of_dependencies_on_the_figure == 1) or (Make_own_graph_for_each_dependency == False):
    figure = plt.figure(figsize=(8, 5.7))
else:
    figure = plt.figure(figsize=(10.5, 9*Number_of_rows/2.3))

gs = GridSpec(ncols=Number_of_columns, nrows=Number_of_rows, figure=figure, wspace=0.24, hspace=0.33) #последнее -
# figure.set_facecolor('#eee') #цвет фона - светло серый                     #-  Увеличиваем пространство между подграфиками

def create_cool_graph(i, j, k, maxmin_array, ax=None):
    # коррекция осей
    print(k)
    build_a_general_graph_on_the_last_line = False
    if ax is None:
        if (Include_general_graph_in_the_figure == True) and (i+1 == Number_of_rows) and (j == 0):
            build_a_general_graph_on_the_last_line = True
        if (Number_of_dependencies_on_the_figure % 2 == 0) and (build_a_general_graph_on_the_last_line == False):
            axis = figure.add_subplot(gs[i, j])
        if (Number_of_dependencies_on_the_figure % 2 != 0) and (k+1 != Number_of_dependencies_on_the_figure) \
                and (build_a_general_graph_on_the_last_line == False):
            axis = figure.add_subplot(gs[i, j])
        if ((Number_of_dependencies_on_the_figure % 2 != 0) and (k+1 == Number_of_dependencies_on_the_figure)) \
                or (build_a_general_graph_on_the_last_line == True):
            axis = figure.add_subplot(gs[i, 0:2])
    else:
        axis = ax

    # grid and ticks
    axis.minorticks_on()
    plt.tick_params(axis='both', which='major', direction='in', length=6, width=0.5, color='#808080', pad=5,
                    labelsize=13)
    plt.tick_params(axis='both', which='minor', direction='in', length=4, width=0.5, color='#808080', pad=5,
                    labelsize=13)
    # axis.grid(which='major', lw=2)
    # axis.grid(which='minor')
    axis.grid(visible=True, which='major', axis='both', color='#bfbfbf', linestyle='-', linewidth=0.5)

    axis.yaxis.set_major_formatter(sf)
    axis.xaxis.set_major_formatter(sf)

    # подпись осей
    if Str_x_dimension != "":
        axis.set_xlabel(Str_x_name + ", " + Str_x_dimension, fontsize=Str_x_name_size)
    else:
        axis.set_xlabel(Str_x_name, fontsize=Str_x_name_size)

    if Str_y_dimension != "":
        axis.set_ylabel(Str_y_name + ", " + Str_y_dimension, fontsize=Str_y_name_size)#axis.set_ylabel(Str_y_name[:-1] + ", $" + Str_y_dimension, fontsize=Str_y_name_size)
    else:
        axis.set_ylabel(Str_y_name, fontsize=Str_y_name_size)

    if build_a_general_graph_on_the_last_line == True:
        axis.set_xlim(maxmin_array[2], maxmin_array[0])
        axis.set_ylim(maxmin_array[3], maxmin_array[1])


    # Загружаем данные из определенного листа excel и погрешности

    df_x = pd.read_excel('Lab_works.xlsx', sheet_name='xy', index_col=None,
                         na_values=['NA'], usecols=String_alphabet[2*k])
    df_y = pd.read_excel('Lab_works.xlsx', sheet_name='xy', index_col=None,
                         na_values=['NA'], usecols=String_alphabet[2*k+1])

    df_x_error = pd.read_excel('Lab_works.xlsx', sheet_name='xy_errors', index_col=None,
                               na_values=['NA'], usecols=String_alphabet[2*k])
    df_y_error = pd.read_excel('Lab_works.xlsx', sheet_name='xy_errors', index_col=None,
                               na_values=['NA'], usecols=String_alphabet[2*k+1])

    # Теперь есть DataFrame df, содержащий данные из 'xy'
    # Create some data
    x_data = df_x.values
    y_data = df_y.values
    x_error_data = df_x_error.values
    y_error_data = df_y_error.values

    x_0 = []
    y_0 = []
    x_error_0 = []
    y_error_0 = []

    for item in x_data:
        if item[0] == item[0]: # проверка на то что элемент массива не nan.
            x_0.append(item[0]) # NaN не равен сам себе, поэтому этот способ работает.
    for item in y_data:
        if item[0] == item[0]:
            y_0.append(item[0])
    for item in x_error_data:
        if item[0] == item[0]:
            x_error_0.append(item[0])
    for item in y_error_data:
        if item[0] == item[0]:
            y_error_0.append(item[0])

    x_data = np.array(x_0)
    y_data = np.array(y_0)
    x_error = np.array(x_error_0)
    y_error = np.array(y_error_0)
    MAX = np.max(x_data)
    MIN = np.min(x_data)
    color_a = random.random()
    color_b = random.random()
    color_c = random.random()
    if k == 0:
        color_a, color_b, color_c = 0, 0, 0

    #x = np.array([1, 2, 3, 4, 5, 6])
    #y = np.array([209.0167457, 255.9921874, 280.4253911, 280.4253911, 233.687826, 228.9663731])

    #x_error = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    #y_error = np.array([0.225418644, 1.533072913, 1.6843913, 1.5791884, 3.3687826, 2.62079663, 1.6843913, 1.5791884, 2.3687826, 2.62079663])
    # y_error_plus = np.array([0.5, 0.5, 1.2])
    # y_error_minus = np.array([0.2, 0.9, 1.7])
    # y_error = [y_error_minus, y_error_plus]

    # bax = brokenaxes(ylims=((y_starting, y_break_point_1), (y_break_point_2, y_ending)), hspace=0.25)
    # axis.set(xlim=(0, 45), ylim=(0, 9))
    # axis.set_xlim(xmin=0, xmax=45)
    # axis.set_ylim(ymin=0, ymax=9)

    # approximation
    if Approximation_by_the_least_squares_method_any_NON_Linear_regression == True and k==0:
        # Определение функции которую будем фитить
        def func(x, a, b, c, d):
            return c*np.exp(-(x-a)**2/b) + d

        # Подгонка модели
        popt, pcov = curve_fit(func, x_data, y_data, maxfev=1000000, p0=[14.21, 0.2, 1, 0])#, p0=[14.21, 0.2, 1, 0]

        # Веса w. Погрешности весов
        w = popt #[5.43, 4.122, 0.19, 7.83, 17.82, 301.7, -0.63]#popt
        # w = [-0.051, ]
        print(w)
        w_err = np.sqrt(np.diag(pcov))#np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])#np.sqrt(np.diag(pcov))
        str_func = r"$c \cdot e^{\frac{-(x-a)^2}{b}} + d$"#r"$c\cdot e^{-\frac{(x-a)^2}{2b^2}} + d$"
        str_non_linear_regression = "Апроксимация функцией \n" # "Апроксимация МНК"
        print('**Approximation_by_the_least_squares_method_any_NON_Linear_regression:(№ =', k + 1, ") ********")
        for l in range(len(w)):
            print(String_alphabet_small[l], " = ", w[l])
            print("sigma_", String_alphabet_small[l], " = ", w_err[l])

        x_non_linear = np.linspace(MIN, MAX, max(int(MAX - MIN), 1) * 100)
        # ax2 = axis.twiny()
        # ax2.plot(x_data*279.88557002, y_data, linestyle="")
        # ax2.set_xlabel(r"$p,$ кэВ", fontsize=16)
        if k == 0:
            axis.plot(x_non_linear, func(x_non_linear, *w), 'r', lw=0.5, label=str_non_linear_regression + str_func,
                      linestyle=Array_of_linestyle[k])
        else:
            axis.plot(x_non_linear, func(x_non_linear, *w), lw=0.5, label=str_non_linear_regression,
                      color=(1 - color_a, 1 - color_b, 1 - color_c), linestyle=Array_of_linestyle[k])


    if Approximation_by_the_least_squares_method_any_Linear_regression == True:
        Y = y_data.T
        x_copy = x_data.copy().reshape(-1, 1)

        def f_polinomial_0(x):
            return x**0
        def f_polinomial_1(x):     #_______________________Функции numpy_____________________
            return x               # `np.sin`, `np.cos`, `np.tan`, `np.arcsin`, `np.arccos`
        def f_polinomial_2(x):     # `np.arctan`, `np.deg2rad`, `np.rad2deg`
            return x**2            # `np.exp`, `np.log`, `np.log10`, `np.log2`, `np.expm1`, `np.log1p`
        def f_polinomial_3(x):     # `np.sinh`, `np.cosh`, `np.tanh`, `np.arcsinh`, `np.arccosh`, `np.arctanh`
            return x**3            # math.exp(1)
        def f_polinomial_4(x):     #
            return x**4            #
        def f_polinomial_5(x):     #
            return x**5            #
        def f_any(x):
            return x**2 + x**3

        Functions = np.array([f_polinomial_4])
        Number_of_functions_for_linear_regression_approximation = len(Functions)

        def create_X(x, m):
            X = Functions[0](x)
            for i in range(1, m):
                x.reshape(X.shape[0], 1)
                X = np.concatenate([X, Functions[i](x)], axis=1)
            return X

        X = create_X(x_copy, Number_of_functions_for_linear_regression_approximation)
        w = np.linalg.pinv(X) @ Y

        str_any = "Пиши сам!"
        str_linear_regression = "Апроксимация МНК функцией\n$f(x) = "
        print('**Approximation_by_the_least_squares_method_any_Linear_regression:(№ =', k + 1, ") ********")
        print("f(x) = ", end='')
        for l in range(Number_of_functions_for_linear_regression_approximation):
            str_linear_regression += String_alphabet_small[k] + "_{" + str(l) + r"}\cdot "
            print(String_alphabet_small[k] + "_" + str(l), end='')
            if Functions[l] == f_polinomial_0:
                str_linear_regression += "1"
                print(" * 1", end='')
            if Functions[l] == f_polinomial_1:
                str_linear_regression += "x"
                print(" * x", end='')
            if Functions[l] == f_polinomial_2:
                str_linear_regression += "x^2"
                print(" * x^2", end='')
            if Functions[l] == f_polinomial_3:
                str_linear_regression += "x^3"
                print(" * x^3", end='')
            if Functions[l] == f_polinomial_4:
                str_linear_regression += "x^4"
                print(" * x^4", end='')
            if Functions[l] == f_polinomial_5:
                str_linear_regression += "x^5"
                print(" * x^5", end='')
            if Functions[l] == np.exp:
                str_linear_regression += "e^x"
                print(" * e^x", end='')
            if Functions[l] == np.expm1:
                str_linear_regression += "(e^{x}-1)"
                print(" * (e^x - 1)", end='')
            if Functions[l] == np.cos:
                str_linear_regression += "cos(x)"
                print(" * cos(x)", end='')
            if Functions[l] == np.sin:
                str_linear_regression += "sin(x)"
                print(" * sin(x)", end='')
            if Functions[l] == np.log:
                str_linear_regression += "ln(x)"
                print(" * ln(x)", end='')
            if Functions[l] == f_any:
                str_linear_regression += str_any
                print(" * ", str_any, end='')
            if l != Number_of_functions_for_linear_regression_approximation-1:
                str_linear_regression += "+"
                print(" + ", end='')
            else:
                str_linear_regression += "$"
        print("\n")
        for l in range(Number_of_functions_for_linear_regression_approximation):
            print(String_alphabet_small[k] + "_", l, " = ", w[l])

        def final_aprox(x, w):
            return (create_X(x.copy().reshape(-1, 1), Number_of_functions_for_linear_regression_approximation) @ w).T

        x_any = np.linspace(MIN, MAX, int(MAX - MIN) * 100)
        if k == 0:
            axis.plot(x_any, final_aprox(x_any, w), 'r', lw=0.5, label=str_linear_regression, linestyle=Array_of_linestyle[k])
        else:
            axis.plot(x_any, final_aprox(x_any, w), lw=0.5, label=str_linear_regression,
                      color=(1 - color_a, 1 - color_b, 1 - color_c), linestyle=Array_of_linestyle[k])

    if Approximation_by_the_least_squares_method_polynomial == True:
        Y = y_data.T
        x_copy = x_data.copy().reshape(-1, 1)

        def create_X(x, m):
            X = np.ones(x.shape)
            for i in range(1, m + 1):
                x.reshape(X.shape[0], 1)
                X = np.concatenate([X, x ** i], axis=1)
            return X

        X = create_X(x_copy, Degree_of_the_polynomial)
        w = np.linalg.pinv(X) @ Y

        print('*****Approximation_by_the_least_squares_method_polynomial:(№ =', k + 1, ") **************")
        t = np.polyfit(x_data, y_data, Degree_of_the_polynomial)
        f_approx = np.poly1d(t)
        print(f_approx)
        str_array = ["Апроксимация МНК полиномом степени " + str(Degree_of_the_polynomial) + "\n$f(x) = "]
        for l in range(Degree_of_the_polynomial + 1):
            print(String_alphabet_small[k] + "_", Degree_of_the_polynomial - l, " = ", f_approx[l])
            string_l = String_alphabet_small[k] + "_{" + str(l) + r"}\cdot x^{" + str(
                Degree_of_the_polynomial - l) + "}"
            str_array.append(string_l)
            if l != Degree_of_the_polynomial:
                str_array.append("+")
            else:
                str_array.append("$")

        def sum_of_strings(str_array, n):
            if n == len(str_array) - 1:
                return str_array[n]
            else:
                return str_array[n] + sum_of_strings(str_array, n + 1)

        if (ax is None) or (Number_of_dependencies_on_the_figure == 1):
            str_label_poly = sum_of_strings(str_array, 0)
        else:
            str_label_poly = "Апроксимация МНК полиномом степени " + str(Degree_of_the_polynomial) \
                             + " для " + Conditions_array[k]

        def final_aprox(x, w):
            return (create_X(x.copy().reshape(-1, 1), Degree_of_the_polynomial) @ w).T

        x_any = np.linspace(MIN, MAX, int(MAX - MIN) * 100)
        if k == 0:
            axis.plot(x_any, final_aprox(x_any, w), 'r', lw=0.5, label=str_label_poly, linestyle=Array_of_linestyle[k])
        else:
            axis.plot(x_any, final_aprox(x_any, w), lw=0.5, label=str_label_poly,
                      color=(1 - color_a, 1 - color_b, 1 - color_c), linestyle=Array_of_linestyle[k])

    if Approximation_by_a_polynomial == True:
        t = np.polyfit(x_data, y_data, Degree_of_the_polynomial)
        f_approx = np.poly1d(t)
        print('*****Approximation_by_a_polynomial:(№ =', k+1, ") **********************************************")
        print(f_approx)
        str_array = ["Апроксимация полиномом степени " + str(Degree_of_the_polynomial) + "\n$f(x) = "]
        for l in range(Degree_of_the_polynomial+1):
            print(String_alphabet_small[k] + "_", Degree_of_the_polynomial-l, " = ", f_approx[l])
            string_l = String_alphabet_small[k] + "_{" + str(l) + r"}\cdot x^{" + str(Degree_of_the_polynomial-l) + "}"
            str_array.append(string_l)
            if l != Degree_of_the_polynomial:
                str_array.append("+")
            else:
                str_array.append("$")

        def sum_of_strings(str_array, n):
            if n == len(str_array)-1:
                return str_array[n]
            else:
                return str_array[n] + sum_of_strings(str_array, n+1)

        if (ax is None) or (Number_of_dependencies_on_the_figure == 1):
            str_label_poly = sum_of_strings(str_array, 0)
        else:
            str_label_poly = "Апроксимация полиномом степени " + str(Degree_of_the_polynomial) \
                             + " для " + Conditions_array[k]

        x_poly = np.linspace(MIN, MAX, int(MAX-MIN)*100)
        if k == 0:
            axis.plot(x_poly, f_approx(x_poly), 'r', lw=0.5, label=str_label_poly, linestyle=Array_of_linestyle[k])
        else:
            axis.plot(x_poly, f_approx(x_poly), lw=0.5, label=str_label_poly,
                      color=(1 - color_a, 1 - color_b, 1 - color_c), linestyle=Array_of_linestyle[k])

    if Approximation_by_the_least_squares_method_linear == True:
        a = (np.mean(x_data*y_data) - np.mean(x_data)*np.mean(y_data))/(np.mean(x_data*x_data) - np.mean(x_data)**2)
        b = np.mean(y_data) - a*np.mean(x_data)
        sigma_a = (np.sqrt((np.mean(y_data*y_data) - np.mean(y_data)**2)/(np.mean(x_data*x_data) -
                                                                          np.mean(x_data)**2)-a**2))/np.sqrt(len(x_data))
        sigma_b = sigma_a*np.sqrt((np.mean(x_data*x_data) - np.mean(x_data)**2))
        print('*****Approximation_by_the_least_squares_method:(№ =', k+1, ") **********************************")
        print()
        print('y = a * x + b')
        print('a =', a)
        print('sigma_a =', sigma_a)
        print('b =', b)
        print('sigma_b =', sigma_b)
        if ax is None:
            if Number_of_dependencies_on_the_figure == 1:
                str_label = "Апроксимация МНК функцией" + "\n" + "$f($" + Str_x_name + "$) = a \cdot$(" + Str_x_name + "$) + b$"
            if Number_of_dependencies_on_the_figure > 1:
                str_label = "Апроксимация МНК функцией" + "\n" + "$f($" + Str_x_name + "$) = a_" + str(k + 1) + \
                            "\cdot$(" + Str_x_name + "$) + b_" + str(k + 1) + "$"
        else:
            str_label = "Апроксимация МНК для " + Conditions_array[k]
        x_squar = np.linspace(MIN, MAX, 2)
        if k == 0:
            axis.plot(x_squar, a*x_squar+b, 'r', lw=0.5, label=str_label, linestyle=Array_of_linestyle[k])
        else:
            axis.plot(x_squar, a * x_squar + b, lw=0.5, label=str_label,
                      color=(1 - color_a, 1 - color_b, 1 - color_c), linestyle=Array_of_linestyle[k])

    if Approximation_by_the_least_squares_method_origin_of_the_coordinates == True:
        a = np.mean(x_data*y_data)/np.mean(x_data*x_data)
        sigma_a = (np.sqrt((np.mean(y_data*y_data)/np.mean(x_data*x_data))-a**2))/np.sqrt(len(x_data))
        print('*****Approximation_by_the_least_squares_method_origin_of_the_coordinates::(№ =', k+1, ") *******")
        print()
        print('y = a * x')
        print('a =', a)
        print('sigma_a =', sigma_a)
        if (ax is None) or (Number_of_dependencies_on_the_figure == 1):
            str_label_zero = "Апроксимация МНК" + "\n" + "$f($" + Str_x_name + "$) = a \cdot$(" + Str_x_name + "$)$"
        else:
            str_label_zero = "Апроксимация МНК для " + Conditions_array[k]

        x_squar_zero = np.linspace(MIN, MAX, 2)
        if k == 0:
            axis.plot(x_squar_zero, a*x_squar_zero, 'r', lw=0.5, label=str_label_zero, linestyle=Array_of_linestyle[k])
        else:
            axis.plot(x_squar_zero, a * x_squar_zero, lw=0.5, label=str_label_zero,
                      color=(1 - color_a, 1 - color_b, 1 - color_c), linestyle=Array_of_linestyle[k])

    if (Error_bool_x == True) and (ax is None):
        axis.errorbar(x_data, y_data, xerr=x_error, fmt=String_of_markers[k], color=(color_a, color_b, color_c),
                      ecolor=(color_a, color_b, color_c), elinewidth=0.5, capsize=3, capthick=0.5, barsabove=False,
                      errorevery=1, lolims=False, uplims=False, xlolims=False, xuplims=False, alpha=1, markersize=4)

    if (Error_bool_y == True) and (ax is None):
        axis.errorbar(x_data, y_data, yerr=y_error, fmt=String_of_markers[k], color=(color_a, color_b, color_c),
                      ecolor=(color_a, color_b, color_c), elinewidth=0.5, capsize=3, capthick=0.5, barsabove=False,
                      errorevery=1, lolims=False, uplims=False, xlolims=False, xuplims=False, alpha=1, markersize=4)

    #show dots on the graph
    if Show_conditions == True and Experiment_danie_pri == True:
        axis.plot(x_data, y_data, String_of_markers[k], markersize='5', color=(color_a, color_b, color_c), #markersize='5
                  label="Экспериментальные данные при " + Conditions_array[k])
    if Show_conditions == True and Experiment_danie_pri == False:
        axis.plot(x_data, y_data, String_of_markers[k], markersize='5', color=(color_a, color_b, color_c),
                  # markersize='5
                  label=Conditions_array[k])
    if Show_conditions == False and k == 1:
        axis.plot(x_data, y_data, String_of_markers[k], markersize='5', color=(color_a, color_b, color_c),
                  label="Выколотые экспериментальные данные")
    if Show_conditions == False and k == 0:
        axis.plot(x_data, y_data, String_of_markers[k], markersize='5', color=(color_a, color_b, color_c),
                  label="Экспериментальные данные")

    # axis.axvline(x=159, color='r', linestyle='--', label=r'$H_c \approx $' + f' {159} Э')
    # axis.axvline(x=426, color='r', linestyle=':', label=r'$H_s \approx $' + f' {426} Э')

    # legend
    if Show_legend == True:
        if Legend_size > 0:
            axis.legend(loc='best', prop={'size': Legend_size})
        else:
            axis.legend(loc='best')

    min_x, max_x = plt.xlim()  # Возвращает кортеж (min_x, max_x) осей
    min_y, max_y = plt.ylim()
    #MAXMIN_array = [MAX_from_matplotlib_x, MAX_from_matplotlib_y, MIN_from_matplotlib_x, MIN_from_matplotlib_y]
    maxmin_array[0] = max(maxmin_array[0], max_x)
    maxmin_array[1] = max(maxmin_array[1], max_y)
    maxmin_array[2] = min(maxmin_array[2], min_x)
    maxmin_array[3] = min(maxmin_array[3], min_y)

if Make_own_graph_for_each_dependency ==  True:
    k = 0 # индекс для итерации по excell
    for i in range(Number_of_rows):
        for j in range(Number_of_columns):
            if (Number_of_dependencies_on_the_figure % 2 != 0) and (k == Number_of_dependencies_on_the_figure):
                k += 1
                continue
            if (k < Number_of_dependencies_on_the_figure):
                create_cool_graph(i, j, k, MAXMIN_array)
                k += 1
            if (i+1 == Number_of_rows) and (j == 0) and (Include_general_graph_in_the_figure == True):
                base_axis = figure.add_subplot(gs[i, 0:2])
                for new_k in range(Number_of_dependencies_on_the_figure):
                    create_cool_graph(i, j, new_k, MAXMIN_array, base_axis)
                break
else:
    base_axis = figure.add_subplot(gs[0, 0:2])
    for new_k in range(Number_of_dependencies_on_the_figure):
        create_cool_graph(0, 0, new_k, MAXMIN_array, base_axis)


#print("start function", k+1, "-----------------------------------------------")
# print("i=", i)
# print("j=", j)
# print("k=", k)
#print("finish----------------------------------------------------------------")
# axis.xaxis.set_major_locator(MultipleLocator(base=5)) # кол-во рисок(шаг)
# axis.xaxis.set_minor_locator(MultipleLocator(base=1))
# axis.yaxis.set_major_locator(MultipleLocator(base=1)) # кол-во рисок(шаг)
# axis.yaxis.set_minor_locator(MultipleLocator(base=0.2))
# axis.xaxis.set_major_formatter(MultipleLocator(base=5))

# axis.setp(linestyle='-', color=(0, 0, 0), marker='o', markerfacecolor=(0, 1, 0, 0.5), linewidth=3)

if (Show_conditions == True) and (Number_of_dependencies_on_the_figure == 1):
    figure.suptitle(Graph_name + " при " + Conditions_array[0], fontsize=Graph_name_size)
else:
    figure.suptitle(Graph_name, fontsize=Graph_name_size)

plt.savefig('foo.pdf')
plt.show()

# Settings
#A = 6  # Want figures to be A6
#plt.rc('figure', figsize=[46.82 * .5**(.5 * A), 33.11 * .5**(.5 * A)])

#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')
#plt.rc('text.latex', preamble=r'\usepackage[russian]{babel}')

#plt.rc('text.latex', unicode=True)
#plt.rcParams['text.latex.preamble'] = [r'\usepackage[utf8x]{inputenc}',
#            r'\usepackage[english,russian]{babel}',
#            r'\usepackage{amsmath}']