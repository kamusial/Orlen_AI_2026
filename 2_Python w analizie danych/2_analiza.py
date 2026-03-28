"""
===========================================================
ZAAWANSOWANE ĆWICZENIE: PYTHON W ANALIZIE DANYCH
Temat: Analiza danych sprzedażowych sklepu internetowego
Autor: materiał dydaktyczny dla studentów
===========================================================

OPIS:
Ten skrypt prowadzi przez pełny proces analizy danych:
1. Generowanie przykładowego zbioru danych
2. Wczytywanie i wstępna inspekcja
3. Czyszczenie danych
4. Analiza eksploracyjna (EDA)
5. Inżynieria cech
6. Analiza statystyczna
7. Budowa modelu regresyjnego
8. Segmentacja klientów metodą KMeans
9. Tworzenie raportu wynikowego

WYMAGANE BIBLIOTEKI:
- pandas
- numpy
- matplotlib
- scikit-learn

INSTALACJA:
pip install pandas numpy matplotlib scikit-learn
"""

# =========================================================
# 1. IMPORT BIBLIOTEK
# =========================================================

import os
import math
import random
import warnings
from dataclasses import dataclass

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans

warnings.filterwarnings("ignore")

# Ustawienie ziarna losowości, aby wyniki były powtarzalne.
# Dzięki temu każdy student, który uruchomi kod, otrzyma bardzo podobne rezultaty.
np.random.seed(42)
random.seed(42)


# =========================================================
# 2. USTAWIENIA GLOBALNE I PARAMETRY PROJEKTU
# =========================================================

DATA_DIR = "data"
OUTPUT_DIR = "output"
PLOTS_DIR = os.path.join(OUTPUT_DIR, "plots")

# Tworzymy katalogi robocze, jeśli jeszcze nie istnieją.
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

DATA_FILE = os.path.join(DATA_DIR, "ecommerce_sales.csv")


# =========================================================
# 3. FUNKCJE POMOCNICZE
# =========================================================

def save_plot(filename: str) -> None:
    """
    Funkcja zapisuje aktualny wykres Matplotlib do pliku PNG.

    Parametry:
    ----------
    filename : str
        Nazwa pliku, do którego zapisany zostanie wykres.

    Zastosowanie:
    -------------
    Dzięki tej funkcji każdy wykres z analizy może być zapisany,
    co pozwala studentom tworzyć automatyczne raporty.
    """
    full_path = os.path.join(PLOTS_DIR, filename)
    plt.tight_layout()
    plt.savefig(full_path, dpi=150)
    plt.close()


def print_section(title: str) -> None:
    """
    Ładnie formatuje sekcje w konsoli, aby kod był bardziej czytelny.
    """
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def generate_customer_id(index: int) -> str:
    """
    Generuje identyfikator klienta w formacie np. CUST_000123.
    """
    return f"CUST_{index:06d}"


def introduce_missing_values(df: pd.DataFrame, columns: list, fraction: float = 0.03) -> pd.DataFrame:
    """
    Wprowadza brakujące wartości do wybranych kolumn.

    Cel dydaktyczny:
    ----------------
    W realnych danych bardzo często występują braki.
    Warto pokazać studentom, jak sobie z nimi radzić.

    Parametry:
    ----------
    df : pd.DataFrame
        Zbiór danych.
    columns : list
        Lista kolumn, do których wprowadzimy braki.
    fraction : float
        Ułamek rekordów, które zostaną uszkodzone.

    Zwraca:
    -------
    pd.DataFrame
        Zbiór danych z brakami.
    """
    df = df.copy()
    n_rows = len(df)

    for col in columns:
        missing_indices = np.random.choice(df.index, size=int(n_rows * fraction), replace=False)
        df.loc[missing_indices, col] = np.nan

    return df


def introduce_outliers(df: pd.DataFrame, col: str, fraction: float = 0.01, multiplier: float = 5.0) -> pd.DataFrame:
    """
    Wprowadza obserwacje odstające (outliers) do wybranej kolumny liczbowej.

    Cel dydaktyczny:
    ----------------
    Dane biznesowe często zawierają anomalie:
    - błędnie zapisane wartości,
    - bardzo nietypowe zamówienia,
    - duże zakupy hurtowe.

    Parametry:
    ----------
    df : pd.DataFrame
        Zbiór danych.
    col : str
        Nazwa kolumny liczbowej.
    fraction : float
        Ułamek rekordów, które zostaną zmodyfikowane.
    multiplier : float
        Współczynnik zwiększający wartości.
    """
    df = df.copy()
    n_rows = len(df)
    outlier_indices = np.random.choice(df.index, size=int(n_rows * fraction), replace=False)
    df.loc[outlier_indices, col] = df.loc[outlier_indices, col] * multiplier
    return df


def winsorize_series(series: pd.Series, lower_q: float = 0.01, upper_q: float = 0.99) -> pd.Series:
    """
    Ogranicza skrajne wartości w serii do określonych kwantyli.

    Wyjaśnienie:
    ------------
    Zamiast usuwać rekordy odstające, możemy "przyciąć" ich wartości,
    aby zmniejszyć wpływ anomalii na analizę i model.

    Parametry:
    ----------
    series : pd.Series
        Kolumna liczbowa.
    lower_q : float
        Dolny kwantyl.
    upper_q : float
        Górny kwantyl.

    Zwraca:
    -------
    pd.Series
        Seria po winsoryzacji.
    """
    lower = series.quantile(lower_q)
    upper = series.quantile(upper_q)
    return series.clip(lower=lower, upper=upper)


def calculate_rmse(y_true, y_pred) -> float:
    """
    Liczy pierwiastek z błędu średniokwadratowego (RMSE).
    """
    return math.sqrt(mean_squared_error(y_true, y_pred))


# =========================================================
# 4. GENEROWANIE PRZYKŁADOWEGO ZBIORU DANYCH
# =========================================================

def generate_synthetic_ecommerce_data(n_rows: int = 5000) -> pd.DataFrame:
    """
    Generuje realistyczny zbiór danych e-commerce.

    Struktura danych:
    -----------------
    - order_id                : identyfikator zamówienia
    - customer_id             : identyfikator klienta
    - order_date              : data zamówienia
    - product_category        : kategoria produktu
    - city                    : miasto klienta
    - age                     : wiek klienta
    - gender                  : płeć
    - income                  : dochód klienta
    - loyalty_years           : liczba lat w programie lojalnościowym
    - site_visits_last_month  : liczba wizyt na stronie
    - discount_percent        : rabat procentowy
    - quantity                : liczba sztuk
    - unit_price              : cena jednostkowa
    - shipping_cost           : koszt dostawy
    - payment_method          : metoda płatności
    - returned                : czy klient zwrócił towar
    - order_value             : wartość zamówienia (zmienna docelowa)

    Cel dydaktyczny:
    ----------------
    Zamiast zależeć od zewnętrznego pliku CSV, generujemy własne dane.
    Dzięki temu ćwiczenie działa od razu i można je swobodnie modyfikować.
    """

    categories = ["Electronics", "Fashion", "Home", "Sports", "Books", "Beauty"]
    cities = ["Warsaw", "Krakow", "Wroclaw", "Poznan", "Gdansk", "Lodz", "Katowice"]
    genders = ["Female", "Male"]
    payment_methods = ["Card", "BLIK", "Transfer", "CashOnDelivery", "MobileWallet"]

    # Losujemy podstawowe zmienne opisujące klientów i zamówienia.
    order_ids = np.arange(1, n_rows + 1)
    customer_ids = [generate_customer_id(np.random.randint(1, 1500)) for _ in range(n_rows)]

    # Zakres dat: dwa lata sprzedaży.
    order_dates = pd.to_datetime(
        np.random.choice(
            pd.date_range("2024-01-01", "2025-12-31", freq="D"),
            size=n_rows
        )
    )

    product_category = np.random.choice(categories, size=n_rows, p=[0.22, 0.20, 0.18, 0.14, 0.12, 0.14])
    city = np.random.choice(cities, size=n_rows)
    gender = np.random.choice(genders, size=n_rows)

    # Wiek klientów – przycinamy do sensownego zakresu.
    age = np.clip(np.random.normal(loc=37, scale=11, size=n_rows).round(), 18, 75)

    # Dochód: rozkład normalny z przycięciem.
    income = np.clip(np.random.normal(loc=7000, scale=2500, size=n_rows), 2500, 25000)

    # Staż lojalnościowy w latach.
    loyalty_years = np.clip(np.random.gamma(shape=2.0, scale=1.5, size=n_rows), 0, 12)

    # Liczba wizyt na stronie.
    site_visits_last_month = np.clip(np.random.poisson(lam=8, size=n_rows), 1, 40)

    # Rabat: większość klientów ma mały rabat, niektórzy większy.
    discount_percent = np.clip(np.random.normal(loc=8, scale=6, size=n_rows), 0, 35)

    # Liczba sztuk w zamówieniu.
    quantity = np.clip(np.random.poisson(lam=2.5, size=n_rows) + 1, 1, 12)

    # Ceny bazowe zależne od kategorii.
    category_base_price = {
        "Electronics": 600,
        "Fashion": 180,
        "Home": 250,
        "Sports": 220,
        "Books": 55,
        "Beauty": 90
    }

    unit_price = np.array([
        np.random.normal(loc=category_base_price[cat], scale=category_base_price[cat] * 0.25)
        for cat in product_category
    ])

    # Minimalna cena jednostkowa nie może być ujemna ani zbyt niska.
    unit_price = np.clip(unit_price, 15, None)

    # Metoda płatności
    payment_method = np.random.choice(payment_methods, size=n_rows, p=[0.35, 0.25, 0.20, 0.08, 0.12])

    # Koszt dostawy – częściowo zależny od kategorii i wartości zamówienia.
    shipping_cost = np.clip(
        np.random.normal(loc=15, scale=5, size=n_rows) +
        np.where(product_category == "Electronics", 8, 0) +
        np.where(product_category == "Books", -4, 0),
        0,
        45
    )

    # Czy produkt został zwrócony – zwroty częściej pojawiają się np. w Fashion.
    return_prob = (
        0.05
        + np.where(product_category == "Fashion", 0.08, 0)
        + np.where(product_category == "Electronics", 0.03, 0)
        + np.where(discount_percent > 20, 0.02, 0)
    )

    returned = np.random.binomial(1, p=np.clip(return_prob, 0, 0.35))

    # Obliczamy wartość zamówienia.
    # Wartość bazuje na cenie, liczbie sztuk, rabacie i kilku efektach biznesowych.
    gross_value = unit_price * quantity

    # Wprowadzamy zależności, aby dane były sensowniejsze analitycznie.
    business_effect = (
        1
        + (income / 100000)                         # wyższy dochód -> trochę wyższe zakupy
        + (site_visits_last_month / 300)           # większa aktywność -> nieco wyższa wartość
        + (loyalty_years / 50)                     # lojalni klienci -> nieco większe koszyki
    )

    discounted_value = gross_value * (1 - discount_percent / 100)

    order_value = discounted_value * business_effect + shipping_cost

    # Dodajemy szum losowy, aby nie było zbyt idealnie.
    order_value = order_value + np.random.normal(0, 40, size=n_rows)

    # Zamówienie nie może mieć wartości ujemnej.
    order_value = np.clip(order_value, 20, None)

    df = pd.DataFrame({
        "order_id": order_ids,
        "customer_id": customer_ids,
        "order_date": order_dates,
        "product_category": product_category,
        "city": city,
        "age": age.astype(int),
        "gender": gender,
        "income": income.round(2),
        "loyalty_years": loyalty_years.round(2),
        "site_visits_last_month": site_visits_last_month,
        "discount_percent": discount_percent.round(2),
        "quantity": quantity,
        "unit_price": unit_price.round(2),
        "shipping_cost": shipping_cost.round(2),
        "payment_method": payment_method,
        "returned": returned,
        "order_value": order_value.round(2)
    })

    # Wprowadzamy braki danych do wybranych kolumn.
    df = introduce_missing_values(df, ["income", "discount_percent", "shipping_cost", "gender"], fraction=0.03)

    # Wprowadzamy obserwacje odstające.
    df = introduce_outliers(df, col="order_value", fraction=0.01, multiplier=4.0)
    df = introduce_outliers(df, col="income", fraction=0.005, multiplier=3.5)

    return df


# =========================================================
# 5. ZAPIS DANYCH DO CSV I WCZYTANIE
# =========================================================

def create_and_save_dataset() -> pd.DataFrame:
    """
    Tworzy zbiór danych, zapisuje go do CSV i zwraca DataFrame.
    """
    df = generate_synthetic_ecommerce_data(n_rows=5000)
    df.to_csv(DATA_FILE, index=False)
    return df


def load_dataset(path: str) -> pd.DataFrame:
    """
    Wczytuje zbiór danych z pliku CSV.
    """
    df = pd.read_csv(path, parse_dates=["order_date"])
    return df


# =========================================================
# 6. WSTĘPNA INSPEKCJA DANYCH
# =========================================================

def inspect_data(df: pd.DataFrame) -> None:
    """
    Wyświetla podstawowe informacje o zbiorze danych.
    """
    print_section("WSTĘPNA INSPEKCJA DANYCH")

    print("Pierwsze 5 rekordów:")
    print(df.head(), "\n")

    print("Informacje o DataFrame:")
    print(df.info(), "\n")

    print("Wymiary zbioru danych (wiersze, kolumny):")
    print(df.shape, "\n")

    print("Liczba brakujących wartości w każdej kolumnie:")
    print(df.isna().sum(), "\n")

    print("Statystyki opisowe dla kolumn liczbowych:")
    print(df.describe().T, "\n")

    print("Statystyki opisowe dla kolumn kategorycznych:")
    print(df.describe(include="object").T, "\n")


# =========================================================
# 7. CZYSZCZENIE DANYCH
# =========================================================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Czyści i przygotowuje dane do dalszej analizy.

    Etapy:
    ------
    1. Usunięcie duplikatów
    2. Uzupełnienie braków
    3. Korekta typów
    4. Ograniczenie wartości odstających dla wybranych kolumn
    5. Dodanie prostych flag jakości danych

    Zwraca:
    -------
    pd.DataFrame
        Oczyszczony zbiór danych
    """
    print_section("CZYSZCZENIE DANYCH")

    df = df.copy()

    # 1. Usuwanie duplikatów.
    # W praktyce czasem ten sam rekord może pojawić się wielokrotnie.
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"Usunięto duplikaty: {before - after}")

    # 2. Uzupełnianie braków.
    # Dla kolumn liczbowych stosujemy medianę, bo jest bardziej odporna na outliery niż średnia.
    numeric_cols = ["income", "discount_percent", "shipping_cost"]
    for col in numeric_cols:
        median_value = df[col].median()
        df[col] = df[col].fillna(median_value)
        print(f"Uzupełniono braki w kolumnie {col} medianą = {median_value:.2f}")

    # Dla kolumny kategorycznej używamy najczęstszej wartości (moda).
    mode_gender = df["gender"].mode()[0]
    df["gender"] = df["gender"].fillna(mode_gender)
    print(f"Uzupełniono braki w kolumnie gender modą = {mode_gender}")

    # 3. Korekta typów danych.
    df["age"] = df["age"].astype(int)
    df["site_visits_last_month"] = df["site_visits_last_month"].astype(int)
    df["quantity"] = df["quantity"].astype(int)
    df["returned"] = df["returned"].astype(int)

    # 4. Ograniczanie wpływu outlierów.
    # Robimy to tylko dla wybranych kolumn, w których duże wartości mogą zaburzać analizę.
    for col in ["income", "order_value", "unit_price"]:
        df[col] = winsorize_series(df[col], lower_q=0.01, upper_q=0.99)
        print(f"Winsoryzacja kolumny: {col}")

    # 5. Dodatkowe flagi jakości danych.
    df["is_high_discount"] = (df["discount_percent"] >= 20).astype(int)
    df["is_returned"] = df["returned"]

    print("\nPo czyszczeniu liczba braków:")
    print(df.isna().sum())

    return df


# =========================================================
# 8. INŻYNIERIA CECH
# =========================================================

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tworzy nowe cechy pomocne w analizie i modelowaniu.

    Dodawane kolumny:
    -----------------
    - order_month
    - order_quarter
    - day_of_week
    - weekend_order
    - gross_value_estimated
    - discount_value
    - value_per_item
    - customer_age_group
    - income_segment
    """
    print_section("INŻYNIERIA CECH")

    df = df.copy()

    # Cechy związane z czasem zamówienia.
    df["order_month"] = df["order_date"].dt.month
    df["order_quarter"] = df["order_date"].dt.quarter
    df["day_of_week"] = df["order_date"].dt.day_name()
    df["weekend_order"] = df["order_date"].dt.dayofweek.isin([5, 6]).astype(int)

    # Szacowanie wartości brutto przed rabatem.
    df["gross_value_estimated"] = df["unit_price"] * df["quantity"]

    # Wartość rabatu w złotówkach.
    df["discount_value"] = df["gross_value_estimated"] * (df["discount_percent"] / 100)

    # Średnia wartość na jedną sztukę w zamówieniu.
    df["value_per_item"] = df["order_value"] / df["quantity"]

    # Grupowanie wieku.
    df["customer_age_group"] = pd.cut(
        df["age"],
        bins=[17, 25, 35, 50, 75],
        labels=["18-25", "26-35", "36-50", "51-75"]
    )

    # Segment dochodowy.
    df["income_segment"] = pd.qcut(
        df["income"],
        q=4,
        labels=["low", "medium", "high", "very_high"]
    )

    print("Dodano nowe kolumny:")
    print([
        "order_month", "order_quarter", "day_of_week", "weekend_order",
        "gross_value_estimated", "discount_value", "value_per_item",
        "customer_age_group", "income_segment"
    ])

    return df


# =========================================================
# 9. ANALIZA EKSPLORACYJNA (EDA)
# =========================================================

def exploratory_data_analysis(df: pd.DataFrame) -> None:
    """
    Przeprowadza analizę eksploracyjną danych i zapisuje wykresy.

    Analiza obejmuje:
    -----------------
    - rozkład wartości zamówienia,
    - średnią sprzedaż wg kategorii,
    - sprzedaż miesięczną,
    - zależność rabatu od wartości zamówienia,
    - liczbę zwrotów wg kategorii,
    - korelacje między zmiennymi liczbowymi.
    """
    print_section("ANALIZA EKSPLORACYJNA DANYCH (EDA)")

    # -----------------------------------------------------
    # 9.1. Podstawowe agregacje
    # -----------------------------------------------------
    print("Średnia wartość zamówienia wg kategorii produktu:")
    print(df.groupby("product_category")["order_value"].mean().sort_values(ascending=False), "\n")

    print("Średnia wartość zamówienia wg miasta:")
    print(df.groupby("city")["order_value"].mean().sort_values(ascending=False), "\n")

    print("Odsetek zwrotów wg kategorii:")
    print(df.groupby("product_category")["returned"].mean().sort_values(ascending=False), "\n")

    # -----------------------------------------------------
    # 9.2. Histogram wartości zamówienia
    # -----------------------------------------------------
    plt.figure(figsize=(10, 5))
    plt.hist(df["order_value"], bins=40)
    plt.title("Rozkład wartości zamówienia")
    plt.xlabel("order_value")
    plt.ylabel("Liczba zamówień")
    save_plot("01_hist_order_value.png")

    # -----------------------------------------------------
    # 9.3. Średnia wartość zamówienia wg kategorii
    # -----------------------------------------------------
    avg_by_category = df.groupby("product_category")["order_value"].mean().sort_values(ascending=False)

    plt.figure(figsize=(10, 5))
    plt.bar(avg_by_category.index, avg_by_category.values)
    plt.title("Średnia wartość zamówienia wg kategorii")
    plt.xlabel("Kategoria")
    plt.ylabel("Średnia wartość zamówienia")
    plt.xticks(rotation=45)
    save_plot("02_avg_value_by_category.png")

    # -----------------------------------------------------
    # 9.4. Sprzedaż miesięczna
    # -----------------------------------------------------
    monthly_sales = df.groupby(df["order_date"].dt.to_period("M"))["order_value"].sum()
    monthly_sales.index = monthly_sales.index.astype(str)

    plt.figure(figsize=(12, 5))
    plt.plot(monthly_sales.index, monthly_sales.values, marker="o")
    plt.title("Sprzedaż miesięczna")
    plt.xlabel("Miesiąc")
    plt.ylabel("Suma order_value")
    plt.xticks(rotation=60)
    save_plot("03_monthly_sales.png")

    # -----------------------------------------------------
    # 9.5. Zależność między rabatem a wartością zamówienia
    # -----------------------------------------------------
    sample_df = df.sample(min(1000, len(df)), random_state=42)

    plt.figure(figsize=(8, 5))
    plt.scatter(sample_df["discount_percent"], sample_df["order_value"], alpha=0.6)
    plt.title("Rabat a wartość zamówienia")
    plt.xlabel("discount_percent")
    plt.ylabel("order_value")
    save_plot("04_discount_vs_order_value.png")

    # -----------------------------------------------------
    # 9.6. Zwroty wg kategorii
    # -----------------------------------------------------
    return_rate = df.groupby("product_category")["returned"].mean().sort_values(ascending=False)

    plt.figure(figsize=(10, 5))
    plt.bar(return_rate.index, return_rate.values)
    plt.title("Odsetek zwrotów wg kategorii")
    plt.xlabel("Kategoria")
    plt.ylabel("Średni returned")
    plt.xticks(rotation=45)
    save_plot("05_returns_by_category.png")

    # -----------------------------------------------------
    # 9.7. Korelacje dla danych liczbowych
    # -----------------------------------------------------
    numeric_columns = [
        "age", "income", "loyalty_years", "site_visits_last_month",
        "discount_percent", "quantity", "unit_price",
        "shipping_cost", "order_value", "gross_value_estimated",
        "discount_value", "value_per_item"
    ]

    corr = df[numeric_columns].corr()

    # Wykres macierzy korelacji z użyciem samego Matplotlib.
    plt.figure(figsize=(10, 8))
    plt.imshow(corr, aspect="auto")
    plt.colorbar()
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title("Macierz korelacji")
    save_plot("06_correlation_matrix.png")

    print("Wykresy zapisano w katalogu:", PLOTS_DIR)


# =========================================================
# 10. ANALIZA STATYSTYCZNA
# =========================================================

def statistical_analysis(df: pd.DataFrame) -> dict:
    """
    Wykonuje prostą analizę statystyczną i zwraca wyniki w słowniku.

    Analizowane zagadnienia:
    ------------------------
    - średnia i mediana wartości zamówienia,
    - kwartyle,
    - porównanie wartości zamówień dla klientów z wysokim i niskim rabatem,
    - korelacje z order_value.
    """
    print_section("ANALIZA STATYSTYCZNA")

    results = {}

    # Miary położenia i rozproszenia.
    results["mean_order_value"] = df["order_value"].mean()
    results["median_order_value"] = df["order_value"].median()
    results["std_order_value"] = df["order_value"].std()
    results["q1_order_value"] = df["order_value"].quantile(0.25)
    results["q3_order_value"] = df["order_value"].quantile(0.75)

    print(f"Średnia wartość zamówienia: {results['mean_order_value']:.2f}")
    print(f"Mediana wartości zamówienia: {results['median_order_value']:.2f}")
    print(f"Odchylenie standardowe: {results['std_order_value']:.2f}")
    print(f"Q1: {results['q1_order_value']:.2f}")
    print(f"Q3: {results['q3_order_value']:.2f}")

    # Porównanie grup: wysoki vs niski rabat.
    high_discount_group = df[df["discount_percent"] >= 20]["order_value"]
    low_discount_group = df[df["discount_percent"] < 20]["order_value"]

    results["high_discount_mean"] = high_discount_group.mean()
    results["low_discount_mean"] = low_discount_group.mean()

    print(f"\nŚrednia wartość zamówienia dla rabatu >= 20%: {results['high_discount_mean']:.2f}")
    print(f"Średnia wartość zamówienia dla rabatu < 20%: {results['low_discount_mean']:.2f}")

    # Korelacje z wartością zamówienia.
    numeric_df = df.select_dtypes(include=[np.number])
    corr_with_target = numeric_df.corr()["order_value"].sort_values(ascending=False)

    results["correlations_with_order_value"] = corr_with_target
    print("\nKorelacje z order_value:")
    print(corr_with_target)

    return results


# =========================================================
# 11. MODELOWANIE REGRESYJNE
# =========================================================

def build_regression_models(df: pd.DataFrame) -> pd.DataFrame:
    """
    Buduje dwa modele regresyjne przewidujące wartość zamówienia:
    - LinearRegression
    - RandomForestRegressor

    Etapy:
    ------
    1. Wybór cech
    2. Podział na zbiory treningowy i testowy
    3. Preprocessing:
       - imputacja braków
       - skalowanie zmiennych liczbowych
       - kodowanie One-Hot cech kategorycznych
    4. Trenowanie modeli
    5. Ocena jakości

    Zwraca:
    -------
    pd.DataFrame
        Tabela z metrykami modeli
    """
    print_section("MODELOWANIE REGRESYJNE")

    df = df.copy()

    # Zmienna docelowa – to, co chcemy przewidywać.
    target = "order_value"

    # Celowo nie używamy order_id i customer_id jako cech,
    # ponieważ są to identyfikatory, a nie sensowne cechy predykcyjne.
    feature_columns = [
        "product_category", "city", "age", "gender", "income",
        "loyalty_years", "site_visits_last_month", "discount_percent",
        "quantity", "unit_price", "shipping_cost", "payment_method",
        "returned", "order_month", "order_quarter", "weekend_order"
    ]

    X = df[feature_columns]
    y = df[target]

    # Podział na zbiory treningowy i testowy.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Wskazujemy kolumny liczbowe i kategoryczne.
    numeric_features = [
        "age", "income", "loyalty_years", "site_visits_last_month",
        "discount_percent", "quantity", "unit_price",
        "shipping_cost", "returned", "order_month",
        "order_quarter", "weekend_order"
    ]

    categorical_features = [
        "product_category", "city", "gender", "payment_method"
    ]

    # Pipeline dla danych liczbowych:
    # - imputacja medianą
    # - skalowanie
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    # Pipeline dla danych kategorycznych:
    # - imputacja najczęstszą wartością
    # - kodowanie One-Hot
    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    # ColumnTransformer pozwala zastosować różne operacje
    # do różnych typów kolumn w jednym, eleganckim przepływie.
    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ])

    # Definicje modeli.
    models = {
        "LinearRegression": LinearRegression(),
        "RandomForestRegressor": RandomForestRegressor(
            n_estimators=200,
            max_depth=12,
            min_samples_split=8,
            random_state=42,
            n_jobs=-1
        )
    }

    results = []

    for model_name, model in models.items():
        print(f"\nTrenowanie modelu: {model_name}")

        # Pipeline łączy preprocessing i model.
        clf = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ])

        clf.fit(X_train, y_train)
        predictions = clf.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        rmse = calculate_rmse(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        print(f"MAE  = {mae:.2f}")
        print(f"RMSE = {rmse:.2f}")
        print(f"R2   = {r2:.4f}")

        results.append({
            "model": model_name,
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "R2": round(r2, 4)
        })

        # Dla modelu lasu losowego wykonamy dodatkowy wykres:
        # porównanie wartości rzeczywistych i przewidzianych.
        if model_name == "RandomForestRegressor":
            comparison_df = pd.DataFrame({
                "actual": y_test.values,
                "predicted": predictions
            }).sample(min(300, len(y_test)), random_state=42)

            plt.figure(figsize=(8, 6))
            plt.scatter(comparison_df["actual"], comparison_df["predicted"], alpha=0.6)
            plt.title("Wartości rzeczywiste vs przewidziane (Random Forest)")
            plt.xlabel("Rzeczywiste order_value")
            plt.ylabel("Przewidziane order_value")
            save_plot("07_actual_vs_predicted_rf.png")

    results_df = pd.DataFrame(results).sort_values(by="R2", ascending=False)
    results_df.to_csv(os.path.join(OUTPUT_DIR, "model_results.csv"), index=False)

    print("\nTabela wyników modeli:")
    print(results_df)

    return results_df


# =========================================================
# 12. SEGMENTACJA KLIENTÓW (KLASTERYZACJA)
# =========================================================

def customer_segmentation(df: pd.DataFrame, n_clusters: int = 4) -> pd.DataFrame:
    """
    Segmentuje klientów na podstawie cech zagregowanych per klient.

    Logika:
    -------
    Najpierw agregujemy dane zamówień do poziomu klienta:
    - liczba zamówień,
    - średnia wartość zamówienia,
    - suma przychodów,
    - średni rabat,
    - średnia liczba wizyt,
    - odsetek zwrotów,
    - średni dochód.

    Następnie stosujemy:
    - standaryzację cech,
    - KMeans.

    Zwraca:
    -------
    pd.DataFrame
        Tabela klientów z przypisanym segmentem.
    """
    print_section("SEGMENTACJA KLIENTÓW")

    # Agregacja do poziomu klienta.
    customer_df = df.groupby("customer_id").agg({
        "order_id": "count",
        "order_value": ["mean", "sum"],
        "discount_percent": "mean",
        "site_visits_last_month": "mean",
        "returned": "mean",
        "income": "mean",
        "loyalty_years": "mean"
    })

    # Spłaszczenie wielopoziomowych nazw kolumn po agg().
    customer_df.columns = [
        "num_orders",
        "avg_order_value",
        "total_revenue",
        "avg_discount_percent",
        "avg_site_visits",
        "return_rate",
        "avg_income",
        "avg_loyalty_years"
    ]

    customer_df = customer_df.reset_index()

    # Wybór cech do klasteryzacji.
    cluster_features = [
        "num_orders",
        "avg_order_value",
        "total_revenue",
        "avg_discount_percent",
        "avg_site_visits",
        "return_rate",
        "avg_income",
        "avg_loyalty_years"
    ]

    X = customer_df[cluster_features].copy()

    # Standaryzacja – bardzo ważna w KMeans.
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Tworzenie modelu KMeans.
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=20)
    customer_df["segment"] = kmeans.fit_predict(X_scaled)

    # Zapis tabeli klientów z segmentami.
    customer_df.to_csv(os.path.join(OUTPUT_DIR, "customer_segments.csv"), index=False)

    # Podsumowanie segmentów.
    segment_summary = customer_df.groupby("segment")[cluster_features].mean().round(2)
    print("Podsumowanie segmentów:")
    print(segment_summary)

    # Wykres: segmenty względem total_revenue i avg_order_value
    plt.figure(figsize=(8, 6))
    plt.scatter(customer_df["total_revenue"], customer_df["avg_order_value"], c=customer_df["segment"])
    plt.title("Segmentacja klientów")
    plt.xlabel("total_revenue")
    plt.ylabel("avg_order_value")
    save_plot("08_customer_segments.png")

    return customer_df


# =========================================================
# 13. RAPORT KOŃCOWY
# =========================================================

def generate_text_report(df: pd.DataFrame,
                         stats_results: dict,
                         model_results: pd.DataFrame,
                         customer_segments: pd.DataFrame) -> None:
    """
    Generuje prosty raport tekstowy z najważniejszymi wnioskami.

    Raport jest zapisywany do pliku TXT, co może być punktem wyjścia
    do automatycznego raportowania w analizie danych.
    """
    print_section("GENEROWANIE RAPORTU KOŃCOWEGO")

    report_path = os.path.join(OUTPUT_DIR, "report.txt")

    # Kilka najważniejszych informacji do raportu.
    total_orders = len(df)
    total_revenue = df["order_value"].sum()
    avg_order_value = df["order_value"].mean()
    top_category = df.groupby("product_category")["order_value"].sum().sort_values(ascending=False).index[0]
    top_city = df.groupby("city")["order_value"].sum().sort_values(ascending=False).index[0]
    best_model = model_results.sort_values("R2", ascending=False).iloc[0]["model"]

    segment_counts = customer_segments["segment"].value_counts().sort_index()

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("RAPORT Z ANALIZY DANYCH SPRZEDAŻOWYCH\n")
        f.write("=" * 60 + "\n\n")

        f.write("1. PODSUMOWANIE ZBIORU DANYCH\n")
        f.write(f"Liczba zamówień: {total_orders}\n")
        f.write(f"Łączny przychód: {total_revenue:.2f}\n")
        f.write(f"Średnia wartość zamówienia: {avg_order_value:.2f}\n")
        f.write(f"Najsilniejsza kategoria sprzedażowa: {top_category}\n")
        f.write(f"Miasto z najwyższą sprzedażą: {top_city}\n\n")

        f.write("2. STATYSTYKI OPISOWE\n")
        f.write(f"Średnia order_value: {stats_results['mean_order_value']:.2f}\n")
        f.write(f"Mediana order_value: {stats_results['median_order_value']:.2f}\n")
        f.write(f"Odchylenie standardowe order_value: {stats_results['std_order_value']:.2f}\n")
        f.write(f"Q1 order_value: {stats_results['q1_order_value']:.2f}\n")
        f.write(f"Q3 order_value: {stats_results['q3_order_value']:.2f}\n\n")

        f.write("3. PORÓWNANIE GRUP RABATOWYCH\n")
        f.write(f"Średnia wartość zamówienia dla rabatu >= 20%: {stats_results['high_discount_mean']:.2f}\n")
        f.write(f"Średnia wartość zamówienia dla rabatu < 20%: {stats_results['low_discount_mean']:.2f}\n\n")

        f.write("4. MODELOWANIE PREDYKCYJNE\n")
        f.write("Wyniki modeli:\n")
        f.write(model_results.to_string(index=False))
        f.write("\n\n")
        f.write(f"Najlepszy model wg R2: {best_model}\n\n")

        f.write("5. SEGMENTACJA KLIENTÓW\n")
        for seg_id, count in segment_counts.items():
            f.write(f"Segment {seg_id}: {count} klientów\n")
        f.write("\n")

        f.write("6. WNIOSKI\n")
        f.write("- Wartość zamówienia silnie zależy od ceny jednostkowej, liczby sztuk i cech klienta.\n")
        f.write("- Segmentacja klientów pozwala identyfikować grupy o różnych zachowaniach zakupowych.\n")
        f.write("- Model regresyjny może wspierać prognozowanie wartości zamówień.\n")
        f.write("- Analiza zwrotów i rabatów może pomóc zoptymalizować politykę sprzedażową.\n")

    print(f"Raport zapisano do pliku: {report_path}")


# =========================================================
# 14. GŁÓWNA FUNKCJA STERUJĄCA
# =========================================================

def main():
    """
    Główna funkcja projektu.
    Steruje kolejnością całego pipeline'u analitycznego.
    """

    print_section("START PROGRAMU")

    # Jeżeli plik nie istnieje, tworzymy dane syntetyczne.
    if not os.path.exists(DATA_FILE):
        print("Plik danych nie istnieje. Generuję dane syntetyczne...")
        create_and_save_dataset()
        print(f"Dane zapisano do: {DATA_FILE}")

    # Wczytanie danych.
    df = load_dataset(DATA_FILE)

    # Wstępna inspekcja.
    inspect_data(df)

    # Czyszczenie danych.
    df_clean = clean_data(df)

    # Inżynieria cech.
    df_features = feature_engineering(df_clean)

    # Zapis oczyszczonego i rozszerzonego zbioru.
    clean_file = os.path.join(OUTPUT_DIR, "cleaned_ecommerce_sales.csv")
    df_features.to_csv(clean_file, index=False)
    print(f"\nOczyszczone dane zapisano do: {clean_file}")

    # Analiza eksploracyjna.
    exploratory_data_analysis(df_features)

    # Analiza statystyczna.
    stats_results = statistical_analysis(df_features)

    # Modele regresyjne.
    model_results = build_regression_models(df_features)

    # Segmentacja klientów.
    customer_segments = customer_segmentation(df_features, n_clusters=4)

    # Raport końcowy.
    generate_text_report(df_features, stats_results, model_results, customer_segments)

    print_section("KONIEC PROGRAMU")
    print("Analiza została zakończona pomyślnie.")
    print(f"Wyniki znajdują się w katalogu: {OUTPUT_DIR}")


# =========================================================
# 15. URUCHOMIENIE PROGRAMU
# =========================================================

if __name__ == "__main__":
    main()