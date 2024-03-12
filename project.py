import streamlit as st
import pandas as pd
import altair as alt

# Page Layout Setup
st.set_page_config(
    page_title = 'Analisis Penjualan Toko',
    page_icon='📒',
    layout='wide'
)

# Calling Data
@st.cache_data 
def load_data_sales_analyst(file_name):
    sa = pd.read_csv(file_name)
    sa['Order Date'] = pd.to_datetime(sa['Order Date'], format="%Y-%m-%d %H:%M:%S")
    # Making a column with just the Year-Month-Date format
    sa['day_month_year'] = sa['Order Date'].dt.strftime("%d %b %Y")
    # Making a column with just the time
    sa['time'] = sa['Order Date'].dt.strftime("%H:%M")
    sa['Sales'] = pd.to_numeric(sa['Sales'])
    sa['Month'] = pd.to_numeric(sa['Month'])
    return sa
sa = load_data_sales_analyst('sales_analyst.csv')

# Make Functions
def title():
    cols_title = st.columns([0.8,2,0.5])
    with cols_title[1]:
        st.title("Projek Analisis Penjualan Produk")

def penjualan_3_teratas_per_bulan():
    st.subheader('Top 3 Penjualan Produk per Bulan')
    months = sa['Month'].unique()
    cols = st.columns(4)
    for i in range(len(months)):
        # Make monthly dataframe
        monthly_sales = sa[sa['Month'] == i+1].groupby(['Month', 'Product']).agg({'Sales': 'sum'})
        monthly_sales_sorted = monthly_sales.sort_values('Sales', ascending=False).reset_index()
        top_3_monthly_sales = monthly_sales_sorted.head(3)
        # Make bar chart about monthly sales
        monthly_bar_chart = alt.Chart(top_3_monthly_sales).mark_bar().encode(
            x=alt.X('Product:N', sort=alt.SortField(field='Sales', order='descending'), title='Nama Produk'),
            y=alt.Y('Sales:Q', title='Pendapatan'),
            color=alt.Color('Product', legend=None)
        ).properties(
            title=f'Bulan ke-{i+1}'
        )
        if i < 4:
            with cols[i]:
                ci = st.container(border=True)
                ci.altair_chart(monthly_bar_chart, use_container_width=True)
        elif 4 <= i < 8:
            with cols[i-4]:
                ci = st.container(border=True)
                ci.altair_chart(monthly_bar_chart, use_container_width=True)
        else:
            with cols[i-8]:
                ci = st.container(border=True)
                ci.altair_chart(monthly_bar_chart, use_container_width=True)

def perbandingan_harga_dengan_produk():
    st.subheader('Perbandingan Harga Setiap Produk')
    chart_harga = alt.Chart(sa).mark_bar().encode(
        y=alt.Y('Product:N', sort=alt.SortField(field='Price Each', order='descending'), title='Produk'),
        x=alt.X('mean(Price Each):Q', title='Harga per Satuan')
    )
    st.altair_chart(chart_harga, use_container_width=True)

def laporan_monthly_sales():
    st.subheader("Laporan Penjualan per Bulan")
    monthly_sales = sa.groupby(['Month', 'Product']).agg({'Sales':'sum', 'Quantity Ordered':'sum'}).reset_index(drop=False)
    monthly_sales_sorted = monthly_sales.sort_values(['Month', 'Sales'], ascending=[True, False])    
    st.write('''
                Pendapatan yang tinggi berasal dari produk elektronik yang sering dipakai oleh kalangan muda pelajar, seperti
                laptop, hp, dan headphone. Harga yang tertinggi dari semua produk dan juga kebutuhan laptop membuat pendapatan setiap
                bulannya pada Macbook Pro Laptop yang tertinggi.
                ''')  
    with st.expander("Tekan untuk melihat chart penjualan per bulan⤵"):
        st.write('Silahkan tekan produk di bagian \'legend\' untuk memperjelas posisi produk di chart')
        # Making Interactive Charts
        selection = alt.selection_point(fields=['Product'], bind='legend')
        scatter_facet = alt.Chart(monthly_sales_sorted).mark_point(size=65).encode(
            x=alt.X("Sales:Q", title='Pendapatan'),
            y=alt.Y("Quantity Ordered:Q", title='Banyak Penjualan'),
            facet=alt.Facet('Month:N', title='Bulan').columns(2),
            color=alt.Color("Product:N", title='Produk'),
            tooltip=[
                alt.Tooltip('Sales', title='Pendapatan'),
                alt.Tooltip('Quantity Ordered', title='Banyak Penjualan')
            ],
            opacity=alt.condition(selection, alt.value(1), alt.value(0))
        ).properties(
            title='Scatterplot Perbandingan Banyak Penjualan dan Pendapatan'
        ).add_params(
            selection
        )
        st.altair_chart(scatter_facet)

def penjualan_produk_per_bulan():
    op = st.selectbox(
        'Pilih angka dari opsi berikut untuk mengecek penjualan per bulan',
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
        index=11
    )
    if op==1:
        curr_month_sales = sa.loc[sa['Month'] == op]
        curr_product_sale = curr_month_sales.groupby(['Product']).agg({'Sales':'sum'}).reset_index()
        product_list = curr_product_sale['Product'].tolist()
        curr_sales_list = curr_product_sale['Sales'].tolist()
        # define the number of columns and rows that will be applied
        st.subheader(f'Penjualan Produk Bulan ke-{op}')
        cols_less_5 = st.columns(5)
        co = st.container(border=True)
        with co:
            for j in range(len(product_list)):
                if j < 5:
                    with cols_less_5[j]:
                        ci = st.container(border=True)
                        ci.metric(
                            label=product_list[j],
                            value='{:,}'.format(round(curr_sales_list[j], 2))
                        )
                elif 5 <= j < 10:
                    with cols_less_5[j-5]:
                        ci = st.container(border=True)
                        ci.metric(
                            label=product_list[j],
                            value='{:,}'.format(round(curr_sales_list[j], 2))
                        )
                elif 10 <= j < 15:
                    with cols_less_5[j-10]:
                        ci = st.container(border=True)
                        ci.metric(
                            label=product_list[j],
                            value='{:,}'.format(round(curr_sales_list[j], 2))
                        )
                else:
                    with cols_less_5[j-15]:
                        ci = st.container(border=True)
                        ci.metric(
                            label=product_list[j],
                            value='{:,}'.format(round(curr_sales_list[j], 2))
                        )
    else:     
        curr_month_sales = sa.loc[sa['Month'] == op]
        prev_month_sales = sa.loc[sa['Month'] == op-1]
        curr_product_sale = curr_month_sales.groupby(['Product']).agg({'Sales':'sum'}).reset_index()
        prev_product_sale = prev_month_sales.groupby(['Product']).agg({'Sales':'sum'}).reset_index()
        product_list = curr_product_sale['Product'].tolist()
        curr_sales_list = curr_product_sale['Sales'].tolist()
        prev_sales_list = prev_product_sale['Sales'].tolist()
        curr_values = [float(val) for val in curr_sales_list]
        prev_values = [float(val) for val in prev_sales_list]
        delta_values = [curr - prev for curr, prev in zip(curr_values, prev_values)]
        st.subheader(f'Penjualan Produk Bulan ke-{op}')
        cols_less_5 = st.columns(5)
        co = st.container(border=True)
        with co:
            for j in range(len(product_list)):
                if j < 5:
                    with cols_less_5[j]:
                        ci = st.container(border=True)
                        ci.metric(
                            label=product_list[j],
                            value='{:,}'.format(round(curr_values[j], 2)),
                            delta='{:,}'.format(round(delta_values[j], 2)),
                        )
                elif 5 <= j < 10:
                    with cols_less_5[j-5]:
                        ci = st.container(border=True)
                        ci.metric(
                            label=product_list[j],
                            value='{:,}'.format(round(curr_values[j], 2)),
                            delta='{:,}'.format(round(delta_values[j], 2)),
                        )
                elif 10 <= j < 15:
                    with cols_less_5[j-10]:
                        ci = st.container(border=True)
                        ci.metric(
                            label=product_list[j],
                            value='{:,}'.format(round(curr_values[j], 2)),
                            delta='{:,}'.format(round(delta_values[j], 2)),
                        )
                else:
                    with cols_less_5[j-15]:
                        ci = st.container(border=True)
                        ci.metric(
                            label=product_list[j],
                            value='{:,}'.format(round(curr_values[j], 2)),
                            delta='{:,}'.format(round(delta_values[j], 2)),
                        )

def best_months():
    st.subheader('Bulan dengan Penjualan Terbaik')
    best_months = sa.groupby('Month').agg({'Sales':'sum'})
    best_months_sorted = best_months.sort_values(by='Sales', ascending=False).reset_index()
    best_months_chart = alt.Chart(best_months_sorted).mark_bar().encode(
        x=alt.X('Month:N', sort=alt.SortField(field='Sales', order='descending'), axis=alt.Axis(labelAngle=0), title='Bulan'),
        y=alt.Y('Sales:Q', title='Penjualan')
    )
    st.altair_chart(best_months_chart, use_container_width=True)
    st.write('''
             Bulan Desember, adalah salah satu bulan yang ditunggu-tunggu oleh penduduk bumi. Salah satu hari libur terbesar ada di dalam bulan ini.
             Oleh karenanya pertukaran hadiah, membeli barang, dan dropshipper dapat membuat sales toko semakin meningkat. 
             ''')

def best_cities():
    kalimat_untuk_markdown = '''
        Menurut laman [rockstarpromovers](https://rockstarpromovers.com/blog/the-pros-and-cons-of-locating-your-business-in-san-francisco/#:~:text=Nowadays%20it%20is%20also%20famous,to%20help%20you%20move%20there.)
        , kota ini menjadi kota dengan 4 dari 12 perusahaan terbesar di dunia. Kota San Fransisco juga menjadi tempat tujuan seseorang ketika ingin membuka bisnis.
    '''
    st.subheader('Kota dengan Penjualan Terbaik')
    best_city = sa.groupby('City').agg({'Sales':'sum'})
    best_city_sorted = best_city.sort_values(by='Sales', ascending=False).reset_index()
    best_city_chart = alt.Chart(best_city_sorted).mark_bar().encode(
        x=alt.X('City:N', sort=alt.SortField(field='Sales', order='descending'), axis=alt.Axis(labelAngle=0), title='Kota'),
        y=alt.Y('Sales:Q', title='Penjualan')
    )
    st.altair_chart(best_city_chart, use_container_width=True)
    st.markdown(kalimat_untuk_markdown)

def best_hours():
    st.subheader('Jam Pengiklanan dengan Penjualan Terbaik')
    best_hour = sa.groupby('Hour').agg({'Sales':'sum'})
    best_hour_sorted = best_hour.sort_values(by='Sales', ascending=False).reset_index()
    best_hour_chart = alt.Chart(best_hour_sorted).mark_bar().encode(
        x=alt.X('Hour:N', sort=alt.SortField(field='Sales', order='descending'), axis=alt.Axis(labelAngle=0), title='Jam Iklan'),
        y=alt.Y('Sales:Q', title='Penjualan')
    )
    st.altair_chart(best_hour_chart, use_container_width=True)
    st.write('''
             Jam 19.00 adalah waktu yang sangat tepat untuk beristirahat baik dari kalangan pekerja hingga kalangan mahasiswa.
             ''')

def best_products():
    st.subheader('Produk dengan Kuantitas Barang Terjual Terbaik')
    best_product = sa.groupby('Product').agg({'Quantity Ordered':'count'})
    best_product_sorted = best_product.sort_values(by='Quantity Ordered', ascending=False).reset_index()
    best_product_chart = alt.Chart(best_product_sorted).mark_bar().encode(
        y=alt.Y('Product:N', sort=alt.SortField(field='Quantity Ordered', order='descending'), axis=alt.Axis(labelAngle=0), title='Nama Produk'),
        x=alt.X('Quantity Ordered:Q', title='Barang Terjual')
    )
    st.altair_chart(best_product_chart, use_container_width=True)
    st.write('''
             Produk yang dibeli terbanyak adalah charging cable, dimana ini merupakan lifeline dari handphone. 
             Juga dengan harganya yang murah, membuat barang ini menjadi barang yang paling banyak terjual.
             ''')

# Start Developing
title()
st.write('')
penjualan_3_teratas_per_bulan()
with st.expander('Bulan dengan Penjualan Terbaik'):
    best_months()
with st.expander('Kota dengan Penjualan Terbaik'):
    best_cities()
with st.expander('Jam Penayangan Iklan dengan Penjualan Terbaik'):
    best_hours()
with st.expander('Produk dengan Jumlah Produk Terjual Terbaik'):
    best_products()
st.write('')
laporan_monthly_sales()
perbandingan_harga_dengan_produk()
penjualan_produk_per_bulan()
