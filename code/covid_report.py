from fpdf import FPDF
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import easygui

# path to folder and data
pth = easygui.enterbox(r"Please provide folder path with graphics")

source_file = easygui.enterbox(r"Please provide full path to source file")

# reading and filtering data
df = pd.read_csv(source_file)
data_for_viz = df[(df['stan_rekordu_na']=='2020-11-23') &(df['wojewodztwo']!='Cały kraj')]

# creating figure
plt.figure(figsize=(6, 6))
plt.tick_params(axis='x')
plt.title('Number of Covid cases per province/region')
plt.barh(y=data_for_viz['wojewodztwo'],width=data_for_viz['liczba_przypadkow'])
for i, v in enumerate(data_for_viz['liczba_przypadkow']):
    plt.text(v-120, i, str(v), color='white',fontweight='bold', fontsize=10, ha='left', va='center')
plt.savefig(f'{pth}\przypadki.jpg',bbox_inches='tight')

# filtering data and creating figure
data_value = data_for_viz['liczba_osob_objetych_kwarantanna'].sum()
plt.figure(figsize=(6, 6))
plt.ylim(0,data_value*1.2)
plt.title('People under quarantine')
plotting = plt.bar(x=[15],height=[data_value],width=0.8)
plt.xlim(10, 20)
plt.xticks([], [])
plt.bar_label(plotting,label_type='edge')
plt.savefig(f'{pth}\kwarantanna.jpg',bbox_inches='tight')

# getting stats on positive and negative tests
positive = data_for_viz['liczba_testow_z_wynikiem_pozytywnym'].sum()
negative = data_for_viz['liczba_testow_z_wynikiem_negatywnym'].sum()

# creating a pie chart
df_for_pie = pd.DataFrame({'results': [positive, negative]},index=['Positive', 'Negative'])
total = positive + negative
plt.style.use('fivethirtyeight')
plot = df_for_pie.plot.pie(y='results', figsize=(5, 5),autopct=lambda p: '{:.2f}%\n{:.0f}'.format(p,p * total / 100),
title = 'Positive and negative Covid tests')
plot.get_legend().remove()
plt.savefig(f'{pth}\_testy.jpg',bbox_inches='tight')

# getting stats on non-covid cases
pos_covid = data_for_viz['zgony_w_wyniku_covid_bez_chorob_wspolistniejacych'].sum()
neg_covid = data_for_viz['zgony_w_wyniku_covid_i_chorob_wspolistniejacych'].sum()

# creating figure
df_for_pie = pd.DataFrame({'results': [pos_covid, neg_covid]},index=['Covid', 'Non-Covid'])
total = positive + negative
plt.style.use('fivethirtyeight')
plot = df_for_pie.plot.pie(y='results', figsize=(5, 5),autopct=lambda p: '{:.2f}%\n{:.0f}'.format(p,p * total / 100),
title = 'Covid and Non-Covid deaths')
plot.get_legend().remove()
plot.set(ylabel="")
plt.savefig(f'{pth}\covidowe_zgony.jpg',bbox_inches='tight')

# getting data for last 20 days
line_data = df[df['wojewodztwo']=='Cały kraj'].tail(20)

# creating graph
plt.figure(figsize=(20, 6))
plotting = sns.lineplot(data=line_data,x='stan_rekordu_na',y='zgony')
plotting.set_title("Deaths within last 20 days")
plotting.set_xlabel('')
plotting.set_ylabel('Number of cases')
plt.xticks(rotation=45)
plt.savefig(f'{pth}\zgony_20_dni.jpg',bbox_inches='tight')

# creating graph
plt.figure(figsize=(20, 6))
plotting = sns.lineplot(data=line_data,x='stan_rekordu_na',y='liczba_przypadkow')
plotting.set_title("Number of people which contracted Covid within last 20 days")
plotting.set_xlabel('')
plotting.set_ylabel('Number of cases')
plt.xticks(rotation=45)
plt.savefig(f'{pth}\przypadki_20_dni.jpg',bbox_inches='tight')



# official size of A4 format paper (in milimeters)
WIDTH = 210
HEIGHT = 297

class PDF(FPDF):
    def footer(self):
        self.set_y(-10)
        self.set_font('helvetica','I',10)
        self.cell(0,10,f'Page {self.page_no()}',align='C')

# instantiating pdf class
pdf = PDF()

# adding page
pdf.add_page()
# setting font
pdf.set_font('Arial','B',16)
pdf.image(f'{pth}\heading.jpg',3,2,WIDTH-6)

# adding first image, 5mm from left,30 mm from top, width is half page width - 5mm
pdf.image(f'{pth}\covidowe_zgony.jpg',5,80,WIDTH/2-20,HEIGHT/4)

# adding second image, half page from left,30 mm from top, width is half page width - 5mm
pdf.image(f'{pth}\przypadki.jpg',WIDTH/2,80,WIDTH/2-5,HEIGHT/4)

# adding third image, 5mm from left,130 mm from top, width is half page width - 5mm
pdf.image(f'{pth}\kwarantanna.jpg',5,160,WIDTH/2-20,HEIGHT/4)

# adding fourth image, half page from left,130 mm from top, width is half page width - 5mm
pdf.image(f'{pth}\_testy.jpg',WIDTH/2,160,WIDTH/2-20,HEIGHT/4)


# footer
pdf.image(f'{pth}\end_footer.jpg',3,250,WIDTH-6)

# adding new page
pdf.add_page()
pdf.image(f'{pth}\heading.jpg',3,2,WIDTH-6)

# adding first image
pdf.image(f'{pth}\zgony_20_dni.jpg',1.5,80,WIDTH-3,HEIGHT/4)

# adding second image
pdf.image(f'{pth}\przypadki_20_dni.jpg',1.5,160,WIDTH-3,HEIGHT/4)

# footer
pdf.image(f'{pth}\end_footer.jpg',3,250,WIDTH-6)

# saving pdf report to file 
pdf.output(f'{pth}\\covid_report.pdf','F')