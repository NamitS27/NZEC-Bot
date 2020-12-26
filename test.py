import matplotlib.pyplot as plt

x = [2,4,6,2,2,2,2,2,2,2,2,2,8,10]
y = [1,2,3,4,6,8,10,5,7,9]

themes = ['Solarize_Light2', '_classic_test_patch', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark', 'seaborn-dark-palette', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'tableau-colorblind10']


x1 = [1,3,5,7,9]
y2 = [2,4,6,8,10]
cnt  = 0
for theme in themes:
    plt.style.use(theme)
    plt.hist([x, y])
    plt.legend(["hi","bye"])
    plt.title(f"{theme}")
    plt.savefig(f"test{cnt}.png")
    cnt += 1