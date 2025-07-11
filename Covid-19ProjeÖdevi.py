# Gerekli Kütüphane ve Fonksiyonlar
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv(r"C:\Users\Şura Gürler\Desktop\metadata.csv")

df.head()

df.columns

df.info()
df.describe()

df.isnull().sum() #Eksik değer kontrolü

# publish_time, year, abstract ve abstract_length boş olanları çıkar
df_clean = df.dropna(subset=['publish_time', 'year', 'abstract'])

# abstract_length sütununu oluştur
df_clean['abstract_length'] = df_clean['abstract'].apply(lambda x: len(str(x).split()))

# journal ve authors sütunundaki eksikleri 'Unknown' ile doldur
df_clean['journal'] = df_clean['journal'].fillna('Unknown')
df_clean['authors'] = df_clean['authors'].fillna('Unknown')

#Yıllara göre yayın sayısı

df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year
df['year'].value_counts().sort_index().plot(kind='bar')

yearly_counts = df_clean['year'].value_counts().sort_index()
yearly_counts.plot(kind='bar', color='skyblue')
plt.title("Yıllara Göre Yayın Sayısı")
plt.xlabel("Yıl")
plt.ylabel("Yayın Sayısı")
plt.show()

#En fazla yayın yapan dergiler

top_journals = df_clean['journal'].value_counts().head(10)
top_journals.plot(kind='barh', color='orange')
plt.title("En Fazla Yayın Yapan Dergiler")
plt.xlabel("Yayın Sayısı")
plt.ylabel("Dergi")
plt.gca().invert_yaxis()
plt.show()


#En aktif yazarlar

author_counts = Counter()
df_clean['authors'].apply(lambda x: author_counts.update([a.strip() for a in x.split(',')]))
top_authors = pd.Series(author_counts).sort_values(ascending=False).head(10)

top_authors.plot(kind='barh', color='green')
plt.title("En Aktif 10 Yazar")
plt.xlabel("Yayın Sayısı")
plt.ylabel("Yazar")
plt.gca().invert_yaxis()
plt.show()


sns.histplot(df_clean['abstract_length'], bins=50, kde=True, color='purple')
plt.title("Abstract Uzunluğu Dağılımı (Kelime Sayısı)")
plt.xlabel("Kelime Sayısı")
plt.ylabel("Yayın Sayısı")
plt.show()

license_counts = df_clean['license'].value_counts().head(10)
license_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140)
plt.title("En Yaygın 10 Lisans Türü")
plt.ylabel('')
plt.show()

top3 = df_clean['journal'].value_counts().head(3).index
df_top3 = df_clean[df_clean['journal'].isin(top3)]

trend = df_top3.groupby(['year', 'journal']).size().unstack().fillna(0)
trend.plot(marker='o')
plt.title("En Çok Yayın Yapan 3 Dergi - Yıllık Yayın Sayısı")
plt.xlabel("Yıl")
plt.ylabel("Yayın Sayısı")
plt.legend(title="Dergi")
plt.show()