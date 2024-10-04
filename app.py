import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Theme Dashboard
st.set_page_config(page_title="Bike Rental Dashboard", page_icon="🚴", layout="wide")

# data day.csv
data_day = pd.read_csv('day.csv')

# Konversi kolom 'dteday' ke datetime jika belum
data_day['dteday'] = pd.to_datetime(data_day['dteday'])

# Title & Icon
st.title("🚴 Bike Rental Dashboard")
st.markdown("### Analyzing Daily and Seasonal Bike Rental Data")

# Sidebar for change year of rent bike between 2011 and 2012
st.sidebar.title("Filter Data")
st.sidebar.markdown("Use the filter below to customize the data view:")
year_filter = st.sidebar.selectbox("Select Year", [2011, 2012])

# Filter data untuk tahun 2011 & 2012
if year_filter == 2011:
    filtered_data = data_day[data_day['yr'] == 0]
else:
    filtered_data = data_day[data_day['yr'] == 1]

# Header 3 Kolom Statistik 
st.markdown("## 🚴 Rental Statistics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Rentals (Year)", value=f"{filtered_data['cnt'].sum():,}")
with col2:
    st.metric(label="Average Daily Rentals", value=f"{filtered_data['cnt'].mean():,.2f}")
with col3:
    st.metric(label="Total Registered Users", value=f"{filtered_data['registered'].sum():,}")

# jarak antar section agar lebih bagus
st.markdown("<br>", unsafe_allow_html=True)

# Grafik 2 line "Number of Bike Rentals Per Month" d
st.markdown("### 📅 Number of Bike Rentals Per Month")
fig2, ax2 = plt.subplots()
monthly_2011 = data_day[data_day['yr'] == 0].groupby(data_day['dteday'].dt.month)['cnt'].sum()
monthly_2012 = data_day[data_day['yr'] == 1].groupby(data_day['dteday'].dt.month)['cnt'].sum()
ax2.plot(monthly_2011.index, monthly_2011.values, label='2011', color='#8E44AD', marker='o')
ax2.plot(monthly_2012.index, monthly_2012.values, label='2012', color='#F1C40F', marker='o')
ax2.set_title('Number of Bike Rentals Per Month', fontsize=16)
ax2.set_xlabel('Month', fontsize=12)
ax2.set_ylabel('Total Rentals', fontsize=12)
ax2.legend(title="Year")
ax2.grid(True)
st.pyplot(fig2)

# spasi  antara grafik
st.markdown("<br><hr><br>", unsafe_allow_html=True)

# Grafik Histogram Distribution of daily bike rentals
st.markdown("### 📊 Distribution of Daily Bike Rentals")
fig_dist, ax_dist = plt.subplots()
sns.histplot(data=filtered_data['cnt'], bins=30, kde=True, color='#3498DB', ax=ax_dist)
ax_dist.set_title('Distribution of Daily Bike Rentals', fontsize=16)
ax_dist.set_xlabel('Number of Rentals', fontsize=12)
ax_dist.set_ylabel('Frequency', fontsize=12)
st.pyplot(fig_dist)

# Jarak antara grafik
st.markdown("<br><hr><br>", unsafe_allow_html=True)

# Grafik bar  rental bike per season
st.markdown("### ☀️ Bike Rentals Per Season")
season_data = filtered_data.groupby('season')['cnt'].sum().reset_index()

# penamaan musim "angka: ke "nama" musim sesuai di notepad
season_map = {1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
season_data['season'] = season_data['season'].map(season_map)

# figure untuk grafik musiman
fig3, ax3 = plt.subplots()

# Warna  untuk tiap musim
colors = ['#8E44AD', '#2980B9', '#27AE60', '#F1C40F']  # Warna ungu, biru, hijau, kuning
sns.barplot(x='season', y='cnt', data=season_data, ax=ax3, palette=colors)

# Menambahkan nilai kuantitas di atas setiap batang
for p in ax3.patches:
    ax3.annotate(f'{int(p.get_height()):,}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')

# Judul grafik musiman
ax3.set_title('Comparison of Total Bike Rentals Per Season', fontsize=16)
ax3.set_xlabel('Season', fontsize=12)
ax3.set_ylabel('Total Rentals', fontsize=12)
plt.grid(True)

# Tampilkan grafik di Streamlit
st.pyplot(fig3)

# Footer
st.markdown("### Jonathan Christian Simbolon")
