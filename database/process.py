import pandas as pd


def process(path):

	df = pd.read_csv(path)
	id_vars = ['Region', 'Groups', 'Division', 'Indicator', 'Category', 'Type']
	df = pd.melt(df, id_vars=id_vars, var_name='Month', value_name='Sales')

	with open("data.txt", "w") as f:
		for index, row in df.iterrows():
			f.write(f"In the {row[0]} region, during the month of {row[6]} the {row[1]} group operating under the {row[2]} division, achieved a {row[5]} {row[3]} of {row[-1]}.\n")


if __name__ == "__main__":
	process("Dashboard 3.csv")